#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""router_server — 把 search_skills 三层漏斗包成常驻 HTTP 服务，供 curl / 容器内 Agent 调用。

为什么要有它: CLI(scripts/search_skills)是一次性进程, 每次调用都要重付三笔冷启动成本 ——
走全库读 994 个 SKILL.md、构造 SentenceTransformer(约 5.3s)、fit 两个 TfidfVectorizer。
常驻服务把这三笔提到启动期付一次, 单次查询从约 6000ms 降到约 80ms。
附带好处: 容器里的 Agent 不必再挂载 5.6G 的 venv, 只要能发 HTTP 就能用
(走 docker 网桥网关; 该地址因机器而异, 本机是 172.16.0.1 而非 docker 默认的 172.17.0.1,
 容器内可从 /proc/net/route 里 Destination=00000000 那行的 Gateway 取)。

排序实现与 CLI 共用 search_skills.Router, 不分叉(重构后已验证逐位一致)。
只用标准库 http.server: venv 里没有 fastapi/flask, 单端点 + CPU 密集场景 async 也无收益,
零新依赖可以绕开 pip / 网络 / EDR 三重限制。

端点(全部无鉴权):
    GET  /health            就绪探针(启动脚本与容器都靠它判活)
    GET  /search?query=...  参数走查询串(curl -G --data-urlencode 最省事)
    POST /search            参数走 JSON 体
    GET  /                  返回用法说明

**无鉴权, 这是刻意的取舍**: 默认绑 0.0.0.0, 所以同网段任何人都能无凭据查询本服务,
拿到 994 个 skill 的名称/描述与宿主机绝对路径(等于对外公示本机目录结构与攻击工具清单)。
只在可信隔离网段里这么用。要收窄暴露面就换绑定地址, 而不是加回 token:
    --host 127.0.0.1     只有本机可达(容器需 --network host)
    --host 172.16.0.1    只有 docker 默认网桥可达, LAN 上连不上(地址按本机实际网桥改)

用法(建议经 scripts/router_server.sh 托管):
    python scripts/router_server.py --port 8787
    curl -s -G --data-urlencode 'query=Redis 未授权访问想拿 shell' \\
         --data-urlencode 'top_k=5' --data-urlencode 'desc_chars=120' \\
         http://127.0.0.1:8787/search

退出码: 0=正常关闭, 2=参数/环境错误(端口被占、语料为空)。
"""
import argparse
import json
import os
import signal
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search_skills as ss  # noqa: E402  (复用 Router / format_text / 常量, 保证两条路径同源)

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8787
MAX_BODY = 64 * 1024        # query 是一句话, 64KB 已远超合理上限, 防内存打爆
MAX_QUERY_LEN = 2000

# 参数名 -> (下界, 上界, 默认值)。上界同时挡住"要 500 条候选"这种把返回体撑爆的调用。
LIMITS = {
    'top_k': (1, 50, 5),
    'desc_chars': (0, 2000, 200),
    'l1_topk': (1, 5000, ss.L1_TOPK),
    'l2_topn': (1, 100, 20),
}


def log(msg):
    sys.stderr.write('[router_server] %s\n' % msg)
    sys.stderr.flush()


# ---------------------------------------------------------------- 网卡枚举
def _iface_addrs():
    """枚举各网卡的 IPv4 地址。

    不用 gethostbyname: 本机 /etc/hosts 把主机名指向了 127.0.1.1, 那样只会打印出回环地址,
    恰恰漏掉 docker0 —— 而它正是容器内 Agent 要连的那个地址。故直接走 ioctl。
    """
    import fcntl
    import struct
    out = []
    try:
        lines = open('/proc/net/dev', encoding='utf-8').read().splitlines()[2:]
    except OSError:
        return out
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for line in lines:
            name = line.split(':')[0].strip()
            if not name:
                continue
            try:
                res = fcntl.ioctl(s.fileno(), 0x8915,  # SIOCGIFADDR
                                  struct.pack('256s', name[:15].encode('utf-8')))
            except OSError:
                continue          # 无 IPv4 的接口(如未启用的 bridge)
            out.append(socket.inet_ntoa(res[20:24]))
    finally:
        s.close()
    return out


def listen_addresses(host, port):
    """列出实际会被暴露的 ip:port, 用于启动时把"绑了 0.0.0.0"这件事说清楚。"""
    if host not in ('0.0.0.0', '::', ''):
        return ['%s:%d' % (host, port)]
    ips = ['127.0.0.1'] + [a for a in _iface_addrs() if a != '127.0.0.1']
    seen, uniq = set(), []
    for ip in ips:
        if ip not in seen:
            seen.add(ip)
            uniq.append('%s:%d' % (ip, port))
    return uniq


# ---------------------------------------------------------------- 参数校验
class BadRequest(Exception):
    """参数不合法 -> 400/422, 而不是让 Router 抛栈变成 500。"""


def _int(name, raw):
    lo, hi, dflt = LIMITS[name]
    if raw is None or raw == '' or raw == []:
        return dflt
    if isinstance(raw, bool):
        raise BadRequest('%s 不能是布尔值' % name)
    try:
        v = int(raw)
    except (TypeError, ValueError):
        raise BadRequest('%s 必须是整数, 收到 %r' % (name, raw))
    if not lo <= v <= hi:
        raise BadRequest('%s 超出范围 [%d, %d], 收到 %d' % (name, lo, hi, v))
    return v


def _bool(name, raw):
    if raw is None or raw == '' or raw == []:
        return False
    if isinstance(raw, bool):
        return raw
    s = str(raw).strip().lower()
    if s in ('1', 'true', 'yes', 'y', 'on'):
        return True
    if s in ('0', 'false', 'no', 'n', 'off'):
        return False
    raise BadRequest('%s 必须是布尔值, 收到 %r' % (name, raw))


def parse_params(raw):
    """把 GET 查询串(值都是 list[str])或 POST JSON 体统一成 Router.search 的 kwargs。"""
    def one(k):
        v = raw.get(k)
        if isinstance(v, list):
            return v[0] if v else None
        return v

    query = one('query')
    if isinstance(query, bytes):
        query = query.decode('utf-8', 'replace')
    query = (query or '').strip() if isinstance(query, str) else ''
    if not query:
        raise BadRequest('缺少非空的 query 参数')
    if len(query) > MAX_QUERY_LEN:
        raise BadRequest('query 过长(%d > %d), 请压缩成一句话任务描述' % (len(query), MAX_QUERY_LEN))

    fmt = (one('format') or 'json')
    if isinstance(fmt, list):
        fmt = 'json'
    fmt = str(fmt).strip().lower()
    if fmt not in ('json', 'text'):
        raise BadRequest('format 只支持 json|text, 收到 %r' % fmt)

    return {'query': query, 'format': fmt,
            'top_k': _int('top_k', one('top_k')),
            'desc_chars': _int('desc_chars', one('desc_chars')),
            'l1_topk': _int('l1_topk', one('l1_topk')),
            'l2_topn': _int('l2_topn', one('l2_topn')),
            'rerank': _bool('rerank', one('rerank'))}


# ---------------------------------------------------------------- handler
class Handler(BaseHTTPRequestHandler):
    # 不设 protocol_version, 用默认的 HTTP/1.0: 每请求关连接, 省掉 keep-alive 的长度记账,
    # 本地环回上握手开销可忽略, 换来的是绝不会因为漏发 Content-Length 而挂住客户端。
    server_version = 'skill-router'
    sys_version = ''            # 不暴露 Python 版本
    router = None               # 由 main() 注入(类属性, 全进程共享一个 Router)
    t_boot = 0.0

    # ---- 基础设施
    def log_message(self, fmt, *args):
        pass                    # 关掉默认 access log; 自己在 _access 里记, 且绝不带头部

    def _access(self, code, t0, note=''):
        log('%s %s %s -> %d %.1fms %s' % (self.client_address[0], self.command,
                                          urlparse(self.path).path, code,
                                          1000 * (time.time() - t0), note))

    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False, indent=1)
        data = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _err(self, code, msg, t0, hint=None):
        body = {'error': {'code': code, 'message': msg}}
        if hint:
            body['error']['hint'] = hint
        try:
            self._send(code, body)
        except (BrokenPipeError, ConnectionResetError):
            pass
        self._access(code, t0, msg)

    def _read_body(self):
        n = self.headers.get('Content-Length')
        if n is None:
            return b''
        try:
            n = int(n)
        except ValueError:
            raise BadRequest('Content-Length 不是整数')
        if n < 0:
            raise BadRequest('Content-Length 为负')
        if n > MAX_BODY:
            raise BadRequest('请求体 %d 字节超过上限 %d' % (n, MAX_BODY))
        return self.rfile.read(n) if n else b''

    # ---- 路由
    def do_GET(self):
        t0 = time.time()
        path = urlparse(self.path).path.rstrip('/') or '/'
        if path in ('/', '/health'):
            self._health(t0, usage=(path == '/'))
        elif path == '/search':
            self._search(parse_qs(urlparse(self.path).query), t0)
        else:
            self._err(404, '未知路径 %s' % path, t0, '可用: /health /search')

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        t0 = time.time()
        path = urlparse(self.path).path.rstrip('/') or '/'
        if path != '/search':
            return self._err(404, '未知路径 %s' % path, t0, 'POST 只支持 /search')
        try:
            body = self._read_body()
        except BadRequest as e:
            return self._err(413 if '超过上限' in str(e) else 400, str(e), t0)
        if not body.strip():
            return self._err(400, '请求体为空', t0, '示例: {"query": "...", "top_k": 5}')
        try:
            raw = json.loads(body.decode('utf-8', 'replace'))
        except (ValueError, UnicodeDecodeError) as e:
            return self._err(400, '请求体不是合法 JSON: %s' % e, t0)
        if not isinstance(raw, dict):
            return self._err(400, '请求体必须是 JSON 对象', t0)
        # POST 体里的 query 也可用查询串覆盖? 不做: 单一来源, 避免"到底哪个生效"的歧义
        self._search(raw, t0)

    def _health(self, t0, usage=False):
        r = self.router
        body = {'status': 'ok', 'n_skills': len(r.slugs), 'emb_model': r.emb_model,
                'ready_ms': r.ready_ms, 'uptime_s': round(time.time() - self.t_boot, 1),
                'reranker_loaded': r._reranker is not None,
                'pid': os.getpid()}
        if usage:
            body['usage'] = {
                'GET /search': 'query(必填) top_k desc_chars l1_topk l2_topn rerank format',
                'POST /search': '同上, 走 JSON 体',
                'auth': '无 —— 能连到这个端口就能查询; 要收窄暴露面用 --host 指定绑定地址',
                'example': 'curl -s -G --data-urlencode "query=Redis 未授权访问想拿 shell" '
                           '--data-urlencode top_k=5 http://127.0.0.1:%d/search'
                           % self.server.server_address[1],
            }
        self._send(200, body)
        self._access(200, t0)

    def _search(self, raw, t0):
        try:
            p = parse_params(raw)
        except BadRequest as e:
            return self._err(422, str(e), t0)
        fmt = p.pop('format')
        query = p['query']
        try:
            result = self.router.search(**p)
        except Exception as e:
            # Router 内部异常(模型/索引损坏等)不该把连接直接掐断, 回 500 + 类型名便于定位
            return self._err(500, '检索失败: %s: %s' % (type(e).__name__, e), t0)
        if fmt == 'text':
            self._send(200, ss.format_text(result) + '\n', 'text/plain; charset=utf-8')
        else:
            self._send(200, result)
        self._access(200, t0, 'top_k=%d rerank=%s q=%r' % (p['top_k'], p['rerank'], query[:60]))

    # 客户端提前断开不应打栈到日志里
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(
        description='search_skills 三层漏斗的常驻 HTTP 服务(无鉴权)。')
    ap.add_argument('--host', default=DEFAULT_HOST,
                    help='监听地址(默认 %s = 所有网卡, 容器可经 docker 网桥网关访问)。'
                         '本服务无鉴权, 要收窄暴露面就填 127.0.0.1 或网桥地址' % DEFAULT_HOST)
    ap.add_argument('--port', type=int, default=DEFAULT_PORT, help='监听端口(默认 %d)' % DEFAULT_PORT)
    ap.add_argument('--emb-model', default=ss.EMB_MODEL, help='L1 embedding 模型')
    ap.add_argument('--rebuild-index', action='store_true', help='强制重新编码全库 embedding')
    ap.add_argument('--prewarm-reranker', action='store_true',
                    help='启动时就加载 L3 cross-encoder(否则首个 rerank 请求要多等约 2s)')
    args = ap.parse_args()

    # 先绑端口再加载模型: 端口被占是常见错误, 不值得先等 5s 冷启动才发现
    try:
        httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    except OSError as e:
        log('无法监听 %s:%d — %s' % (args.host, args.port, e))
        log('→ 先看是否已在跑: bash scripts/router_server.sh status')
        return 2

    try:
        router = ss.Router(emb_model=args.emb_model, rebuild_index=args.rebuild_index)
    except Exception as e:
        log('Router 初始化失败: %s: %s' % (type(e).__name__, e))
        httpd.server_close()
        return 2
    if args.prewarm_reranker:
        router.reranker   # 触发懒加载

    Handler.router = router
    Handler.t_boot = time.time()

    addrs = listen_addresses(args.host, args.port)
    if len(addrs) <= 4:
        log('监听 %s' % ' '.join(addrs))
    else:
        # 本机挂了上百个 docker 网络时, 全打出来只会淹没真正有用的那条; 显示回环 + 前 3 个
        log('监听 %s ... (共 %d 个 IPv4 地址)' % (' '.join(addrs[:4]), len(addrs)))
    if args.host in ('0.0.0.0', '::', ''):
        log('警告: 已绑定所有网卡且无鉴权 —— 上面任一地址可达者都能无凭据查询本服务,')
        log('      拿到 %d 个 skill 的名称/描述与宿主机绝对路径(等于公示本机目录结构与工具清单)。'
            % len(router.slugs))
        log('      只在可信隔离网段这么用。收窄暴露面: --host 127.0.0.1(仅本机, 容器需 --network host),')
        log('      或 --host <docker 网桥地址>(仅容器可达, LAN 上连不上)。')
    log('语料 %d 条, 冷启动 %sms' % (len(router.slugs), router.ready_ms))
    log('健康检查: curl -s http://127.0.0.1:%d/health' % args.port)

    stop = threading.Event()

    def _bye(signum, _frame):
        log('收到信号 %d, 关闭中 ...' % signum)
        stop.set()
        # shutdown() 必须在 serve_forever 之外的线程调用, 否则互相等死
        threading.Thread(target=httpd.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, _bye)
    signal.signal(signal.SIGINT, _bye)

    try:
        httpd.serve_forever(poll_interval=0.2)
    finally:
        httpd.server_close()
        log('已退出 (存活 %.1fs)' % (time.time() - Handler.t_boot))
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""search_skills — 攻击 skill 库三层漏斗路由 CLI（供 Claude Code 等 Agent 通过 Bash 调用）。

流水线: L1 embedding top-k 粗筛 -> L2 RRF(余弦名次 + TF-IDF 名次)融合排序 -> L3 cross-encoder 精排(默认启用, --no-rerank 关)。
设计与评测数据见仓库根目录 DESIGN.md; 离线评测与选点标定用 demo/router_demo.py。

用法:
    python scripts/search_skills.py "一句话任务描述" --top-k 5
    python scripts/search_skills.py "一句话任务描述" --no-rerank --top-k 5   # 退回 L1+L2, 省约 1.4s
    echo "一句话任务描述" | python scripts/search_skills.py - --format text

约定:
    - 结果 JSON 走 stdout, 诊断/计时信息走 stderr, 便于 Agent 直接解析;
    - query 传 "-" 表示从 stdin 读取;
    - 退出码 0=正常, 2=参数或索引错误。
"""
import argparse
import io
import json
import os
import re
import sys
import threading
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(ROOT, '_index')
# 与 demo/router_demo.py 及评测 harness 保持一致的语料口径
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}

EMB_MODEL = 'BAAI/bge-m3'  # 多语言 1024 维: 语料 description 100% 中英混排(每条带中文「信号:」标签), 纯英文模型会漏召回
RERANK_MODEL = 'BAAI/bge-reranker-v2-m3'
# 选点标定结果(见 demo/logs 与 DESIGN.md §2.2): top-k 是与语料规模解耦的成本预算, k=50 时本语料金标零丢失
L1_TOPK = 50
RRF_K0 = 60  # reciprocal rank fusion 平滑常数, 与 demo/router_demo.py 保持一致
# L3 精排默认开启: 只靠 L1+L2 的 RRF 融合分排头部, 会把"语义相关但不对症"的 skill 顶到 top1
# (实测 query "Redis 未授权访问想拿 shell" 关 L3 时 top1=gopherus-ssrf, 开 L3 才修正成
# unauthorized-access-common-services)。代价是延迟约 0.09s → 热态约 1.4s(本机 CPU 无 GPU),
# 所以 L2_TOPN 从 20 收到 10, 把 L3 成本砍半。两条调用路径(CLI 与 router_server)都引用这两个
# 常量, 而不是各写各的字面量 —— 否则改了这里仍会被调用方的旧默认值覆盖掉。
RERANK_DEFAULT = True
L2_TOPN = 10


def err(msg):
    sys.stderr.write('[search_skills] %s\n' % msg)


def model_path(hub_id):
    """优先用 demo/models/ 下的本地副本(见 demo/fetch_models.sh), 否则回落到 hub id。"""
    local = os.path.join(ROOT, 'demo', 'models', *hub_id.split('/'))
    return local if os.path.isdir(local) else hub_id


# ---------------------------------------------------------------- 语料
def load_skills():
    """遍历仓库 SKILL.md, 返回 {slug: {'name','desc','path'}}。"""
    docs = {}
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', 'demo') and not d.startswith('_')]
        if 'SKILL.md' not in files:
            continue
        rel = os.path.relpath(dp, ROOT).replace(os.sep, '/')
        parts = rel.split('/')
        if parts[0] in REGISTERED or len(parts) < 2 or parts[0] == 'scripts':
            continue
        text = io.open(os.path.join(dp, 'SKILL.md'), encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', text, re.S)
        if not fm:
            continue
        dm = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
        nm = re.search(r'^name:\s*(.+)$', fm.group(1), re.M)
        if not dm:
            continue
        slug = parts[-1]
        docs[slug] = {'name': (nm.group(1).strip() if nm else slug),
                      'desc': dm.group(1).strip().strip('"'),
                      # 绝对路径: 调用方(Agent)的 cwd 通常是目标项目而非本库, 相对路径还得再拼根目录
                      'path': os.path.join(dp, 'SKILL.md')}
    return docs


# ---------------------------------------------------------------- L1
def load_embeddings(slugs, texts, emb_model, rebuild):
    """返回 (emb 矩阵, SentenceTransformer 模型); 全库向量按模型名缓存在 _index/。"""
    from sentence_transformers import SentenceTransformer
    os.makedirs(INDEX_DIR, exist_ok=True)
    path = os.path.join(INDEX_DIR, 'l1_embs_%s.npz' % emb_model.replace('/', '__'))
    model = SentenceTransformer(model_path(emb_model))
    if not rebuild and os.path.exists(path):
        z = np.load(path)
        if list(z['slugs']) == slugs:
            err('L1 索引命中缓存: %s %s' % (emb_model, z['emb'].shape))
            return z['emb'], model
        err('L1 索引已过期(slug 不对齐), 重新编码')
    err('L1 编码全库 %d 条 (model=%s) ...' % (len(slugs), emb_model))
    emb = model.encode(texts, batch_size=64, normalize_embeddings=True,
                       show_progress_bar=False).astype('float32')
    np.savez_compressed(path, slugs=np.array(slugs), emb=emb)
    err('L1 索引已写入: %s %s' % (path, emb.shape))
    return emb, model


# ---------------------------------------------------------------- L2
def rank_vector(scores):
    """分数向量 -> 名次向量 (0 = 最高分), 供 RRF 融合使用; 与 demo/router_demo.py 的 rank_matrix 同构。"""
    order = np.argsort(-scores)
    rank = np.empty_like(order)
    rank[order] = np.arange(len(order))
    return rank


# ---------------------------------------------------------------- L3
def load_reranker():
    try:
        from sentence_transformers import CrossEncoder
    except ImportError:  # pragma: no cover
        from sentence_transformers.cross_encoder import CrossEncoder
    return CrossEncoder(model_path(RERANK_MODEL))


# ---------------------------------------------------------------- 检索
class Router(object):
    """三层漏斗的常驻态封装: 语料 / 全库 embedding / TF-IDF 向量器 / 模型只在构造时加载一次。

    为什么要这个类: 原来每次查询都要重做三件昂贵的事 —— 走全库读 994 个 SKILL.md、构造
    SentenceTransformer(约 5.7s)、对全库语料 fit 两个 TfidfVectorizer(约 0.28s)。CLI 是一次性
    进程, 这三笔每次都付(所以单次调用约 6s); HTTP 服务(scripts/router_server.py)只在启动时付
    一次, L1+L2 的单次查询降到约 0.09s(默认还叠加 L3 精排, 那部分另需约 1.4s)。

    两条路径共用这一份实现, 排序逻辑不分叉: 数值与重构前逐位一致(TF-IDF 只是把 fit 从每查询
    提前到构造期, 同语料同参数, 结果不变)。
    """

    def __init__(self, emb_model=EMB_MODEL, rebuild_index=False):
        t0 = time.time()
        self.emb_model = emb_model
        self.docs = load_skills()
        if not self.docs:
            raise RuntimeError('未加载到任何 skill, 请确认在仓库根目录下运行')
        self.slugs = sorted(self.docs)
        l1_texts = ['%s %s' % (self.docs[s]['name'], self.docs[s]['desc']) for s in self.slugs]
        corpus = ['%s %s %s %s' % (self.docs[s]['name'], self.docs[s]['name'],
                                   self.docs[s]['name'], self.docs[s]['desc']) for s in self.slugs]
        self.emb, self.enc = load_embeddings(self.slugs, l1_texts, emb_model, rebuild_index)
        # L2 的 TF-IDF 双通道(与 demo/router_demo.py 同构: word 1-2gram + char_wb 3-5gram)只 fit 一次
        from scipy.sparse import hstack
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vec_w = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.vec_c = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=1)
        self.X = hstack([self.vec_w.fit_transform(corpus), self.vec_c.fit_transform(corpus)])
        self._reranker = None
        # torch 推理串行化: CPU 上并发只会互相抢核并抬高内存峰值, 排队反而更快更稳
        self._lock = threading.Lock()
        self.ready_ms = round(1000 * (time.time() - t0), 1)
        err('Router 就绪: %d 条语料, 一次性加载 %sms' % (len(self.slugs), self.ready_ms))

    @property
    def reranker(self):
        """L3 cross-encoder 懒加载: 只有真收到 rerank 请求才付这笔加载成本。"""
        if self._reranker is None:
            err('L3 首次调用, 加载 cross-encoder %s ...' % RERANK_MODEL)
            self._reranker = load_reranker()
        return self._reranker

    def tfidf_scores(self, query):
        """query 对全库的 TF-IDF 相似度向量; 向量器与 X 已在构造期 fit 好。"""
        from scipy.sparse import hstack
        Q = hstack([self.vec_w.transform([query]), self.vec_c.transform([query])])
        return (Q @ self.X.T).toarray()[0]

    def search(self, query, top_k=20, l1_topk=L1_TOPK, rerank=RERANK_DEFAULT, l2_topn=L2_TOPN,
               desc_chars=200):
        """单查询三层漏斗。

        latency_ms 计的是流水线本身: L1/L2 的一次性加载在构造期就付掉了(见 meta.ready_ms),
        但 L3 的 cross-encoder 是**懒加载**的 —— 下面 t0 的设置早于 self.reranker 的取值, 所以
        首次精排那笔加载(本机约 1.4s)会被算进 latency_ms.l3。常驻服务靠启动预热避开它,
        CLI 一次性进程避不开(每次调用都是首次)。
        """
        t_start = time.time()
        slugs, docs = self.slugs, self.docs

        # ---- L1: 余弦 top-k 粗筛 (k 是与语料规模 N 解耦的成本预算, 直接等于 L2/L3 的候选量上限)
        with self._lock:
            q_emb = self.enc.encode([query], normalize_embeddings=True,
                                    show_progress_bar=False).astype('float32')
        sims = (q_emb @ self.emb.T)[0]
        topk = min(l1_topk, len(slugs))
        survivors = np.argsort(-sims)[:topk]
        # top-k 模式下不存在"零候选"; degraded 表示粗筛未起剔除作用(k >= 语料规模), 等价于全库进 L2
        degraded = topk >= len(slugs)
        if degraded:
            err('L1 top-k=%d 不小于语料规模 %d, 粗筛未剔除任何候选' % (l1_topk, len(slugs)))
        t_l1 = time.time() - t_start

        # ---- L2: RRF 融合 (全库余弦名次 + 全库 TF-IDF 名次), 再限制在 L1 存活集内排序
        # 单用 TF-IDF 会丢掉 embedding 的语义信号 (bge-m3 实测 baseline @5 84.1% -> L2 @5 94.4%, 见 demo/router_demo.py)
        t0 = time.time()
        sim_t = self.tfidf_scores(query)
        fused = 1.0 / (RRF_K0 + rank_vector(sims)) + 1.0 / (RRF_K0 + rank_vector(sim_t))
        ranked = survivors[np.argsort(-fused[survivors])]
        t_l2 = time.time() - t0

        # ---- L3(可选): cross-encoder 对 L2 头部精排
        rerank_scores = {}
        t_l3 = 0.0
        if rerank:
            t0 = time.time()
            head = ranked[:l2_topn]
            pairs = [(query, docs[slugs[j]]['name'] + ' ' + docs[slugs[j]]['desc']) for j in head]
            with self._lock:
                sc = self.reranker.predict(pairs, batch_size=32, show_progress_bar=False)
            head = head[np.argsort(-sc)]
            ranked = np.concatenate([head, ranked[l2_topn:]])
            rerank_scores = {int(j): float(s) for j, s in zip(head, np.sort(sc)[::-1])}
            t_l3 = time.time() - t0

        # ---- 组装返回体
        candidates = []
        for j in ranked[:top_k]:
            slug = slugs[j]
            d = docs[slug]
            desc = d['desc'] if len(d['desc']) <= desc_chars else d['desc'][:desc_chars] + '…'
            item = {'slug': slug, 'name': d['name'], 'description': desc, 'path': d['path'],
                    'score': float(fused[j]), 'l1_sim': float(sims[j])}
            if rerank:
                item['rerank_score'] = rerank_scores.get(int(j))
                if item['rerank_score'] is not None:
                    item['score'] = item['rerank_score']
            candidates.append(item)

        return {'query': query, 'candidates': candidates,
                'meta': {'l1_kept': int(survivors.size), 'n_skills': len(slugs),
                         'l1_topk': int(topk), 'rrf_k0': RRF_K0,
                         'emb_model': self.emb_model, 'rerank': rerank, 'degraded': degraded,
                         'ready_ms': self.ready_ms,
                         'latency_ms': {'l1': round(1000 * t_l1, 1), 'l2': round(1000 * t_l2, 1),
                                        'l3': round(1000 * t_l3, 1),
                                        'total': round(1000 * (time.time() - t_start), 1)}}}


def search(query, top_k=20, emb_model=EMB_MODEL, l1_topk=L1_TOPK, rerank=RERANK_DEFAULT,
           l2_topn=L2_TOPN, desc_chars=200, rebuild_index=False):
    """一次性进程语义(CLI 用): 新建 Router 查一次即退出。常驻服务请直接复用 Router 实例。"""
    return Router(emb_model=emb_model, rebuild_index=rebuild_index).search(
        query, top_k=top_k, l1_topk=l1_topk, rerank=rerank, l2_topn=l2_topn, desc_chars=desc_chars)


def format_text(result):
    lines = ['query: %s' % result['query'],
             'meta : l1_kept=%(l1_kept)d/%(n_skills)d l1_topk=%(l1_topk)d model=%(emb_model)s '
             'rerank=%(rerank)s degraded=%(degraded)s total=%(latency_ms)s' % result['meta']]
    for i, c in enumerate(result['candidates'], 1):
        lines.append('%2d. %-52s score=%.5f l1_sim=%.3f' % (i, c['slug'], c['score'], c['l1_sim']))
        lines.append('    %s' % c['description'])
        lines.append('    %s' % c['path'])
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(
        description='三层漏斗 skill 路由: 输入一句话任务描述, 输出最匹配的 skill 候选。')
    ap.add_argument('query', help='自然语言任务描述; 传 "-" 从 stdin 读取')
    ap.add_argument('--top-k', type=int, default=20,
                    help='返回候选数 (默认 20; 精排只重排头部 --l2-topn 条, 其余仍按 L2 名次跟在后面)')
    ap.add_argument('--emb-model', default=EMB_MODEL, help='L1 embedding 模型 (hub id 或本地目录名)')
    ap.add_argument('--l1-topk', type=int, default=L1_TOPK,
                    help='L1 保留的候选条数; 与语料规模解耦的成本预算 (默认 50, 本语料金标零丢失)')
    ap.add_argument('--no-rerank', action='store_false', dest='rerank',
                    help='关掉默认的 L3 cross-encoder 精排, 退回 L1+L2 的 RRF 排序 '
                         '(一次性进程能省约 2.7s: 权重加载 + 推理; 但头部排序会明显变差)')
    ap.add_argument('--l2-topn', type=int, default=L2_TOPN,
                    help='精排时送进 L3 的条数 (默认 %d; L3 耗时与之成正比, 20 条约 3.0s)' % L2_TOPN)
    ap.add_argument('--desc-chars', type=int, default=200, help='返回体中 description 截断长度')
    ap.add_argument('--format', choices=('json', 'text'), default='json')
    ap.add_argument('--rebuild-index', action='store_true', help='强制重新编码全库 embedding')
    args = ap.parse_args()

    query = sys.stdin.read().strip() if args.query == '-' else args.query.strip()
    if not query:
        err('query 为空')
        return 2

    try:
        result = search(query, top_k=args.top_k, emb_model=args.emb_model, l1_topk=args.l1_topk,
                        rerank=args.rerank, l2_topn=args.l2_topn,
                        desc_chars=args.desc_chars, rebuild_index=args.rebuild_index)
    except Exception as e:
        err('检索失败: %s: %s' % (type(e).__name__, e))
        return 2

    out = format_text(result) if args.format == 'text' else json.dumps(result, ensure_ascii=False, indent=1)
    sys.stdout.write(out + '\n')
    err('完成: %d 个候选, 耗时 %sms' % (len(result['candidates']), result['meta']['latency_ms']['total']))
    return 0


if __name__ == '__main__':
    sys.exit(main())

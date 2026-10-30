#!/usr/bin/env bash
# router_server.sh — search_skills HTTP 服务的进程托管(start/stop/status/logs/curl)。
#
# 为什么是手动脚本而不是 systemd: 本库跑在渗透测试机上, 未必有 root、未必有 systemd 用户实例,
# 且服务只在需要路由时开着更省心。nohup + pidfile 是最小可用集, 依赖只有 bash 和 curl。
#
# 用法:
#   bash scripts/router_server.sh start          # 后台起服务(默认 0.0.0.0:8787), 等到 /health 通才返回
#   bash scripts/router_server.sh status         # 进程 + /health 实况
#   bash scripts/router_server.sh logs 100       # 看最近 N 行日志(默认 50)
#   bash scripts/router_server.sh stop           # SIGTERM, 10s 不退再 SIGKILL
#   bash scripts/router_server.sh restart
#   bash scripts/router_server.sh curl "Redis 未授权访问想拿 shell" [top_k=5] [rerank=0] ...
#                (L3 精排默认开: 约 1.4s/查询但头部排序明显更准; 追加 rerank=0 退回 L1+L2 约 0.09s)
#
# 环境变量:
#   ROUTER_PORT  监听端口(默认 8787)
#   ROUTER_HOST  监听地址(默认 0.0.0.0 = 所有网卡)。服务**无鉴权**, 绑 0.0.0.0 就意味着同网段
#                任何人都能无凭据查询到全库 skill 名称/描述; 要收窄暴露面就设
#                127.0.0.1(仅本机, 容器需 --network host)或 docker 网桥地址(仅容器, LAN 连不上)
#   ROUTER_LIB_PREFIX
#                返回体里 candidates[].path 的前缀(默认 /opt/attack-skill-library, 即 deploy.py
#                部署到容器里的扁平文件库)。服务在宿主跑而 Agent 在容器里, 返回宿主真实路径
#                容器 Read 不到。设成空串(ROUTER_LIB_PREFIX= 而非 unset)则不改写
#   SKILL_PYTHON 指定解释器(透传给 scripts/search_skills --print-python)
#
# 退出码: 0=成功 / 2=用法错误 / 3=环境未就绪(缺解释器或模型权重) / 4=启动失败 / 5=停止失败
set -euo pipefail

SELF="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT="$(cd "$(dirname "$SELF")/.." && pwd)"
SERVER="$ROOT/scripts/router_server.py"
WRAPPER="$ROOT/scripts/search_skills"
RUN_DIR="$ROOT/.run"
PIDFILE="$RUN_DIR/router.pid"
LOGFILE="$RUN_DIR/router.log"
PORT="${ROUTER_PORT:-8787}"
HOST="${ROUTER_HOST:-0.0.0.0}"
# 用 ${VAR-default} 而非 ${VAR:-default}: 显式设成空串是"关闭改写"的有效取值, 不能被当成未设
LIB_PREFIX="${ROUTER_LIB_PREFIX-/opt/attack-skill-library}"
HEALTH="http://127.0.0.1:$PORT/health"

die()  { printf '[router_server] %s\n' "$*" >&2; exit "${2:-2}"; }
info() { printf '[router_server] %s\n' "$*"; }

# pidfile 里的 pid 必须确实是本服务 —— pid 会被系统回收复用, 光看进程活着不够
alive_pid() {
  local p
  [ -f "$PIDFILE" ] || return 1
  p="$(head -n1 "$PIDFILE" 2>/dev/null || true)"
  [ -n "$p" ] || return 1
  [ -d "/proc/$p" ] || return 1
  tr '\0' ' ' < "/proc/$p/cmdline" 2>/dev/null | grep -q 'router_server\.py' || return 1
  printf '%s' "$p"
}

need_curl() { command -v curl >/dev/null 2>&1 || die "缺 curl, 无法探活/调用服务" 3; }

# 必须确认响应真的来自本服务: 端口被别的进程占着时也会返回 200, 光看退出码会误判
health() { curl -fsS --max-time 3 "$HEALTH" 2>/dev/null | grep -q '"n_skills"'; }

resolve_py() {
  local py
  py="$(SKILL_QUIET=1 "$WRAPPER" --print-python)" || exit 3   # wrapper 自己会打印原因并以 3 退出
  printf '%s' "$py"
}

cmd_start() {
  need_curl
  local p
  if p="$(alive_pid)"; then
    info "已在运行 (pid=$p, port=$PORT)"
    health && info "$(curl -fsS --max-time 3 "$HEALTH")"
    return 0
  fi
  rm -f "$PIDFILE"
  [ -f "$SERVER" ] || die "找不到 $SERVER" 3
  [ -f "$WRAPPER" ] || die "找不到 $WRAPPER" 3
  [ -d "$ROOT/demo/models/BAAI/bge-m3" ] || die "缺 L1 模型权重 → 先跑: bash $ROOT/demo/fetch_models.sh" 3

  local py; py="$(resolve_py)"
  mkdir -p "$RUN_DIR"
  info "启动中: $py $SERVER --host $HOST --port $PORT --lib-prefix '$LIB_PREFIX'"
  case "$HOST" in
    0.0.0.0|::|"")
      info "警告: 绑所有网卡且服务无鉴权 —— 同网段任何人都能无凭据查到全库 skill 清单。"
      info "      要收窄: ROUTER_HOST=127.0.0.1(仅本机) 或 ROUTER_HOST=<docker 网桥地址>(仅容器)"
      ;;
  esac
  [ -n "$LIB_PREFIX" ] || info "注意: ROUTER_LIB_PREFIX 为空 → 不改写 path, 返回宿主机真实路径"
  info "日志: $LOGFILE"
  # nohup + 重定向: 脱离当前终端; 日志追加而非覆盖, 便于回看上一次崩溃原因
  nohup "$py" "$SERVER" --host "$HOST" --port "$PORT" --lib-prefix "$LIB_PREFIX" >>"$LOGFILE" 2>&1 &
  local pid=$!
  printf '%s\n' "$pid" > "$PIDFILE"

  # 轮询就绪: 索引命中缓存约 8s; 若 _index/ 缺失需现场编码全库(CPU 约 2 分钟), 故上限给足
  local i=0
  while [ "$i" -lt 240 ]; do
    if ! kill -0 "$pid" 2>/dev/null; then
      rm -f "$PIDFILE"
      printf '[router_server] 进程已退出, 最近日志:\n' >&2
      tail -n 25 "$LOGFILE" >&2 || true
      exit 4
    fi
    if health; then
      info "就绪 (pid=$pid, 用时 ${i}s)"
      local h
      h="$(curl -fsS --max-time 3 "$HEALTH")" && printf '%s\n' "$h" | sed 's/^/[router_server]   /'
      info "调用: bash $SELF curl \"一句话任务描述\""
      return 0
    fi
    if [ $((i % 15)) -eq 14 ]; then info "仍在加载模型/语料 ... ${i}s"; fi
    i=$((i + 1)); sleep 1
  done
  printf '[router_server] 240s 内未就绪, 最近日志:\n' >&2
  tail -n 25 "$LOGFILE" >&2 || true
  info "服务可能仍在编码全库, 可用 status 复查; 需要放弃就 stop"
  exit 4
}

cmd_stop() {
  local p
  if ! p="$(alive_pid)"; then
    info "未在运行"; rm -f "$PIDFILE"; return 0
  fi
  info "停止 pid=$p (SIGTERM)"
  kill "$p" 2>/dev/null || true
  local i=0
  while [ "$i" -lt 10 ]; do
    kill -0 "$p" 2>/dev/null || { rm -f "$PIDFILE"; info "已停止"; return 0; }
    i=$((i + 1)); sleep 1
  done
  info "10s 未退出, SIGKILL"
  kill -9 "$p" 2>/dev/null || true
  sleep 1
  kill -0 "$p" 2>/dev/null && die "无法停止 pid=$p" 5
  rm -f "$PIDFILE"; info "已强制停止"
}

cmd_status() {
  local p h
  if p="$(alive_pid)"; then
    info "运行中 pid=$p port=$PORT host=$HOST"
    if h="$(curl -fsS --max-time 3 "$HEALTH" 2>/dev/null)"; then
      printf '%s\n' "$h" | sed 's/^/[router_server]   /'
    else
      info "警告: 进程在但 /health 无响应(仍在加载? 看 logs)"
    fi
    return 0
  fi
  info "未运行 (port=$PORT)"
  [ -f "$PIDFILE" ] && info "存在残留 pidfile: $(head -n1 "$PIDFILE")" || true
  return 1
}

cmd_logs() { tail -n "${1:-50}" "$LOGFILE" 2>/dev/null || die "还没有日志: $LOGFILE" 2; }

# curl "<query>" [k=v ...] —— 人工/脚本调用的便捷入口; Agent 侧 SKILL.md 用的是裸 curl
cmd_curl() {
  need_curl
  local q="${1:-}"; [ -n "$q" ] || die '用法: router_server.sh curl "一句话任务描述" [top_k=5] [rerank=0]' 2
  shift || true
  local args=(-sS -G "http://127.0.0.1:$PORT/search" --data-urlencode "query=$q")
  local kv
  for kv in "$@"; do
    case "$kv" in *=*) args+=(--data-urlencode "$kv") ;; *) die "额外参数必须是 k=v 形式, 收到: $kv" 2 ;; esac
  done
  curl "${args[@]}"
}

usage() { sed -n '2,27p' "$SELF"; }

case "${1:-}" in
  start)   cmd_start ;;
  stop)    cmd_stop ;;
  restart) cmd_stop; cmd_start ;;
  status)  cmd_status ;;
  logs)    shift; cmd_logs "${1:-50}" ;;
  curl)    shift; cmd_curl "$@" ;;
  ''|-h|--help|help) usage ;;
  # 不用 die + $(printf '\n\n'): 命令替换会把尾部换行全吃掉, 错误信息会和 usage 黏成一行
  *)       printf '[router_server] 未知子命令: %s\n\n' "$1" >&2; usage >&2; exit 2 ;;
esac

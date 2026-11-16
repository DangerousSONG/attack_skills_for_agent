#!/usr/bin/env bash
# skill-router 常驻服务保活包装：崩溃自动重启 + 单实例锁 + 开机自启入口（crontab @reboot）
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY=/home/panjiahao/safe-range/PentestAgent/venv/bin/python
RUN="${HOME:-/home/panjiahao}/.cache/skill-router"
mkdir -p "$RUN"
LOG="$RUN/router_server.log"
PIDFILE="$RUN/router_server.pid"
LOCK="$RUN/router_server.lock"
PORT=8787
# 返回体 candidates[].path 的前缀, 指向**消费方**(靶机/容器)里的扁平文件库, 宿主上没有它是
# 正常的(服务不做存在性校验)。消费方必须先跑 deploy.py --library-dir 这个前缀, 否则 Agent
# Read 不到 path, 下一步就会误拿 slug 去调 Skill 工具(库 skill 未注册, 只会 Unknown skill)。
LIB_PREFIX=/opt/attack-skill-library

# 单实例锁：防止 cron/手动重复拉起
exec 9>"$LOCK"
flock -n 9 || exit 0

# 已有活着的实例则退出
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  exit 0
fi
if ss -ltn 2>/dev/null | grep -q ":$PORT "; then
  exit 0
fi

echo $$ >"$RUN/supervisor.pid"
echo "[keepalive] $(date '+%F %T') supervisor started (pid $$)" >>"$LOG"
cd "$DIR"
while true; do
  # 日志超过 20MB 则滚动一次，避免无界增长
  if [ -f "$LOG" ] && [ "$(stat -c%s "$LOG" 2>/dev/null || echo 0)" -gt 20971520 ]; then
    mv -f "$LOG" "$LOG.1"
  fi
  echo "[keepalive] $(date '+%F %T') launching router_server.py" >>"$LOG"
  "$PY" "$DIR/router_server.py" --host 0.0.0.0 --port "$PORT" \
    --lib-prefix "$LIB_PREFIX" >>"$LOG" 2>&1 &
  CHILD=$!
  echo "$CHILD" >"$PIDFILE"
  wait "$CHILD"
  RC=$?
  echo "[keepalive] $(date '+%F %T') router_server.py exited rc=$RC, restart in 3s" >>"$LOG"
  sleep 3
done

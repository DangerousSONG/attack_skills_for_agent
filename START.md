


# 运行方式
``` bash
cd /home/panjiahao/safe-range/attack_skills_for_agent

/home/panjiahao/safe-range/PentestAgent/venv/bin/python demo/router_demo.py
```


## 部署skill-router和skill-library
python3 scripts/deploy.py   --skills-dir  /home/panjiahao/.claude/skills   --library-dir /home/panjiahao/safe-range/attack-skill-library



## 服务器启动
```bash
cd /home/panjiahao/safe-range/attack_skills_for_agent
bash scripts/router_server.sh start     # 后台起，阻塞到 /health 通才返回（约 5-10s）
bash scripts/router_server.sh status    # 进程 + /health 实况
bash scripts/router_server.sh curl "Redis 未授权访问想拿 shell" top_k=5   # 调试用
bash scripts/router_server.sh logs 100
bash scripts/router_server.sh stop
```

服务**无鉴权**，直接 curl 即可：
```bash
curl -sS -G "http://127.0.0.1:8787/search" \
  --data-urlencode 'query=Redis 未授权访问想拿 shell' \
  --data-urlencode top_k=5 --data-urlencode desc_chars=120
```

容器内把 `ROUTER_API` 指向宿主的 docker 网桥网关（本机是 `172.16.0.1`，不是 docker 默认的
`172.17.0.1`；容器内可读 `/proc/net/route` 里 `Destination` 为 `00000000` 那行的 `Gateway`）。

> 默认绑 `0.0.0.0` 且无鉴权，同网段任何人都能查到全库 skill 清单与宿主机绝对路径。
> 要收窄暴露面：`ROUTER_HOST=127.0.0.1 bash scripts/router_server.sh start`（仅本机，
> 容器需 `--network host`），或 `ROUTER_HOST=172.16.0.1`（仅 docker 默认网桥可达）。






### 服务运维
```bash
cd /home/panjiahao/safe-range/attack_skills_for_agent

# ---- 查状态 ----
systemctl --user status skill-router-keepalive.service        # 守护 + 服务总览
systemctl --user is-active skill-router-keepalive.service     # 只要一个词: active
curl -sS http://127.0.0.1:8787/health                         # 服务真实就绪状态

# ---- 看日志 ----
tail -f ~/.cache/skill-router/router_server.log               # 实时（推荐）
tail -n 100 ~/.cache/skill-router/router_server.log
journalctl --user -u skill-router-keepalive.service -n 50     # systemd 层事件

# ---- 重启（改了 router_server.py / search_skills.py 之后必须做）----
systemctl --user restart skill-router-keepalive.service
# 注意: restart 只重启守护脚本。若只想重启里面的 python 而不惊动 systemd:
kill "$(cat ~/.cache/skill-router/router_server.pid)"          # keepalive 3s 后自动拉起新进程

# ---- 临时停服（维护窗口）----
systemctl --user stop skill-router-keepalive.service           # 停守护
kill "$(cat ~/.cache/skill-router/router_server.pid)" 2>/dev/null   # 再停服务本体
# 顺序不能反: 先 kill 服务本体，守护会立刻把它拉回来

# ---- 恢复 ----
systemctl --user start skill-router-keepalive.service

# ---- 调试用查询（这两个还能安全用）----
bash scripts/router_server.sh curl "Redis 未授权访问想拿 shell" top_k=5 rerank=0
curl -sS -G http://127.0.0.1:8787/search \
  --data-urlencode 'query=Redis 未授权访问想拿 shell' \
  --data-urlencode top_k=5 --data-urlencode rerank=0
```
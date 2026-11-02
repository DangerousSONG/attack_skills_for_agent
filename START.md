


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



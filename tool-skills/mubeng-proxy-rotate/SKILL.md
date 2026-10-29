---
name: mubeng-proxy-rotate
description: "mubeng: Proxy pool rotation and load balancing. Signals: internal network penetration, tunnel, proxy rotation, rotation interval, detect proxies."
zh-signals: "mubeng: 代理池轮换负载均衡。信号:内网穿透,隧道,代理轮换,轮换间隔,检测代理。"
---

# mubeng

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/kitabisa/mubeng
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/kitabisa/mubeng@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `mubeng -f proxies.txt -a localhost:8080` | 代理轮换 |
| `-f p.txt -r 10` | 轮换间隔 |
| `-m` | 检测代理 |

## 攻击场景 Playbook

### 代理池轮换负载均衡

```bash
mubeng -f proxies.txt -a 127.0.0.1:8080
# 大量请求分散出口
```

## 注意事项

Go 代理池,自动轮换+健康检查。

---
name: mubeng-proxy-rotate
description: "mubeng: Proxy pool rotation and load balancing. Signals: internal network penetration, tunnel, proxy rotation, rotation interval, detect proxies."
zh-signals: "mubeng: 代理池轮换负载均衡。信号:内网穿透,隧道,代理轮换,轮换间隔,检测代理。"
when-to-use: "Use during internal penetration or tunneling when requests must rotate through a proxy pool with health checking and load balancing. Requires a list of proxies and a rotation interval."
---

# mubeng

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/kitabisa/mubeng
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/kitabisa/mubeng@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `mubeng -f proxies.txt -a localhost:8080` | Proxy rotation |
| `-f p.txt -r 10` | Rotation interval |
| `-m` | Detect proxies |

## Attack Scenario Playbook

### Proxy pool rotation with load balancing

```bash
mubeng -f proxies.txt -a 127.0.0.1:8080
# Spread large request volumes across egress points
```

## Notes

Go proxy pool with automatic rotation and health checking.

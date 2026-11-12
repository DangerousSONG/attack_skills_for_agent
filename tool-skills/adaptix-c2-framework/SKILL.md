---
name: adaptix-c2-framework
description: "AdaptixC2: builds a C2 framework and manages sessions. Signals: c2, command and control, start server, generate multi-platform payloads, lateral movement essential"
zh-signals: "AdaptixC2: C2 控制框架搭建与会话管理。信号:c2,命令控制,启动服务端,生成多平台载荷,横向必备。"
when-to-use: >-
  Use when deploying a modern command-and-control framework for multi-platform
  operations; start the team server, generate platform-specific agents, and
  manage sessions, SOCKS proxies, and pivoting.
---

# AdaptixC2

- Attack Category: C35 C2 Frameworks
- Upstream Repository: https://github.com/Adaptix-Framework/AdaptixC2
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Adaptix-Framework/AdaptixC2 && build server+agent per the docs
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./adaptix-server -listen 0.0.0.0:443` | Start the server |
| `agent generation: listeners→generate in the console` | Generate multi-platform payloads |
| `socks proxy module` | Essential for lateral movement |
| `pivot in the console` | Internal network pivot |

## Attack Scenario Playbook

### C2 Framework Setup and Session Management

```bash
./adaptix-server
# Web console + multiple listeners; beacons support Win/Linux/macOS
```

## Notes

Modern open-source C2 (forked from the Havoc line), supports multi-protocol listeners + SOCKS proxy + a rich post-exploitation module set.

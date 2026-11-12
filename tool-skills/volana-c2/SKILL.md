---
name: volana-c2
description: "volana: Covert channel C2. Signals: C2, command and control, covert C2, encryption, disguised process."
zh-signals: "volana: 隐蔽信道 C2。信号:c2,命令控制,隐蔽 C2,加密,伪装进程。"
when-to-use: >-
  Use when you need a lightweight, encrypted C2 channel that disguises its
  process to maintain covert command and control.
---

# volana

- Attack Category: C35 C2 Frameworks and Remote Control
- Upstream Repository: https://github.com/ariary/volana
- Upstream License: Unlicense (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ariary/volana && cd volana && go build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./volana -l 10.0.0.5:4444` | Covert C2 |
| `-e 'cmd'` | Encryption |
| `-p` | Disguised process |

## Attack Scenario Playbook

### Covert Channel C2

```bash
./volana -l 443
# Encryption + process disguise
```

## Notes

A lightweight C2 focused on stealth.

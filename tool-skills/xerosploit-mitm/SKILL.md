---
name: xerosploit-mitm
description: "xerosploit: LAN man-in-the-middle toolkit. Signals: man-in-the-middle, MITM, interactive MITM framework, target discovery, MITM modules."
zh-signals: "xerosploit: 局域网中间人全家桶。信号:中间人,mitm,交互 MITM 框架,目标发现,中间人模块。"
when-to-use: >-
  Use for LAN MITM engagements requiring an interactive framework to discover
  targets and run sniffing, replacement, and injection modules.
---

# xerosploit

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/LionSec/xerosploit
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/LionSec/xerosploit && cd xerosploit && python3 install.py
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `xerosploit` | Interactive MITM framework |
| `scan` | Target discovery |
| `mitm` | MITM module |
| `sniff` | Traffic sniffing |
| `replace` | Web injection |

## Attack Scenario Playbook

### All-in-One LAN Man-in-the-Middle Toolkit

```bash
xerosploit && scan && select target && mitm
# sniff/replace/inject in one shot
```

## Notes

A MITM attack framework with a rich module set.

---
name: sniffjoke-traffic-obf
description: "sniffjoke: anti-sniffing traffic obfuscation. Signals: MITM, mitm, transparent obfuscation, debug, silent."
zh-signals: "sniffjoke: 反嗅探流量混淆。信号:中间人,mitm,透明混淆,调试,静默。"
when-to-use: >-
  Use when you need to obfuscate network traffic so that passive sniffers and IDS
  fail to parse it; supports transparent addressing, debug, and silent modes.
---

# sniffjoke

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/vecna/sniffjoke
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install sniffjoke
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sniffjoke -r` | Transparent obfuscation |
| `-d` | Debug |
| `-q` | Quiet |

## Attack Scenario Playbook

### Anti-Sniffing Traffic Obfuscation

```bash
sniffjoke
# make IDS/sniffers fail to parse the traffic
```

## Notes

Network traffic obfuscation to counter passive sniffing.

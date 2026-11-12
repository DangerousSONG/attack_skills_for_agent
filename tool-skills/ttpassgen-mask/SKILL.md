---
name: ttpassgen-mask
description: "ttpassgen generates multi-encoding masks. Signals: password cracking, hash cracking, statistics"
zh-signals: "ttpassgen: 多编码掩码生成。信号:密码破解,哈希破解,统计。"
when-to-use: >-
  Use when generating mask-based password wordlists, including multi-byte encodings such
  as GBK or Big5, for authorized password cracking.
---

# ttpassgen

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/tp7309/TTPassGen
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install TTpassgen
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ttpassgen -t '?l?l?l?d?d' -o out.txt` | Mask generation |
| `-t pattern -s` | Statistics |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Multi-Encoding Mask Generation

```bash
ttpassgen -t '?l?l?d?d?d'
# supports encodings such as GBK/Big5
```

## Notes

Multi-encoding mask wordlist generation, well suited to Chinese-language environments.

---
name: pybozocrack-md5-lookup
description: "PyBozoCrack: Quickly checks weak hashes. Signals: password cracking, hash cracking, MD5 online lookup, batch, includes special characters."
zh-signals: "PyBozoCrack: 弱哈希秒查。信号:密码破解,哈希破解,MD5 在线库查询,批量,含特殊字符。"
when-to-use: >-
  Use when you need a zero-cost first-pass check of weak MD5 hashes against
  online lookup tables; supports single hashes or batch files and returns
  plaintext for common passwords.
---

# PyBozoCrack

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/ikkebr/PyBozoCrack
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install pybozocrack
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `pybozocrack 1b8c...` | MD5 online lookup |
| `pybozocrack -f hashes.txt` | Batch |
| `-s` | Includes special characters |

## Attack Scenario Playbook

### Instant lookup of weak hashes

```bash
pybozocrack 5f4dcc3b5aa765d61d8327deb882cf99
# Common passwords already in the tables come back as plaintext immediately
```

## Notes

Only queries rainbow table results already indexed by Google; it does not crack complex passwords, but it is a zero-cost instant check for weak ones, ideal for fast first-pass screening.

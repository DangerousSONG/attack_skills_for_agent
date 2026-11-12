---
name: cracken-fast-crack
description: "cracken: Filters billion-scale dictionaries using masks. Signals: password cracking, hash cracking, high-speed mask filtering, range."
zh-signals: "cracken: 亿级字典掩码过滤。信号:密码破解,哈希破解,掩码高速过滤,范围。"
when-to-use: "Use cracken when you need to filter billions of existing wordlist entries against a mask pattern at high speed, e.g., to trim rockyou.txt to candidates matching a target's password policy before hash cracking."
---

# cracken

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/shmuelamar/cracken
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install cracken
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cracken 'h?s?a' -w wordlist.txt` | High-speed mask filtering |
| `-p pattern -m min-max` | Range |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Billion-Scale Dictionary Mask Filtering

```bash
cracken '?u?l?l?l?l?l?d' -w rockyou.txt
# Rust performance, hundreds of millions of lines per second
```

## Notes

A Rust mask filtering tool that works with existing wordlists.

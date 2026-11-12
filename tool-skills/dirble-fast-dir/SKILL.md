---
name: dirble-fast-dir
description: "dirble: fast directory brute-forcing. Signals: web vulnerability, injection, directory scanning, dictionary plus threads, recursion."
zh-signals: "dirble: 高速目录爆破。信号:web漏洞,注入,目录扫描,字典+线程,递归。"
when-to-use: "Use for fast Rust-based directory and file brute-forcing with wordlists, threads, extensions, and recursion."
---

# dirble

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/nccgroup/dirble
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install dirble
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dirble https://t.com` | Directory scanning |
| `dirble url -w wordlist.txt -t 20` | Wordlist plus threads |
| `-r` | Recursion |
| `-e php,html` | Extensions |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### High-speed directory brute forcing

```bash
dirble https://t.com -t 50
# Written in Rust by NCC, extremely fast
```

## Notes

Rust directory scanner from NCC, with better performance than the dirb family.

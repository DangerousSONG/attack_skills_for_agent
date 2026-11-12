---
name: wordlistctl-download
description: "wordlistctl: BlackArch wordlist repository. Signals: password cracking, hash cracking, wordlist download, list, search."
zh-signals: "wordlistctl: BlackArch 字典仓库。信号:密码破解,哈希破解,字典下载,列表,搜索。"
when-to-use: >-
  Use when you need to locate or download wordlists from the BlackArch repository for password or
  hash cracking; list or search categories, then download the chosen list locally.
---

# wordlistctl

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/BlackArch/wordlistctl
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/BlackArch/wordlistctl && cd wordlistctl
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 wordlistctl.py -f rockyou -d` | Wordlist download |
| `-l` | List |
| `-s 'category'` | Search |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### BlackArch Wordlist Repository

```bash
python3 wordlistctl.py -f rockyou -d
# One-click management of 300+ wordlists
```

## Notes

A BlackArch wordlist management tool.

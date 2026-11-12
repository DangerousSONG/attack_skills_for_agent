---
name: cangibrina-admin-finder
description: "cangibrina: Discovers administrative panel URLs. Signals: web scanning, vulnerability scanning, admin panel scanning, dictionary, threads."
zh-signals: "cangibrina: 后台地址发现。信号:web扫描,漏洞扫描,后台扫描,字典,线程。"
when-to-use: >-
  Use when assessing a web target and you need to discover hidden administrative
  panel URLs by brute-forcing common paths with a wordlist and configurable
  threads.
---

# cangibrina

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/fnk0c/cangibrina
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/fnk0c/cangibrina && cd cangibrina
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python cangibrina.py -u https://t.com` | Admin panel scanning |
| `-u url -w wordlist.txt` | Wordlist |
| `-t 20` | Threads |

## Attack Scenario Playbook

### Admin Panel URL Discovery

```bash
python cangibrina.py -u https://t.com -w /usr/share/wordlists/dirb/common.txt
# Multi-engine admin panel brute force
```

## Notes

A multi-engine admin panel discovery tool.

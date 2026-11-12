---
name: dirb-dir-scan
description: "dirb: classic directory enumeration. Signals: web scanning, vulnerability scanning, standard scan, large dictionary, extensions."
zh-signals: "dirb: 目录枚举经典款。信号:web扫描,漏洞扫描,标准扫描,大字典,扩展名。"
when-to-use: >-
  Use when you need a stable, classic directory brute-force scan of a web server with wordlist selection, file extensions and optional recursion control.
---

# dirb

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://gitlab.com/kalilinux/packages/dirb
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install dirb
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dirb https://target.com` | Standard scan |
| `big.txt` (not shipped with the library) | Large wordlist |
| `-X .php,.bak` | Extensions |
| `-r` | No recursion |
| `-a UA` | User-Agent spoofing |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### The classic directory enumeration

```bash
dirb https://target.com /usr/share/wordlists/dirb/common.txt -X .php,.html,.bak
```

## Notes

The pioneer of directory scanning preinstalled on Kali; average speed but stable, and friendly to script pipelines.

> 📎 **Reference Document Notice**: this skill is adapted from an upstream open-source repository; the following reference document is **not distributed with this library**: `big.txt`. The key points of the related topics are retained in the corresponding descriptions in this document; if you need the expanded content, grep the library using keywords from the body text or search on your own.

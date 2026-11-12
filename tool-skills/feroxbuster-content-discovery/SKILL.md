---
name: feroxbuster-content-discovery
description: "feroxbuster performs recursive content discovery and API endpoint brute-forcing. Signals: web scanning, vulnerability scanning, single-target scan, deep recursion."
zh-signals: "feroxbuster: 递归内容发现、API 端点爆破。信号:web扫描,漏洞扫描,单目标扫描,深度递归。"
when-to-use: "Use when performing recursive content discovery and API endpoint brute forcing against a web application. Requires a target URL and a wordlist, optionally with recursion depth."
---

# feroxbuster

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/epi052/feroxbuster
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install feroxbuster or brew install feroxbuster; there are also single-binary releases
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-u URL` | Single-target scan |
| `--deep-scan` | Deep recursion |
| `-w wordlist -x php js` | Multiple extensions |
| `-C 403` | Filter status codes |
| `--collect-extensions` | Automatically collect new extensions from responses |
| `--smart-scan` | Probe with HEAD first, then confirm with GET |
| `-r` | Follow redirects |
| `--insecure` | Ignore TLS certificate errors |

## Attack Scenario Playbook

### Recursive content discovery

```bash
feroxbuster -u https://target.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -x php,js,html -C 404,403 -t 80
```

### API endpoint brute force

```bash
feroxbuster -u https://api.target.com/v1 -w endpoints.txt -C 404 -r --insecure
```

## Notes

Written in Rust and extremely fast, with support for automatically learning extensions from responses; use -C (exclude) rather than -x for status code filtering.

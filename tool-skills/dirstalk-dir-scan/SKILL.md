---
name: dirstalk-dir-scan
description: "dirstalk: distributed directory scanning. Signals: web scanning, vulnerability scanning, threads, status filtering."
zh-signals: "dirstalk: 分布式目录扫描。信号:web扫描,漏洞扫描,线程,状态过滤。"
when-to-use: >-
  Use when performing directory brute-force scanning with optional distributed
  agents; provide a target URL and wordlist, and filter by status codes or set
  the thread count.
---

# dirstalk

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/stefanoj3/dirstalk
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/stefanoj3/dirstalk@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dirstalk scan https://t.com -d wordlist.txt` | Directory scanning |
| `-d w.txt -t 30` | Threads |
| `-s status_codes=200,301` | Status filtering |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Distributed directory scanning

```bash
dirstalk scan https://t.com -d raft-medium.txt
# Supports distributed agents
```

## Notes

Go directory scanner with support for distributed scanning.

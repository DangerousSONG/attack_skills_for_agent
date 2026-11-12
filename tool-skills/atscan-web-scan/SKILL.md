---
name: atscan-web-scan
description: "ATSCAN: combines dork and vulnerability scanning engines. Signals: port scan, nmap, dork scan, XSS/SQLi scan, threads"
zh-signals: "ATSCAN: dork+漏洞双引擎。信号:端口扫描,nmap,dork 扫描,XSS/SQLi 扫描,线程。"
when-to-use: >-
  Use when you need a combined dork and vulnerability scanning engine for a
  target, covering dork search, XSS/SQLi checks, and port scanning. Supports
  thread control and output files.
---

# ATSCAN

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/AlisamTechnology/ATSCAN-V3.1
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/AlisamTechnology/ATSCAN-V3.1
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `perl atscan.pl -d 'dork' -l 10` | Dork scan |
| `--target t.com -s` | XSS/SQLi scan |
| `-t 10` | Threads |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Dork + Vulnerability Dual Engine

```bash
perl atscan.pl -d 'inurl:php?id=' -l 20
# Search engine + vulnerability scanning in one
```

## Notes

A Perl multi-engine scanner combining dork/port/XSS/SQLi.

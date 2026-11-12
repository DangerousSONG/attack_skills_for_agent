---
name: v3n0m-sql-xss
description: "V3n0M-Scanner: Multi-vulnerability batch scanning. Signals: web vulnerabilities, injection, dork scan, SSRF patterns, XSS patterns."
zh-signals: "V3n0M-Scanner: 多漏洞批量扫描。信号:web漏洞,注入,dork 扫描,SSRF 模式,XSS 模式。"
when-to-use: "Use when batch-scanning web targets or dork results for SQLi, XSS, SSRF, and LFI at once during early vulnerability triage. Requires a dork or URL list and the Python dependencies installed."
---

# V3n0M-Scanner

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/v3n0m-Scanner/V3n0M-Scanner
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/v3n0m-Scanner/V3n0M-Scanner && cd V3n0M-Scanner && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 v3n0m.py -d 'dork' -p 10` | Dork scan |
| `-s 'dork' -x ssrf` | SSRF pattern |
| `-s dork -x xss` | XSS pattern |
| `-f out.txt` | Output |

## Attack Scenario Playbook

### Multi-vulnerability batch scanning

```bash
python3 v3n0m.py -d 'inurl:php?id=' -p 20
# SQLi/XSS/SSRF/LFI all in one
```

## Notes

A long-standing batch vulnerability scanner, supporting 6 vulnerability types.

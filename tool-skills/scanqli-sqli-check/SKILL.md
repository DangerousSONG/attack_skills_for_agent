---
name: scanqli-sqli-check
description: "ScanQLi: Quickly validates SQL injection. Signals: web vulnerabilities, injection, SQLi scanning, database enumeration, threads."
zh-signals: "ScanQLi: SQLi 快速验证。信号:web漏洞,注入,SQLi 扫描,库枚举,线程。"
when-to-use: >-
  Use when you need to quickly validate SQL injection on a suspected parameter;
  provide the target URL and optionally enumerate databases or set the thread
  count.
---

# ScanQLi

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/bambish/ScanQLi
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/bambish/ScanQLi && cd ScanQLi
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 scanqli.py -u 'https://t.com/?id=1'` | SQLi scan |
| `-u url --dbs` | Database enumeration |
| `-t 10` | Threads |

## Attack Scenario Playbook

### Fast SQLi Validation

```bash
python3 scanqli.py -u 'https://t.com/item?id=5'
# Dual mode: error-based / time-based blind injection
```

## Notes

A lightweight SQLi scanner that supports batch URLs.

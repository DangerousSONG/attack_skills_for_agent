---
name: bbscan-batch-scan
description: "BBScan: batch screens web sensitive paths. Signals: web vulnerability, injection, concurrent processes, custom PoC scripts, collect only, no PoC request"
zh-signals: "BBScan: 批量 Web 敏感路径初筛。信号:web漏洞,注入,并发进程,自定义 PoC 脚本,仅收集,不请求 PoC。"
when-to-use: >-
  Use when you need lightweight batch screening of many web hosts for
  sensitive paths such as git leaks, backups, and admin panels. Supports
  concurrency and custom PoC scripts.
---

# BBScan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/lijiejie/BBScan
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/lijiejie/BBScan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python BBScan.py -u https://t.com` | Single-target sensitive path + information leak scan |
| `python BBScan.py -f urls.txt` | Batch |
| `-p 20` | Concurrent processes |
| `--script scripts/` | Custom PoC scripts |
| `-d` | Collect only, do not request PoC |

## Attack Scenario Playbook

### Batch Web Sensitive Path Screening

```bash
python BBScan.py -f subs.txt -p 50
# Probe git/.svn/.env/backup file/admin panel paths in bulk, then dig deeper manually on hits
```

## Notes

Lightweight batch scanner by lijiejie, with built-in sensitive path rules for git leaks, path traversal, backup files, and more; ideal for large-scale asset screening.

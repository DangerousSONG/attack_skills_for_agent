---
name: snallygaster-secret-scan
description: "snallygaster: web server sensitive file survey. Signals: web vulnerability, injection, secret file scan, debug, disable HTTP."
zh-signals: "snallygaster: Web 服务器敏感文件普查。信号:web漏洞,注入,秘密文件扫描,调试,禁 HTTP。"
when-to-use: >-
  Use during web server reconnaissance to check a host for exposed sensitive
  files, debug endpoints, and insecure HTTP configurations.
---

# snallygaster

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/hannob/snallygaster
- Upstream License: 0BSD (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install snallygaster
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `snallygaster target.com` | Secret file scan |
| `-d` | Debug |
| `--nohttp` | Disable HTTP |
| `-n` | Ignore certificate errors |

## Attack Scenario Playbook

### Web server sensitive file survey

```bash
snallygaster corp.com
# By default checks 50+ high-risk paths such as /.git/.env/.svn/backup files/phpinfo/database dumps
```

## Notes

One of the most comprehensive 'secret file' scanners; purely passive GET requests, non-invasive within the authorized scope.

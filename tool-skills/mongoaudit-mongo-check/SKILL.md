---
name: mongoaudit-mongo-check
description: "mongoaudit: MongoDB unauthorized and weak configuration checks. Signals: port scanning, nmap, MongoDB audit, with authentication, JSON output."
zh-signals: "mongoaudit: MongoDB 未授权+弱配置。信号:端口扫描,nmap,MongoDB 审计,带认证,JSON 输出。"
when-to-use: >-
  Use when assessing a MongoDB instance for unauthorized access, weak authentication and outdated vulnerabilities, with optional credentials and JSON report output.
---

# mongoaudit

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/stampery/mongoaudit
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install mongoaudit
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `mongoaudit -h 10.0.0.5 -p 27017` | MongoDB audit |
| `-h host -u user -p pass` | With authentication |
| `-f out.json` | JSON output |

## Attack Scenario Playbook

### MongoDB unauthorized access and weak configuration

```bash
mongoaudit -h 10.0.0.5
# Unauthorized access, weak credentials, outdated version vulnerabilities
```

## Notes

MongoDB security audit with 10+ checks including CVE coverage.

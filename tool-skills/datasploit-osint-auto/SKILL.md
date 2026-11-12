---
name: datasploit-osint-auto
description: "datasploit: Generates one-click OSINT reports. Signals: email harvesting, employee information, automated OSINT reporting, IP mode, email mode."
zh-signals: "datasploit: 一键 OSINT 综合报告。信号:邮箱收集,员工信息,自动化 OSINT 报告,IP 模式,邮箱模式。"
when-to-use: >-
  Use when you need a one-click OSINT report covering domain, IP, email,
  employee, leak, and GitHub data; provide a target domain, IP, or email and
  run the corresponding mode.
---

# datasploit

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/DataSploit/datasploit
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/DataSploit/datasploit && cd datasploit && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python datasploit.py -i target.com` | Automated OSINT report |
| `-i ip` | IP mode |
| `-i email` | Email mode |
| `-o out/` | Output |

## Attack Scenario Playbook

### One-click OSINT report

```bash
python datasploit.py -i corp.com
# Covers domain/IP/email/leak/GitHub dimensions
```

## Notes

Automated OSINT framework that outputs a consolidated assessment report.

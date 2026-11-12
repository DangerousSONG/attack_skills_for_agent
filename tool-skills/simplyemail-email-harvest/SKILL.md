---
name: simplyemail-email-harvest
description: "SimplyEmail: bulk email address harvesting. Signals: email collection, employee info, multi-source email collection, detailed, JSON output."
zh-signals: "SimplyEmail: 邮箱地址批量收割。信号:邮箱收集,员工信息,邮箱收集(多源),详细,JSON 输出。"
when-to-use: >-
  Use when collecting employee email addresses from public sources for an authorized target
  domain, to build username lists for later security testing.
---

# SimplyEmail

- Attack Category: C03 OSINT Intelligence Gathering
- Upstream Repository: https://github.com/killswitch-GUI/SimplyEmail
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/killswitch-GUI/SimplyEmail && cd SimplyEmail && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python SimplyEmail.py -e target.com -l` | Email collection (multi-source) |
| `-s` | Start an HTTP service for live viewing |
| `-v` | Verbose |
| `--json email.json` | JSON output |

## Attack Scenario Playbook

### Bulk Email Address Harvesting

```bash
python SimplyEmail.py -e corp.com -l
# Crawl the official site and public sources to collect emails, then assemble username lists for spraying
```

## Notes

Multi-source email harvesting plus an online report service, outputting username lists that can feed spraying tools directly.

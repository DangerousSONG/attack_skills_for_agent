---
name: slackpirate-slack
description: "SlackPirate: Slack workspace pentesting. Signals: email collection, employee info, Slack data harvesting, cookie mode, full export."
zh-signals: "SlackPirate: Slack 工作区渗透。信号:邮箱收集,员工信息,Slack 数据收割,Cookie 模式,全导出。"
when-to-use: "Use when performing Slack workspace reconnaissance to harvest messages, files, tokens, and sensitive data, including full export. Requires a workspace cookie or token."
---

# SlackPirate

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/emtunc/SlackPirate
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/emtunc/SlackPirate && cd SlackPirate && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 SlackPirate.py --token xoxb-xxx` | Slack data harvesting |
| `--cookie 'd=xxx'` | Cookie mode |
| `--dump` | Full export |
| `-o out/` | Output |

## Attack Scenario Playbook

### Slack workspace pentest

```bash
python3 SlackPirate.py --token xoxb-leaked
# Search for keys, files, users and channels
```

## Notes

Slack information gathering: search messages, files, tokens and sensitive data.

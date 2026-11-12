---
name: twint-twitter
description: "twint archives target accounts comprehensively. Signals: email collection, employee information, pull all user tweets, keyword search, time window"
zh-signals: "twint: 目标账号全量考古。信号:邮箱收集,员工信息,拉取用户全部推文,关键词搜索,时间窗。"
when-to-use: "Use when conducting Twitter/X OSINT against a target handle or keyword to harvest tweets, emails, phone numbers, and follower relationships for employee and contact discovery. Requires the twint CLI and a valid target handle or search term."
---

# twint

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/twintproject/twint
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `twint -u username -o out.csv --csv` | Pull all tweets from a user |
| `-s 'keyword'` | Keyword search |
| `--since 2023-01-01 --until 2023-06-01` | Time window |
| `-u user --followers` | Follower list |
| `--email --phone` | Filter tweets that leak contact details |

## Attack Scenario Playbook

### Full Archival of a Target Account

```bash
twint -u victim -o tweets.csv --csv
# Pair with grep -iE 'password|vpn|internal|@corp' to mine sensitive self-disclosures
```

## Notes

Scrapes without an API key; when the interface breaks switch to --retweets or your own cookies; a snapshot-style tool whose availability changes with X platform policy.

---
name: holehe-email-check
description: "holehe profiles email registration footprints. Signals: email collection, employee info, check registered sites, show only registered, save cookies."
zh-signals: "holehe: 邮箱注册足迹画像。信号:邮箱收集,员工信息,查邮箱注册站点,只显示已注册,保存 cookies。"
when-to-use: >-
  Use when profiling an email address to discover which online services it is
  registered on via forgot-password side channels during people OSINT.
---

# holehe

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/megadose/holehe
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install holehe
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `holehe test@gmail.com` | Find sites the email is registered on |
| `--only-used` | Show only registered sites |
| `-C creds.json` | Save cookies |
| `-p 20` | Concurrency |
| `--no-passwords` | Do not trigger the password recovery logic |

## Attack Scenario Playbook

### Email Registration Footprint Profiling

```bash
holehe victim@corp.com --only-used
# Output the sites where the account is registered (Twitter/Instagram/Adobe, etc.) to sketch a target profile
```

## Notes

Determines registration status through forgot-password side channels without generating any login attempts, so it stays discreet.

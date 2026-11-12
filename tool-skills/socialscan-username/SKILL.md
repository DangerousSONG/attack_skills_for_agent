---
name: socialscan-username
description: "socialscan: credential combination pre-reconnaissance. Signals: email collection, employee info, email availability or registration lookup, username bulk, specified platform."
zh-signals: "socialscan: 凭据组合前置侦察。信号:邮箱收集,员工信息,邮箱可用性/注册查询,用户名批量,指定平台。"
when-to-use: >-
  Use before credential attacks to check whether target emails or usernames are registered on major platforms, helping build accurate username and email dictionaries.
---

# socialscan

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/iojw/socialscan
- Upstream License: MPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install socialscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `socialscan --email victim@x.com` | Email availability / registration lookup |
| `--username user1 user2` | Usernames in bulk |
| `--platform twitter github` | Specify platforms |
| `--json` | JSON output |

## Attack Scenario Playbook

### Pre-Reconnaissance for Credential Combinations

```bash
socialscan --email a@corp.com --email b@corp.com --username ceo_corp
# Confirm which common usernames/emails are taken to build a precise credential dictionary
```

## Notes

Asynchronous concurrent lookups, faster than holehe; the results feed username-anarchy to generate variant dictionaries.

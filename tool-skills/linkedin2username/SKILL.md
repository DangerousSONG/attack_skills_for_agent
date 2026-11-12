---
name: linkedin2username
description: "linkedin2username: Generate LinkedIn employee usernames. Signals: email collection, employee information, username generation, deep dive."
zh-signals: "linkedin2username: LinkedIn 员工用户名。信号:邮箱收集,员工信息,员工用户名生成,深挖。"
when-to-use: >-
  Use during OSINT before password spraying when you need to turn a company's
  LinkedIn employee listings into likely username or email candidates.
---

# linkedin2username

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/initstring/linkedin2username
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/initstring/linkedin2username
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 linkedin2username.py -c target -u user@mail.com -p pass` | Employee username generation |
| `-c company -n` | Deep dive |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### LinkedIn Employee Usernames

```bash
python3 linkedin2username.py -c 'Target Corp' -u me@mail.com
# scrape the employee directory with a logged-in session and convert it to usernames
```

## Notes

From initstring; converts a LinkedIn company page into a username wordlist.

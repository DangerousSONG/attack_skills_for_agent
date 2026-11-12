---
name: crosslinkedin-osint
description: "CrossLinked: Builds employee dictionaries from LinkedIn. Signals: email harvesting, employee information, format."
zh-signals: "CrossLinked: LinkedIn 员工字典。信号:邮箱收集,员工信息,格式。"
when-to-use: "Use during email OSINT to generate employee email candidates from LinkedIn based on a known corporate email format."
---

# CrossLinked

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/m8sec/CrossLinked
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install crosslinked
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `crosslinked -f '{first}.{last}@corp.com' corp` | LinkedIn employee email generation |
| `-f fmt -t company` | Format |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### LinkedIn Employee Dictionary

```bash
crosslinked -f '{first}.{last}@corp.com' 'Target Corp'
# Preparation step for email spraying
```

## Notes

By m8sec, converts LinkedIn employee information into an email dictionary.

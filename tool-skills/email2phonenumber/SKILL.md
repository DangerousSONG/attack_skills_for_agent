---
name: email2phonenumber
description: "email2phonenumber: reverse lookup phone number from email. Signals: email collection, employee information, email to phone number, deep mode."
zh-signals: "email2phonenumber: 邮箱反查手机号。信号:邮箱收集,员工信息,邮箱→手机号,深度模式。"
when-to-use: >-
  Use when performing OSINT to reverse-lookup a phone number from an email
  address; run in normal or deep mode and save the result for social
  engineering or account recovery research.
---

# email2phonenumber

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/martinvigo/email2phonenumber
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/martinvigo/email2phonenumber && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python email2phonenumber.py -e victim@gmail.com` | Email → phone number |
| `-e email -s` | Deep mode |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Reverse-Lookup Phone Number from Email

```bash
python email2phonenumber.py -e target@mail.com
# A breakthrough point for social engineering
```

## Notes

An OSINT tool that reverse-looks-up phone numbers from leaked data.

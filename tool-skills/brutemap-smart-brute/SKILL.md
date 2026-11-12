---
name: brutemap-smart-brute
description: "brutemap: Brute-forces web login forms. Signals: web vulnerability, injection, login brute force, automatic form recognition, threads."
zh-signals: "brutemap: Web 登录表单口令爆破。信号:web漏洞,注入,登录爆破,自动识别表单,线程。"
when-to-use: >-
  Use when brute-forcing a web login form with user and password lists,
  optionally auto-detecting form fields and response differences. Supports
  thread control.
---

# brutemap

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/brutemap-dev/brutemap
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/brutemap-dev/brutemap && cd brutemap && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python brutemap.py -u https://t.com/login -U users.txt -P pass.txt` | Login brute force |
| `-u url --auto` | Automatic form recognition |
| `-t 10` | Threads |

## Attack Scenario Playbook

### Web Login Form Credential Brute Force

```bash
python brutemap.py -u https://t.com/admin/login -U admin.txt -P top100.txt
# Automatically locate form fields + determine failure from the response
```

## Notes

Web authentication brute forcing that auto-detects login forms and response differences.

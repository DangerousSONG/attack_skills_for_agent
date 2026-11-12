---
name: plecost-wordpress-finger
description: "WordPress target vulnerability surface. Signals: web vulnerability, injection, plugin inventory, JSON output, concurrency 10."
zh-signals: "Plecost: WP 目标漏洞面。信号:web漏洞,注入,插件清单,JSON 输出,并发 10。"
when-to-use: >-
  Use when you have an authorized WordPress target and need to fingerprint the core version,
  installed plugins and themes to map CVE exposure before exploitation. Requires a reachable
  URL and optionally a plugin inventory file.
---

# Plecost

- Attack Category: C09 Web Exploitation (CMS Vulnerabilities)
- Upstream Repository: https://github.com/iniqua/plecost
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install plecost
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `plecost -u https://t.com` | WordPress version/plugin/theme vulnerability scan |
| `-i /usr/share/wordpress/plugins.txt` | Plugin inventory |
| `-o report.json` | JSON output |
| `-n 10` | Concurrency 10 |

## Attack Scenario Playbook

### WordPress target vulnerability surface

```bash
plecost -u https://blog.t.com -o wp.json
# Output plugins and versions that have CVEs, then target those CVEs
```

## Notes

A lightweight pure-Python WordPress vulnerability scanner, lighter than WPScan, with a continuously updated vulnerability database.

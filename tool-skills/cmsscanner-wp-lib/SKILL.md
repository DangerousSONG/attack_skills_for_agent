---
name: cmsscanner-wp-lib
description: "CMSScanner: Uses a WPScan-based engine for generic CMS scanning. Signals: web vulnerability, injection, generic CMS scanning, plugin/theme/user enumeration, forced scan."
zh-signals: "CMSScanner: WPScan 引擎二次开发。信号:web漏洞,注入,通用 CMS 扫描,枚举插件/主题/用户,强制扫描。"
when-to-use: >-
  Use when building or running a custom CMS scanner; the WPScan engine library enumerates
  plugins, themes, and users across supported CMS platforms.
---

# CMSScanner

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/wpscanteam/CMSScanner
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install cms_scanner
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cms_scan -u https://t.com` | Generic CMS scanning |
| `--enumerate p,t,u` | Enumerate plugins/themes/users |
| `-f` | Forced scan |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### WPScan engine secondary development

```bash
cms_scan -u https://t.com -e u
# The underlying library from the WPScan team, ideal for writing custom scanners
```

## Notes

The low-level scanning library behind WPScan, providing a unified API for building custom CMS scanners.

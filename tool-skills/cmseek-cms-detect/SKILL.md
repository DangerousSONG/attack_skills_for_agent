---
name: cmseek-cms-detect
description: "CMSeeK: Identifies CMS fingerprints and detects deep links. Signals: web vulnerability, injection, CMS identification plus vulnerability detection, follow redirects, rescan."
zh-signals: "CMSeeK: CMS 指纹识别+深链检测。信号:web漏洞,注入,CMS 识别+漏洞检测,跟踪重定向,重扫。"
when-to-use: >-
  Use when fingerprinting a web target's CMS and automatically running its
  built-in vulnerability checks; supports redirect following and batch rescans.
---

# CMSeeK

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/Tuhinshubhra/CMSeeK
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Tuhinshubhra/CMSeeK && cd CMSeeK && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python cmseek.py -u https://t.com` | CMS identification + vulnerability detection |
| `--follow-redirect` | Follow redirects |
| `-r` | Rescan |
| `--batch` | Batch mode |
| `--user-agent Mozilla/5.0` | Custom user agent |

## Attack Scenario Playbook

### CMS Fingerprinting + Deep Link Detection

```bash
python cmseek.py -u https://t.com
# Identifies 170+ CMS types and automatically runs the matching vulnerability detection modules
```

## Notes

CMS detection and deep scanning in one tool; when WordPress/Joomla or similar is detected it automatically switches to the matching detection flow.

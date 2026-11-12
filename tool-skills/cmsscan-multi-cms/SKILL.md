---
name: cmsscan-multi-cms
description: "CMSScan: Performs unified detection across multiple CMSs. Signals: web vulnerability, injection, CMS detection plus scanning, specified CMS, report output."
zh-signals: "CMSScan: 多 CMS 统一检测。信号:web漏洞,注入,CMS 检测+扫描,指定 CMS,输出报告。"
when-to-use: >-
  Use when you want a single scan across WordPress, Joomla, and Drupal targets
  to detect the CMS and its vulnerabilities. Supports specifying a CMS, deep
  scanning, and report output.
---

# CMSScan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/ajinabraham/CMSScan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ajinabraham/CMSScan && cd CMSScan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python cms.py -u https://t.com` | CMS detection plus scanning |
| `-u url -c wordpress` | Specify the CMS |
| `-o report` | Output report |
| `-d` | Deep scan |

## Attack Scenario Playbook

### Unified multi-CMS detection

```bash
python cms.py -u https://t.com -d
# Handles WP/Joomla/Drupal in one pass
```

## Notes

By ajinabraham (author of MobSF), a unified entry point for multi-CMS scanning.

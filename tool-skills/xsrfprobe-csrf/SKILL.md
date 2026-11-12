---
name: xsrfprobe-csrf
description: "XSRFProbe: Site-wide CSRF audit. Signals: web vulnerability, injection, site-wide CSRF detection, crawl site forms, crawl depth."
zh-signals: "XSRFProbe: CSRF 全站审计。信号:web漏洞,注入,全站 CSRF 检测,爬取全站表单,爬深。"
when-to-use: >-
  Use when auditing a web application for CSRF issues site-wide, including
  missing tokens, SameSite and Referer validation weaknesses.
---

# XSRFProbe

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/0xInfection/XSRFProbe
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install xsrfprobe
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `xsrfprobe -u https://t.com` | Site-wide CSRF detection |
| `-c` | Crawl site-wide forms |
| `-d depth` | Crawl depth |
| `--cookie='x=1'` | Carry a session |
| `-o out` | Output directory |

## Attack Scenario Playbook

### Site-wide CSRF audit

```bash
xsrfprobe -u https://target.com -c -d 2 -o report
# Test each form for missing tokens/same-origin validation bypass/Referer validation flaws
```

## Notes

The benchmark for automated CSRF auditing; detects whether tokens are validated, whether they are predictable, and whether Referer checks can be bypassed.

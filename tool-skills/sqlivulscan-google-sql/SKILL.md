---
name: sqlivulscan-google-sql
description: "sqlivulscan uses dorks to batch find injection points. Signals: web vulnerability, injection, single target, engine selection"
zh-signals: "sqlivulscan: dork 批量找注入点。信号:web漏洞,注入,单目标,引擎选择。"
when-to-use: >-
  Use when hunting SQL injection points at scale via Google or Bing dorks, or
  when testing a single URL parameter for SQL injection.
---

# sqlivulscan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/Hadesy2k/sqlivulscan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Hadesy2k/sqlivulscan && cd sqlivulscan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python sqlivulscan.py -d 'inurl:php?id='` | Google dork to find SQLi |
| `-t 'http://t.com/?id=1'` | Single target |
| `-e bing` | Engine selection |

## Attack Scenario Playbook

### Batch injection point discovery with dorks

```bash
python sqlivulscan.py -d 'inurl:index.php?id='
# Automatically harvest URLs and test them one by one for error-based injection
```

## Notes

Batch SQLi discovery through search engines plus dorks.

---
name: pinkerton-js-secret
description: "Harvest frontend keys. Signals: web vulnerability, injection, JS key/endpoint extraction, depth."
zh-signals: "Pinkerton: 前端密钥收割。信号:web漏洞,注入,JS 密钥/端点提取,深度。"
when-to-use: >-
  Use when auditing frontend JavaScript for hardcoded keys, secrets and
  endpoints with a configurable crawl depth.
---

# Pinkerton

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/oppsec/Pinkerton
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install pinkerton
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `pinkerton -u https://t.com` | JS key/endpoint extraction |
| `-u url -d 3` | Depth |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Frontend Key Harvesting

```bash
pinkerton -u https://t.com
# Regex-match API key/AccessToken/private key in JS
```

## Notes

Sensitive information extraction from JS files, with 30+ key regexes.

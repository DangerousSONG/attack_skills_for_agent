---
name: xspear-xss-param
description: "XSpear: Parameter-level XSS validation. Signals: web vulnerability, injection, XSS scan, POST data, header injection."
zh-signals: "XSpear: 参数级 XSS 验证。信号:web漏洞,注入,XSS 扫描,POST 数据,头注入。"
when-to-use: >-
  Use when validating XSS at the parameter level, optionally routing traffic
  through Burp for manual confirmation and enabling blind XSS callbacks.
  Accepts GET URLs, POST data, and custom headers.
---

# XSpear

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/hahwul/XSpear
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install XSpear
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `XSpear -u 'https://t.com/?q=123'` | XSS scan |
| `-d 'q=123'` | POST data |
| `--headers='Cookie: a=1'` | Header injection |
| `-b http://127.0.0.1:8080` | Route through Burp |
| `--filter-body='unique'` | Filter |
| `-v` | Verbose |

## Attack Scenario Playbook

### Parameter-Level XSS Validation

```bash
XSpear -u 'https://target/item?id=1' -b http://127.0.0.1:8080
# Results sync to Burp for manual confirmation; supports blind XSS callbacks
```

## Notes

Ruby-based dedicated XSS scanner; the report is grouped by parameter, which pairs efficiently with Burp for secondary confirmation.

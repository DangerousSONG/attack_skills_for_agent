---
name: traxss-xss
description: "traxss scans XSS with authentication. Signals: web vulnerability, injection, with Header, DOM mode"
zh-signals: "traxss: 带认证 XSS 扫描。信号:web漏洞,注入,带 Header,DOM 模式。"
when-to-use: "Use traxss to scan a web application for XSS, especially when the target requires an authenticated session or custom headers such as cookies, or when you need to test DOM-based injection."
---

# traxss

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/M4cs/traxss
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/M4cs/traxss && cd traxss && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 traxss.py -u 'https://t.com/?q=x'` | XSS scan |
| `-u url -H 'Cookie: x'` | With Header |
| `-u url -d` | DOM mode |

## Attack Scenario Playbook

### XSS scanning with authentication

```bash
python3 traxss.py -u 'https://t.com/profile?name=x' -H 'Cookie: session=1'
# Scan with an active session
```

## Notes

Multi-mode XSS scanning with support for custom headers.

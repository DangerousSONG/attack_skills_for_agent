---
name: xsscon-xss
description: "XSSCon: Reflected/stored XSS probing. Signals: web vulnerability, injection, XSS scan, with cookie, threads."
zh-signals: "XSSCon: 反射/存储 XSS 探测。信号:web漏洞,注入,XSS 扫描,带 Cookie,线程。"
when-to-use: "Use to probe web parameters for reflected and stored/DOM XSS, including authenticated scans with cookies."
---

# XSSCon

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/menkrep1337/XSSCon
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/menkrep1337/XSSCon && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 xsscon.py -u 'https://t.com/?q=x'` | XSS scan |
| `-u url --cookies 'x=1'` | With cookies |
| `-u url -t 10` | Threads |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Reflected/stored XSS probing

```bash
python3 xsscon.py -u 'https://t.com/search?q=test'
# DOM/reflected dual mode
```

## Notes

Lightweight XSS scanner with cookie-based authentication support.

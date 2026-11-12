---
name: webpwn3r-xss-scan
description: "webpwn3r: Parameter-level vulnerability scanning. Signals: web vulnerabilities, injection, XSS/injection scan, batch."
zh-signals: "webpwn3r: 参数级漏洞扫描。信号:web漏洞,注入,XSS/注入扫描,批量。"
when-to-use: "Use to scan crawled parameters at scale for XSS and injection issues, including batch URL input."
---

# webpwn3r

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/zigoo0/webpwn3r
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/zigoo0/webpwn3r
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python webpwn3r.py -u https://t.com` | XSS/injection scan |
| `-u url -w urls.txt` | Batch |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Parameter-Level Vulnerability Scanning

```bash
python webpwn3r.py -u https://t.com
# Test each crawled parameter one by one
```

## Notes

Web vulnerability scanning at parameter scale.

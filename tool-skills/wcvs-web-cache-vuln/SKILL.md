---
name: wcvs-web-cache-vuln
description: "Web Cache Vulnerability Scanner (wcvs): Cache poisoning probing. Signals: web vulnerabilities, injection, web cache vulnerability scan, include cache poisoning, custom dictionary."
zh-signals: "Web Cache Vulnerability Scanner (wcvs): 缓存投毒探测。信号:web漏洞,注入,Web 缓存漏洞扫描,包含缓存投毒,自定义字典。"
when-to-use: >-
  Use when testing an authorized web application or CDN for web cache poisoning and deception
  issues, with optional custom wordlists and HTML reporting.
---

# Web Cache Vulnerability Scanner (wcvs)

- Attack Category: C09 Web Exploitation (Cache Poisoning)
- Upstream Repository: https://github.com/Hackmanit/Web-Cache-Vulnerability-Scanner
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/Hackmanit/Web-Cache-Vulnerability-Scanner@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `wcvs -u 'https://t.com'` | Web cache vulnerability scan |
| `-u url -sp -sm` | Include cache poisoning |
| `-u url -d wordlist.txt` | Custom wordlist |
| `-o report.html` | HTML report |

## Attack Scenario Playbook

### Cache poisoning probing

```bash
wcvs -u 'https://t.com' -sp
# Detect cache key handling flaws and poisoning feasibility
```

## Notes

Detects web cache poisoning/deception issues (fake URLs, HTTP header poisoning, cookie poisoning). From the Hackmanit academic team.

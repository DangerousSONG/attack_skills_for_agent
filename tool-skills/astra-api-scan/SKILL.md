---
name: astra-api-scan
description: "Astra: batch scans REST API vulnerabilities. Signals: api attack, interface testing, REST API scan, JSON report, API-only mode"
zh-signals: "Astra: REST API 漏洞批扫。信号:api攻击,接口测试,REST API 扫描,JSON 报告,仅 API 模式。"
when-to-use: >-
  Use when assessing a REST API endpoint and you need batch vulnerability
  scanning aligned with OWASP API Security Top 10, including authentication,
  SQLi, XSS, and information disclosure; supports authenticated headers and JSON
  reports.
---

# Astra

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/flipkart-incubator/Astra
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/flipkart-incubator/Astra && cd Astra && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python astra.py -u https://t.com/api -m scan` | REST API scan |
| `-H 'Authorization: Bearer x'` | Header |
| `-m scan -o json` | JSON report |
| `-u URL -m api` | API-only mode |

## Attack Scenario Playbook

### Batch REST API vulnerability scanning

```bash
python astra.py -u https://api.target.com -m scan
# Outputs results for each OWASP API Top 10 category (authentication/SQLi/XSS/information disclosure)
```

## Notes

API scanner from Flipkart, covering the OWASP API Security Top 10.

---
name: corstest-cors
description: "CORStest: Validates CORS configurations. Signals: web vulnerability, injection, CORS testing, batch."
zh-signals: "CORStest: CORS 配置验证。信号:web漏洞,注入,CORS 测试,批量。"
when-to-use: "Use CORStest when validating a web application's CORS configuration, singly or in batch, to detect permissive cross-origin policies that could enable data theft."
---

# CORStest

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/RUB-NDS/CORStest
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/RUB-NDS/CORStest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python corstest.py -u https://t.com` | CORS testing |
| `-u url -i urls.txt` | Batch |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### CORS Configuration Validation

```bash
python corstest.py -u https://t.com
# Backed by RUB-NDS academic research
```

## Notes

An academic-grade CORS testing tool that detects 9 kinds of misconfiguration.

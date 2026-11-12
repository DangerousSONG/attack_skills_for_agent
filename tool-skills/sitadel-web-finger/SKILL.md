---
name: sitadel-web-finger
description: "Sitadel: quick web asset assessment. Signals: web vulnerability, injection, comprehensive web scan, fingerprinting only, directory brute force."
zh-signals: "Sitadel: Web 资产快速体检。信号:web漏洞,注入,全面 Web 扫描,仅指纹识别,目录爆破。"
when-to-use: >-
  Use when you need a quick web asset assessment combining fingerprinting,
  directory brute force, and basic injection tests; run it against a target URL
  during early web reconnaissance.
---

# Sitadel

- Attack Category: C09 Web Exploitation (Combined Exploitation)
- Upstream Repository: https://github.com/shenril/Sitadel
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/shenril/Sitadel && cd Sitadel && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python sitadel.py https://t.com` | Comprehensive web scan |
| `-f fingerprint` | Fingerprinting only |
| `-a bruteforce` | Directory brute force |
| `-c attack` | XSS/CRLF/SQLi attack testing |

## Attack Scenario Playbook

### Quick web asset assessment

```bash
python sitadel.py https://t.com full
# Fingerprinting, brute force and attack modules in one run, producing a list of risk points
```

## Notes

Modular architecture with four engine types (fingerprint/CMS/brute force/attack), well suited to a quick early assessment.

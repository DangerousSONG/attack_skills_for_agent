---
name: wafninja-waf-bypass
description: "WAFNinja: WAF fingerprinting plus bypass retries. Signals: web vulnerabilities, injection, SQLi payload, identify WAF vendor, custom payload."
zh-signals: "WAFNinja: WAF 指纹+绕过重试。信号:web漏洞,注入,SQLi payload,识别 WAF 厂商,自定义 payload。"
when-to-use: "Use when a web endpoint is protected by a WAF and you need to fingerprint the WAF vendor and retry XSS or SQLi payloads to find a bypass."
---

# WAFNinja

- Attack Category: C09 Web Exploitation (WAF Bypass)
- Upstream Repository: https://github.com/khalilbijjou/WAFNinja
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/khalilbijjou/WAFNinja && cd WAFNinja && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python wafninja.py -u 'https://t.com/?id=1' -t xss` | Batch XSS payload testing |
| `-t sqli` | SQLi payload |
| `--fingerprint` | Identify the WAF vendor |
| `-p 'payload'` | Custom payload |

## Attack Scenario Playbook

### WAF fingerprinting + bypass retries

```bash
python wafninja.py -u 'https://t.com/?q=x' --fingerprint
python wafninja.py -u 'https://t.com/?q=x' -t sqli
# Observe which payload is no longer answered with 403
```

## Notes

A payload library plus WAF fingerprinting; when requests get blocked it quickly identifies the WAF type and tries obfuscated bypasses.

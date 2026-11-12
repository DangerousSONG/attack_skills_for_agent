---
name: identywaf-fingerprint
description: "identYwaf identifies web protections before testing. Signals: web vulnerability, injection, identify WAF brand or model, request file input, random UA."
zh-signals: "identYwaf: 渗透前识别防护。信号:web漏洞,注入,识别 WAF 品牌/型号,从请求文件识别,随机 UA。"
when-to-use: >-
  Use before web vulnerability testing to identify the WAF brand and model behind
  a target URL or captured request, so you can choose an appropriate bypass
  strategy; supports random user agents.
---

# identYwaf

- Attack Category: C09 Web Exploitation (WAF Bypass)
- Upstream Repository: https://github.com/stamparm/identYwaf
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/stamparm/identYwaf
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python identYwaf.py -u 'https://t.com'` | Identify the WAF brand/model |
| `-r req.txt` | Identify from a request file |
| `--random-agent` | Random UA |
| `--health-check` | Connectivity check |

## Attack Scenario Playbook

### Identify protections before pentesting

```bash
python identYwaf.py -u 'https://t.com'
# Output like 'Cloudflare (Cloudflare Inc.)' decides the follow-up bypass strategy
```

## Notes

By Miroslav Stampar (author of sqlmap), with a large and actively maintained WAF fingerprint database covering 80+ WAF products.

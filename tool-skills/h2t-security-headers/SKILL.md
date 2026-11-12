---
name: h2t-security-headers
description: "h2t audits HTTP security header configuration. Signals: web vulnerabilities, injection, HTTP security header scanning, insecure configuration detection, remediation recommendations."
zh-signals: "h2t: 安全头配置审计。信号:web漏洞,注入,扫描 HTTP 安全头,检测不安全配置,输出修复建议。"
when-to-use: >-
  Use when auditing an authorized web application's HTTP security headers and insecure
  configuration, such as missing CSP, HSTS or X-Frame-Options, before assessing clickjacking
  and browser-side risk.
---

# h2t

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/gildasio/h2t
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/gildasio/h2t && cd h2t
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./h2t.sh -S https://t.com` | Scan HTTP security headers |
| `-S url -b` | Detect insecure configuration |
| `-H` | Output remediation recommendations |

## Attack Scenario Playbook

### Security Header Configuration Audit

```bash
./h2t.sh -S https://t.com
# Detect missing CSP/HSTS/X-Frame-Options to support clickjacking assessment
```

## Notes

Audits HTTP security response headers to help assess the browser-side attack surface.

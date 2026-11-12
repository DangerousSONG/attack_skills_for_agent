---
name: hsecscan-header-audit
description: "hsecscan audits OWASP security headers. Signals: web vulnerability, injection, security header scan, verbose, passive mode."
zh-signals: "hsecscan: OWASP 安全头审计。信号:web漏洞,注入,安全头扫描,详细,被动模式。"
when-to-use: >-
  Use when you need a quick passive audit of OWASP security headers on a web target, optionally
  running through a proxy in passive mode.
---

# hsecscan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/riramar/hsecscan
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/riramar/hsecscan && cd hsecscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python hsecscan.py -u https://t.com` | Security header scan |
| `-u url -d` | Verbose |
| `-u url -p` | Passive mode |

## Attack Scenario Playbook

### OWASP security header audit

```bash
python hsecscan.py -u https://t.com
# Full header detection
```

## Notes

An implementation of the OWASP security headers project.

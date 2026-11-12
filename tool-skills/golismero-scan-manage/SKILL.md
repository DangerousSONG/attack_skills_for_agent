---
name: golismero-scan-manage
description: "Golismero performs scanning with knowledge-base management. Signals: web vulnerabilities, injection, fully automated scanning, HTML report, plugin enable."
zh-signals: "Golismero: 带知识库管理的扫描。信号:web漏洞,注入,全自动扫描,HTML 报告,启用插件。"
when-to-use: >-
  Use when you want an automated web vulnerability scan with knowledge-base
  management and HTML reporting, enabling bundled plugins such as nikto and
  nmap.
---

# Golismero

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/golismero/golismero
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/golismero/golismero
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python golismero.py scan t.com` | Fully automated scan |
| `python golismero.py scan t.com -o report.html` | HTML report |
| `-e nikto,nmap` | Enable plugins |
| `-a` | All plugins |

## Attack Scenario Playbook

### Scanning with Knowledge-Base Management

```bash
python golismero.py scan t.com -o report.html
# Results are deduplicated and classified by the knowledge base, suited to team collaboration
```

## Notes

Open-source vulnerability management framework, plugin-based, with built-in deduplication and a reporting system.

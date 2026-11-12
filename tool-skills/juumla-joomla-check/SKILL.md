---
name: juumla-joomla-check
description: "juumla performs quick Joomla checks. Signals: web vulnerability, injection, backup file detection, component detection."
zh-signals: "juumla: Joomla 快速体检。信号:web漏洞,注入,备份文件探测,组件检测。"
when-to-use: >-
  Use when quickly checking a Joomla site for version, vulnerable components,
  exposed backup files, and readable configuration; point it at the target URL
  during web enumeration.
---

# juumla

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/oppsec/juumla
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install juumla
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `juumla -u https://t.com` | Joomla detection and vulnerability scan |
| `-u url --backup-files` | Backup file detection |
| `-u url -c` | Component detection |

## Attack Scenario Playbook

### Quick Joomla health check

```bash
juumla -u https://t.com
# Version/CVE/backup files/readable configuration in a single run
```

## Notes

Lightweight Joomla scanner from oppsec.

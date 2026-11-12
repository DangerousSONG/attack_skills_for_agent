---
name: vbscan-vbulletin
description: "VBScan: vBulletin vulnerability scanning. Signals: web vulnerabilities, injection, vBulletin scan, with cookie, report output."
zh-signals: "VBScan: vBulletin 漏洞扫描。信号:web漏洞,注入,vBulletin 扫描,带 Cookie,输出报告。"
when-to-use: "Use when scanning a vBulletin forum for known version, component, and vulnerability issues."
---

# VBScan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/rezasp/vbscan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/rezasp/vbscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `perl vbscan.pl https://t.com/forum` | vBulletin scan |
| `--cookies 'x=1'` | With Cookie |
| `-o` | Output report |

## Attack Scenario Playbook

### vBulletin vulnerability scan

```bash
perl vbscan.pl https://t.com/forum
# Version / component / vulnerability database comparison
```

## Notes

A dedicated scanner for vBulletin forums.

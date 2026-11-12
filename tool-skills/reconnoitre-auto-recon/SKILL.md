---
name: reconnoitre-auto-recon
description: "reconnoitre: Automates internal network reconnaissance. Signals: red team, methodology, service enumeration, DNS enumeration, full scan."
zh-signals: "reconnoitre: 内网自动侦察。信号:红队,方法论,服务枚举,DNS 枚举,全量。"
when-to-use: "Use when performing automated internal network reconnaissance against a CIDR range and you need service, DNS and SNMP enumeration archived per host with a red team methodology."
---

# reconnoitre

- Attack Category: C50 Red Team Methodology and Automation
- Upstream Repository: https://github.com/codingo/Reconnoitre
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/codingo/Reconnoitre && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 reconnoitre.py -t 10.0.0.0/24 -o out/ --services` | Service enumeration |
| `-t cidr -o out --dns` | DNS enumeration |
| `-t cidr -o out --perform` | Full run |
| `--snmp` | SNMP enumeration |

## Attack Scenario Playbook

### Automated Internal Network Reconnaissance

```bash
python3 reconnoitre.py -t 10.0.0.0/24 -o enum/ --perform
# Automatically archives the directory structure + services + DNS, by codingo
```

## Notes

Automated internal network reconnaissance framework, archiving the output per host.

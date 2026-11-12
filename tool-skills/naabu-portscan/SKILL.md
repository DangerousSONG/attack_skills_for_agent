---
name: naabu-portscan
description: "naabu: Attack surface pipeline integrated with nmap. Signals: port scanning, nmap, single target, batch, top 100 ports."
zh-signals: "naabu: 与 nmap 联动的攻击面流水线。信号:端口扫描,nmap,单目标,批量,top 100 端口。"
when-to-use: "Use when performing fast port scanning of single or multiple targets as part of an attack surface pipeline, typically chained into nmap. Requires target hosts and a port range or top-port selection."
---

# naabu

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/projectdiscovery/naabu
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-host target.com` | Single target |
| `-list hosts.txt` | Batch |
| `-top-ports 100` | Top 100 ports |
| `-p -` | All ports |
| `-rate 3000` | Rate |
| `-nmap-cli 'nmap -sV -oX nmap-output.xml'` | Automatically hand off to nmap once ports are found |

## Attack Scenario Playbook

### Attack Surface Pipeline Integrated with nmap

```bash
naabu -list subdomains.txt -top-ports 1000 -rate 5000 -nmap-cli 'nmap -sV -sC -oX nmap.xml'
# naabu quickly filters live ports, nmap takes over service fingerprinting and script scanning
```

## Notes

A standard component of the ProjectDiscovery ecosystem; -nmap-cli is the key feature that chains fast scanning and deep scanning into a single command.

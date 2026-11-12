---
name: interlace-parallel
description: "Interlace parallelizes penetration testing commands. Signals: red team, methodology, parallel command execution, placeholders, port list."
zh-signals: "Interlace: 渗透命令并行化。信号:红队,方法论,并行命令执行,占位符,端口列表。"
when-to-use: >-
  Use when you need to parallelize an existing command across many targets or ports, turning
  single-threaded recon or scanning steps into concurrent jobs.
---

# Interlace

- Attack Category: C50 Red Team Methodology and Automation
- Upstream Repository: https://github.com/codingo/Interlace
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install interlace
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `interlace -tL targets.txt -threads 5 -c 'nmap {{target}}'` | Parallel command execution |
| `-c 'cmd _target_ _port_'` | Placeholders |
| `-pL ports.txt` | Port list |

## Attack Scenario Playbook

### Parallelizing pentest commands

```bash
interlace -tL ips.txt -threads 20 -c 'nmap -sV {{target}} -oN scans/_target_.nmap'
# Turn a single command into parallel jobs
```

## Notes

Parallel command scheduler for pentesting, by codingo.

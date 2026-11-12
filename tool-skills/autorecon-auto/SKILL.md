---
name: autorecon-auto
description: "AutoRecon: performs fully automated recon for authorized targets. Signals: port scan, nmap, single-target full enumeration, batch, port range"
zh-signals: "AutoRecon: 打靶/授权环境全自动侦察。信号:端口扫描,nmap,单目标全自动枚举,批量,端口范围。"
when-to-use: >-
  Use when you need fully automated enumeration of one or more authorized hosts, from port
  scanning through service-specific checks and consolidated reports.
---

# AutoRecon

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/Tib3rius/AutoRecon
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pipx install git+https://github.com/Tib3rius/AutoRecon.git
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `autorecon 10.0.0.5` | Single-target fully automated enumeration |
| `autorecon --targets targets.txt` | Batch |
| `-p 'T:80,443'` | Port range |
| `-o outdir` | Output |
| `--single-target` | See upstream documentation |

## Attack Scenario Playbook

### Fully Automated Recon for Lab / Authorized Environments

```bash
autorecon 192.168.1.10 -o result
# Automatic: port scan → service identification → run service-specific scripts (nmap NSE/enum4linux/nikto...) → consolidated report
```

## Notes

A god tool for OSCP/labs; automatically schedules the matching enumeration tool per service and produces a well-organized directory structure.

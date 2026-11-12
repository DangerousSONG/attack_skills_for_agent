---
name: vhostscan-virtual-host
description: "VHostScan: Shared IP virtual host discovery. Signals: port scan, nmap, virtual host enumeration, SSL."
zh-signals: "VHostScan: 共享 IP 虚拟主机发现。信号:端口扫描,nmap,虚拟主机枚举,SSL。"
when-to-use: >-
  Use when a target IP may host multiple virtual hosts and you need to enumerate
  them via Host header fuzzing, including SSL-enabled services behind shared
  IPs.
---

# VHostScan

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/codingo/VHostScan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install vhostscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `vhostscan -t 10.0.0.5 -w vhosts.txt` | Virtual host enumeration |
| `-t ip -p 443 --ssl` | SSL |
| `-oN out.txt` | Output |
| `--fuzzy-logic` | Fuzzy matching |

## Attack Scenario Playbook

### Shared IP virtual host discovery

```bash
vhostscan -t 10.0.0.5 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
# Discover hidden sites hosted on the same IP
```

## Notes

A virtual host discovery tool that enumerates via the Host header.

---
name: fscan-intranet
description: "fscan performs one-shot internal initial scans and deep single-host validation. Signals: port scanning, nmap, specified ports, single module."
zh-signals: "fscan: 内网一把梭初扫、单主机深度验证。信号:端口扫描,nmap,指定端口,单模块。"
when-to-use: >-
  Use for a one-shot internal network sweep covering host discovery, ports, service fingerprints, default credentials and built-in POCs, or for deep validation of one host.
---

# fscan

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/shadow1ng/fscan
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
Download fscan.exe / fscan from the release page
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `fscan -h 192.168.0.0/16` | Full scan (ports + services + weak credentials + vulnerabilities) |
| `-h ip -p 22,80,3306` | Specified ports |
| `-m smb` | Single module |
| `-user admin -pwd admin` | Brute-force credentials |
| `-nopoc` | Disable vulnerability probing |
| `-o result.txt` | See the upstream documentation |
| `output` | See the upstream documentation |

## Attack Scenario Playbook

### One-shot internal network sweep

```bash
fscan -h 10.0.0.0/16 -o result.txt
# Automatic: live hosts → ports → service fingerprints → default credentials → built-in POCs such as MS17-010/EternalBlue
```

### Deep validation of a single host

```bash
fscan -h 10.0.0.5 -m all -user administrator -pwd 'Admin@123'
```

## Notes

A domestic red-team tool for internal networks with a built-in POC library (mostly 2021-2023, so watch the currency of the results); the output maps cleanly onto CSV.

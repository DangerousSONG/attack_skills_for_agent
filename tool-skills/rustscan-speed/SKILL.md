---
name: rustscan-speed
description: "RustScan: Fast full-port scanning on a single host. Signals: port scanning, nmap, batch file, pass parameters to nmap, batch rate."
zh-signals: "RustScan: 单机全端口秒扫。信号:端口扫描,nmap,批量文件,透传参数给 nmap,batch 速率。"
when-to-use: >-
  Use when you need to scan all ports on a single host very quickly and then
  pass the results to nmap for service detection.
---

# RustScan

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/bee-san/RustScan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
docker run -it --rm --name rustscan rustscan/rustscan:latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `rustscan -a 10.0.0.5` | All ports on a single IP in about 3 seconds |
| `-a ips.txt` | Batch file |
| `-- -sV` | Pass parameters through to nmap |
| `-b 2500` | Batch rate |
| `-t 1500` | Timeout in ms |

## Attack Scenario Playbook

### All-Ports Scan of a Single Host in Seconds

```bash
rustscan -a 10.0.0.5 -- -sV -sC -oN deep.txt
# RustScan lists the open ports first, then automatically runs nmap fingerprinting
```

## Notes

Adaptive batch scanning avoids IDS single-IP threshold alerts; run it under WSL on Windows.

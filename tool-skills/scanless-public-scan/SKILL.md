---
name: scanless-public-scan
description: "scanless: Performs anonymous port scanning. Signals: port scanning, nmap, public scan service proxy, specified engine."
zh-signals: "scanless: 匿名端口扫描。信号:端口扫描,nmap,公共扫描服务代扫,指定引擎。"
when-to-use: >-
  Use when you need to port scan a target anonymously by proxying through
  public online scanning services to hide your real source IP.
---

# scanless

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/vesche/scanless
- Upstream License: Unlicense (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install scanless
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `scanless -t 10.0.0.5` | Proxy scan via a public scanning service |
| `-s hackertarget` | Specify engine |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Anonymous Port Scanning

```bash
scanless -t target.com
# Scan through third-party services to hide the real IP
```

## Notes

Uses online port scanning services to conceal the scan source.

---
name: pbscan-stateless-scan
description: "Second-level full-subnet scanning. Signals: port scanning, nmap, stateless port scanning, rate, banner capture."
zh-signals: "pbscan: 全网段秒级扫描。信号:端口扫描,nmap,无状态端口扫描,速率,banner 抓取。"
when-to-use: >-
  Use when scanning large CIDR ranges for open ports and you need stateless, high-rate scanning
  with optional banner capture.
---

# pbscan

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/gvb84/pbscan
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/gvb84/pbscan && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pbscan -r 10.0.0.0/24 -p 1-65535` | Stateless port scanning |
| `-r cidr -rate 100000` | Rate |
| `-banner` | Banner capture |

## Attack Scenario Playbook

### Full-subnet scanning in seconds

```bash
./pbscan -r 10.0.0.0/16 -p top100 -rate 500000
# Stateless scanning, a /16 in minutes
```

## Notes

Stateless port scanner, pure rate with no upper limit.

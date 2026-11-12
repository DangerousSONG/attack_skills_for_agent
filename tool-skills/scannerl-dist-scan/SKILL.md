---
name: scannerl-dist-scan
description: "scannerl: Distributed whole-network scanning in Erlang. Signals: port scanning, nmap, distributed fingerprint scanning, batch processing."
zh-signals: "scannerl: Erlang 分布式全网扫描。信号:端口扫描,nmap,分布式指纹扫描,批处理。"
when-to-use: >-
  Use when you need to scan large networks (CIDR ranges) for open ports and
  service fingerprints at scale using distributed, plugin-driven workers.
---

# scannerl

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/avast/scannerl
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/avast/scannerl && cd scannerl && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `scannerl -H 10.0.0.0/24 -P 1-1000 -M banner` | Distributed fingerprint scanning |
| `-H cidr -p top100 -B` | Batch processing |
| `-o out.txt` | Output |
| `-F erlang` | Plugin |

## Attack Scenario Playbook

### Erlang distributed whole-network scanning

```bash
scannerl -H 10.0.0.0/16 -P top1000
# By Avast; a single node scans 16 segments
```

## Notes

Avast's Erlang distributed port scanner, a performance beast.

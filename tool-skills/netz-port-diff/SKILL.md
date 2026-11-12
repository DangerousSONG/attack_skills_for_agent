---
name: netz-port-diff
description: "netz: Network change monitoring. Signals: port scanning, nmap, subnet snapshot, change detection."
zh-signals: "netz: 网络变化监控。信号:端口扫描,nmap,网段快照,变化检测。"
when-to-use: >-
  Use when monitoring a network segment for changes between scans by taking
  snapshots and diffing them to find newly appeared services during an engagement.
---

# netz

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/spectralops/netz
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/spectralops/netz@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `netz 10.0.0.0/24` | Network segment snapshot |
| `netz diff snap1.json snap2.json` | Change detection |
| `-o out.json` | Output |

## Attack Scenario Playbook

### Network Change Monitoring

```bash
netz 10.0.0.0/24 -o before.json
# Spot newly appeared services during the engagement
```

## Notes

By SpectralOps, network segment snapshot plus diff comparison.

---
name: nsntrace-trace
description: "Process-level traffic capture. Signals: port scanning, nmap, per-process packet capture, debugging, filtering."
zh-signals: "nsntrace: 进程级流量捕获。信号:端口扫描,nmap,按进程抓包,调试,过滤。"
when-to-use: "Use nsntrace when you need to capture the traffic of a specific process on Linux for debugging or malware analysis, writing the packets to a pcap with optional filters."
---

# nsntrace

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/jonasdn/nsntrace
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install nsntrace
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `nsntrace -o out.pcap ping 8.8.8.8` | Per-process packet capture |
| `-o file -d` | Debug |
| `-f filter` | Filtering |

## Attack Scenario Playbook

### Process-level traffic capture

```bash
nsntrace -o malware.pcap ./suspect.bin
# Network forensics scoped to a single process
```

## Notes

Linux packet capture tool that filters traffic by process name.

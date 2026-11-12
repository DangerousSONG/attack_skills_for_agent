---
name: angry-ip-scan
description: "Angry IP Scanner (ipscan): performs lightweight host discovery. Signals: port scan, nmap, GUI scan, CLI output alive+ports"
zh-signals: "Angry IP Scanner (ipscan): 轻量存活探测。信号:端口扫描,nmap,GUI 扫描,CLI 输出存活+端口。"
when-to-use: "Use Angry IP Scanner when you need quick host discovery and port checks across IP ranges, through its GUI or CLI mode, as a lightweight alternative to nmap during network scanning."
---

# Angry IP Scanner (ipscan)

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/angryip/ipscan
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
release download ipscan.exe; CLI: java -jar ipscan.jar
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ipscan 192.168.0.0/16` | GUI scan |
| `java -jar ipscan.jar -a -q -s -p 80,443,22 10.0.0.0/24 > out.txt` | CLI output of live hosts + ports |

## Attack Scenario Playbook

### Lightweight host discovery

```bash
java -jar ipscan.jar -a -q 10.0.0.0/24  # Ping + port checks to quickly build a live host list
```

## Notes

GUI first; CLI output needs parsing. For large ranges, screen them roughly with masscan first and follow up afterwards.

---
name: hosthunter-sweep
description: "HostHunter maps IPs to hostnames via OSINT. Signals: network topology, internet mapping, OSINT hostname discovery, batch."
zh-signals: "HostHunter: IP→主机名 OSINT。信号:网络拓扑,互联网测绘,OSINT 主机名发现,批量。"
when-to-use: >-
  Use when you have a set of IP addresses and need to map them to hostnames
  through public OSINT sources for network topology or internet-mapping work.
---

# HostHunter

- Attack Category: C04 Network Topology and Internet Mapping
- Upstream Repository: https://github.com/SpiderLabs/HostHunter
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/SpiderLabs/HostHunter && cd HostHunter
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 hosthunter.py 10.0.0.5 10.0.0.6` | OSINT hostname discovery |
| `-f targets.txt` | Batch |
| `-o out.csv` | Output |

## Attack Scenario Playbook

### IP→hostname OSINT

```bash
python3 hosthunter.py 1.2.3.4 5.6.7.8
# Reverse lookup via certificate transparency plus online sources
```

## Notes

By SpiderLabs; discovers hostnames for target IPs.

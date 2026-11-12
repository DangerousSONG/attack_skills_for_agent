---
name: braa-snmp-mass
description: "braa: batch brute-forces SNMP community strings. Signals: port scan, nmap, timeout/retries, process table"
zh-signals: "braa: SNMP 团体串批量撞库。信号:端口扫描,nmap,超时/重试,进程表。"
when-to-use: >-
  Use during SNMP enumeration when you need to brute-force community strings
  across a whole subnet and read system, user, and process information at scale.
---

# braa

- Attack Category: C42 Network Service Enumeration
- Upstream Repository: https://github.com/mteg/braa
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install braa
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `braa public@10.0.0.0/24:.1.3.6.1.2.1.1.5` | Batch SNMP sysName query |
| `braa private@10.0.0.5:.1.3.6.1.4.1.77.1.2.25` | Enumerate users with the private community string |
| `-t 1` | Timeout/retries |
| `public@x:.1.3.6.1.2.1.25.4.2.1.2` | Process table |

## Attack Scenario Playbook

### Batch SNMP community string brute force

```bash
for c in public private community; do braa $c@10.0.0.0/24:.1.3.6.1.2.1.1.5; done
# Hit community string → read system info / routing table / ARP table
```

## Notes

A high-speed SNMP batch query tool that scans a whole subnet in a single process; extremely effective when paired with a community string wordlist.

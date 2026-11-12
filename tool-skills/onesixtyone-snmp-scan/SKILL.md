---
name: onesixtyone-snmp-scan
description: "Network-wide scan for default SNMP community strings. Signals: port scanning, nmap, direct CIDR scanning, timeout."
zh-signals: "onesixtyone: 默认团体串全网扫描。信号:端口扫描,nmap,CIDR 直接扫,超时。"
when-to-use: >-
  Use when scanning large network ranges for SNMP-enabled devices using default
  community strings such as public, private, and manager; supports CIDR targets
  and custom dictionaries.
---

# onesixtyone

- Attack Category: C42 Network Service Enumeration
- Upstream Repository: https://github.com/trailofbits/onesixtyone
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install onesixtyone
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `onesixtyone -c community.txt -i targets.txt` | SNMP scan (custom community string list) |
| `-c dict.txt 10.0.0.0/24` | Direct CIDR scan |
| `-o out.log` | Output |
| `-w 100` | Timeout |

## Attack Scenario Playbook

### Network-wide scan for default community strings

```bash
echo -e 'public\nprivate\nmanager' > c.txt && onesixtyone -c c.txt -i ips.txt
# Sweeps default community strings off legacy devices/printers/switches
```

## Notes

The Trail of Bits maintained version, a classic SNMP community string scanner, extremely lightweight and suitable for large network segments.

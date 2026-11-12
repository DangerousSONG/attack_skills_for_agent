---
name: asnmap-network-recon
description: "asnmap: maps all enterprise network ranges for a target ASN. Signals: network topology, internet mapping, asnmap"
zh-signals: "asnmap: 目标企业网段全量测绘。信号:网络拓扑,互联网测绘,asnmap`。"
when-to-use: >-
  Use at the start of external recon when you need to map a target
  organization's full ASN and CIDR ranges before feeding them into scanners.
---

# asnmap

- Attack Category: C04 Network Topology Mapping
- Upstream Repository: https://github.com/projectdiscovery/asnmap
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/asnmap/cmd/asnmap@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `echo corp.com | asnmap` | Domain → ASN/CIDR |
| `asnmap -a AS15169 -silent` | Output a CIDR list for an ASN |
| `cat ips.txt | asnmap -json` | Bulk IP → ASN attribution |

## Attack Scenario Playbook

### Full Enumeration of the Target Enterprise's Network Ranges

```bash
echo corp.com | asnmap -silent | tee cidrs.txt
# Output all ASN+CIDR for the organization, then feed them to amass/nmap for full scanning
```

## Notes

By ProjectDiscovery, maps IP to ASN/CIDR to establish the asset boundary of the enterprise network.

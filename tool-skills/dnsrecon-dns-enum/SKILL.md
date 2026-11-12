---
name: dnsrecon-dns-enum
description: "dnsrecon: SRV record internal service discovery and zone transfer attempts. Signals: subdomain, domain enumeration, standard enumeration, dictionary brute force."
zh-signals: "dnsrecon: SRV 记录挖内部服务、Zone Transfer 尝试。信号:子域名,域名枚举,标准枚举,字典爆破。"
when-to-use: "Use dnsrecon when performing domain reconnaissance and you need standard enumeration, zone-transfer attempts, dictionary brute-forcing, or SRV record discovery to map internal services and domain controllers."
---

# dnsrecon

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/darkoperator/dnsrecon
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install dnsrecon or pip install dnsrecon
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-d target.com` | Standard enumeration |
| `-t axfr` | Zone transfer check |
| `-t brt -D wordlist` | Dictionary brute force |
| `-t srv` | SRV record enumeration |
| `-t rvl` | Reverse lookup |
| `--csv out.csv` | CSV output |
| `--threads 10` | Threads |

## Attack Scenario Playbook

### Discovering internal services via SRV records

```bash
dnsrecon -d corp.com -t srv --csv srv.csv
# Output such as _ldap._tcp → locate domain controller / mail / conferencing services
```

### Zone transfer attempt

```bash
dnsrecon -d target.com -t axfr
```

## Notes

A Python-enhanced version of dnsenum; SRV enumeration is highly valuable in AD environments; XML/CSV output makes piping easy.

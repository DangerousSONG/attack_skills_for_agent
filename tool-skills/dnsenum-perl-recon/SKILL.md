---
name: dnsenum-perl-recon
description: "dnsenum: comprehensive DNS enumeration. Signals: subdomain, domain enumeration, standard enumeration, dictionary brute force, recursive subdomains."
zh-signals: "dnsenum: DNS 全面枚举。信号:子域名,域名枚举,标准枚举,字典爆破,递归子域。"
when-to-use: >-
  Use when performing DNS reconnaissance against a domain, including NS/MX/A
  records, zone transfer attempts, dictionary brute force, recursive subdomains,
  and whois netblock reverse lookup.
---

# dnsenum

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/fwaeytens/dnsenum
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install dnsenum
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dnsenum target.com` | Standard enumeration |
| `-f wordlist.txt` | Dictionary brute force |
| `-r` | Recursive subdomains |
| `-w` | Whois netblock reverse lookup |
| `-d 15` | Dictionary threads |
| `-o out.xml` | XML output |

## Attack Scenario Playbook

### Comprehensive DNS Enumeration

```bash
dnsenum corp.com -w -r -o dns.xml
# Output: NS/MX/A/AXFR attempts/whois netblocks/reverse resolution
```

## Notes

A classic Perl script; zone transfer (-f) is a straight-up break point on misconfigured domains.

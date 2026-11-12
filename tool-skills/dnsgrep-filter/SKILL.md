---
name: dnsgrep-filter
description: "dnsgrep: filter targets from massive DNS data. Signals: subdomain, domain enumeration, regex."
zh-signals: "dnsgrep: 海量 DNS 数据筛目标。信号:子域名,域名枚举,正则。"
when-to-use: >-
  Use when you have a large DNS dataset and need to quickly filter it down to
  subdomains or records matching a domain or regex.
---

# dnsgrep

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/erbbysam/dnsgrep
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/erbbysam/dnsgrep && cd dnsgrep && go build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cat big_dns.txt | ./dnsgrep -f corp.com` | DNS data filtering |
| `-f domain -o out.txt` | Output |
| `-r regex` | Regex |

## Attack Scenario Playbook

### Filter Targets from Massive DNS Data

```bash
cat rapid7_dns.txt | ./dnsgrep -f '\.corp\.com'
# Mine target subdomains from the dataset
```

## Notes

Quickly filters large DNS datasets (such as CERT datasets).

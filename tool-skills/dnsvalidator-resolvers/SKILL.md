---
name: dnsvalidator-resolvers
description: "dnsvalidator: build clean resolver pool. Signals: subdomain, domain enumeration, validate DNS resolvers, threads, concurrency."
zh-signals: "dnsvalidator: 构建干净 resolver 池。信号:子域名,域名枚举,验证 DNS 解析器,线程,并发。"
when-to-use: "Use before subdomain brute forcing or large-scale DNS enumeration to validate and filter public resolvers, removing poisoned or unreliable ones. Requires a candidate resolver list and is typically run as a prerequisite for amass or shuffledns."
---

# dnsvalidator

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/vortexau/dnsvalidator
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/vortexau/dnsvalidator && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 dnsvalidator.py -tL public_resolvers.txt -o valid.txt` | Validate DNS resolvers |
| `-tL file -threads 100` | Threads |
| `-c 500` | Concurrency |

## Attack Scenario Playbook

### Build a clean resolver pool

```bash
python3 dnsvalidator.py -tL resolvers.txt -o clean.txt
# Essential before subdomain brute forcing, removes poisoned resolvers
```

## Notes

DNS resolver cleansing tool, a prerequisite for amass and shuffledns.

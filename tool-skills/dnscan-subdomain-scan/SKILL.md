---
name: dnscan-subdomain-scan
description: "dnscan: recursive subdomain brute-forcing. Signals: subdomain, domain enumeration, dictionary subdomain brute force, threads, recursive scan after discovered subdomains."
zh-signals: "dnscan: 递归子域爆破。信号:子域名,域名枚举,字典爆破子域,线程,发现子域后递归扫。"
when-to-use: >-
  Use when brute-forcing subdomains from a dictionary and recursively scanning
  newly discovered subdomains; set a wordlist and enable recursive mode for
  deep subdomain coverage.
---

# dnscan

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/rbsec/dnscan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/rbsec/dnscan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python dnscan.py -d target.com -w wordlist.txt` | Wordlist subdomain brute force |
| `-d domain -w subs.txt -t 30` | Threads |
| `-D` | Recursively scan subdomains once they are discovered |
| `-o out.txt` | Output |
| `-x example.com` | Exclude domain |

## Attack Scenario Playbook

### Recursive subdomain brute force

```bash
python dnscan.py -d corp.com -w subdomains-top1mil.txt -D -o found.txt
```

## Notes

Recursive mode (-D) works well for deep subdomains such as dev.us.corp.com; wildcard detection is supported.

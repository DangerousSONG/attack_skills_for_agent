---
name: fierce-dns-recon
description: "Fierce discovers adjacent network segments. Signals: asset mapping, subdomains, classic DNS reconnaissance, wordlists, IP sweep depth."
zh-signals: "Fierce: 周边网段发现。信号:资产测绘,子域名,经典 DNS 侦察,字典,IP 遍历深度。"
when-to-use: >-
  Use when doing classic DNS reconnaissance and you want to infer adjacent internal network
  ranges and discover systems that have no public DNS records.
---

# Fierce

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/mschwager/fierce
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install fierce
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `fierce --domain target.com` | Classic DNS reconnaissance |
| `--subdomains wordlist` | Wordlist |
| `--traverse 10` | IP sweep depth |
| `--dns-servers 8.8.8.8` | Resolver |

## Attack Scenario Playbook

### Adjacent network segment discovery

```bash
fierce --domain corp.com --traverse 10
# Infer and sweep adjacent network segments from DNS records, often revealing internal systems with no domain name
```

## Notes

A Perl-era classic; its "domain to network range" inference logic is still reused today.

---
name: aiodnsbrute-dns
description: "aiodnsbrute: brute-forces subdomains at million scale. Signals: subdomain, domain enumeration, async DNS brute force, concurrency"
zh-signals: "aiodnsbrute: 百万级子域爆破。信号:子域名,域名枚举,异步 DNS 爆破,并发。"
when-to-use: "Use when brute-forcing subdomains at high volume with asynchronous DNS queries. Requires a target domain, a wordlist, and concurrency settings."
---

# aiodnsbrute

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/blark/aiodnsbrute
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install aiodnsbrute
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `aiodnsbrute -w wordlist.txt -t 500 corp.com` | Async DNS brute force |
| `-w w.txt -t t -o out.txt` | Output |
| `--max-tasks 5000` | Concurrency |

## Attack Scenario Playbook

### Million-scale subdomain brute force

```bash
aiodnsbrute -w all.txt -t 2000 corp.com
# asyncio-based, far faster than dnsrecon
```

## Notes

Async DNS brute force with extremely strong performance.

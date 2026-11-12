---
name: altdns-permutation
description: "altdns: mutates known subdomains for brute forcing. Signals: subdomain, domain enumeration, permutation candidate generation, resolve after generation, threads"
zh-signals: "altdns: 已知子域变形爆破。信号:子域名,域名枚举,置换生成候选子域,生成后解析,线程。"
when-to-use: >-
  Use when you already have known subdomains and want to generate permutation candidates such as
  dev-api and api-dev, then resolve them to find hidden hosts.
---

# altdns

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/infosec-au/altdns
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install py-altdns
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `altdns -i known.txt -o permutations.txt -w words.txt` | Generate permutation candidate subdomains |
| `-r -s resolved.txt` | Resolve after generation |
| `-t 20` | Threads |

## Attack Scenario Playbook

### Mutation Brute Force of Known Subdomains

```bash
altdns -i subs.txt -o cand.txt -w ~/tools/words.txt -r -s resolved.txt
# Generate permutations such as dev-api/api-dev from known subdomain patterns and resolve them
```

## Notes

Solves "unknown patterns beyond the known subdomains"; works best when paired with massdns/puredns for resolution.

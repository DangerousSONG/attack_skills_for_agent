---
name: knockpy-subdomain
description: "Knock enumerates subdomains and detects takeovers. Signals: subdomain, domain enumeration, passive and dictionary enumeration, custom dictionary, brute-only mode."
zh-signals: "Knock: 子域枚举+接管检测。信号:子域名,域名枚举,被动+字典枚举,自定义字典,纯爆破模式。"
when-to-use: >-
  Use when enumerating subdomains and checking for subdomain takeover; choose
  passive-plus-dictionary mode or brute-force mode and supply a custom wordlist
  if needed.
---

# Knock

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/guelfoweb/knock
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install knockpy
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `knockpy target.com` | Passive + dictionary enumeration |
| `-w wordlist.txt` | Custom wordlist |
| `--bruteforce` | Brute-force only mode |
| `-o json` | JSON output |
| `--resolve` | Resolution verification |
| `-t 5` | Threads |

## Attack Scenario Playbook

### Subdomain Enumeration + Takeover Detection

```bash
knockpy corp.com -o json
jq -r '.subdomains[] | select(.zone_transfer==true)' report/*.json  # zone transfer solves it outright
```

## Notes

Built-in takeover detection (three/others); when a zone transfer is found it dumps all zones directly.

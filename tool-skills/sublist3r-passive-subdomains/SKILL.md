---
name: sublist3r-passive-subdomains
description: "Sublist3r generates fast subdomain lists. Signals: asset mapping, subdomain, classic passive subdomain enumeration, live port probing, threads"
zh-signals: "Sublist3r: 快速子域清单。信号:资产测绘,子域名,经典被动子域枚举,探测存活端口,线程。"
when-to-use: >-
  Use when you need a fast passive subdomain list for initial asset mapping.
  It aggregates multiple search engines without API keys, and can optionally
  brute-force, probe live ports, and set thread count.
---

# Sublist3r

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/aboul3la/Sublist3r
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/aboul3la/Sublist3r && cd Sublist3r && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python sublist3r.py -d target.com` | Classic passive subdomain enumeration |
| `-b` | Enable the bruteforce module |
| `-p 80,443` | Probe live ports |
| `-t 50` | Threads |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Fast Subdomain List

```bash
python sublist3r.py -d target.com -t 100 -o subs.txt
cat subs.txt | httpx -silent -o alive.txt
```

## Notes

A classic long-standing tool that aggregates multiple search engines; runs without an API key, ideal for quickly producing a first-pass list.

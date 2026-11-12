---
name: fav-up-favicon-lookup
description: "Fav-up: real IP reverse lookup using favicon hashes. Signals: network topology, internet mapping, batch favicon."
zh-signals: "Fav-up: 真实 IP 反查(favicon 哈希)。信号:网络拓扑,互联网测绘,批量 favicon。"
when-to-use: >-
  Use when locating the real origin IP behind a WAF or CDN by matching favicon
  hashes against Shodan and Censys.
---

# Fav-up

- Attack Category: C04 Network Topology and Internet Mapping
- Upstream Repository: https://github.com/pielco11/fav-up
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/pielco11/fav-up && cd fav-up && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 favUp.py -fw favicon.ico` | Reverse lookup IP from favicon |
| `-sc` | Query Shodan/Censys at the same time |
| `-w targets.txt` | Batch favicons |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Real IP reverse lookup (favicon hash)

```bash
curl -s https://target.com/favicon.ico -o fav.ico
python3 favUp.py -fw fav.ico -sc  # Match the hash against assets with the same icon on Shodan → origin IP
```

## Notes

One of the three classic techniques for locating the origin server behind a WAF/CDN (favicon hash / DNS records / certificate transparency); verify it with tools such as cloudmare.

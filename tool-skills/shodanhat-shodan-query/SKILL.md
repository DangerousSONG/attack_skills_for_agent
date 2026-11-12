---
name: shodanhat-shodan-query
description: "ShodanHat: batch Shodan asset harvesting. Signals: network topology, internet mapping, certificate matching, combined filters."
zh-signals: "ShodanHat: Shodan 批量资产收割。信号:网络拓扑,互联网测绘,证书匹配,组合过滤。"
when-to-use: >-
  Use during internet-facing asset discovery when you have a Shodan API key and
  want to run bulk queries by org, SSL certificate, product, or country and
  export the results for source-site and admin panel mapping.
---

# ShodanHat

- Attack Category: C04 Network Topology Mapping
- Upstream Repository: https://github.com/HatBashBR/ShodanHat
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/HatBashBR/ShodanHat && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python ShodanHat.py -k $KEY -q 'org:Target'` | Shodan search + write results to database |
| `-q 'ssl:corp.com'` | Certificate matching |
| `-q 'product:Apache' --country BR` | Combined filters |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Batch Shodan Asset Harvesting

```bash
python ShodanHat.py -k KEY -q 'hostname:corp.com 200 OK'
# Bypass the CDN to hit origin servers and admin panels directly
```

## Notes

A Shodan query wrapper with result export and bulk IP handling, useful with an API key for corporate asset inventories.

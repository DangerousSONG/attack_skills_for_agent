---
name: dnsmap-subdomain
description: "dnsmap: fast subdomain initial screening. Signals: asset mapping, subdomain, subdomain brute force, custom dictionary, result file."
zh-signals: "dnsmap: 快速子域初筛。信号:资产测绘,子域名,子域爆破,自定义字典,结果文件。"
when-to-use: "Use when performing initial subdomain enumeration for asset mapping and you need a lightweight, zero-config brute force with the built-in dictionary or a custom wordlist."
---

# dnsmap

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/resurrecting-open-source-projects/dnsmap
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install dnsmap
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dnsmap target.com` | Subdomain brute force |
| `-w wordlist` | Custom wordlist |
| `-r out.txt` | Result file |
| `-i ipskip.txt` | Ignore IPs |

## Attack Scenario Playbook

### Fast subdomain initial screening

```bash
dnsmap corp.com -r subs.txt
```

## Notes

Lightweight subdomain brute forcing; the dictionary is built in, so it runs with zero configuration.

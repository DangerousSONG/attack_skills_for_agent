---
name: hakrevdns-reverse
description: "hakrevdns reverse-resolves IP ranges to domains. Signals: network topology, internet mapping, dictionaries."
zh-signals: "hakrevdns: IP 段反查域名。信号:网络拓扑,互联网测绘,字典。"
when-to-use: "Use during network topology mapping to reverse-resolve IP ranges into domains for asset discovery. Requires an IP range or host list and optionally a wordlist."
---

# hakrevdns

- Attack Category: C04 Network Topology and Internet Mapping
- Upstream Repository: https://github.com/hakluke/hakrevdns
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/hakluke/hakrevdns@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `echo 10.0.0.5 | hakrevdns -d corp.local` | PTR reverse lookup |
| `-d domain -w wordlist` | Wordlist |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Reverse-Resolve IP Ranges to Domains

```bash
echo {1..254} | sed 's/^/10.0.0./' | hakrevdns
# Enumerate internal/public PTR records
```

## Notes

By hakluke, a reverse DNS enumeration tool.

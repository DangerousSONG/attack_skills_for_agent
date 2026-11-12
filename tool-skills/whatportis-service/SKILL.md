---
name: whatportis-service
description: "whatportis: Non-standard port identification. Signals: port scan, nmap, port service query, service reverse lookup, fuzzy."
zh-signals: "whatportis: 非标准端口识别。信号:端口扫描,nmap,端口服务查询,服务反查,模糊。"
when-to-use: >-
  Use when you see non-standard ports and need to identify the likely service
  through port-to-service queries and fuzzy reverse lookup.
---

# whatportis

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/ncrocfer/whatportis
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install whatportis
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `whatportis 3306` | Port service query |
| `whatportis mysql` | Service reverse lookup |
| `--like` | Fuzzy |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Non-standard port identification

```bash
whatportis 8443
# Supports fingerprinting
```

## Notes

Port-to-service mapping lookups, useful for IOC analysis.

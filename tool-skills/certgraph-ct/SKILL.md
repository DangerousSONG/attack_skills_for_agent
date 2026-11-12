---
name: certgraph-ct
description: "CertGraph: Builds asset graphs from Certificate Transparency logs. Signals: asset mapping, subdomains, CT log graph traversal, depth, CT logs only."
zh-signals: "CertGraph: CT 日志资产图。信号:资产测绘,子域名,证书透明度图遍历,深度,只查 CT log。"
when-to-use: >-
  Use during asset mapping to traverse Certificate Transparency logs and discover
  related domains and subdomains through certificate SAN fields.
---

# CertGraph

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/JamesHabben/certgraph
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/JamesHabben/certgraph@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `certgraph target.com` | Certificate transparency graph traversal |
| `-depth 5` | Depth |
| `-ct` | CT logs only |

## Attack Scenario Playbook

### CT log asset graph

```bash
certgraph corp.com -depth 4 -o graph.json  # Recursively discover related domains from SAN fields
```

## Notes

Recursively crawls domains from certificate SAN fields; a wildcard certificate can link an entire organization's assets at once.

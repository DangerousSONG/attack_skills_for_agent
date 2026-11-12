---
name: graphinder-js-endpoints
description: "Graphinder discovers hidden GraphQL endpoints. Signals: attack surface, cloud assets, subdomain correlation."
zh-signals: "Graphinder: 隐藏 GraphQL 端点发现。信号:攻击面,云资产,子域联动。"
when-to-use: "Use Graphinder when mapping a target's external attack surface and you need to discover hidden GraphQL endpoints by correlating subdomains and extracting endpoints from JavaScript bundles."
---

# Graphinder

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/EscuelaTechnica/graphinder
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install graphinder
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `graphinder -d corp.com` | GraphQL endpoint discovery in JS |
| `-d domain -s` | Subdomain correlation |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Hidden GraphQL Endpoint Discovery

```bash
graphinder -d corp.com
# Dig through JS bundles for /graphql endpoints
```

## Notes

Extracts GraphQL/Apollo endpoints from JavaScript files.

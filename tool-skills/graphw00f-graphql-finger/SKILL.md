---
name: graphw00f-graphql-finger
description: "graphw00f locates GraphQL endpoints and fingerprints technology stacks. Signals: API attacks, interface testing, full fingerprint database detection."
zh-signals: "graphw00f: GraphQL 端点定位+技术栈。信号:api攻击,接口测试,指纹库全检测。"
when-to-use: >-
  Use during API or GraphQL reconnaissance when you need to locate a GraphQL
  endpoint and fingerprint its engine so you can map known vulnerabilities.
---

# graphw00f

- Attack Category: C10 API and GraphQL Attacks
- Upstream Repository: https://github.com/dolevf/graphw00f
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/dolevf/graphw00f && cd graphw00f && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 main.py -d -t https://t.com/graphql` | GraphQL engine fingerprinting |
| `-f` | Full fingerprint database detection |
| `-p` | Probe for GraphQL endpoints only |

## Attack Scenario Playbook

### GraphQL Endpoint Discovery and Tech Stack Fingerprinting

```bash
python3 main.py -d -t https://t.com/api
# Identify engines such as Apollo/Hasura/Lighthouse, then target the matching CVEs
```

## Notes

A GraphQL server fingerprint database; once the engine is identified, look up its known vulnerabilities (such as the debug interface in older Apollo releases).

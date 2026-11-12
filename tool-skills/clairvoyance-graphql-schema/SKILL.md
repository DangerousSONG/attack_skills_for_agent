---
name: clairvoyance-graphql-schema
description: "clairvoyance: Collects information from introspection-disabled GraphQL. Signals: API attack, interface testing, authenticated requests, dictionary enhancement."
zh-signals: "clairvoyance: 关闭内省的 GraphQL 信息收集。信号:api攻击,接口测试,带认证,字典增强。"
when-to-use: >-
  Use when a GraphQL endpoint has introspection disabled and you need to
  reconstruct the schema via field guessing and error differences.
---

# clairvoyance

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/nikitastupin/clairvoyance
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install clairvoyance
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python -m clairvoyance https://t.com/graphql -o schema.json` | Reconstruct schema when introspection is disabled |
| `-H 'Authorization: Bearer x'` | With authentication |
| `-w wordlist.txt` | Wordlist enhancement |

## Attack Scenario Playbook

### Information gathering against GraphQL with introspection disabled

```bash
python -m clairvoyance https://api.target.com/graphql -o schema.graphql
# Rebuild the full schema via field guessing and error message differences
```

## Notes

Schema reconstruction when introspection is blocked; the output can be imported directly into GraphQLmap/Burp.

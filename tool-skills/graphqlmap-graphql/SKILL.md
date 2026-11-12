---
name: graphqlmap-graphql
description: "GraphQLmap enumerates GraphQL interface attack surfaces. Signals: API attacks, interface testing, interactive mode, NoSQL injection testing, mutation testing."
zh-signals: "GraphQLmap: GraphQL 接口攻击面枚举。信号:api攻击,接口测试,交互模式,NoSQL 注入测试,测试 mutation。"
when-to-use: >-
  Use when testing a GraphQL API and you want to dump its schema, enumerate
  queries and mutations, and probe for NoSQL or SQL injection and authorization
  flaws.
---

# GraphQLmap

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/swisskyrepo/GraphQLmap
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/swisskyrepo/GraphQLmap && cd GraphQLmap && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python graphqlmap.py -u https://t.com/graphql` | Interactive mode |
| `dump_new` | Export the schema and endpoints |
| `nosqli` | NoSQL injection testing |
| `postgresqli` | SQL injection testing |
| `mutation` | Test mutations |
| `intent` | See the upstream documentation |
| `privilege bypass probe` | See the upstream documentation |

## Attack Scenario Playbook

### GraphQL interface attack surface enumeration

```bash
python graphqlmap.py -u https://api.target.com/graphql
GraphQLmap > dump_new  # export all type/query/mutation
GraphQLmap > nosqli  # parameter injection testing
```

## Notes

Interactive GraphQL penetration testing; the dumped interface surface directly guides privilege bypass and injection testing.

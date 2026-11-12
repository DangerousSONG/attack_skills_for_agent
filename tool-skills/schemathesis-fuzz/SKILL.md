---
name: schemathesis-fuzz
description: "Schemathesis: OpenAPI specification-driven fuzzing. Signals: API attack, interface testing, property-based fuzzing, test endpoints only, full checks."
zh-signals: "Schemathesis: OpenAPI 规范驱动模糊测试。信号:api攻击,接口测试,属性化模糊测试,只测端点,全检查。"
when-to-use: >-
  Use when an OpenAPI schema is available and you want property-based fuzzing of API endpoints
  with authenticated requests to surface crashes and validation gaps.
---

# Schemathesis

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/schemathesis/schemathesis
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install schemathesis
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `st run https://t.com/openapi.json` | Property-based fuzzing |
| `-H 'Authorization: Bearer x'` | Header |
| `-E POST /users` | Test endpoints only |
| `--checks all` | All checks |
| `-o yaml` | Report format |
| `--stateful=links` | Stateful testing |

## Attack Scenario Playbook

### OpenAPI Specification-Driven Fuzzing

```bash
st run https://api.target.com/openapi.json -H 'Authorization: Bearer $TOKEN' --checks all
# Automatically generates boundary values/type confusion/SQLi-style inputs and outputs reproducible cases
```

## Notes

Automatically generates test cases from the OpenAPI/Swagger specification; contract violations and 5xx responses are both findings.

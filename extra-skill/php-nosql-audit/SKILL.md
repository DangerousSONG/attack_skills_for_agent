---
name: php-nosql-audit
description: "PHP Web source code NoSQL injection audit tool. Identifies user input reaching MongoDB/DocumentDB query construction, analyzes whether operator injection ($gt/$ne/$where, etc.) is possible, and outputs severity grading, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的 NoSQL 注入风险，识别 operator 注入导致的鉴权绕过与数据泄露。信号:PHP 审计,NoSQL 注入,MongoDB,operator 注入,源码审计"
when-to-use: "Use when reviewing PHP source code where user input reaches MongoDB/DocumentDB query construction and operator injection is possible."
---

# PHP NoSQL Injection Audit (php-nosql-audit)

Analyze PHP project source code to identify how user input enters NoSQL query conditions, and detect operator injection leading to authentication bypass / data exposure.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-NOSQL-{sequence}`

## Mandatory Sinks to Check (Required)
Common in MongoDB drivers / ODM:
- `collection->find($filter)`
- `findOne($filter)` / `update($filter, {value})` / `delete($filter)`
- `where($condition)` or `->filter({value})`
- Wrapper functions that splice user input into the query array/expression

## Mandatory Dangerous Patterns (Required)
Must output the evidence for the following judgments:
- User input used directly as part of the filter/condition array (especially the result of `json_decode`)
- Behavior that "treats user input as a structured condition" without enforcing types/allowlists
- Query contains operator fields that can be abused: `$ne/$gt/$lt/$or/$and/$where/$regex`

## tracer Trigger Conditions
When the user input is JSON / an array / a nested structure and several layers of wrapping exist before query construction, the trace must reach the final sink.

## Report Output
```
{output_path}/vuln_audit/nosql_{timestamp}.md
```

## Entry Template (Mandatory)
Every vulnerability must include:
- Location evidence (the query construction function / the final find/update call)
- Data flow chain (input parsing -> type -> query condition)
- Exploitability preconditions (authentication state / whether login is required / whether the query operator can be changed)
- Verification PoC (must use the real route and the real parameter name; the payload is a structured NoSQL condition example)
- Recommended fixes (strict field allowlist + enforced types + never treat user input as a query expression)

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected NoSQL injection vulnerability must cite the matching evidence points of the **NOSQL row** in the `## 9) Sink Evidence Type Checklist` section of the trace output item by item (the status may be pending verification, but the evidence citations must exist):
1. `EVID_NOSQL_QUERY_CONSTRUCTION`: evidence of the NoSQL query construction point (the corresponding find/update/delete or query builder execution point)
2. `EVID_NOSQL_USER_INPUT_INTO_QUERY_STRUCTURE`: evidence of user input entering the query condition structure (the controllable field entering the filter/where structure)
3. `EVID_NOSQL_OPERATOR_INJECTION_FIELDS`: evidence of the operator injection fields ($ne/$gt/$or/$where/$regex, etc.)

## Handling Missing tracer Evidence (Mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.

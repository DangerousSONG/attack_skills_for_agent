---
name: php-sql-audit
description: "PHP web source code SQL injection vulnerability auditing tool. Identifies every SQL execution point in the source code, analyzes injection risk, and outputs exploitability ratings, PoCs, and remediation recommendations (omissions are forbidden)."
zh-signals: "PHP 源码 SQL 注入审计技能，追踪用户输入到 SQL 执行点的数据流并输出可利用性分级与修复建议。信号:SQL注入,源码审计,数据流追踪,PDO,mysqli"
when-to-use: "Use when auditing PHP application source code for SQL injection, tracing user input into SQL sinks such as PDO, mysqli, or ORM queries."
---

# PHP SQL Injection Audit (php-sql-audit)

Analyze PHP project source code, identify SQL execution code (PDO/mysqli/ORM), trace user input to SQL construction points, verify whether SQL injection exists, and output a complete vulnerability report.

## CRITICAL: No Omissions and No False Positives
- You must audit every path where a string source appearing in route parameters (GET/POST/Body/parameter fields) reaches SQL
- You must use "data flow tracing evidence" to determine exploitability; keyword guessing alone is not sufficient
- No omissions: no omission placeholders may appear; the complete vulnerability evidence chain and remediation recommendations must be output

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-SQL-{sequence-number}`

## Input Dependencies
It is recommended to have at least the following (consistent with `shared/IO_PATH_CONVENTION.md`; when merging into a pipeline, read the equivalent section of the consolidated report):
- `routes_{timestamp}.md` (when written separately it is usually `route_mapping/routes_{timestamp}.md`)
- `params_{timestamp}.md` (when written separately it is usually `route_mapping/params_{timestamp}.md`)
Optional but recommended:
- `route_tracer/` output, used to precisely determine the actual usage state of a parameter

## SQL Sink Identification (mandatory)
1. PDO / PDOStatement
   - Relatively dangerous: `$pdo->query($sql)` / `$pdo->exec($sql)` (when $sql comes from concatenation or includes user input)
   - Form check: `$pdo->prepare($sql)` is safer only when placeholders are used in `$sql` and subsequent `bindParam/bindValue` or correct parameter passing is applied
   - ORM/DB wrappers: `DB::select(DB::raw({value}))`, Doctrine `createQuery`, etc.
2. mysqli / mysqli_stmt
   - `mysqli_query($conn, $sql)` is dangerous when concatenated
   - `mysqli_prepare` can only be safe when prepare + bind are used correctly
3. Typical dangerous construction patterns (mandatory)
   - SQL string concatenated with variables: `.`, `sprintf`, `vsprintf`, `implode/join` + SQL keywords
   - Dynamic sorting: `order by $x` / `ORDER BY ".$x."` (commonly high severity)

## Conditions That Require Triggering the Tracer (mandatory)
You must call `php-route-tracer` (or equivalent tracing evidence) when any of the following holds:
- A parameter passes through multiple layers of calls, or a field extracted after JSON decoding reaches SQL
- The SQL construction point sits in a base class / utility class / parent function
- Branch conditions (if/try/catch) make it uncertain whether the SQL executes

## Report Output
Output to:
```
{output_path}/vuln_audit/
└── sql_{timestamp}.md
```

## Vulnerability Report Entry Template (mandatory)
```markdown
### [{severity-prefix}-SQL-{sequence-number}] {risk title}

| Item | Information |
|------|------|
| Severity Level | {🔴/🟠/🟡/🔵} (CVSS {score}) |
| Reachability (R) | {0-3} - {rationale} |
| Impact Scope (I) | {0-3} - {rationale} |
| Exploitation Complexity (C) | {0-3} - {rationale} |
| Exploitability | ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent |
| Location | {file}:{line} ({Function/Class}) |

#### Data Flow Chain (Source → Sink)
(Write it line by line per route: request parameter read -> variable assignment/concatenation/transformation -> branch -> SQL enters the execution point. Omissions are forbidden)

#### Exploitability Preconditions
- Authentication Requirement: {none / login required / specific privilege required}
- Input Controllability: {fully controllable / conditionally controllable / not controllable}
- Trigger Condition: {branch / exception / environment-dependent}

#### Evidence Citation (Mandatory: from php-route-tracer)
Every suspected SQL vulnerability must cite the evidence points corresponding to the **SQL rows** of `## 9) Sink Evidence Type Checklist` in the trace output (a pending-verification status is allowed, but the evidence citation must exist):
1. `EVID_SQL_EXEC_POINT`: location of the SQL execution function/statement (matching the trace's SQL execution point evidence)
2. `EVID_SQL_STRING_CONSTRUCTION`: location of the SQL string construction/concatenation (matching the trace's SQL concatenation evidence)
3. `EVID_SQL_USER_PARAM_TO_SQL_FRAGMENT`: mapping from user-controllable parameter to SQL fragment (matching the trace's controllability matrix field evidence)

#### Handling Missing tracer Evidence (mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.

#### Verification PoC (mandatory, executable request)
```http
{HTTP Method} {full path with query/Body} HTTP/1.1
Host: {host}
{required Header/Session/JWT/Cookie}

{Payload}
```

#### Recommended Fix
- Give the key points of the secure implementation (PDO prepare + bind, and ensure no SQL fragment concatenates user input)
- Give code search commands (`rg`/`grep` style) to locate all similar concatenation points
```

## Output Completeness Check (Mandatory)
- [ ] Output at least: risk statistics + a complete entry for every vulnerability
- [ ] No omission placeholders anywhere
- [ ] Every vulnerability includes: data flow chain, exploitability preconditions, executable PoC, remediation recommendations


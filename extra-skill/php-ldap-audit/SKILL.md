---
name: php-ldap-audit
description: "PHP web source code LDAP injection audit tool. Identifies user-controllable data flowing into LDAP filter/DN construction and executed by ldap_search/ldap_read, and outputs exploitability grading, PoC, and remediation recommendations (never omit)."
zh-signals: "审计 PHP 源码中的 LDAP 注入风险，追踪用户可控数据进入 filter/DN 构造并被执行的过程。信号:PHP审计,LDAP注入,filter构造,注入检测,安全审计"
when-to-use: >-
  Use when auditing PHP source code for LDAP injection — user-controlled data reaching
  filter/DN construction and ldap_search/read execution — and you need exploitability
  grading and fixes.
---

# PHP LDAP Injection Audit (php-ldap-audit)

Analyze PHP project source code, identify LDAP query related code (filter/DN construction), and detect LDAP injection risks: an attacker can change LDAP query semantics by controlling filter or DN fragments, leading to unauthorized queries, data disclosure, or authentication bypass.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-LDAP-{sequence number}`

## LDAP Sink (Required)
Identify the following functions/statements as the final execution points:
- `ldap_search({value})` / `ldap_read({value})` / `ldap_list({value})`
- And their project-level wrappers (as long as a filter/DN string is ultimately passed in)

## Mandatory Evidence Points (Required, aligned with the trace contract)
Every suspected LDAP vulnerability must cite the evidence point IDs corresponding to the **LDAP rows** in `## 9) Sink Evidence Type Checklist` of the `php-route-tracer` trace, item by item:
1. `EVID_LDAP_EXEC_POINT`: evidence of the LDAP query execution point (the final argument passing location of the ldap_* function call/wrapper)
2. `EVID_LDAP_FILTER_STRING_CONSTRUCTION`: evidence of the LDAP filter/DN string construction location (concatenation/templating)
3. `EVID_LDAP_USER_PARAM_TO_FILTER_FRAGMENT`: evidence of the mapping from a user-controllable parameter to a filter/DN fragment

## Controllability and Injection Point Confirmation (Required)
Must output and judge:
- Where the user input comes from: `$_GET/$_POST/json/php://input/$_COOKIE/$_FILES` or derived fields
- How the filter/DN is built: direct string concatenation, escaped, or backed by an allowlist
- The semantic points the injection can alter: for example whether `*`, `(`, `)` and other LDAP filter syntax characters can be injected (or whether escaping can be bypassed via encoding)
- Whether escaping/sanitization exists: prefer `ldap_escape` (or a custom equivalent), and it must be proven to be applied to the final filter/DN construction

## tracer Trigger Conditions (Required)
Trigger `php-route-tracer` (or equivalent-depth tracing) when any of the following holds:
- The filter/DN is concatenated from multiple variables/function layers or built after JSON decoding
- There are branches (if/switch/try) or early return/throw before the filter/DN reaches `ldap_search/read/list`
- The escaping logic has conditional branches (some branches do not escape, or only part of the fields is escaped)

## Report Output
Output to:
```
{output_path}/vuln_audit/ldap_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
Every LDAP vulnerability must include the following structure:
```markdown
### [{severity prefix}-LDAP-{sequence number}] LDAP injection vulnerability (filter/DN concatenation changes query semantics)

| Item | Information |
|------|------|
| Severity Level | {🔴/🟠/🟡/🔵} (CVSS {score}) |
| Reachability (R) | {0-3} - {rationale} |
| Impact Scope (I) | {0-3} - {rationale} |
| Exploitation Complexity (C) | {0-3} - {rationale} |
| Exploitability | ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent |
| Location | {file}:{line} ({Function}) |

#### Data Flow Chain (Source → Sink)
(write line by line per route: input read -> variable concatenation/transformation/escaping -> final filter/DN generation -> ldap_* execution, never omit)

#### Exploitability Preconditions
- Authentication Requirement: {none / login required / specific privilege required}
- Input Controllability: {fully controllable / conditionally controllable / not controllable}
- Trigger Condition: {branch / exception / environment-dependent}
- Escaping/allowlist reliability: {reliably protected / protection missing / protection bypassable}

#### Evidence Citation (Mandatory: from php-route-tracer)
- `EVID_LDAP_EXEC_POINT`: {summary of the corresponding evidence point}
- `EVID_LDAP_FILTER_STRING_CONSTRUCTION`: {summary of the corresponding evidence point}
- `EVID_LDAP_USER_PARAM_TO_FILTER_FRAGMENT`: {summary of the corresponding evidence point}

#### Validation PoC (Mandatory: provide an executable request)
```http
{HTTP Method} {real route with full parameters} HTTP/1.1
Host: {host}
{required Cookie/Auth}

{Payload}
```

PoC generation strategy (must be stated clearly):
- First use a "probe payload" to prove the filter/DN is evaluated (return count/status code/response difference)
- Then use an "injection payload" to prove the query semantics can be changed (e.g. widening the match scope/bypassing a condition)

#### Recommended Fix
- Use `ldap_escape($value, '', LDAP_ESCAPE_FILTER)` (or an equivalent function) to strictly escape user input in the filter
- Apply an allowlist to controllable fields (only allow a legal character set, fixed attribute names, length limits)
- Prohibit direct string concatenation for filter/DN; use parameterized/templated safe assembly (even though PHP has no native LDAP parameterization, assemble strictly at the code level)
- Provide code search commands (`rg`) to locate all filter/DN concatenation points
```

## Handling Missing tracer Evidence (Mandatory)
- If any key evidence point in the LDAP rows of the trace contract (`EVID_LDAP_EXEC_POINT / EVID_LDAP_FILTER_STRING_CONSTRUCTION / EVID_LDAP_USER_PARAM_TO_FILTER_FRAGMENT`) is missing or cannot be mapped to this vulnerability: the status may only be marked `⚠️Unverified`, and you must not directly claim `✅Confirmed Exploitable`.

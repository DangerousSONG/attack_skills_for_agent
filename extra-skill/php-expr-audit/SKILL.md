---
name: php-expr-audit
description: "PHP web source code expression injection (non-template) audit tool. Identifies user-controllable expression strings reaching expression engine evaluation/compilation and ultimately causing sensitive semantic execution, and outputs exploitability ratings, PoCs, and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中用户可控表达式进入求值/编译引擎的表达式注入风险，输出分级与 PoC。信号:PHP 表达式注入,源码审计,表达式求值,RCE,PoC"
when-to-use: "Use when performing white-box PHP source audit and you need to identify user-controlled expression strings reaching evaluation or compilation sinks."
---

# PHP Expression Injection (Non-Template) Audit (php-expr-audit)

Analyze PHP project source code to identify "expression evaluation/compilation" entry points: user-controllable expression strings passed into an expression engine (or PHP language-level code execution functions), thereby altering conditional logic, routing decisions, permission expressions, or executing sensitive semantics (Expression Injection / code injection class).

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-EXPR-{sequence number}`

## EXPR Sinks (Mandatory)
Identify the expression engine evaluation/compilation entry points (priority), as well as PHP language-level "string is code" execution functions:
- `ExpressionLanguage->evaluate({value})`
- `ExpressionLanguage->compile({value})` and its subsequent execution/evaluation usage points
- `eval($code)` (when `$code` can be controlled by the user)
- `assert($assertion)` (when `$assertion` is a string that can be controlled by the user)
- deprecated `/e` modifier in `preg_replace({value}, $replacement, {value})` (when the replacement is controllable)
- Equivalent "expression parsing/evaluation" engines (project-wrapped evaluate/parse/compile methods, as long as the expression string is ultimately used as input)

## Mandatory Evidence Points (Mandatory, aligned with the trace contract)
Every suspected EXPR vulnerability must cite the evidence point IDs corresponding to the **EXPR row** of `## 9) Sink Evidence Type Checklist` in the `php-route-tracer` trace:
1. `EVID_EXPR_EVAL_ENTRY`: location evidence of the expression parsing/compilation/evaluation entry point
2. `EVID_EXPR_EXPR_CONTROL`: mapping evidence of whether the expression string comes from user-controllable input
3. `EVID_EXPR_EXEC_CHAIN_ENTRY`: evidence of subsequent use of the evaluation result (how the evaluation result enters sensitive semantics / security-critical branches, or the final execution point)

## Controllability and Injection Semantics Confirmation (Mandatory)
You must output and judge:
- Where the expression string comes from: request field / JSON field / parameter concatenation used as expression input
- Whether an allowlist/sandbox exists: are functions, variables, constants, and types restricted; is expression syntax rejected or replaced
- Whether "the evaluation result enters security-critical logic" exists: e.g. entering if/filter conditions, permission decisions, expression execution outside templates, etc.
- Whether branch bypass exists: some branches do not restrict expressions, or only partially sanitize inputs

## tracer Trigger Conditions (Required)
Trigger `php-route-tracer` (or equivalent-depth tracing) when any of the following is met:
- The expression string passes through multiple function layers / JSON decoding / concatenation before reaching evaluate/compile
- The expression engine evaluation result participates in security-critical conditions or sensitive operations (must be traceable in the trace)
- The expression restriction logic has conditional branches (some branches have no restriction, or the restriction can be bypassed)

## Report Output
Output to:
```
{output_path}/vuln_audit/expr_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
Every EXPR injection vulnerability must contain the following structure:
```markdown
### [{severity prefix}-EXPR-{sequence number}] Expression Injection Vulnerability (Non-Template)

| Item | Information |
|------|------|
| Severity Level | {🔴/🟠/🟡/🔵} (CVSS {score}) |
| Reachability (R) | {0-3} - {rationale} |
| Impact Scope (I) | {0-3} - {rationale} |
| Exploitation Complexity (C) | {0-3} - {rationale} |
| Exploitability | ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent |
| Location | {file}:{line} ({Function}) |

#### Data Flow Chain (Source → Sink)
(Write it line by line per route: input read -> expression string construction -> evaluate/compile entry -> evaluation result entering sensitive semantics, must not be omitted)

#### Exploitability Preconditions
- Authentication Requirement: {none / login required / specific privilege required}
- Input Controllability: {fully controllable / conditionally controllable / not controllable}
- Trigger Condition: {branch / exception / environment-dependent}
- Sandbox/allowlist reliability: {reliably protected / protection missing / protection bypassable}

#### Evidence Citation (Mandatory: from php-route-tracer)
- `EVID_EXPR_EVAL_ENTRY`: {brief summary of the corresponding evidence point}
- `EVID_EXPR_EXPR_CONTROL`: {brief summary of the corresponding evidence point}
- `EVID_EXPR_EXEC_CHAIN_ENTRY`: {brief summary of the corresponding evidence point}

#### Verification PoC (Mandatory: provide an executable request)
```http
{HTTP Method} {real route with full parameters} HTTP/1.1
Host: {host}
{required Cookie/Auth}

{Payload}
```

PoC generation strategy (must be spelled out):
- Step 1: use a "probe payload" to prove the expression is really evaluated (e.g. arithmetic results, conditional branch result changes, return value differences)
- Step 2: once the probe is confirmed, construct an "injection payload" proving that security-critical semantics can be altered (e.g. bypassing filters / changing permission decision results); if it must depend on a specific engine function allowlist, mark it as `🔍environment-dependent/⚠️to be verified`, but still give an actionable attempt

#### Recommended Fix
- Never pass user input directly as an expression string into evaluate/compile
- Use a strict allowlist: only fixed expression templates + parameter placeholders (and validate parameter types/ranges)
- Enable a sandbox policy for the expression engine: restrict functions/variables/access scope; disable dangerous operations (if the engine supports it)
- Apply a rejection policy for expression syntax (e.g. reject injected control characters) and state where the rejection happens
- Provide code search commands (`rg`) to locate all evaluate/compile entry points and expression string construction points
```

## Handling Missing tracer Evidence (Mandatory)
- If any key evidence point in the EXPR row of the trace contract (`EVID_EXPR_EVAL_ENTRY / EVID_EXPR_EXPR_CONTROL / EVID_EXPR_EXEC_CHAIN_ENTRY`) is missing or cannot be matched to this vulnerability: the status may only be marked `⚠️to be verified`, and you must not state `✅confirmed exploitable`.

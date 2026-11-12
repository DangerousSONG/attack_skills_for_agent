---
name: php-cmd-audit
description: "PHP web source code command injection auditing tool. Identifies command execution sinks (exec/system/shell_exec etc.), traces user input into command string construction, and outputs exploitability ratings, PoCs, and remediation recommendations (no omissions allowed)."
zh-signals: "PHP 源码命令注入审计，识别命令执行 Sink 并追踪用户输入到拼接点，输出分级与 PoC。信号:PHP审计,命令注入,Sink,数据流追踪,代码审计"
when-to-use: "Use when performing a white-box security audit of a PHP codebase for OS command injection sink-to-source data flows."
---

# PHP Command Injection Audit (php-cmd-audit)

Analyze PHP project source code, identify code related to system command execution, and trace user input to command construction points to verify whether a command injection risk exists.

## CRITICAL
- Exploitability must be judged using data flow chain evidence
- No omissions allowed: no omission placeholders may appear; every entry must contain the complete evidence chain and an observable verification framework
- Every high/medium severity entry must contain: location evidence + Source→Sink data flow chain + exploitation preconditions + executable PoC + remediation recommendation

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-CMD-{sequence}`

## Command Execution Sinks (Mandatory)
Identify the following functions/syntax:
- `exec/system/shell_exec/passthru`
- `proc_open/popen/pcntl_exec`
- Backtick syntax: `` `cmd` ``
Dangerous patterns:
- The command string includes user input through concatenation (GET/POST/Body/parameter fields)
- No allowlist and no shell escaping, especially when it contains `;|&`, `$()`, backticks, newlines, etc.

## Tracing and Verification (Mandatory)
Conditions that trigger `php-route-tracer`:
- The command string is composed of multiple variables
- A parameter goes through JSON decoding / multi-layer passing
- Command construction is affected by if/try branches

## Report Output
Output to:
```
{output_path}/vuln_audit/cmd_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
```markdown
### [{severity-prefix}-CMD-{sequence}] {risk title}

| Item | Information |
|------|------|
| Severity Level | {🔴/🟠/🟡/🔵} (CVSS {score}) |
| Reachability (R) | {0-3} - {rationale} |
| Impact Scope (I) | {0-3} - {rationale} |
| Exploitation Complexity (C) | {0-3} - {rationale} |
| Exploitability | ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent |
| Location | {file}:{line} ({Function/Class}) |

#### Data Flow Chain (Source → Sink)
(Write out line by line: request parameter read -> concatenation/assembly -> command execution function/statement)

#### Exploitability Preconditions
- Authentication Requirement: {none / login required / specific privilege required}
- Input Controllability: {fully controllable / conditionally controllable / not controllable}
- Trigger Condition: {branch / exception / environment-dependent}

#### Evidence Citation (Mandatory: from php-route-tracer)
Every suspected command injection vulnerability must cite, item by item, the corresponding evidence points of the **CMD row** in `## 9) Sink Evidence Type Checklist` of the trace output (the status may be pending verification, but the evidence citation must exist):
1. `EVID_CMD_EXEC_POINT`: command execution function/statement location (corresponds to the CMD execution point evidence in the trace)
2. `EVID_CMD_COMMAND_STRING_CONSTRUCTION`: command string / key parameter construction location (concatenation/templating evidence)
3. `EVID_CMD_USER_PARAM_TO_CMD_FRAGMENT`: mapping evidence from a user-controllable parameter to a key command fragment

#### Handling Missing tracer Evidence (Mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.

#### Verification PoC (Mandatory)
```http
POST {full-path} HTTP/1.1
Host: {host}
{required Cookie/Auth}

{Payload}
```

#### Recommended Fix
- Enforce a command argument allowlist plus a safe argument concatenation strategy (avoid shell=true)
- Recommend alternative implementations (e.g., spawning a process without a shell, or avoiding concatenation entirely)
- Provide code search commands (`rg`) to locate similar concatenation points
```

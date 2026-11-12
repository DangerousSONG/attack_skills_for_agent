---
name: php-injection-audit
description: |
  PHP source code injection vulnerability audit. Triggered during PHP white-box audits when injection vulnerabilities need to be detected.
  Covers 6 types of injection: SQL injection (PDO/MySQLi/ORM), NoSQL injection (MongoDB),
  command injection (system/exec/passthru), LDAP injection, expression injection (eval/preg_replace /e), and SSRF.
  Requires the data-flow evidence (EVID_*) provided by php-audit-pipeline as audit input.
zh-signals: "PHP 源码注入类漏洞审计，覆盖 SQL、NoSQL、命令、LDAP、表达式注入与 SSRF 的 Source→Sink 验证。信号:PHP注入审计,SQL注入,命令注入,SSRF,源码审计"
when-to-use: "Use when performing white-box PHP source audits to detect injection vulnerabilities and validate whether Source-to-Sink filtering is sufficient."
metadata:
  tags: php injection, sql injection, command injection, nosql, ldap injection, ssrf, eval, preg_replace, injection audit, code injection, php source audit
  category: code-audit
---

# PHP Injection Vulnerability Source Code Audit
This skill focuses on the source code level: determining whether "injection actually holds". Its core is verifying whether filtering along the Source→Sink path is sufficient. Runtime exploitation techniques such as crafting payloads or bypassing WAFs belong to the corresponding black-box exploit skills.

## Further Reading

- Dangerous patterns of the 6 injection types / secure vs. insecure code comparison / EVID evidence examples → [references/injection-patterns.md](references/injection-patterns.md)

---

## Quick Reference Table of the 6 Injection Types

| Type | Typical Sink | Dangerous Pattern | Severity |
|------|-----------|----------|--------|
| SQL injection | `PDO::query`, `mysqli_query`, `DB::raw`, `whereRaw` | String concatenation into SQL | Critical-High |
| Command injection | `exec`, `system`, `shell_exec`, `passthru`, `proc_open`, backticks | User input concatenated into the command string | Critical |
| SSRF | `curl_exec`, `file_get_contents`, `SoapClient` | Server-side request with a user-controllable URL | High-Medium |
| Expression injection | `eval`, `assert`, `preg_replace(/e)`, `create_function` | User input enters a code execution context | Critical |
| NoSQL injection | MongoDB `find()`, `$where`, operators `$ne/$gt/$regex` | Array/object parameters bypass equality comparison | High |
| LDAP injection | `ldap_search`, `ldap_list`, `ldap_bind` | User input concatenated into the filter string | High-Medium |

## General Audit Workflow (4 Steps)

**Step 1 -- Confirm the EVID evidence points**: from the EVID_* evidence produced by Phase 3 of `php-audit-pipeline`, select the entries belonging to injection classes (EVID_SQL_*, EVID_CMD_*, EVID_SSRF_*, EVID_EXPR_*, EVID_LDAP_*). Sinks without EVID evidence can only be marked "to be verified".

**Step 2 -- Judge filtering effectiveness**: trace every filtering/escaping operation along the Source→Sink path and evaluate whether it is effective for the current injection type. Common traps: `addslashes` is ineffective against GBK wide bytes, `intval` is ineffective against array parameters, and `escapeshellarg` can be bypassed in specific locales.

**Step 3 -- Assess bypass feasibility**: when filtering exists but is insufficient, analyze the concrete bypass path (encoding differences, type confusion, secondary processing, etc.). If a bypass idea can be given, mark it "confirmed"; otherwise mark it "to be verified" and record the known filtering method.

**Step 4 -- Determine severity**: use the three-dimension scoring formula of `php-audit-pipeline`, `Score = R*0.40 + I*0.35 + C*0.25`. Impact is usually high for injection vulnerabilities (command/expression injection I=3, SQL injection I=2-3), but reachability and exploitation complexity must be considered together.

## SQL Injection Audit Points

- **PDO prepared statements**: confirm that placeholder binding with `prepare()` + `execute()` is complete. `PDO::query($sql)` and `PDO::exec($sql)` execute directly, so any concatenation is dangerous
- **ORM traps**: variable concatenation in `whereRaw`/`havingRaw`/`orderByRaw`/`selectRaw` is not protected by ORM parameterization
- **Dynamic ORDER BY / LIMIT**: these two clauses cannot use parameterized binding, so `intval()` or a whitelist is the only safe option
- **sprintf %s concatenation**: `sprintf("SELECT * FROM t WHERE id='%s'", $input)` is essentially concatenation
- **Second-order injection**: data is escaped when stored but not escaped when read back and concatenated into a new query; tracing must cross the storage boundary

## Command Injection Audit Points

- **Effectiveness of escapeshellarg**: usually effective on its own, but when combined with `escapeshellcmd` it can actually introduce a bypass (the quote pairing is broken)
- **Multi-argument concatenation**: `exec("convert " . escapeshellarg($src) . " " . $dest)` — if `$dest` is not escaped, injection is still possible
- **Backticks**: an easily overlooked command execution method; search globally for variable references inside backticks
- **proc_open array mode**: `proc_open([$cmd, $arg1, $arg2], ...)` avoids shell parsing and is a safe way to execute commands

## SSRF Audit Points

- **Protocol restrictions**: check whether protocols other than `http/https` are restricted (`gopher://` can reach internal services, `file://` can read local files)
- **IP blacklist bypasses**: decimal `2130706433`, octal `0177.0.0.1`, IPv6 `[::1]`, and DNS rebinding all bypass simple IP checks
- **Redirect following**: curl does not follow redirects by default, but with `CURLOPT_FOLLOWLOCATION=true` a 302 redirect can be used to bypass the URL whitelist
- **DNS resolution timing**: the pattern of resolving and checking first and then issuing the request has a TOCTOU race (the DNS rebinding exploitation point)

## Expression Injection Audit Points

- **eval/assert**: any user-controllable data entering `eval()` is Critical. `assert()` can execute strings in PHP < 8.0
- **preg_replace /e**: removed in PHP 7.0, but may still exist in legacy systems. The alternative `preg_replace_callback` is safe
- **create_function**: essentially `eval`; removed in PHP 8.0 but common in older projects
- **Controllable callbacks**: if the callback argument of `array_map`/`usort`/`call_user_func` is user-controllable, it is equivalent to code execution

## NoSQL / LDAP Audit Points (brief)

- **MongoDB operator injection**: the PHP array parameter `$_GET['user'][$ne]=1` can bypass equality matching; check whether the input is type-cast
- **$where injection**: MongoDB's `$where` accepts JavaScript expressions, so user control over it is equivalent to code execution
- **LDAP filter concatenation**: injecting `*)(uid=*))(|(uid=*` into `(&(uid=$input)(pass=$pass))` can modify the query logic
- **Missing ldap_escape**: PHP 5.6+ provides `ldap_escape()`, but many projects do not use it; check whether `(`, `)`, `*`, `\`, and `NUL` are escaped

## Detection Checklist

- [ ] All injection EVID_* evidence points have been reviewed one by one
- [ ] All SQL concatenation points have been verified for the use of parameterization/prepared statements
- [ ] Variable concatenation in ORM Raw methods has been marked in full
- [ ] Every argument segment of the command execution functions has been checked for escaping
- [ ] The URL source and protocol restrictions of SSRF sinks have been confirmed
- [ ] The argument controllability of eval/assert/preg_replace /e has been traced
- [ ] Type coercion of NoSQL query parameters has been checked
- [ ] The escaping handling of LDAP filters has been confirmed
- [ ] Points with insufficient filtering have a concrete bypass idea or are marked "Unverified"
- [ ] Severity scoring used the unified formula, consistent with the pipeline

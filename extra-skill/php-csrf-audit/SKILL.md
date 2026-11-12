---
name: php-csrf-audit
description: "PHP Web source code CSRF audit tool. Identifies whether state-changing endpoints are protected by CSRF, traces token generation, verification and bypass conditions, and outputs exploitability grading, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的 CSRF 防护，追踪 token 生成校验与绕过条件并输出分级与修复建议。信号:PHP CSRF,状态变更,token校验,绕过,源码审计"
when-to-use: "Use when auditing PHP source code for missing CSRF protection on state-changing endpoints and you need token flow analysis, exploitability grading, and PoC."
---

# PHP CSRF Audit (php-csrf-audit)

Analyze PHP project source code to determine whether every endpoint that may cause state changes (POST/PUT/PATCH/DELETE, or side-effecting GET) implements CSRF protection (token verification, SameSite/CORS coordination, double-submit cookie, etc.).

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-CSRF-{sequence}`

## Protection Points and Mandatory Checks
Must identify and output:
1. State-changing entry points: the route's HTTP method and whether it has side effects (database writes / permission updates / transaction initiation / task triggers, etc.)
2. CSRF token generation: token source (session/cookie/random), field name, and how it is injected into the form or request header
3. CSRF token verification: the location and conditions of the backend validation logic (whether it only validates logged-in users, whether bypass branches exist)
4. Verification bypass: whether cases such as "some branches do not verify", "only a specific Content-Type is verified" or "verification happens only for AJAX" exist
5. Same-origin / cross-site aids: `SameSite`, CORS / cross-origin settings, and Referer/Origin validation (note: relying on Referer/Origin alone may also be unreliable)

## Data Flow Tracing Requirements
Must trace at least one chain:
- From the token source (e.g. `$_SESSION['csrf']`) to the front-end output
- Then to the backend token reception (`$_POST/headers`) and verification (comparison / hash check)

## Report Output
Output to:
```
{output_path}/vuln_audit/csrf_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
Must include the following sections:
- Location evidence (route + location of the verification function/middleware)
- Data flow chain (token generation -> front-end carry -> backend verification)
- Exploitability preconditions (whether login is required; whether the attacker can craft the page; browser same-site policy)
- Verification PoC (must contain the real route and request structure; if a login session is required, state the cookie/login-state details)
- Recommended fixes (where to place token verification, failure response policy, unified field name, coverage for bypass branches)

## Evidence Citation (Mandatory: from php-route-tracer)
Every CSRF risk must cite the evidence points in the trace item by item (the status may be pending verification, but the evidence citations must exist):
1. `EVID_CSRF_STATE_CHANGE_HANDLER_EXEC`: execution evidence of the state-changing handler (branch-path evidence from the trace)
2. `EVID_CSRF_TOKEN_SOURCE`: CSRF token source and generation evidence (session/cookie/random, etc.)
3. `EVID_CSRF_TOKEN_RECEIVE`: location evidence of where the CSRF token is received in the request and enters the verification logic (parameter entry-point / branch evidence from the trace)
4. `EVID_CSRF_TOKEN_VERIFY`: location evidence of the CSRF comparison / hash decision (condition and early-return evidence from the trace)
5. `EVID_CSRF_BYPASS_BRANCH`: bypass branch evidence (e.g. only certain Content-Types are verified, or verification applies only to AJAX)

## Handling Missing tracer Evidence (Mandatory)
- If the trace contract validation fails or any of the key evidence points 1~5 above is missing, the risk can only be marked as `⚠️pending verification`; no "confirmed exploitable" assertion may be made.

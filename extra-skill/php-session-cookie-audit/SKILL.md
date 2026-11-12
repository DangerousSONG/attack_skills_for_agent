---
name: php-session-cookie-audit
description: "PHP Web source code session and cookie security audit tool. Identifies session fixation, insecure cookie flags, JWT verification flaws and remember-me risks, and outputs severity grading, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的会话固定、Cookie flags、JWT 校验与持久登录风险。信号:php审计,会话固定,cookie flags,jwt,session"
when-to-use: >-
  Use when auditing PHP source code for session fixation, missing cookie flags, JWT
  verification flaws, or weak remember-me authentication.
---

# PHP Session and Cookie Security Audit (php-session-cookie-audit)

Analyze the security settings and implementation logic of authentication sessions in PHP project source code, focusing on detecting:
- session fixation
- missing cookie flags (HttpOnly/Secure/SameSite)
- JWT verification flaws (algorithm confusion, unverified exp/iss/aud, weak keys)
- remember-me / persistent login weaknesses (if present)

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-SESS-{sequence}`

## Mandatory Checks (Required)
1. Session initialization:
   - whether `session_regenerate_id` is called after login
   - whether reasonable timeouts and cookie parameters are set
2. Cookie flags:
   - whether `HttpOnly`, `Secure` and `SameSite` are explicitly set
3. JWT:
   - whether the algorithm used for decode/verify is fixed
   - whether `exp`/`nbf`/`iss`/`aud` are validated
   - whether the secret / public key is hardcoded or read insecurely
4. Logout / invalidation:
   - whether logout truly clears the session and the token

## PoC Requirements (Mandatory)
- For session fixation: provide the request sequence (fix the session id before login -> verify the session changes after login)
- For cookie flags: explain the browser-observable difference and the impact (and provide sample HTTP response headers)
- For JWT: provide a request PoC skeleton for "missing signature algorithm / claim validation" (must explain how the payload is crafted)

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected session or cookie security risk must cite the matching evidence points of the **SESS row** in the `## 9) Sink Evidence Type Checklist` section of the trace output item by item (the status may be pending verification, but the evidence citations must exist):
1. `EVID_SESS_SESSION_INIT_REGEN`: evidence of session fixation defenses such as `session_regenerate_id` after login
2. `EVID_SESS_COOKIE_FLAGS`: evidence that the cookie flags (HttpOnly/Secure/SameSite) are set
3. `EVID_SESS_JWT_VERIFY_CLAIMS`: evidence of the JWT signature algorithm being fixed and of claim validation such as exp/nbf/iss/aud
4. `EVID_SESS_LOGOUT_CLEAR`: evidence that logout truly clears the session and the token

## Handling Missing tracer Evidence (Mandatory)
- If the trace contract validation fails or any of the key evidence points 1~4 above is missing, the risk can only be marked as `⚠️pending verification`; no "confirmed exploitable" assertion may be made.

## Report Output
```
{output_path}/vuln_audit/sess_{timestamp}.md
```

## Entry Template (Mandatory)
Must include: location evidence + data flow chain (token/session -> verification -> authorization) + exploitability preconditions + PoC + remediation recommendations + `rg` search statements.

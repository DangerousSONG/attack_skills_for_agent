---
name: php-open-redirect-audit
description: "PHP Web source code open redirect audit tool. Identifies user-controlled redirect destinations that reach the Location header or redirect helpers, analyzes the validation and allowlist, and outputs severity grading, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的开放重定向，识别用户可控跳转目的地并评估校验与 allowlist。信号:开放重定向,PHP审计,Location,跳转劫持,钓鱼"
when-to-use: "Use when auditing PHP source code for open redirects, where user-controlled destinations reach Location headers or redirect helpers and you need grading, PoCs, and fixes."
---

# PHP Open Redirect Audit (php-open-redirect-audit)

Analyze PHP project source code to determine whether any "jump / redirect" behavior may be controlled by the user through the destination address, hijacking phishing or OAuth flows.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-REDIR-{sequence}`

## Mandatory Sinks to Check (Required)
Identify the following redirect output points:
- `header("Location: {value}")`
- `<meta http-equiv="refresh" content="{value}">`
- `redirect()` / `to()` / `return redirect({value})`
- Custom redirect functions (which ultimately emit the Location output internally)

## Controllability Tracing (Required)
Must trace the following two categories of variables:
1. Destination source: usually comes from `$_GET['next']` / `$_POST['url']` / `Referer` / `return_to`
2. Destination validation: whether only relative paths are allowed, whether there is an allowlist, whether the scheme is rejected (`http://` / `//`), and whether the domain is validated

## Bypass Conditions (Required)
Must identify and output potential bypasses:
- Scheme bypass: `//evil.com`, `http:%2f%2fevil.com`
- Encoding bypass: double encoding, URL-encoded colons/slashes
- Trailing/whitespace character bypass (common in legacy implementations)

## Report Output
```
{output_path}/vuln_audit/redir_{timestamp}.md
```

## Entry Template (Mandatory)
Every vulnerability must include:
- Location evidence: redirect function location + route
- Data flow chain: user input -> validation -> header/redirect
- Exploitability preconditions: usually requires a login (if the redirect happens after login) and whether the attacker can control the parameter
- Verification PoC (must use the real route; replace the destination parameter with the actual field name)
- Recommended fixes: allow only relative paths + server-side allowlist + normalize the encoding/scheme before validation

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected open redirect vulnerability must cite the matching evidence points of the **REDIR row** in the `## 9) Sink Evidence Type Checklist` section of the trace output item by item (the status may be pending verification, but the evidence citations must exist):
1. `EVID_REDIR_OUTPUT_POINT`: location evidence of the redirect output point (the final output location of header/redirect)
2. `EVID_REDIR_DEST_SOURCE_MAPPING`: evidence of the destination source variable mapping (from the route parameter to the destination variable)
3. `EVID_REDIR_DEST_VALIDATION_NORMALIZATION`: branch evidence of destination validation / normalization / allowlist / scheme refusal (including the encoding bypass handling branch)

## Handling Missing tracer Evidence (Mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.

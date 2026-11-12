---
name: php-frontend-audit
description: |
  PHP source code audit for frontend interaction class vulnerabilities. Triggered during PHP white-box audits when frontend security related vulnerabilities need to be detected.
  Covers 5 frontend risk classes: XSS (reflected / stored / DOM), CSRF (missing token validation),
  open redirect (controllable header Location), CRLF injection (HTTP response splitting), session and cookie security (fixation / hijacking / attributes).
  Requires data-flow evidence provided by php-audit-pipeline.
zh-signals: "PHP 源码前端交互类漏洞审计，覆盖 XSS、CSRF、开放重定向、CRLF 注入与会话安全。信号:XSS审计,CSRF,开放重定向,CRLF注入,会话安全"
when-to-use: "Use during PHP white-box audits to determine whether frontend security issues such as XSS, CSRF, open redirect, CRLF injection, or insecure sessions are exploitable, using data-flow evidence from the audit pipeline."
metadata:
  tags: xss, csrf, open redirect, crlf injection, session, cookie, cross-site scripting, cross-site request forgery, session security, http response splitting, frontend security audit
  category: code-audit
---

# PHP Frontend Interaction Vulnerability Source Code Audit
This skill focuses on source-level judgement of "whether the frontend security vulnerability holds", the core being to verify whether user-controllable data output in HTTP responses is safe. Payload crafting, WAF bypass, and other runtime exploitation techniques fall within the corresponding black-box exploit skill scope.

## Further Reading

- Dangerous patterns / secure pattern code comparisons / EVID evidence examples for the 5 frontend vulnerability classes → [references/frontend-patterns.md](references/frontend-patterns.md)

---

## Quick Reference Table for the 5 Frontend Vulnerability Classes

| Type | Typical Sink | Trigger Condition | Severity |
|------|-----------|----------|--------|
| XSS (reflected/stored/DOM) | `echo`, `print`, template output `{!! !!}` | User input output into an HTML context without escaping | High-Critical |
| CSRF | State-changing form/API | Missing token validation and no SameSite protection | Medium-High |
| Open Redirect | `header("Location:")`, framework `redirect()` | Redirect target URL fully user-controllable | Medium |
| CRLF Injection | `header()`, `setcookie()` | User input containing `\r\n` entering HTTP response headers | Medium-High |
| Session Security | `session_start()`, `setcookie()` | Session fixation / missing cookie attributes | Medium-High |

## XSS Audit Points

- **Output context determines escaping requirements**: HTML body, attributes, JavaScript strings, and URLs each need a different escaping strategy; a single `htmlspecialchars` cannot cover all scenarios
- **htmlspecialchars check**: confirm the `ENT_QUOTES` flag is used (the default `ENT_COMPAT` does not escape single quotes) and that the encoding parameter is correct (`'UTF-8'`)
- **Template engine autoescaping**: Blade `{{ }}` autoescapes but `{!! !!}` does not; Twig `{{ }}` autoescapes but the `|raw` filter skips escaping; Smarty depends on the `$escape_html` configuration
- **Stored vs reflected**: stored XSS requires tracing across the storage boundary — whether the data is filtered on write is not important, the key is whether it is escaped on output
- **DOM XSS**: the PHP backend outputs JSON into a `<script>` tag or an HTML data attribute, and frontend JS reads it and writes it into the DOM (`innerHTML`/`document.write`)

## CSRF Audit Points

- **Identify state-changing operations**: all POST/PUT/DELETE requests that modify data should have token validation
- **Framework middleware exceptions**: Laravel `VerifyCsrfToken`'s `$except` array, ThinkPHP's `token_on` configuration — excluded routes are high-risk targets
- **SameSite attribute**: `SameSite=Lax` defends against most CSRF (but not GET-based), `None` offers no protection, and the default value varies by browser
- **Custom token implementation**: check whether the token is bound to the session, whether it is single-use, and whether it has an expiry limit

## Open Redirect Audit Points

- **Controllable header Location**: `header("Location: " . $_GET['url'])` is the classic pattern, as are framework calls like `redirect($url)`
- **parse_url bypass**: `//evil.com` (protocol-relative URL), `///evil.com`, `\evil.com` (IE compatible), and the `javascript:` pseudo-protocol all bypass simple validation
- **Safe allowlist**: the correct implementation parses the host and then compares it against an allowed domain list, rather than relying on regex matching or prefix checks (`example.com.evil.com` bypasses prefix checks)

## CRLF Audit Points

- **header() + user input**: in `header("X-Custom: " . $input)`, a `$input` containing `\r\n` can inject extra response headers
- **PHP version differences**: `header()` in PHP 7.0+ already detects `\r\n` and raises a warning (but `setcookie()` only got complete protection up to PHP 8.x)
- **Exploitation**: inject a `Set-Cookie` header to achieve session fixation, or inject a blank line and then write the body to achieve XSS

## Session Security Audit Points

- **session_regenerate_id timing**: this function should be called after a successful login to prevent session fixation. The `true` argument deletes the old session file
- **Cookie attributes**: `session.cookie_httponly=1` (prevents JS from reading), `session.cookie_secure=1` (HTTPS only), `session.cookie_samesite=Lax`
- **Custom session handler**: when implementing `SessionHandlerInterface`, is there an injection risk in `read()`/`write()` (e.g. SQL concatenation when storing in a DB)

## Detection Checklist

- [ ] All frontend EVID_* evidence points have been reviewed one by one
- [ ] The context type of every echo/print output point has been annotated, and the escaping matches the context
- [ ] Whether the template engine's autoescaping is disabled has been checked
- [ ] CSRF token validation on state-changing routes has been confirmed, and exempt routes have been flagged
- [ ] The source of the target parameters of header() and redirect() has been traced
- [ ] CRLF injection has been cross-checked against PHP versions and affected functions
- [ ] Session configuration (php.ini / code ini_set) has been audited
- [ ] All four cookie attributes (httponly/secure/samesite/path) have been checked item by item
- [ ] Severity scoring used the unified formula, consistent with the pipeline

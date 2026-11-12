---
name: java-frontend-audit
description: |
  Java source code front-end security vulnerability audit. Triggered during Java white-box audits when front-end security vulnerabilities need to be detected.
  Covers 5 categories of risk: XSS (JSP/Thymeleaf/FreeMarker output escaping), CSRF (Spring Security/custom token),
  open redirect (sendRedirect/forward), CRLF injection (header/cookie), and session management (fixation/timeout/concurrency).
  Requires the data-flow evidence provided by java-audit-pipeline.
zh-signals: "审计 Java 源码中的 XSS、CSRF、开放重定向、CRLF 注入与 Session 管理前端安全漏洞。信号:XSS,CSRF,开放重定向,CRLF注入,Session管理,Java审计"
when-to-use: >-
  Use during Java white-box source audit when validating whether front-end security
  vulnerabilities hold, relying on data-flow evidence produced by java-audit-pipeline.
metadata:
  tags: xss, csrf, open redirect, crlf injection, session, jsp, thymeleaf, freemarker, spring security, front-end security, java source audit
  category: code-audit
---

# Java Front-End Security Vulnerability Source Code Audit
This skill focuses on the source code level: determining whether a "front-end security vulnerability actually holds". Its core is verifying whether filtering and escaping are sufficient as user input flows into the HTTP response (HTML/header/cookie/redirect). Runtime exploitation techniques such as crafting payloads or bypassing WAFs belong to the corresponding black-box exploit skills.

## Further Reading

- Dangerous patterns of the 5 front-end vulnerability categories / secure vs. insecure code comparison / EVID evidence examples -> [references/frontend-vuln-patterns.md](references/frontend-vuln-patterns.md)

---

## Quick Reference Table of the 5 Front-End Security Vulnerability Categories

| Type | Typical Sink | Dangerous Pattern | Severity |
|------|-----------|----------|--------|
| XSS | JSP `<%= %>`, `th:utext`, `${var?no_esc}`, `out.println()` | User input output to HTML/JS context without escaping | High-Medium |
| CSRF | State-changing POST/PUT/DELETE endpoints | `csrf().disable()` or write endpoints lacking token validation | High-Medium |
| Open redirect | `sendRedirect()`, `return "redirect:" + url` | User-controllable URL passed directly into a redirect function | Medium |
| CRLF injection | `setHeader()`, `addHeader()`, `addCookie()` | User input written into the HTTP header without filtering `\r\n` | Medium-High |
| Session management | `getSession()`, `Cookie` construction, `session-timeout` | Session not regenerated after login / cookie missing security attributes | Medium-High |

## General Audit Workflow (4 Steps)

**Step 1 -- Confirm the EVID evidence points**: from the EVID_* evidence produced by Phase 3 of `java-audit-pipeline`, select the front-end security entries (EVID_XSS_*, EVID_CSRF_*, EVID_REDIR_*, EVID_CRLF_*, EVID_SESSION_*). Sinks without EVID evidence can only be marked "to be verified".

**Step 2 -- Judge filtering effectiveness**: trace every filtering/escaping operation along the Source->Sink path and evaluate whether it is effective for the current vulnerability type. Common traps: `<c:out>` is safe but `<%= %>` does not escape, `th:text` is safe but `th:utext` does not escape, and URL whitelists can be bypassed with `//evil.com`.

**Step 3 -- Assess bypass feasibility**: when filtering exists but is insufficient, analyze the concrete bypass path (context switching, encoding differences, URL parsing differences, etc.). If a bypass idea can be given, mark it "confirmed"; otherwise mark it "to be verified" and record the known filtering method.

**Step 4 -- Determine severity**: use the three-dimension scoring formula of `java-audit-pipeline`, `Score = R*0.40 + I*0.35 + C*0.25`. For XSS, stored has I=2-3 and reflected has I=1-2; CSRF depends on the impact of the protected operation.

## XSS Audit Points

- **JSP output**: both `<%= request.getParameter("x") %>` and `<% out.println(input); %>` do not escape, so outputting directly into HTML is reflected XSS; secure pattern: `<c:out value="${param.x}"/>` or `${fn:escapeXml(param.x)}`, JSTL escapes HTML entities by default
- **Thymeleaf**: `th:utext="${userInput}"` does not escape (raw HTML output) — dangerous; `th:text="${userInput}"` automatically HTML-escapes — safe
- **FreeMarker**: after globally configuring `output_format=HTMLOutputFormat` + `auto_escaping_policy=ENABLE_IF_SUPPORTED`, output is escaped by default; `${var?no_esc}` explicitly skips escaping — dangerous; without global escaping configured, every `${}` is dangerous
- **Context differences**: escaping `< > & " '` suffices for an HTML body; an HTML attribute additionally requires handling quote closure; a JavaScript context needs JS encoding rather than HTML escaping; a URL parameter needs URL encoding — using the wrong escaping function for a context is equivalent to no defense at all
- **DOM-based XSS**: the backend returns JSON that the frontend renders via `innerHTML` / `document.write()` / `eval()`; the backend audit must confirm that the JSON response uses the `Content-Type` `application/json` rather than `text/html`
- **Stored XSS**: data read from the database is output without escaping — trace whether the write point filters the data and whether the read point escapes it
- **Rich text scenarios**: use a whitelist filtering library such as OWASP Java HTML Sanitizer (`PolicyFactory`) or `Jsoup.clean(html, Safelist.basic())`

## CSRF Audit Points

- **Spring Security default**: the CSRF token is enabled by default, but REST API projects commonly use `.csrf().disable()` (older versions) or `http.csrf(csrf -> csrf.disable())` (Lambda DSL) — once disabled globally, all state-changing endpoints are exposed
- **Custom token**: evaluate the generation strength (`SecureRandom` is safe vs. `Math.random()` is predictable), whether it is bound to the session, and the validation timing (Controller layer vs. Filter layer)
- **Token delivery**: forms use `<input type="hidden" name="_csrf" value="..."/>`; AJAX uses the `X-CSRF-TOKEN` request header together with `<meta name="_csrf">` — if either delivery method is missing, that scenario is unprotected
- **Relationship between CORS and CSRF**: permissive CORS (`Access-Control-Allow-Origin: *` + `Allow-Credentials: true`) lets cross-origin JS read the CSRF token from the response, indirectly bypassing CSRF protection
- **State-changing GET requests**: a GET performing a write operation (such as `/deleteUser?id=1`) inherently has no CSRF protection — `<img src="">` is enough to trigger it

## Open Redirect Audit Points

- **Direct servlet redirect**: `response.sendRedirect(request.getParameter("url"))` / `response.sendRedirect(request.getParameter("next"))` — fully user-controllable
- **Spring MVC**: `return "redirect:" + target` or `RedirectView(url)` where target comes from a request parameter
- **Bypass techniques**: `//evil.com` (protocol-relative URL), `/\evil.com` (some parsers treat `\` as a path separator), URL encoding `%2F%2Fevil.com`, the `@` symbol `http://trusted.com@evil.com`, and unicode homoglyphs
- **Secure pattern**: whitelist domain validation + restricting to relative paths only (starting with `/` and not starting with `//`); parse with `UriComponentsBuilder` and then validate the host

## CRLF Injection Audit Points

- **HTTP header injection**: `response.setHeader("X-Custom", userInput)` or `response.addHeader("Location", "/path?lang=" + input)` — injecting `\r\nSet-Cookie: admin=1` allows setting arbitrary headers
- **Servlet container differences**: Tomcat 7.0.67+ / Jetty 9.2.15+ reject `\r\n` in header values by default; older versions or custom HTTP frameworks (such as the raw Netty API) may lack this protection — confirming the container version is key
- **Cookie value injection**: `new Cookie("lang", userInput)` — injecting `\r\nSet-Cookie: session=evil` allows hijacking the session
- **Secure pattern**: filter or reject the `\r`, `\n`, and `\0` control characters in values; upgrade to a newer Servlet container version

## Session Management Audit Points

- **Session fixation**: the session ID does not change before and after login — an attacker induces the victim to use a known session ID; secure pattern: after a successful login, rebuild it with `request.getSession().invalidate()` + `request.getSession(true)`; Spring Security `SessionFixationProtection.migrateSession` is enabled by default
- **Cookie attributes**: `HttpOnly` prevents XSS from stealing cookies (`cookie.setHttpOnly(true)`); `Secure` restricts transmission to HTTPS (`cookie.setSecure(true)`); `SameSite=Lax/Strict` prevents CSRF (Servlet 4.0+ or Spring `server.servlet.session.cookie.same-site`)
- **Timeout configuration**: `<session-timeout>30</session-timeout>` in `web.xml` (minutes); Spring Boot `server.servlet.session.timeout=30m`; an overly long timeout increases the session hijacking window
- **Concurrent login control**: Spring Security `sessionManagement().maximumSessions(1).maxSessionsPreventsLogin(true)` — when not configured, the same account can log in from multiple places, making stolen credentials hard to detect

## Detection Checklist

- [ ] All front-end security EVID_* evidence points have been reviewed one by one
- [ ] Whether JSP `<%= %>` / `out.println()` output points escape has been confirmed, and all Thymeleaf `th:utext` occurrences have been marked
- [ ] The CSRF protection status has been confirmed (whether it is disabled, the token delivery method, GET write operations)
- [ ] The URL source and whitelist validation of redirect sinks have been confirmed
- [ ] User input filtering at HTTP header/cookie write points has been checked, and the container version has been recorded
- [ ] The session lifecycle (fixation/timeout/concurrency/cookie attributes) has been reviewed
- [ ] Points with insufficient filtering have a concrete bypass idea or are marked "Unverified"
- [ ] Severity scoring used the unified formula, consistent with the pipeline

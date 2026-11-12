---
name: ctf-web-methodology
description: "Overall methodology for CTF web challenges. Use when facing a CTF lab range, the xbow benchmark, or a web security competition. Includes quick challenge type identification, an attack strategy selection decision tree, common challenge patterns, and the criteria for deciding when to switch direction. Use it together with the specific vulnerability skills under exploit/"
zh-signals: "面向 CTF Web 挑战的总体方法论，提供挑战类型识别、攻击策略决策树与方向切换判断。信号:CTF,Web挑战,靶场,漏洞利用,策略"
when-to-use: "Use when facing a CTF web challenge, xbow benchmark, or web security competition and you need to identify the challenge type, choose an attack strategy, or decide when to switch approaches."
metadata:
  tags: "ctf,web,methodology,challenge,benchmark,lab-range,competition,strategy,capture the flag"
  category: "ctf"
---

# CTF Web Challenge Methodology

## Further Reading

The following reference material is **loaded on demand**; pick the corresponding file based on the challenge type identified in Phase 2:

- Server-side injection (SQLi/SSTI/LFI/XXE/SSRF) → [references/server-side.md](references/server-side.md)
- Server-side execution (command injection/RCE/file upload/CRLF) → [references/server-side-exec.md](references/server-side-exec.md)
- Server-side advanced (race condition/HTTP smuggling/cache poisoning) → [references/server-side-advanced.md](references/server-side-advanced.md)
- Deserialization (PHP/Java/Python/Node/.NET) → [references/server-side-deser.md](references/server-side-deser.md)
- Authentication and access (password/MFA/OAuth/IDOR/logic flaws) → [references/auth-and-access.md](references/auth-and-access.md)
- JWT attacks (none/weak key/JWK injection/algorithm confusion) → [references/auth-jwt.md](references/auth-jwt.md)
- Authentication infrastructure (LDAP/Kerberos/SAML/certificates) → [references/auth-infra.md](references/auth-infra.md)
- Client-side (XSS/CSP bypass/DOM/CSS injection) → [references/client-side.md](references/client-side.md)
- Client-side advanced (Unicode folding XSS/CSS font exfiltration/CSP nonce bypass/postMessage) → [references/client-side-advanced.md](references/client-side-advanced.md)
- Node.js and prototype pollution → [references/node-and-prototype.md](references/node-and-prototype.md)
- CVE exploitation collection (Log4Shell/Gitea/Grafana, etc.) → [references/cves.md](references/cves.md)
- Web3/blockchain (Solidity/reentrancy/flash loan) → [references/web3.md](references/web3.md)
- Server-side injection 2 (deep XXE/GraphQL exploitation/variable injection) → [references/server-side-2.md](references/server-side-2.md)
- Server-side execution 2 (OPcache webshell/disable_functions bypass/LD_PRELOAD) → [references/server-side-exec-2.md](references/server-side-exec-2.md)
- Server-side advanced 2 (SSRF→Docker/Rogue MySQL/URL parsing differences/LaTeX RCE) → [references/server-side-advanced-2.md](references/server-side-advanced-2.md)
- SQLi deep dive (second-order injection/Shift-JIS encoding/PCRE backtracking WAF bypass/QR code injection) → [references/sql-injection.md](references/sql-injection.md)
- Web practical field notes (common traps/debugging tips/quick judgments) → [references/field-notes.md](references/field-notes.md)
- HTTP response analysis techniques → [references/response-analysis.md](references/response-analysis.md)
- Flag extraction methodology → [references/flag-extraction.md](references/flag-extraction.md)

---

CTF web challenges and real penetration tests are fundamentally different: the goal is clear (get the flag), the vulnerabilities are deliberately planted, and there is usually only one entry point. This methodology helps you identify the challenge type quickly and choose the shortest path.

## Core Mental Model

**CTF is essentially a puzzle**. The challenge author deliberately left an attack path for you to find.

Key principles:
1. **Breadth first, then depth** — spend 2-3 rounds on quick reconnaissance to get the whole picture, then dig into the specific vulnerability
2. **Clue-driven** — the result of every step tells you what to do next
3. **Rule of 3 rounds** — if a method shows no substantive progress after 3 rounds, switch direction
4. **Do not brute force** — if brute force is required, you are probably on the wrong track (CTF usually has an elegant solution)

## Phase 1: Quick Reconnaissance (1-3 rounds)

Execute by priority (do not do all of them; stop and analyze as soon as you find something):

1. **Visit the home page** — `http_request` GET on the home page and observe:
   - What kind of application is it? (login page/blog/shop/API)
   - What features does it have? (search/upload/register/comments)
   - Are there hints in the page footer or comments?

2. **Read the source** — inspect the HTML source (not the rendered page):
   - HTML comments `<!-- hint: ... -->`
   - Hidden form fields `<input type="hidden">`
   - API paths and variables in the JavaScript
   - Referenced JS/CSS file paths

3. **Path probing** — check common paths:
   - `/robots.txt` — often hides sensitive paths that are forbidden
   - `/flag`, `/flag.txt`, `/flag.php`
   - `/.git/`, `/.svn/` — source code leaks
   - `/backup.sql`, `/www.zip`, `/source.tar.gz`
   - `/admin`, `/login`, `/api`

4. **Fingerprinting** — `httpx -tech-detect` or `curl -sI` to identify the tech stack

## Phase 2: Challenge Type Identification and Strategy Selection

Based on the reconnaissance results, classify quickly:

| What You See | What It Might Be | Next Step |
|----------|------------|--------|
| Search box / query parameter | SQL injection | Read `sql-injection-methodology` |
| Login page | Weak password / SQL injection / JWT | Log in following the CSRF-safe flow first, then try SQLi |
| File upload feature | File upload vulnerability | Read `file-upload-methodology` |
| Template rendering / user input reflected | SSTI/XSS | Try `{{7*7}}` and `${7*7}` |
| File path parameter in the URL | LFI/path traversal | Try `../../etc/passwd` |
| Deserialization data (base64 cookie) | Deserialization RCE | Read `deserialization-methodology` |
| API endpoints + JSON | IDOR / access control bypass | Read `idor-methodology` |
| JWT token (eyJ...) | JWT attack | Read `jwt-attack-methodology` |
| Source code visible (.git leak, etc.) | Source code audit | Read `ctf-source-audit` |
| ping/curl functionality | Command injection | Read `command-injection-methodology` |
| XML input / SOAP | XXE | Read `xxe-injection-methodology` |
| URL / file path parameter | SSRF | Read `ssrf-methodology` |

## Phase 2.5: CSRF-Safe Login Flow (critical!)

Many web applications (DVWA, WordPress, etc.) have login forms with a CSRF token (hidden fields such as `user_token`, `csrf_token`, `_token`). **If you do not GET the page first to obtain the token and then POST it in the same session, the login will fail even with the correct password.**

### Correct flow (http_request manages cookies automatically)

Example:
```
1. GET /login.php              ← fetch the page, the session cookie is saved automatically
2. Extract the user_token value from the response HTML
3. POST /login.php             ← the same session cookie is carried automatically
   body: username=admin&password=password&Login=Login&user_token=<extracted value>
4. Verify: the response is no longer the login page (body size changes, Welcome/Dashboard appears)
```

### Common traps
- **A new session on every request** — if the GET and POST are not in the same session, token validation will inevitably fail (the server binds the token to the session)
- **The token name is not fixed** — it may be `user_token`, `csrf_token`, `_token`, `csrfmiddlewaretoken`
- **The token is in a meta tag** — `<meta name="csrf-token" content="...">`, not necessarily in the form
- **Configuration must be changed after logging in** (such as the DVWA security level) — keep using the same session, otherwise the change is lost

### Judging whether the login succeeded
- The response body size changes noticeably (e.g. 1523→7274 bytes)
- Keywords such as `Welcome`, `Dashboard`, `Logout` appear
- The `Login` form no longer appears

## Phase 3: Vulnerability Exploitation

- SQL injection: **UNION SELECT first**, EXTRACTVALUE as a fallback
- Command injection: **just cat /flag.txt**, do not bother with a reverse shell
- When continuous interaction is required (reverse shell/SSH/database), use the `interactive_session` tool instead of bash+nc
- LFI: **just read /flag.txt**, do not read /etc/passwd first
- **Fake flags** — `flag{test}` is not the real flag; **multi-stage vulnerabilities** — use LFI to get the source, then dig out the second bug
- **WAF bypass** — case variation/double encoding/comments `/*!select*/`; **encoding** — URL/double/Unicode

## Phase 4: Strategy Switching

- 5 variants of the same payload failed → switch direction
- SQL injection confirmed but files cannot be read → the flag is in the database
- It feels "almost there" but still fails → the most dangerous signal, step back and re-examine

## Vulnerability Type Judgment
- Observe the functionality: if it displays data rather than querying (SQL injection), it may be SSTI/XSS

## Efficiency Traps
- When there is no length limit on the full data, there is no need to extract it in segments
- Segment concatenation is error-prone, and manual concatenation carries the risk of mistakes

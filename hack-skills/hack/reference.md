# hack — 详细参考（由 SKILL.md 拆分）

### R6. Code audit: sink→source, or source forward

[CODE_AUDIT.md](./CODE_AUDIT.md). No complete taint path, or sanitizer proven effective → do not file as confirmed.

### R7. Middleware audit is document-driven

Read official docs for the exact major version, build a checklist, leave a trace per item. A middleware conclusion with no comparison table is unfinished.

### Blue quality gate (when the primary role is blue)

Success is shorter dwell time, not close-rate. Details: [BLUE_TEAM.md](./BLUE_TEAM.md).

- **B1.** Ask first whether this loses data, privilege, or the business *now*. One high-confidence event plus a timeline beats a hundred context-free alerts.
- **B2.** Alert fatigue is the main risk. Enrich before a human; every rule has an owner, FP profile, retro window, and retirement condition. Six months silent → check the log source first.
- **B3.** Containment defaults to reversible. Preserve evidence, then contain, then eradicate. Wiping logs is not containment.
- **B4.** Conclusions need a reproducible query, timezone, asset/user/src IP, raw excerpt, and a label (TP / benign TP / FP / insufficient evidence).
- **B5.** Expand the same user, host, IP, token, hash inside the window. Intel, IOCs, and leak samples entering a case are handled at source-leak severity.
- **B6.** Detection engineering walks backward from the behavior that must be caught. Strict high-confidence rules first. Quality gate in [BLUE_TEAM.md](./BLUE_TEAM.md).
- **B7.** IR follows an approved playbook. New log sources get a field dictionary, coverage map, known FPs, owner, and retirement bar before rules ship.

## 4. Core Skill Map

If the full repository is present, prefer these together. Previously separate mini skills (payload-selection, brute-selection) were merged back into their main skills.

- [Attack Surface Mapping](../attack-surface-mapping/SKILL.md) · [Recon and Methodology](../recon-and-methodology/SKILL.md)
- [XSS](../xss-cross-site-scripting/SKILL.md) · [SQLi](../sqli-sql-injection/SKILL.md) · [SSRF](../ssrf-server-side-request-forgery/SKILL.md) · [XXE](../xxe-xml-external-entity/SKILL.md) · [SSTI](../ssti-server-side-template-injection/SKILL.md)
- [IDOR](../idor-broken-object-authorization/SKILL.md) · [CMDi](../cmdi-command-injection/SKILL.md) · [Path Traversal / LFI](../path-traversal-lfi/SKILL.md) · [CSRF](../csrf-cross-site-request-forgery/SKILL.md)
- [API Security Router](../api-sec/SKILL.md) · [JWT / OAuth](../jwt-oauth-token-attacks/SKILL.md) · [OAuth / OIDC](../oauth-oidc-misconfiguration/SKILL.md) · [SAML](../saml-sso-assertion-attacks/SKILL.md) · [Auth Bypass](../authbypass-authentication-flaws/SKILL.md)
- [Business Logic](../business-logic-vulnerabilities/SKILL.md) · [Upload](../upload-insecure-files/SKILL.md) · [NoSQL](../nosql-injection/SKILL.md) · [Request Smuggling](../request-smuggling/SKILL.md)
- [Prototype Pollution](../prototype-pollution/SKILL.md) · [Type Juggling](../type-juggling/SKILL.md) · [HPP](../http-parameter-pollution/SKILL.md) · [Race](../race-condition/SKILL.md)
- [XSLT](../xslt-injection/SKILL.md) · [Insecure SCM](../insecure-source-code-management/SKILL.md) · [CSV Formula](../csv-formula-injection/SKILL.md) · [WebSocket](../websocket-security/SKILL.md) · [Dependency Confusion](../dependency-confusion/SKILL.md)
- [CORS](../cors-cross-origin-misconfiguration/SKILL.md) · [Ghost Bits Cast](../ghost-bits-cast-attack/SKILL.md) · [401/403 Bypass](../401-403-bypass-techniques/SKILL.md) · [Common Services](../unauthorized-access-common-services/SKILL.md)

## 5. High-Value Expert Intuitions

Points baseline models miss that hit often in real bounty work:

1. **The same filter is reused across pages**: one bypass usually ports.
2. **Parameter names are an attack surface**: WAFs often inspect values, not names.
3. **Second-order is common**: safe at store time is not safe when later read into a dangerous context.
4. **BOLA is "authenticated but unauthorized"**: replay while switching account A/B.
5. **Older API versions miss patches**: fixing v2 does not retire v1.
6. **Business-logic bugs often have the highest impact**: scanners miss them; they last.
7. **Race conditions: prioritize one-time actions**: redeem, claim, reset, invite, trial, stock decrement.
8. **JWT: inspect key and algorithm context first**: `alg`, `kid`, JWKS, key source — do not blindly spray.

## 6. Output Standard

Default three layers by audience:

1. Decision: what happened, impact, what to do now (one page)
2. Technical: attack chain or event timeline, repro or query, evidence
3. Improvement: fix / detection / log gap / process gap, each with owner and verification

Use templates in [EVIDENCE_REPORT.md](./EVIDENCE_REPORT.md). Medium and above: write to disk immediately. Severe: notify the authorized contact immediately.

Two gates before a finding is "confirmed":

- **Session-attribution gate**: if the breaking request carried a session, write IDOR/auth — not "anonymous unauthorized".
- **Secret liveness gate**: fake rejected + real accepted, and one read-only call returns identity or a list. Otherwise it is a clue.

## 7. Anti-patterns

- Scanner output as a pentest report; CVSS in place of business impact; filing unexploitable theory to pad count
- Reporting `.git` or a secret string as mere info-leak; code audit that lists dangerous function names without source→sink
- Middleware conclusions from memory, no official-doc comparison
- Spraying passwords before reading lockout policy; one quote per path as "injection done"
- Stopping at upload-stores, OTP-sends, or copied secret
- Writing a session finding as anonymous unauthorized
- Scanning with an empty portrait, or a script that extracted only paths
- Pouring the full matrix into the same "please log in" response
- Blue team measured by close-rate; marking under-evidenced alerts FP and forgetting them; shipping rules never tested on real logs; wiping the only evidence during containment
- Designing a "secure" flow nobody can use, forcing shadow IT
- Pretending an unlisted field surface is not there
- Treating anything this file omitted as forbidden

## Suggested Prompts

- "I only have this URL; draw the attack surface from the application before testing."
- "Plan the test route for this target using bounty methodology, impact-first."
- "This is a REST API; prioritize BOLA, BFLA, mass assignment, and JWT."
- "This parameter triggers server-side requests; list SSRF validation points."
- "Payment / coupon / inventory flow: business logic and race first."
- "I only see login and password-reset: Auth Bypass + OAuth/JWT + CSRF."
- "Audit this repo sink-to-source; no finding without a taint path."
- "`.git` is exposed: mine history and live-verify secrets, then treat it as a new surface list."

## Installation Notes

Recommended skill name: `hack`

Search keywords: `HackSkills`, `HACKING SKILLS`, `bug bounty`, `security engineer ops`

## Guidelines

- Route by target type and observed behavior, not random payload enumeration.
- Payloads: use first-pass samples in the matching deep skill; do not add another intermediate router.
- Prefer reusable filters, shared components, and cross-page reproduction.
- Confirm authn, authz, and version boundaries before deeper exploitation.
- Keep the process explainable, auditable, and reproducible.
- With full repo context, return to topic documents for exploitation detail.

---
name: src-hunter
description: "Hands-on SRC / crowdsourced testing / bug bounty vulnerability hunting workflow skill. Includes: a 5-phase methodology (intake -> recon -> enum -> hunt -> report), 19 attack-class playbooks (SQLi/XSS/RCE/SSRF/IDOR/CSRF/Path Traversal/File Upload/SSTI/XXE/Race/HTTP Smuggling/OAuth/JWT/SAML/GraphQL/Mobile/LLM/DoS), 305 structured payloads, 263 WAF/EDR bypass variants, 2887 real disclosed HackerOne High/Critical reports, statistics over 77,000 WooYun cases, Chinese OA / middleware fingerprint library, and banking / telecom vertical playbooks. Triggered when the user mentions \"SRC hunting / vulnerability hunting / bug bounty / crowdsourced testing / hackerone / bounty / SRC / any vulnerability / penetration testing\" or asks how to test a target, how to test an API, or how to bypass a WAF."
zh-signals: "SRC/众测/Bug bounty 实战漏洞挖掘工作流。信号:SRC,Bug bounty,众测,漏洞挖掘,WAF绕过"
when-to-use: "Use when the user mentions SRC, bug bounty, crowdsourced testing, or asks how to test a target URL or API or how to bypass a WAF."
argument-hint: "<target-or-program-or-phase>"
level: 2
---

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: Confirm that `scope.md` exists for the current case and that `auth.status=granted`. Without scope -> `case-init.ps1`; **never** auto-set `-AuthGranted`
2. `NOW`: Read `../../field-journal/precedent-pentest.md` — daily operating instructions; it does not replace scope
3. `NOW`: Confirm whether the current task falls within the applicability of this skill
4. `NEXT`: Read `../../tool-index.md` and verify tool availability and real paths
5. `NEXT`: Call bootstrap when a tool is missing; do not guess paths
6. `ACT`: Enter the workflow. By default only the playbook skeletons are read; `payloader/` and `waf-bypass.md` are opened only after scope has been granted and the user explicitly asks for payloads
7. `MUST NOT` treat the "2887 H1 reports" as a directory already tracked in this repo (`h1-reports/` is not in the tree)
8. `MUST NOT` disable protection because the payload corpus triggers antivirus alerts; verify the Git blob/hash against `docs/SECURITY-REVIEW-2026-09-03.md` first

# SRC Hunter — Hands-On Vulnerability Hunting Workflow

Hands-on Security Response Center / crowdsourced testing / bug bounty hunting skill. Translates white-box methodology into black-box probing, layered with real case statistics and a payload library.

---

## When to Use This Skill

**Keyword hits**:
- "SRC hunting" / "SRC vulnerability" / "SRC testing" / "Security Response Center"
- "bug bounty" / "bounty" / "crowdsourced testing"
- "hackerone" / "h1" / "bugcrowd" / "intigriti" / "yeswehack"
- "how to hunt / how to test / how to attack + a target / an endpoint / a parameter"
- "WAF bypass" / "bypass the WAF" / "WAF bypass"
- Broken access control classes such as "any account / any modification / any deletion / any operation"
- Logic flaws such as "password reset" / "account recovery"
- "unauthorized access" / "default credentials" / "Actuator" / "exposed Spring" / "unauthorized Redis"
- The user hands you a URL or API endpoint and asks you to test it

**Do not use this skill for**:
- Pure white-box source code auditing (use the `code-audit` skill)
- Fixing known vulnerabilities / defensive Q&A (use a general conversation)
- Standalone CTF challenges (this is a real-environment workflow)

---

## Workflow — 5 Phases

### Phase 1 · Intake (accepting the job)

Input: program name / SRC entry URL / subdomain.

What to do:
- Capture the scope (in-scope domains / IPs / mobile apps / API endpoints)
- Capture out-of-scope (forbidden targets, third-party services, cloud asset exclusions)
- Capture the rules (payout tiers, disclosure window, retest policy, safe-harbor)
- Capture test accounts / test headers (such as `X-Bug-Bounty: <handle>`)

**Priority judgment** (based on the hit type, estimating hit rate; see `references/methodology/05-srctimebox-priority.md`):
- 6-hour window -> run the high hit-rate classes (password reset 88% / any-account 86.4% / withdrawal 83.1%)
- Single-day window -> add information disclosure + asset exposure + Actuator
- HVV / key period -> full spectrum

-> see [`references/methodology/00-index.md`](references/methodology/00-index.md)

### Phase 2 · Recon (passive reconnaissance)

Intelligence gathering that sends no traffic to the target:

- **CT logs**: crt.sh / Censys (find subdomains)
- **Historical snapshots**: Wayback / CommonCrawl
- **GitHub search**: `org:target` + keywords (password / api_key / SECRET)
- **Search engine dorks**: `site:target.com inurl:/admin`, `filetype:env`, `intitle:Index of`
- **ASN / IP ranges**: bgp.he.net to find IP blocks
- **Favicon hash**: FOFA / Shodan to find assets sharing the same favicon
- **DNS history**: SecurityTrails / Whoisxmlapi

### Phase 3 · Enum (active probing)

**Asset enumeration**:
- Subdomains: amass / subfinder / puredns / dnsx
- Liveness: httpx / naabu
- Screenshots: gowitness / aquatone
- Content discovery: ffuf / feroxbuster / dirsearch
- Technology fingerprinting: wappalyzer / webanalyze (also check `references/dictionaries/chinese-srcfingerprints.md` to identify Chinese-made components)
- JS extraction: linkfinder / subjs / gau / katana
- Subdomain takeover fingerprints: subjack / subzy

### Phase 4 · Hunt (vulnerability probing)

Follow the matching playbook per attack class; **every playbook includes**: methodology + parameter frequency table + real H1 cases + structured payloads + WAF bypass variants.

**Priority paths** (ordered by hit rate + value):

| Playbook | Entry Hint | File |
|---|---|---|
| **Unauthorized access** | Actuator/Swagger/default ports/weak passwords | `references/playbooks/unauth-access.md` |
| **Information disclosure** | .git/.svn/.env/heapdump/path enumeration | `references/playbooks/info-disclosure.md` |
| **Arbitrary-X broken access control** | User-state IDs that can be enumerated/modified | `references/playbooks/arbitrary-x-authz.md` |
| **Business logic** | Password reset/payment/orders/verification codes | `references/playbooks/logic-flaws.md` |
| **OAuth/SAML/JWT** | Auth flow/redirect_uri/token | `references/playbooks/oauth-saml-jwt.md` |
| **API REST** | BOLA/Mass Assignment/rate limits | `references/playbooks/api-rest.md` |
| **SQLi** | Any user input reaching the DB | `references/playbooks/sqli.md` |
| **RCE** | Deserialization/SSTI/XXE/prototype chain/frameworks | `references/playbooks/rce.md` |
| **SSRF** | URL parameters/cache/Host injection | `references/playbooks/ssrf-cache-host.md` |
| **Path traversal** | File path parameters/LFI/RFI | `references/playbooks/path-traversal.md` |
| **File upload** | Upload points + parsing flaws | `references/playbooks/file-upload.md` |
| **XSS** | Any user input reaching HTML/JS | `references/playbooks/xss.md` |
| **HTTP smuggling** | Reverse proxy + Content-Length | `references/playbooks/http-smuggling.md` |
| **GraphQL** | introspection/nesting | `references/playbooks/graphql.md` |
| **Race conditions** | Concurrent requests / TOCTOU | `references/playbooks/race-conditions.md` |
| **DoS** | ReDoS / unthrottled resources / algorithm explosion | `references/playbooks/dos.md` |
| **Mobile** | Android / iOS APK | `references/playbooks/mobile.md` |
| **LLM Agent** | Prompt injection / tool invocation | `references/playbooks/llm-prompt-injection.md` |
| **Internal network post-exploitation** | Credentials / lateral movement / domain | `references/playbooks/intranet-postexp.md` |

**General methodology** (independent of attack class):

| Document | Key Content |
|---|---|
| [`methodology/01-attack-priority.md`](references/methodology/01-attack-priority.md) | Value ordering: RCE>file write>auth bypass>injection>information disclosure |
| [`methodology/02-bypass-toolkit.md`](references/methodology/02-bypass-toolkit.md) | General bypass decision tree + encoding/obfuscation/WAF |
| [`methodology/03-evidence-discipline.md`](references/methodology/03-evidence-discipline.md) | Black-box evidence rules + anti-hallucination + compliance |
| [`methodology/04-control-gap-hunting.md`](references/methodology/04-control-gap-hunting.md) | 9 classes of sensitive operations -> expected control -> probing for gaps |
| [`methodology/05-srctimebox-priority.md`](references/methodology/05-srctimebox-priority.md) | 6h / single-day / HVV / monthly time-box templates |

**Industry vertical playbooks** (check these first when assets are industry-specific):

| Industry | Document | When to Use |
|---|---|---|
| Banking / payment / finance | [`industry/banking-finance.md`](references/industry/banking-finance.md) | The target includes payment / online banking / third-party payment aggregation |
| Telecom / ISP | [`industry/telecom-isp.md`](references/industry/telecom-isp.md) | The target is an operator / BOSS / network management / IoT SIM platform |

**Dictionaries / credentials**:

| Document | Purpose |
|---|---|
| [`dictionaries/default-credentials-cn.md`](references/dictionaries/default-credentials-cn.md) | Default credentials for Chinese-made products such as Seeyon / Tongda / Wanhu / Weaver / Yonyou / Kingdee / Huawei / ZTE / Hikvision |
| [`dictionaries/chinese-srcfingerprints.md`](references/dictionaries/chinese-srcfingerprints.md) | Chinese OA / middleware fingerprints + high-frequency parameters + one-shot detection commands |

### Phase 5 · Report (submission)

-> Use the template [`templates/report-submission.md`](references/templates/report-submission.md)

**Three-part skeleton**:
1. **Title**: precise down to the endpoint + vulnerability type, no more than 80 words
2. **Reproduction steps**: each step executable / screenshotted / with HAR
3. **Impact + remediation advice**: CVSS 4.0 vector + business impact paragraph

---

## MCP Tool Integration

This skill supports invoking a local MCP server as the tool layer. **The primary choice is jshookmcp** (134 curated tools / 386 in full / 36 domains, with built-in Burp Suite bridge / Frida / WASM / anti-debugging / Android adb / sourcemap reconstruction). Full index and scenario mapping:

-> [`references/tools/mcp-jshook.md`](references/tools/mcp-jshook.md)

The `search` profile is recommended by default (context cost ~3K tokens); activate tools on demand via `mcp__jshook__search_tools` + `mcp__jshook__activate_tools`, avoiding a one-shot 40K+ token load with the `full` profile.

---

## Data Asset Scale

| Category | Scale |
|---|---|
| Attack-class playbooks | 19 |
| General methodology documents | 6 |
| Industry vertical playbooks | 2 (banking / telecom) |
| Dictionaries / credentials | 3 |
| Report templates | 1 |
| Structured payloads | **305** (177 web + 128 intranet) |
| WAF / EDR bypass variants | **263 steps**, covering 23 classes of web attacks |
| Tool command quick reference | 114 entries (Nmap/SQLMap/Burp/MSF/...) |
| Real HackerOne cases (disclosed High/Critical) | **2887 reports**, split by weakness into 141 category MDs |
| WooYun historical case statistics (non-reproducible) | 88,636 entries |

Real H1 cases are **embedded directly at the end of the matching playbook** (each playbook ends with a "Real H1 Cases" Top 12 table + summary).

---

## Compliance and Legal Red Lines

Every playbook ends with a "things not to do" section. General red lines (apply to every SRC program):

- ❌ Assets/domains out of scope -> stop immediately and report
- ❌ Actually taking other people's PII -> only prove accessibility, then destroy it immediately
- ❌ Sustained load / DoS / high traffic -> only 1–3 PoC packets, then stop immediately
- ❌ Modifying other people's data (even with write permission) -> validate only on objects you control
- ❌ Phishing or social engineering in production -> don't do it
- ❌ Submitting unreproduced guesses -> HTTP packet / screenshot / video evidence required
- ✅ Tag yourself with a test header (such as `X-Bug-Bounty: <handle>`)
- ✅ Stage broken access control scenarios with your own two accounts
- ✅ Use an OOB domain for SSRF probing; never use someone else's DNSLog
- ✅ Self-check with `references/templates/report-submission.md` before submitting

---

## CLI Mnemonic Prefix

`srchunter` (for example: `srchunter scope set <program>`, `srchunter recon run`, `srchunter findings new <type>`). The CLI is not implemented yet; this is only a naming convention.

---

## Reference / Cross-Chain Structure

```
src-hunter/
├── SKILL.md                    # This file — skill entry point
├── README.md                   # Project description
└── references/
    ├── methodology/   6 docs   # General playbooks
    ├── playbooks/    19 docs   # Attack-class playbooks (each with H1 cases + payload library)
    ├── industry/      3 docs   # Industry verticals
    ├── dictionaries/  3 docs   # Dictionaries / credentials
    ├── templates/     1 doc    # Report template
    ├── h1-reports/             # Raw data for 2887 H1 reports + 141 category MDs
    │   ├── raw/                # Raw JSON (for resume / secondary analysis)
    │   └── by-weakness/        # Markdown categorized by CWE
    └── payloader/              # 305 structured payload records
        ├── raw/                # JSON (machine-readable)
        ├── by-category/        # MD by category
        ├── tools/              # Tool commands
        └── waf-bypass.md       # 263-step WAF bypass set
```


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?

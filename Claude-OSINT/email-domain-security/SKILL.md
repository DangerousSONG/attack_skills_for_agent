---
name: email-domain-security
description: "Rigorous, defensible email-spoofability verdict and SPF supply-chain risk analysis computed from published DNS alone. Deepens the record-level SPF/DMARC/DKIM/BIMI/MTA-STS/DNSSEC fetch recipes in the offensive-osint arsenal (§16.14) with the reasoning that section doesn't do: a priority-ordered composite verdict for whether an attacker can actually land header-From-spoofed mail in an inbox, and by which vector (exact-domain vs subdomain) — grounded in the single most-misunderstood distinction in email security: the envelope MAIL FROM that SPF authenticates vs the visible header From: that only DMARC governs. Explains precisely why SPF -all/~all alone is NOT spoof-proof without DMARC enforcement, and why SPF +all bypasses DMARC even under p=reject pct=100. Covers RFC 7208 §4.6.4's 10-DNS-lookup / 2-void-lookup PermError fail-open condition with a runnable stdlib-only lookup-counter script, plus the SPF-include-takeover supply-chain vector (an attacker re-registering a dead include inherits SPF-pass authority over the victim domain) with strict transient-vs-NXDOMAIN discrimination discipline so a temporary SERVFAIL is never mistaken for a takeover lead. Fully passive: DNS TXT reads only, no mail sent, no RCPT TO probe, no API keys. Use when auditing a domain's real spoofing resistance (not just its published records), explaining to a client why 'we have SPF -all' does not mean they're covered, investigating an SPF PermError or an unusually long include chain, evaluating a dead SPF include as a takeover lead, or writing a defensible spoofability finding for a deliverable."
when-to-use: "Rigorous, defensible email-spoofability verdict and SPF supply-chain risk analysis computed from published DNS alone. Deepens the record-level SPF/DMARC/DKIM/BIMI/MTA-STS/DNSSEC fetch recipes in the 
version: 1.0
sources: asm_reference_impl, rfc_7208, public_research
triggers:
  - email spoofability
  - email spoofing verdict
  - is this domain spoofable
  - spoof feasibility
  - header from spoofing
  - envelope from vs header from
  - BEC feasibility
  - business email compromise feasibility
  - SPF DMARC verdict
  - DMARC enforcement
  - DMARC alignment
  - SPF supply chain
  - SPF PermError
  - SPF lookup limit
  - 10 DNS lookup limit
  - SPF void lookup
  - SPF include takeover
  - dead SPF include
  - SPF +all
  - DMARC p=none
  - DMARC p=reject
  - DMARC subdomain policy
  - duplicate DMARC record
  - email domain security
  - email authentication audit
  - phishing feasibility domain
  - spoof proof domain
---

# Email Domain Security — Spoofability Verdict & SPF Supply-Chain Analysis

> Companion skills: **`offensive-osint` §16.14** (raw record-fetch recipes — dig/PowerShell one-liners for SPF/DMARC/DKIM/BIMI/MTA-STS/TLS-RPT/DNSSEC/CAA, the MX→IdP inference table, the DMARC reporting-vendor table). **`osint-methodology`** (confidence levels, output format, severity rubric this skill inherits). Fetch the records with §16.14 first; bring the raw TXT text here for the verdict. This skill does not re-list what a record *is* — it reasons about what a domain's *combination* of records actually lets an attacker do.

## 0. When to Use / When NOT

**Use this skill when:**

- Asked to audit spoof feasibility, produce an email-spoofability verdict, or explain "is domain X spoofable."
- You already have raw SPF/DMARC TXT text (via `offensive-osint` §16.14 or your own `dig`) and need the *verdict*, not just the record dump.
- Investigating an SPF PermError, a long or unusual include chain, or a dead `include:` target.
- Writing a client-facing finding that has to survive the pushback "we have SPF `-all`, why is this flagged?"
- Reasoning about DMARC subdomain policy inheritance, `pct=` partial enforcement, or duplicate-record handling.

**Do NOT use this skill when:**

- You haven't fetched the raw records yet. Run `offensive-osint` §16.14's dig/PowerShell recipes first, then bring the text here.
- You want to actually *send* a spoofed test message or run an SMTP `RCPT TO` liveness check. That is active engagement work requiring explicit authorization and is out of scope for this passive-DNS skill — see §14.
- You're auditing TLS/cert posture rather than email auth — that's `offensive-osint` §16.15 / TLS deep audit territory.
- You need AXFR / zone-transfer analysis. `dns_deep`-class modules run that check alongside the email-auth sweep, but it's a distinct DNS finding (open zone transfer, unrelated to spoofability) — see the note in §9.

---

## 1. Scope & Authorization Posture

Same posture as the companion skills: assets you own or have written authorization to assess. Everything in this skill is **passive** — reading published, public DNS TXT records that any resolver on the internet can already see — so it carries essentially zero detectability risk on its own.

But the *verdict* this skill produces is the input to a decision someone downstream might act on (an authorized phishing-simulation send, a client remediation ticket, a bug bounty report). Flag the boundary explicitly: a passive verdict of "spoofable" is a strong, defensible claim about DNS-published policy — it is not itself proof that a spoofed message was delivered. See §14.

---

## 2. Confidence Levels

Inherits `osint-methodology` §2's three-tier scale, mapped onto email-auth assertions specifically:

| Level | Meaning here |
|---|---|
| **TENTATIVE** | A mechanism in the SPF chain could not be resolved (timeout / SERVFAIL / no nameservers) — the verdict for *that mechanism* is inconclusive. See §8's transient-vs-dead discipline; never silently upgrade this to FIRM. |
| **FIRM** | Record(s) present, parsed under RFC 7208 (SPF) / RFC 7489 (DMARC) grammar, verdict computed purely from directly observed TXT text. This is the ceiling for everything this skill produces on its own. |
| **CONFIRMED** | The verdict was cross-checked against actual mail-flow behavior (an authorized send-and-verify test). Outside this skill's passive scope — only ever assigned after an active test someone else ran. |

**Default posture:** everything this skill outputs is at most FIRM. Never claim CONFIRMED spoofability from DNS reading alone, no matter how conclusive the record combination looks.

---

## 3. Output Format

Same finding schema as the companion skills, with the fields this domain actually populates in practice:

```
Finding:
  module:      email_spoof   # or dns_deep / email-domain-security, depending on your pipeline
  asset_key:   domain:<target>
  category:    DNS_MISCONFIG   # the real implementation groups ALL email-auth findings under
                                # this one category — these are DNS record misconfigurations,
                                # not mail-server misconfigurations. Don't invent a separate
                                # EMAIL_SECURITY category unless your own schema needs one.
  severity:    <high|medium|low|info>     # see §7 / §8 for exact per-condition mapping
  confidence:  <tentative|firm|confirmed> # see §2 — almost always FIRM
  title:       "Email spoofable — <vector>"   # or the specific SPF supply-chain title
  description: <cite the exact reasons — see the "reasons" convention below>
  evidence:
    spf:                          <raw SPF TXT, or "(none)">
    dmarc:                        <raw DMARC TXT, or "(none)">
    vector:                       <e.g. "header-From spoof (exact domain, SPF +all bypasses DMARC)">
    effective_subdomain_policy:   <sp= value or the inherited p= value>
    reasons:                      [<ordered list of full-sentence reasons — see below>]
  dedup_key:   "emailspoof:<target>"   # or "spfsupply:<target>:<kind>", "spfmulti:<target>",
                                        # "dmarcmulti:<target>" — stable across re-scans so the
                                        # same finding doesn't duplicate on the next audit
  remediation: <the specific DMARC/SPF ratchet needed to close the exact vector found>
```

**The `reasons` convention:** the verdict logic (§7) doesn't just return a label — it builds an ordered list of full, client-report-ready sentences explaining *why* the domain is spoofable by that vector. Quote them directly in a deliverable rather than re-writing the explanation from scratch; they're already written in the right register (e.g. *"SPF terminates in `+all` (or bare `all`), returning an SPF pass for any sender IP. An attacker aligns the envelope sender to the target domain, so DMARC passes on the SPF leg and the spoofed message is delivered even if DMARC is set to reject."*).

---

## 4. Source Hygiene & Citations

For every record pulled: **FQDN queried + record type + UTC timestamp + resolver used + raw text verbatim**.

- Query against public resolvers (1.1.1.1 / 8.8.8.8 / 9.9.9.9), not local/system DNS — an operator's local resolver may be split-horizon or stale, masking what the internet actually sees. This matters more here than almost anywhere else in the arsenal: the whole verdict depends on seeing exactly what a real mail receiver's resolver sees.
- Capture the raw TXT text verbatim, not a paraphrase — SPF/DMARC grammar is unforgiving (a missing `;`, a `pct=` typo, a duplicate record) and the raw text is the only thing that lets someone else verify your parse.
- If you walked an SPF include chain, log every hop (host → TXT-or-NXDOMAIN-or-transient) — the walk itself is evidence, not just the final lookup count.

---

## 5. Do NOT

- **Do NOT treat SPF `-all`/`~all` as spoof-proof by itself.** This is the single misconception this skill exists to correct — see §6. SPF governs the invisible envelope return-path; the visible header From: is governed only by DMARC.
- **Do NOT assert CONFIRMED spoofability from DNS reading alone.** Passive analysis caps at FIRM (§2). CONFIRMED requires an authorized send-and-verify test — out of this skill's scope (§14).
- **Do NOT send actual spoofed test mail, or run an SMTP `RCPT TO`/`MAIL FROM` probe, as "confirmation."** That's active engagement work requiring explicit authorization; this skill is DNS-reads-only.
- **Do NOT flag a transient DNS failure (SERVFAIL / timeout / no-nameservers) on an SPF include as "dead" or a takeover lead.** Only an explicit NXDOMAIN qualifies — see §8's transient-vs-dead discipline. A dead-include false-positive is the kind of finding that gets a report laughed out of a client review.
- **Do NOT count a macro-expanded SPF target (`%{d}`, `%{i}`, `%{s}`, …) as a resolvable takeover candidate.** The mechanism still costs a DNS lookup toward the RFC 7208 budget, but you cannot passively resolve the literal macro string — doing so will NXDOMAIN and produce a false takeover claim.
- **Do NOT ignore a `redirect=` modifier that sits after a terminal `all` mechanism** — per RFC 7208 §6.1 it is never reached (SPF evaluation stops at `all`), so don't count it toward the lookup budget or walk it.
- **Do NOT assert an SPF-include-takeover finding from NXDOMAIN alone.** NXDOMAIN is necessary but not sufficient — you still have to check whether the registrable domain is actually available for an attacker to register (WHOIS/RDAP). NXDOMAIN + confirmed-available = takeover lead; NXDOMAIN + still-registered-to-someone = just a dead reference.

---

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

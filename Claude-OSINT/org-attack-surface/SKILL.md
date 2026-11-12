---
name: org-attack-surface
description: "Passive organization attack-surface mapping: legal entity to group, domain, subnet/ASN, online asset attribution via GLEIF/SEC EDGAR/passive DNS/crt.sh pivots, confidence grading. Signals: attack surface mapping, asset attribution."
zh-signals: "组织级攻击面测绘:法人实体→集团→域名→网段/ASN→在线资产全链路归属判定(GLEIF/SEC EDGAR/被动DNS/crt.sh 组织名枢轴),带置信度分级,纯被动。信号:攻击面测绘,资产归属。"
when-to-use: >-
  Org-grade attack-surface mapping: given a company's legal identity, discover its ENTIRE owned internet footprint — corporate family -> owned domains -> owned netblocks/ASN -> live assets — with attri
version: 1.0
sources: asm_reference_impl, gleif, public_research
triggers:
  - org attack surface
  - organization attack surface
  - org footprint
  - corporate footprint
  - corporate family
  - corporate family mapping
  - corporate family tree
  - subsidiary discovery
  - subsidiary attack surface
  - subsidiary mapping
  - GLEIF
  - LEI lookup
  - legal entity identifier
  - legal name to LEI
  - EDGAR subsidiary
  - SEC EDGAR
  - Exhibit 21
  - 10-K subsidiaries
  - OpenCorporates
  - Wikidata corporate graph
  - reverse WHOIS
  - reverse whois pivot
  - crt.sh organization search
  - crt.sh O=
  - certificate transparency org pivot
  - CT org pivot
  - dark netblock
  - org-first RIR search
  - ARIN Whois-RWS
  - ARIN org search
  - RIPE DB search
  - RIPE organisation search
  - RDAP entity search
  - ASN discovery
  - BGPView
  - RIPEstat
  - hyperscaler scope guard
  - cloud netblock over-attribution
  - shared hosting CDN attribution
  - AWS netblock attribution
  - M&A footprint
  - M&A attack surface
  - shadow IT discovery
  - promote to scan
  - discover-only candidate
  - org identity resolution
  - corporate identity resolution
  - owned netblock discovery
  - owned ASN discovery
  - org index search
  - outward identity search
  - identity-seeded discovery
  - attribution confidence
  - ownership tier
  - owner signal
  - independent evidence combiner
  - rule of three attribution
  - namesake grafting
  - org tree walk
  - subsidiary entity pivot
  - registrant org pivot
  - WHOIS privacy pivot
  - Shodan org filter
  - Censys organization filter
  - company name to attack surface
---

# Org Attack Surface — Corporate-Family Footprint Mapping

> Companion skills: [`osint-methodology`](../osint-methodology/) (the "how to think" 5-stage recon
> pipeline this plugs into) and [`offensive-osint`](../offensive-osint/) (the per-host arsenal you run
> once this skill hands you owned domains/netblocks — see its §14 Public Records and §28 Infrastructure
> OSINT for the tool directory this skill deepens rather than duplicates). This skill answers a
> different, upstream question: **not** "what does `acme.com` expose", but "what does **Acme
> Corporation, the legal entity**, own across every domain, netblock, and subsidiary it has — including
> the parts with no DNS trail back to the seed at all."

## 0. When to Use / When NOT

**Use this skill when:**

- The engagement starts from a **company name or legal entity**, not a domain — you need to derive
  the domain(s) first, not just enumerate one.
- You need to find an org's **subsidiaries, sister brands, or M&A-acquired footprint** that a
  DNS/CT-only sweep of one seed domain would never surface.
- You suspect **"dark" IP space** — netblocks or ASNs registered to the org's legal entity with
  no DNS record pointing at them (forgotten datacenter allocations, un-linked M&A infrastructure,
  IPs that only ever ran raw services).
- You need **attribution discipline**: every candidate domain/netblock/ASN this skill surfaces
  carries an explicit, auditable ownership score — never a bare "looks related."
- You are scoping a large or conglomerate engagement and need to prune scope by real corporate
  ownership before spending recon budget on strangers.

**Do NOT use this skill when:**

- You already have a confirmed, bounded target list and just need per-host recon — go straight to
  `offensive-osint`.
- The target's authorization isn't established — see §1.
- You need active exploitation or post-exploitation — out of scope here and everywhere in this
  skill family.

---

## 1. Authorization & Legal Posture

Same posture as the companion skills: intended for assets the operator owns or has **written
authorization** to assess. This skill is unusually likely to surface entities the operator did NOT
ask about (subsidiaries, sister brands, M&A targets) — that is the point, but it sharpens the scope
question rather than loosening it.

**Soft scope check** — ask once when unclear:
> *"This will surface the target's subsidiaries and related infrastructure, some of which may be
> outside your engagement scope. Should I include the full corporate family, or stay bounded to the
> named entity and its direct domains?"*

**Always-on guardrail specific to this skill:** every asset this skill discovers beyond the seed
domain — related domains, dark netblocks, discover-only ASNs, index-search IPs — is a **lead**, not
a target. See §6.6 and every "discover-only" callout below. Nothing this skill produces is
automatically in scope for active testing; a human confirms ownership first.

---

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

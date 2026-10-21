---
name: org-attack-surface
description: "Org-grade attack-surface mapping: given a company's legal identity, discover its ENTIRE owned internet footprint — corporate family -> owned domains -> owned netblocks/ASN -> live assets — with attribution discipline, not just DNS breadth. The org-first attribution pyramid (legal entity -> LEI/registration -> corporate family -> owned domains -> owned netblocks/ASN -> live assets). Corporate-identity resolution via the GLEIF LEI API (legal name -> LEI, exact-LEI direct-children expansion, downward-only depth-capped BFS, NEVER a name re-resolution), SEC-EDGAR full-text search + Exhibit-21 subsidiary entity names, OpenCorporates entity corroboration, Wikidata SPARQL corporate graph (P856/P355/P749/P1830). Domain attribution via reverse-WHOIS (WhoisXML preview-then-purchase quota guard, SecurityTrails associated-domains — both paid), crt.sh O= certificate-transparency organization pivot (keyless), infrastructure correlation (shared NS/MX/SaaS-TXT, netblock membership, reverse-DNS PTR), and the independent-evidence combiner (1-prod(1-w_i), rule of three, OwnerTier NONE/WEAK/MODERATE/STRONG/CONFIRMED) — discover-only `related:` candidates are NEVER auto-scanned. Netblock/ASN attribution via org-first RIR queries (ARIN Whois-RWS org-handle search, RIPE DB organisation + inverse-org search) that recover 'dark netblocks' with no DNS link to the seed, ASN discovery (RIPEstat + BGPView union), the HYPERSCALER-SCOPE GUARD (never attribute a whole AWS/GCP/Azure/Cloudflare announced range to a tenant — keep only the seed-containing block, tag shared_hosting_cdn), and org-identity-seeded internet-scan-index queries (Shodan/Censys/ZoomEye/FOFA/BinaryEdge org: filters + an always-on keyless crt.sh fallback). Promote-to-scan triage ranks forgotten discover-only netblocks by remote-access exposure (gateway-vendor/KEV/control-plane/datastore port scoring) into an operator queue. Attribution confidence rubric + anti-patterns (namesake grafting via GLEIF name re-resolution, single-signal ownership, hyperscaler over-attribution, privacy-WHOIS pivot poisoning, RIR org-name collisions). Passive/keyless-first OSINT only — every paid-key dependency is enrichment on top of a keyless core, never a hard requirement. Use when mapping an organization's full corporate-family internet footprint, resolving a legal entity to its LEI/subsidiaries, discovering domains/netblocks/ASNs an org owns beyond its one seed domain, auditing M&A/shadow-IT sprawl, or scoping an engagement that starts from a company NAME rather than a domain."
when-to-use: "Org-grade attack-surface mapping: given a company's legal identity, discover its ENTIRE owned internet footprint — corporate family -> owned domains -> owned netblocks/ASN -> live assets — with attri
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

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

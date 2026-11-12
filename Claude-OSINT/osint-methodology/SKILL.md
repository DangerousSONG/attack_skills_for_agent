---
name: osint-methodology
description: "Six-stage OSINT recon methodology: seed, asset expansion, enrichment, exposure analysis, convergence, limited active validation; includes severity, identity mapping, time budget, deliverables. Signals: OSINT methodology, recon pipeline, attack surface assessment, intelligence workflow."
zh-signals: "六阶段 OSINT 侦察方法论管线:种子→资产扩展→增强→暴露分析→收敛→有限主动验证,含严重度分级、身份面测绘、时间预算与交付模板。信号:osint方法论,侦察管线,攻击面评估,情报工作流。"
when-to-use: >-
  Comprehensive OSINT methodology for external red-team operations and authorized attack-surface assessments. Covers the 6-stage recon pipeline (seed → asset expansion → enrichment → exposure analysis
version: 2.3
sources: community, public_research
triggers:
  - external recon
  - external red team
  - red team external
  - attack surface management
  - attack surface mapping
  - ASM
  - perimeter recon
  - target reconnaissance
  - bug bounty recon
  - asset discovery
  - footprint
  - attack path
  - identity fabric
  - SSO discovery
  - IdP fingerprinting
  - tenant fingerprinting
  - M365 enumeration
  - Microsoft 365 recon
  - API discovery
  - GraphQL introspection
  - mobile recon
  - APK analysis
  - cloud bucket enumeration
  - breach correlation
  - secret leak hunt
  - origin discovery
  - CDN bypass
  - WAF bypass
  - vulnerability prioritization
  - CVE prioritization
  - EPSS
  - CISA KEV
  - phishing infrastructure
  - pretext development
  - bug bounty submission
  - responsible disclosure
  - client report
  - exec summary
  - risk translation
  - confidence upgrade
  - time budget
  - engagement profile
  - asset triage
  - detection-aware probing
  - back-off strategy
  - OSINT methodology
  - open source intelligence
  - target profiling
  - OSINT workflow
  - recon methodology
  - threat actor investigation
  - attribution
---

# OSINT Methodology — External Red-Team Edition

## 0. When to Use / When NOT

**Use this skill when:** planning or executing authorized external recon (red team, bug bounty, ASM); mapping an org's attack surface; investigating a person/entity/threat-actor; producing client deliverables.

**Do NOT use this skill when:** the user needs active exploitation, post-exploitation, or malware dev; blue-team/detection content; or the target's authorization is unclear — surface the scope question first.

---

## 1. Authorization & Legal Posture

Intended for assets the operator owns or has **written authorization** to assess.

**Soft scope check** — when authorization isn't established, ask once:
> *"Quick scope check: is this a target you own or have written authorization to assess? I want to make sure we stay on the right side of the engagement boundary."*

Once asserted, don't re-ask. If the engagement type is stated ("pentest of acme.com under contract"), proceed.

**Always-on guardrails:**

- Never weaken auth, rate limits, or safety controls on the target side.
- No destructive probes (SYN scans at line-rate, masscan, fuzzing) outside explicit `--aggressive` mode.
- Never paste real PII, credentials, session tokens, or API keys into cloud-hosted LLMs.
- Never act against assets outside documented scope, even "obviously related" ones.

---

## 2. Confidence Levels

Every assertion carries a confidence level.

| Level | Meaning |
|---|---|
| **TENTATIVE** | Plausible from indirect evidence; unverified. Snippet-only dork match, email pattern inferred from name, single passive-source subdomain. |
| **FIRM** | Directly observed, uncorroborated. Subdomain resolves; Shodan banner returned; CT-log entry. |
| **CONFIRMED** | Multiple independent corroborations OR directly verified. Live-validated token; bucket listable; three-source subdomain convergence. |

**Rule of three for attribution:** 3 independent weak signals, OR 1 strong + 1 weak. Never single-source attribute.

### 2.1 Confidence Upgrade Workflows

| Asset type | TENTATIVE → FIRM | FIRM → CONFIRMED |
|---|---|---|
| Subdomain | ≥2 passive sources OR DNS resolves | Serves on a standard port AND banner/cert returned |
| IP | ≥2 sources (passive DNS, ASN, Shodan) | TCP SYN-ACK or ICMP reply |
| WebApp | URL extracted but not yet hit | HTTP returns 2xx/3xx/4xx AND content-length > 0 |
| Email | Name-pattern inferred OR snippet-only | Listed in Hunter/IntelX/breach, OR SMTP 250 (abort at DATA) |
| Bucket | Permutation candidate + HEAD returns 200/301/403 (exists) | GET listing = CONFIRMED |
| Credential / secret | Regex match in captured text | Read-only validator returns success (scope + account-ID documented) |
| Person | Name from single source | Confirmed by second independent source |
| SSO tenant | OIDC discovery endpoint returns metadata | Tenant GUID extracted AND domain ties back via MX/autodiscover/SP record |

Default reporting posture: never claim CONFIRMED without explicit corroboration. When in doubt, downgrade.

---

## 3. Output Format

Each finding uses this schema (drops cleanly into asset-management tools):

```
Finding:
  id:          <stable hash or UUID>
  module:      <technique that discovered it>
  asset_key:   <typed key, e.g. sub:api.example.com>
  category:    <e.g. SECRET_LEAK, OPEN_GRAPHQL_API, SSO_EXPOSURE>
  severity:    <info|low|medium|high|critical>
  confidence:  <tentative|firm|confirmed>
  title:       <one-line summary>
  description: <2-5 sentences>
  evidence:
    url:       <where found>
    timestamp: <UTC ISO8601>
    sha256:    <hash of any downloaded artifact>
    raw:       <truncated to 2 KiB>
  references:  [<CVE-ID, advisory URL, vendor doc>]
  remediation: <action the asset owner can take>
```

Always use UTC timestamps.

---

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

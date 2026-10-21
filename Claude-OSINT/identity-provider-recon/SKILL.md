---
name: identity-provider-recon
description: "Organization-grade identity-fabric mapping: tenant/federation fingerprinting and the pre-auth user-ENUMERATION oracle methodology — enumeration and fingerprint only, never credential submission. Covers domain-to-tenant resolution (Microsoft getuserrealm.srf Managed/Federated namespace check, Entra OIDC metadata tenant-GUID extraction, Autodiscover v2), keyless Microsoft tenant-federation mapping (GetFederationInformation SOAP -> sibling-domain discovery, discover-only ROE, FEDERATED_WITH provenance edge held out of attack-path pivoting), Okta org-slug derivation + OIDC fingerprint + governed custom-domain enumeration, ADFS passive/active fingerprint + version inference, Google Workspace MX-correlated detection, generic OIDC (Auth0/Keycloak/Ping Identity/OneLogin/Duo) discovery, SAML metadata (5 paths), Azure AD Seamless-SSO Negotiate-challenge detection, Microsoft Defender for Identity (MDI) sensor-API presence check, the user-enumeration oracle methodology for Microsoft GetCredentialType (IfExistsResult semantics: exists / doesn't-exist / exists-in-federated-tenant / throttled) and Okta /api/v1/authn (errorCode differential), Medium-detectability discipline with a hard 20-candidate-per-tenant cap and admin/role interest-based ranking, and name x confirmed-email-pattern login-candidate synthesis that FAILS CLOSED with zero output when no org pattern is confirmed. Grounded directly in a production ASM implementation's sso_idp.py, tenant_recon.py, and core/email_patterns.py modules. Deepens — does not duplicate — offensive-osint skill's Identity Fabric endpoint reference with the tenant-federation MAP, the oracle WORKFLOW, and the candidate-SYNTHESIS methodology that reference lacks. Use when fingerprinting an organization's identity provider, mapping its tenant/federation boundary, running an authorized pre-auth user-enumeration pass, or synthesizing login candidates from harvested names to feed that oracle — never for password spray, credential submission, or auth bypass."
when-to-use: "Organization-grade identity-fabric mapping: tenant/federation fingerprinting and the pre-auth user-ENUMERATION oracle methodology — enumeration and fingerprint only, never credential submission. Cove
version: 1.0
sources: asm_reference_impl, public_research
triggers:
  - identity fabric
  - identity provider recon
  - IdP recon
  - IdP fingerprinting
  - tenant fingerprinting
  - tenant recon
  - SSO discovery
  - SSO fingerprinting
  - federation mapping
  - federation boundary
  - tenant federation map
  - domain to tenant resolution
  - GetFederationInformation
  - M365 tenant federation
  - Entra tenant recon
  - Azure AD tenant recon
  - Azure AD enum
  - entra enum
  - getuserrealm
  - Managed vs Federated namespace
  - okta enum
  - Okta org slug
  - Okta governed domains
  - Okta OIE vs Classic
  - ADFS enum
  - ADFS version fingerprint
  - ADFS mex endpoint
  - Google Workspace enum
  - SAML metadata discovery
  - generic OIDC discovery
  - Auth0 fingerprint
  - Keycloak fingerprint
  - tenant GUID extraction
  - Seamless SSO detection
  - Azure AD Seamless SSO
  - AZUREADSSOACC
  - MDI presence
  - Defender for Identity detection
  - user enumeration oracle
  - account existence enumeration
  - pre-auth user enum
  - GetCredentialType
  - IfExistsResult
  - Okta authn enum
  - authn endpoint enumeration
  - credential type endpoint
  - user enum detectability
  - email pattern synthesis
  - login candidate synthesis
  - login candidate list
  - name to email pattern
  - sibling tenant domains
  - federated sibling domain
  - fail closed synthesis
  - identity fabric mapping
---

# Identity-Provider Recon — Tenant, Federation & User-Enumeration Oracle Mapping

> Companion skills: [`osint-methodology`](../osint-methodology/) (§6.2 detectability tagging, §11
> identity-fabric pointer — the "how to think" skill this plugs into) and
> [`offensive-osint`](../offensive-osint/) (§22 Identity Fabric — the concrete endpoint/payload
> reference this skill builds a workflow on top of, rather than re-listing). This skill answers the
> question those two don't: **how do the tenant, its federation partners, its IdP, and its
> user-enumeration oracle fit together as one map** — and where exactly enumeration stops and
> credential submission begins.

## 0. When to Use / When NOT

**Use this skill when:**

- You need to resolve a domain to its identity tenant (Entra/Okta/ADFS/Google Workspace) and
  determine whether auth is Managed or Federated.
- You need to map an org's **federation boundary** — every sibling domain that shares the same
  M365/Azure AD tenant trust, not just the seed.
- You need to distinguish Entra vs. Okta vs. ADFS vs. Google Workspace vs. a generic OIDC IdP from
  passive/low-detectability signals.
- You need to detect Seamless SSO or Microsoft Defender for Identity (MDI) presence — both change
  the risk calculus of anything downstream.
- You have **authorization for a Medium-detectability, log-generating pass** and need to run a
  pre-auth user-enumeration oracle (GetCredentialType / Okta `/api/v1/authn`) to build a valid-account
  list — **without ever submitting a password**.
- You have harvested employee names and a **confirmed** org email-format pattern and need to
  synthesize ranked login candidates to feed that oracle.

**Do NOT use this skill when:**

- You need to submit credentials, replay breach creds, forge/replay a token, or confirm an
  auth-bypass — that is a different, higher-authorization tier. See §14.
- The target's authorization for **active, logged** probing isn't established — the passive half of
  this skill (§7–§10) needs the same soft-scope posture as every companion skill; the active half
  (§11) needs it explicitly, because it generates tenant-side audit-log events (§1, §11.4).
- You already have concrete endpoints and just need the reference table — go straight to
  `offensive-osint` §22.

---

## 1. Authorization & Legal Posture

Same base posture as `osint-methodology` §1: intended for assets the operator owns or has **written
authorization** to assess.

**This skill carries a sharper posture than most of the pack because §11 is not passive.** Every
domain-resolution, federation, IdP-fingerprint, Seamless-SSO, and MDI probe in §7–§10 is Low
detectability (a metadata GET/POST that any browser makes) — but the user-enumeration oracle in §11
is **Medium detectability**: it is a targeted, per-account POST against a live authentication
endpoint, and both Microsoft and Okta log it in the tenant's own sign-in/audit trail. Treat §7–§10
and §11 as two separate authorization tiers even within one engagement.

**Soft scope check** — ask once before running §11:
> *"I can build a valid-account list by probing Microsoft/Okta's pre-auth user-existence oracle. This
> never submits a password, but it IS logged in the tenant's own audit trail and is rate-limited on
> my end to stay under the radar. Confirm you want me to run this active pass?"*

**Always-on guardrails specific to this skill:**

- Never submit a real password, a guessed password, or any credential to any login endpoint. §11's
  oracles work by reading the *shape* of a rejection (§11.2, §11.3), not by trying to succeed.
- Cap user-enumeration at 20 candidates per tenant (§11.4) — this is not a suggestion, it is the
  production cap in the module this skill is grounded in.
- A `discover_only` federated sibling domain (§8) is a lead, never a target. Confirm ownership before
  extending §7–§11 to it.
- Nothing in this skill authorizes §14's excluded techniques, no matter how interesting the oracle
  results look.

---

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

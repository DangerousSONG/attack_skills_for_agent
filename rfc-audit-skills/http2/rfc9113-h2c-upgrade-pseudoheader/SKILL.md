---
name: rfc9113-h2c-upgrade-pseudoheader
description: Audit h2c upgrade negotiation and pseudo-header validation — a reverse proxy forwarding Upgrade: h2c + HTTP2-Settings opens a raw-byte tunnel that bypasses authentication/WAF (CVE-2026-88008 Traefik GHSA-w4v4-9rw7-5326 CVSS 9.1 CWE-444+863, fixed in PR #13797 stripping the h2c token; CVE-2026-88011 v2 sibling; CVE-2026-73548 Envoy generic-upgrade smuggling); HTTP2-Settings must not be forwarded with requests (RFC 9113 §3.2), and pseudo-header rules (§8.3) are the audit anchors; BishopFox h2csmuggler demonstrated default forwarding in HAProxy/Traefik/Nuster as early as 2020
zh-signals: 审计 h2c 升级协商与伪头校验——反向代理透传 Upgrade: h2c + HTTP2-Settings 即打开绕过认证/WAF 的原始字节隧道（CVE-2026-88008 Traefik GHSA-w4v4-9rw7-5326 CVSS 9.1 CWE-444+863，修复 PR #13797 剥离 h2c token；CVE-2026-88011 v2 同族；CVE-2026-73548 Envoy 通用升级走私）；HTTP2-Settings 不得随请求转发（RFC 9113 §3.2）、伪头字段规则（§8.3）是判定锚点；BishopFox h2csmuggler 2020 年已实证 HAProxy/Traefik/Nuster 默认透传
rfc: RFC 9113 §3.2（Starting HTTP/2 with Prior Knowledge / h2c Upgrade）/ §8.1.2.1（伪头字段规则）+ RFC 7540 §3.2
license: Apache-2.0
---

# RFC 9113 §3.2 h2c Upgrade Negotiation and Pseudo-Header Validation Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §3.2 (key points):
> `HTTP2-Settings` is a **connection-specific** header field (hop-by-hop) and must not be forwarded by intermediaries; h2c upgrade is only allowed on cleartext connections.

RFC 9113 §8.1.2.1 (key points):
> Pseudo-header fields (:method/:path/:authority/:scheme) must appear before all regular fields **and must not be duplicated**; regular fields must not use the ":" prefix.

Core pattern in one sentence: **the essence of the h2c upgrade is "the proxy and the server diverge in their understanding of protocol state" — the proxy thinks it is forwarding HTTP/1.1, the backend returns 101 and the entire connection becomes a raw tunnel invisible to the proxy. The two gates the RFC provides (don't forward HTTP2-Settings; upgrade only on cleartext) still fell on Traefik/Envoy in 2026, showing this is a vulnerability class that keeps resurrecting, not a historical CVE.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| HU-1 | Send HTTP/1.1 `Upgrade: h2c` + `HTTP2-Settings` + `Connection: Upgrade, HTTP2-Settings` to the target (h2csmuggler standard payload) | Proxy/gateway forwards the upgrade headers to the backend → same class as CVE-2026-88008; connection becomes a tunnel after the 101 → authentication/WAF fully bypassed |
| HU-2 | Initiate an h2c upgrade on a TLS connection (spec-forbidden, most clients refuse) | Proxy still forwards it → BishopFox h2-over-TLS smuggling channel holds |
| HU-3 | H2 frames containing duplicate/out-of-order pseudo-headers or colon-prefixed regular fields (`:path` twice, `:x-foo: bar`) | Not rejected as a stream/connection error → §8.1.2.1 pseudo-header validation missing (H2→H1 downgrade smuggling entry) |
| HU-4 | The upgrade request itself carries a body on a keep-alive connection | Body not consumed before entering the tunnel → byte-residue smuggling (same root cause as CVE-2026-73548 Envoy: upgrade payload forwarded before the 101 confirmation) |
| HU-5 | Illegal `HTTP2-Settings` value (invalid base64url / decoded payload is not a valid SETTINGS block) | Backend still returns 101 → §3.2 upgrade-payload validation missing (fingerprint + exploitation surface) |

Method: h2csmuggler scan (BishopFox/Assetnote dual versions) + handcrafted upgrade requests; verify whether protected paths return 200 after the tunnel is established.

## 3. Attack-Surface Hypotheses

- **Full authentication/WAF bypass**: HU-1/HU-2 — after the 101, the proxy degrades to a TCP tunnel; all middleware (BasicAuth/IPAllowList/RateLimit) is out of play
- **Request smuggling / tenant cross-talk**: HU-4 — byte residue in shared keep-alive connection pools can deliver other tenants' responses downstream (CVE-2026-73548 mechanism)
- **H2→H1 downgrade smuggling**: HU-3 — missing pseudo-header validation restores HTTP/1.1 semantic divergence in H2-front/H1-back architectures (complementary to `rfc9113-content-length-data-mismatch`)

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2026-88008** | Traefik v2.11.26–2.11.56 / v3.4.2–3.7.12 (fixed 3.7.13, GHSA-w4v4-9rw7-5326) | forwardedheaders middleware passes the Upgrade token + HTTP2-Settings verbatim; after the 101, net/http ReverseProxy switches to tunnel mode → the entire middleware chain is skipped. CVSS 9.1, CWE-444 + CWE-863 |
| **CVE-2026-88011** | Traefik v2 family (GHSA sibling) | Same mechanism, independently numbered on the v2 branch |
| **CVE-2026-73548** | Envoy generic upgrade path | Upgrade payload forwarded before receiving the upstream 101 confirmation; upstream treats it as a second pipelined request on keep-alive → response poisoning; root cause: missing pausedForGenericUpgrade state |
| BishopFox h2csmuggler research (2020) | HAProxy / Traefik / Nuster forward by default; AWS ALB / NGINX / Apache / Squid / Envoy via misconfiguration | First systematic demonstration of the h2c smuggling class; tool and Docker demo public |

## 5. Differential Verification

Control group: patched Traefik 3.7.13 (strips the h2c token + removes HTTP2-Settings); AWS ALB/NGINX default configuration (no forwarding) as the "secure-by-default benchmark".
Comparison fields: HU-1 forwarding or not, HU-2 whether TLS upgrades are terminated by the proxy itself, HU-3 pseudo-header-violation error-code correctness.
False-positive exclusion: the proxy supports h2c itself and terminates the upgrade (returns its own 101) → not forwarding, passes; if the backend never returns 101 the upgrade chain does not hold → record as "depends on backend configuration", not a proxy violation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `h2csmuggler-http2` (h2c upgrade automation), `smuggler-desync` / `http2smugl-desync` (upgrade-payload and downgrade-smuggling combinations)
- Tool layer (what to attack with): h2csmuggler (BishopFox/Assetnote), hyper-2 custom client (h2c over TLS)
- Post-hit actions: HU-1 confirmed → enumerate the protected paths reachable through the tunnel → verify whether WAF rules apply to tunnel traffic → output the bypass evidence chain

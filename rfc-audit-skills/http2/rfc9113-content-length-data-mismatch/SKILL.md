---
name: rfc9113-content-length-data-mismatch
description: Audit HTTP/2 implementations' consistency check between Content-Length and the sum of DATA frame lengths — in H2 Content-Length has no transfer meaning, but when forwarded/downgraded verbatim into H1 it regains semantics and becomes request smuggling (related CVE-2021-21295 Netty <4.1.60 H2→H1 downgrade smuggling and the 4.1.61 follow-up fix; CVE-2026-58055 nghttpx ≤1.69.0 Upgrade+CL keep-alive smuggling; sibling/complementary to the H3-side rfc9114-content-length-data-mismatch)
zh-signals: 审计 HTTP/2 实现 Content-Length 与 DATA 帧长度和的一致性校验——H2 中 CL 无传输含义但被原样转发/降级到 H1 时恢复语义即请求走私（关联 CVE-2021-21295 Netty <4.1.60 H2→H1 降级走私及 4.1.61 补漏；CVE-2026-58055 nghttpx ≤1.69.0 Upgrade+CL keep-alive 走私；与 H3 侧 rfc9114-content-length-data-mismatch 同族互补）
rfc: RFC 7540 §8.1.2 / RFC 9113 §8.1.1（Content-Length 与消息体一致性）/ RFC 9113 §8.1（消息格式）
license: Apache-2.0
---

# RFC 9113 §8.1.1 Content-Length vs DATA Consistency Audit (H2 Side)

## 1. Normative Clauses (Original Sources)

RFC 9113 §8.1.1 (key points, same origin as RFC 7540 §8.1.2):
> A request/response containing Content-Length whose value does not equal the sum of DATA frame payload lengths is **malformed**;
> In H2 Content-Length has no transfer-framing meaning, but is retained as metadata; implementations must not rely on it to determine message boundaries;
> When a proxy converts H2 to other versions, it **must re-establish or validate** the message-boundary semantics.

Core pattern in one sentence: **H2 DATA frames carry their own lengths, so Content-Length becomes a "mere comment" — but the downstream H1 world treats it as gospel. If a proxy does not re-validate CL when downgrading, the comment becomes a backdoor injected into the H1 request body. HTTP/2 did not eliminate smuggling; it just pushed it to the version boundary.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| CM-1 | H2 request with CL=5 but actually sends 5+N bytes of DATA (or multiple DATA frames whose total ≠ CL) | Not rejected as malformed and forwarded on downgrade → smuggling surface (same class as CVE-2021-21295) |
| CM-2 | CL matches the actual body but the proxy **re-declares** CL on downgrade (value recalculated/truncated) | Boundary recalculation error → implementation-side conversion defect |
| CM-3 | Single HEADERS + END_STREAM with CL>0 (no DATA frames) on the downgrade path | The scenario missed by the Netty 4.1.60 fix (patched in 4.1.61): CL not validated when endStream=true → downgrade smuggling |
| CM-4 | Upgrade + CL + request body forwarded via proxy to a keep-alive H1 backend | Boundary split on the reused backend connection → same class as CVE-2026-58055 (response-queue poisoning) |
| CM-5 | TE header residue (transfer-encoding forbidden in H2) converted to CL or forwarded verbatim on downgrade | Not stripped / not rejected → H2→H1 conversion obligation violated |

Method: h2 client crafting CL/DATA-inconsistent requests; observe whether the H2 side rejects + the boundary actually read by the H1 backend after proxy downgrade (control backend: httpd with strict CL parsing).

## 3. Attack-Surface Hypotheses

- **H2→H1 downgrade smuggling**: CM-1/CM-3 — classic front-end-H2 / back-end-H1 architecture; inject a second request, poison cross-tenant responses
- **Response-queue poisoning**: CM-4 — keep-alive backend connection reuse; the smuggled request's response goes to an unrelated client
- **Cache poisoning / access-control bypass**: smuggled requests bypass front-end auth and hit the backend directly (generic smuggling consequences)

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2021-21295** | Netty <4.1.60 (GHSA family) | H2 Content-Length propagated without validation in Http2MultiplexHandler; converted to H1 objects via Http2StreamFrameToHttpObjectCodec and forwarded → downgrade smuggling |
| **Netty 4.1.61 follow-up** | Netty | 4.1.60 missed the "single header frame with endStream=true" scenario — incomplete boundary-condition coverage is the recurrence pattern of this family |
| **CVE-2026-58055** | nghttpx ≤1.69.0 | Upgrade + CL + request body forwarded to keep-alive backends with hop-by-hop headers re-inserted; backend parsing ambiguity → smuggling + cross-client response-queue poisoning |

## 5. Differential Verification

Control group: Netty ≥4.1.61, recent Envoy with strict validation.
Comparison fields: CM-1/CM-3 rejection rate, CM-2 downgrade CL recalculation correctness, CM-4 connection-reuse determination (connections with Upgrade must never be reused), CM-5 TE stripping.
False-positive exclusion: end-to-end H2 (backend also H2) must still reject CL inconsistency (§8.1.1 malformed determination is independent of the downstream version), but severity is rated by "downgrade-smuggling exploitability" — pure-H2 intranet cases rate medium/low.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `smuggler-desync` (CL-inconsistency probing and exploitation), `http2smugl-desync` (H2 smuggling variants), `h2csmuggler-http2` (h2c upgrade-chain combinations)
- Tool layer (what to attack with): Python h2 (independent CL/DATA construction), strict H1 control backend, proxy downgrade chain
- Post-hit actions: CM-1 confirmed → build a cross-user response-poisoning PoC → merge evidence with the H3-side `rfc9114-content-length-data-mismatch` into a "CL-consistency cross-version weakness family"

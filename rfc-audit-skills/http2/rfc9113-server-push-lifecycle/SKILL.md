---
name: rfc9113-server-push-lifecycle
description: Audit HTTP/2 server-push (PUSH_PROMISE / reserved-stream) lifecycle implementations — enabling push is an attack-surface amplifier: Cache-Digest header triggering a crash on push (CVE-2020-9490 Apache httpd 2.4.20-2.4.43, CVSS 7.5, mitigated by H2Push off); push-method access-control failure (CVE-2023-30631 Apache Traffic Server push_method_enabled config ineffective, CVSS 7.5); http4s Ember push-frame DoS (CVE-2026-69203, mitigated by proxy stripping PUSH_PROMISE); RFC 9113 §6.6/§8.4 require that clients can reject push and servers can advertise ENABLE_PUSH=0, but reserved-stream state-machine obligations are scattered and have repeatedly failed in history
zh-signals: 审计 HTTP/2 服务端推送（PUSH_PROMISE/reserved 流）生命周期实现——推送开启即攻击面放大器：Cache-Digest 头触发推送时崩溃（CVE-2020-9490 Apache httpd 2.4.20-2.4.43，CVSS 7.5，H2Push off 缓解）；推送方法访问控制失效（CVE-2023-30631 Apache Traffic Server push_method_enabled 配置失效，CVSS 7.5）；http4s Ember 推送帧 DoS（CVE-2026-69203，缓解靠代理剥离 PUSH_PROMISE）；RFC 9113 §6.6/§8.4 要求客户端可拒绝推送、服务端可宣告 ENABLE_PUSH=0，但 reserved 流状态机的实现义务分散且历史上反复出事
rfc: RFC 9113 §6.6（PUSH_PROMISE）/ §8.4（Server Push）/ §5.1（reserved 流状态）
license: Apache-2.0
---

# RFC 9113 §6.6/§8.4 Server-Push Lifecycle Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §8.4 (key points):
> A server **must not** push any resource the client has not requested; the client can advertise `SETTINGS_ENABLE_PUSH=0` to decline push and **must** treat violating pushes as a connection error; the stream promised by a PUSH_PROMISE enters the reserved state and can only converge via HEADERS or RST_STREAM afterwards.

Core pattern in one sentence: **push hands the privilege of "server-initiated streams" to an application-configuration switch — historically it has repeatedly become a crash source (Cache-Digest), an access-control failure source (missing push-method authorization), and a DoS source (promised streams that never converge). The RFC provides the client-side rejection mechanism (ENABLE_PUSH=0 + violations are connection errors); the audit first checks "is it on by default", then "if on, did the reserved-stream state machine and push-payload validation keep up."**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| SP-1 | After the client sends `SETTINGS_ENABLE_PUSH=0`, a PUSH_PROMISE is still received | Not disconnected as a connection error (PROTOCOL_ERROR) → §8.4 rejection mechanism ineffective |
| SP-2 | Craft a malformed Cache-Digest value (invalid gzip payload / oversized claim) and induce the server to push | Server crashes on the push path → same class as CVE-2020-9490 |
| SP-3 | PUSH_PROMISE appears on a connection where the client advertised push disabled | Not rejected / no disconnect → server-side obligation missing, complementary to SP-1 |
| SP-4 | PUSH_PROMISE with an even promised-stream ID (client-initiated direction) or an already-occupied ID | Not handled as a connection error → §6.6 stream-ID validation missing |
| SP-5 | Reserved streams that never converge (neither HEADERS nor RST sent) | No timeout cleanup → promised-stream residency occupies the stream table (same pattern as the H3-side skill) |
| SP-6 | Request via the PUSH method (extension semantics predating RFC 8297) + push-method access control | Push path bypasses regular method authorization → same class as CVE-2023-30631 |

Method: h2 client advertising ENABLE_PUSH=0 and observing push behavior; craft Cache-Digest variants to induce pushes; measure reserved-stream residency duration.

## 3. Attack-Surface Hypotheses

- **Remote-crash DoS**: SP-2 — the push path is a historically crash-prone, low-coverage area (Cache-Digest parsing, gzip handling)
- **Access-control bypass**: SP-6 — if the push method bypasses the regular HTTP-method authorization matrix, it is equivalent to a hidden attack entry
- **Stream-table residency**: SP-5 — non-converging reserved streams interact with the concurrent-stream cap and can freeze the concurrency quota

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2020-9490** | Apache httpd 2.4.20–2.4.43 (mod_http2) | Specially crafted Cache-Digest header value → server crashes when performing HTTP/2 PUSH; mitigated by `H2Push off`; CVSS 7.5 |
| **CVE-2023-30631** | Apache Traffic Server 8.0.0–9.2.0 | `proxy.config.http.push_method_enabled` config ineffective (input-validation defect), push-method access control fails; CVSS 7.5 |
| **CVE-2026-69203** | http4s Ember Server | Push-frame-related DoS; official mitigation is proxy-layer stripping of PUSH_PROMISE frames; fixed in 0.23.35 |
| Cross-reference | H3-side `rfc9114-server-push-frame-rejection` | The same attack pattern audited in parallel on QUIC stacks (the server must accept client rejection of push) |

## 5. Differential Verification

Control group: modern nginx/Envoy versions that never send any PUSH_PROMISE after ENABLE_PUSH=0.
Comparison fields: SP-1/SP-3 error disposition, SP-2 push-path robustness, SP-5 reserved-stream timeout.
False-positive exclusion: an intermediary interprets and terminates push (forwarding as a regular 200 response) → passes; push disabled but the implementation retains reserved code paths that are never triggered → record as exposure surface, not a violation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (PUSH_PROMISE/Cache-Digest mutation), `dharma-grammar-fuzz` (push-frame sequence generation)
- Tool layer (what to attack with): Python h2 (ENABLE_PUSH=0 advertisement + push observation), memory/crash sampling
- Post-hit actions: SP-1 confirmed → verify whether pushed content bypasses authenticated resources → output the "push-disable advertisement ignored" evidence chain; SP-2 confirmed → archive the minimal crashing payload

---
name: rfc9114-server-push-frame-rejection
description: Audit whether HTTP/3 clients/servers strictly reject server-push legacy frames — PUSH_PROMISE and MAX_PUSH_ID receipt must terminate the connection with H3_FRAME_UNEXPECTED (RFC 9114 §7.2.5/§7.2.7); silently swallowing them means a missing protocol-error obligation (evidence: quic-go#5686, inconsistent handling within the same function in v0.60.0)
zh-signals: 审计 HTTP/3 客户端/服务端是否严格拒绝服务端推送遗留帧——PUSH_PROMISE 与 MAX_PUSH_ID 收到必须按 H3_FRAME_UNEXPECTED 终止连接（RFC 9114 §7.2.5/§7.2.7），静默吞掉即协议错误义务缺失（实证：quic-go#5686，v0.60.0 同函数内不一致处理）
rfc: RFC 9114 §7.2.5（PUSH_PROMISE）/ §7.2.7（MAX_PUSH_ID）/ §4.6（Server Push）
license: Apache-2.0
---

# RFC 9114 §7.2.5/§7.2.7 Server-Push Legacy Frame Rejection Obligations Audit

## 1. Normative Clauses (Original Sources)

RFC 9114 §7.2.5 (original text):
> A server MUST NOT send a PUSH_PROMISE frame. A client MUST treat the receipt of a PUSH_PROMISE frame as a connection error of type H3_FRAME_UNEXPECTED.
> If a PUSH_PROMISE frame is received on the control stream, the client MUST respond with a connection error of type H3_FRAME_UNEXPECTED.
> A client MUST NOT send a PUSH_PROMISE frame. A server MUST treat the receipt of a PUSH_PROMISE frame as a connection error of type H3_FRAME_UNEXPECTED.

RFC 9114 §7.2.7 (original text):
> A server MUST NOT send a MAX_PUSH_ID frame. A client MUST treat the receipt of a MAX_PUSH_ID frame as a connection error of type H3_FRAME_UNEXPECTED.
> Receipt of a MAX_PUSH_ID frame on any other stream [than the control stream] MUST be treated as a connection error of type H3_FRAME_UNEXPECTED.

RFC 9114 §4.6: HTTP/3 removed server push; the HTTP/2 legacy frame slots in §7.2 (PRIORITY 0x2 / PING 0x6 / WINDOW_UPDATE 0x8 / CONTINUATION 0x9) must receive H3_FRAME_UNEXPECTED on receipt (§7.2.8).

Core pattern in one sentence: **H3 abandoned H2's push and flow-control frames wholesale but kept their type codes — these type codes must kill the connection on receipt; silently skipping them leaves a backdoor for "deprecated semantics", and at the end of that backdoor lies whatever each implementation happens to think.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| SP-1 | Server sends a PUSH_PROMISE frame to a client connection (payload: valid push ID + compressed request header block) | Client fails to terminate with H3_FRAME_UNEXPECTED → violation (quic-go#5686 confirmed this bug exists in v0.60.0: silently discarded) |
| SP-2 | Server sends a MAX_PUSH_ID frame to a client connection | Client fails to terminate → violation (same root cause as SP-1, reported together in quic-go#5686) |
| SP-3 | Client sends a PUSH_PROMISE frame to a server | Server fails to terminate with H3_FRAME_UNEXPECTED → violation |
| SP-4 | PUSH_PROMISE received on the control stream / MAX_PUSH_ID received on a non-control stream | Not terminated with H3_FRAME_UNEXPECTED → violation |
| SP-5 | Send H2 legacy reserved frames (0x2 PRIORITY / 0x6 PING / 0x8 WINDOW_UPDATE / 0x9 CONTINUATION) | Not terminated with H3_FRAME_UNEXPECTED per §7.2.8 → violation (compare against the known-correct reserved-frame handling path) |

Method: h3i frame-by-frame injection; comparison implementations: rama proxy docs show the H2 reserved-frame path is correctly distinguished; within quic-go's same file, 0x2/0x6/0x8/0x9 correctly closeConn while 0x5/0xd are missed — an intra-library comparison pinpoints it.

## 3. Attack-Surface Hypotheses

- **Deprecated-semantics backdoor revival**: SP-1 — a silently swallowed push frame looks harmless, but if residual push-handling code paths survive inside the implementation (ported from H2), silent skipping + subsequent normal frames may activate the residual state machine
- **Systematic absence of protocol-error obligations**: SP-1~SP-5 all land in the "unknown/unsupported frame silently skipped" fallback branch — auditing how many other MUST clauses that fallback branch is reused for is the amplification point
- **Parsing-confusion stepping stone**: deprecated-frame payloads are often handled by "length skip" like unknown frames; a length-field parsing error becomes an out-of-bounds read/assertion surface

## 4. Related Historical CVEs / Evidence

| Evidence | Implementation | Root cause |
|---|---|---|
| **quic-go issue #5686** (2026-06, confirmed in v0.60.0, possibly all versions) | quic-go http3/frames.go | PUSH_PROMISE (0x5) and MAX_PUSH_ID (0xd) fall into the payload-skip fallback block and are silently discarded, while fellow reserved frames 0x2/0x6/0x8/0x9 correctly closeConn — the intra-function inconsistency is the best entry-point evidence for auditing this clause |
| erlang_quic 1.0.0 changelog | erlang_quic | "Server push lifecycle correctness (PUSH_PROMISE pairing, duplicate detection, MAX_PUSH_ID enforcement)" — the implementation once spent a whole release fixing the push lifecycle |
| No standalone CVE yet | — | Low-mid impact self-assessed (quic-go#5686), but obligations are dense and concentrated in the same fallback branch; treat as a blind-spot clause |

## 5. Differential Verification

Control group: quic-go ≥ fixed version, nghttp3, erlang_quic ≥ 1.0.0.
Comparison fields: termination behavior for SP-1~SP-5 individually; specifically compare the code-path difference between "reserved frames correctly handled" and "missed push frames" within the same parser.
False-positive exclusion: an implementation that does not compile any push-related code and routes 0x5/0xd through a unified H2-reserved-frame error path is compliant; flag only "silently skipped".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (deprecated frame + subsequent normal-frame combination sequences), `grammarinator-gen-fuzz` (frame-type grammar generation)
- Tool layer (with what): h3i, aioquic
- Post-hit actions: confirm silent swallowing → probe whether residual push code paths can be activated → assess the combined surface interacting with CANCEL_PUSH/GOAWAY

---
name: rfc9114-goaway-drain-enforcement
description: Audit whether HTTP/3 implementations enforce GOAWAY graceful-shutdown semantics strictly per RFC 9114 §5.2/§7.2.6 — identifier monotonicity, rejecting new requests after receipt, and the conservative default on GOAWAY-less shutdown (evidence: quiche#2700, quic-go#5326, erlang_quic 1.0.0 fix; no standalone CVE)
zh-signals: 审计 HTTP/3 实现对 GOAWAY 优雅关闭语义是否严格按 RFC 9114 §5.2/§7.2.6——标识符单调性、收帧后拒新请求、无 GOAWAY 关闭的默认假设错误即连接生命周期与请求完整性漏洞（实证：quiche#2700、quic-go#5326、erlang_quic 1.0.0 修复；无独立 CVE）
rfc: RFC 9114 §5.2（Connection Shutdown）/ §7.2.6（GOAWAY 帧）
license: Apache-2.0
---

# RFC 9114 §5.2 GOAWAY Graceful-Shutdown Semantics Audit

## 1. Normative Clauses (Original Sources)

RFC 9114 §5.2 (original text, key points):
> Endpoints MUST NOT initiate new requests or promise new pushes on the connection after receipt of a GOAWAY frame from the peer.
> An endpoint MAY send multiple GOAWAY frames indicating different identifiers, but the identifier in each frame MUST NOT be greater than the identifier in any previous frame... Receiving a GOAWAY containing a larger identifier than previously received MUST be treated as a connection error of type H3_ID_ERROR.
> If a connection terminates without a GOAWAY frame, clients MUST assume that any request that was sent, whether in whole or in part, might have been processed.

RFC 9114 §7.2.6 (original text, key points):
> A client MUST treat receipt of a GOAWAY frame containing a stream ID of any other type as a connection error of type H3_ID_ERROR.
> A client MUST treat a GOAWAY frame on a stream other than the control stream as a connection error of type H3_FRAME_UNEXPECTED.

Core pattern in one sentence: **GOAWAY is the final arbiter frame of "which requests count" — identifier monotonicity + reject-new-on-receipt + the conservative default on abnormal shutdown together guarantee requests are neither lost nor executed twice; any one of them loosened leaves the application facing lost or duplicated requests.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| GA-1 | After a normal handshake, send a GOAWAY with identifier N, then another GOAWAY with identifier N+k (larger) | Peer not terminated with H3_ID_ERROR → violates the monotonicity MUST NOT |
| GA-2 | After receiving a server GOAWAY (identifier N), keep sending new requests on streams with identifier ≥ N and observe whether the server rejects them (H3_REQUEST_REJECTED) | Server keeps accepting → violates the peer-side obligation dependency of "MUST NOT initiate new requests after receipt" |
| GA-3 | Send GOAWAY on a non-control stream / a server GOAWAY whose payload is a push-direction identifier | Peer not terminated with H3_FRAME_UNEXPECTED / H3_ID_ERROR → violation |
| GA-4 | Observe the implementation's own shutdown behavior: does it send GOAWAY on active close, and is the identifier semantics correct (accepted boundary)? | Closing without GOAWAY → downstream clients enter the "request might have been processed" uncertainty state (quiche#2700 evidenced pattern) |
| GA-5 | After sending GOAWAY, does the server explicitly cancel (CANCEL/RESET) in-flight streams ≥ identifier (§5.2 SHOULD) and keep processing streams < identifier? | In-flight streams left hanging — neither processed nor cancelled → availability surface |

Method: aioquic/h3i constructing multi-GOAWAY sequences; inspect control-implementation shutdown-path logs (whether GOAWAY is sent, identifier values).

## 3. Attack-Surface Hypotheses

- **Duplicate execution / loss of requests**: GA-1/GA-4 — identifier rollback makes the client misjudge "request not accepted" and retry while it was actually executed → duplicate charges/orders for non-idempotent operations; or conversely, loss
- **Graceful-shutdown hijacking**: GA-2 — accepting new requests after GOAWAY then closing without GOAWAY; the "might have been processed" state can be exploited for transaction-uncertainty attacks
- **Connection-lifecycle resource hanging**: GA-5 — in-flight streams not cancelled during shutdown; combined with high-frequency connection rotation, dangling stream state can accumulate

## 4. Related Historical CVEs / Evidence

| Evidence | Implementation | Root cause |
|---|---|---|
| **quic-go issue #5686 same-ecosystem evidence** (quiche#2700, quic-go#5326) | quiche / quic-go / erlang_quic | Shutdown path sends no GOAWAY or has wrong GOAWAY drain semantics — erlang_quic 1.0.0 changelog explicitly fixes "GOAWAY drain enforcement: reject new requests after a GOAWAY is sent or received" and the false H3_ID_ERROR on mutual dual-end GOAWAY; quiche at the edge closes connections with H3_NO_ERROR after tens of thousands of requests without GOAWAY |
| No standalone CVE for this clause yet | — | A "many MUSTs but every implementation for itself" clause: compliance bugs are dense but severity is scattered; treat as a blind-spot clause |

## 5. Differential Verification

Control group: quic-go ≥ 0.60, nghttp3, erlang_quic ≥ 1.0.0.
Comparison fields: GA-1 H3_ID_ERROR, GA-2 new-request rejection, GA-4 GOAWAY existence and identifier semantics at shutdown, GA-5 in-flight stream handling.
False-positive exclusion: an implementation that "logs an increasing GOAWAY and continues with the minimum identifier" with provably equivalent behavior to termination is compliant; flag only "accepts increasing", "closes without GOAWAY", "accepts new requests after receipt".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (control-stream frame-sequence fuzz), `grammarinator-gen-fuzz` (GOAWAY-sequence grammar generation)
- Tool layer (with what): h3i, aioquic
- Post-hit actions: confirm identifier rollback accepted → construct a replay scenario where "request executed but client judges it unexecuted" → assess business-layer impact (duplicate execution of non-idempotent operations)

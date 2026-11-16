---
name: rfc9114-grease-reserved-frames
description: Audit whether HTTP/3 implementations meet the tolerance obligations for GREASE/reserved frame types, reserved SETTINGS identifiers, and unknown unidirectional stream types per RFC 9114 §9/§7.2.8 — unknown frames must be length-skipped, never rejected; H2 reserved frames 0x02/0x06/0x08/0x09 must kill the connection, never be GREASE-skipped; rejecting GREASE is a forward-compatibility break (evidence: aioquic <1.6 stream-tail GREASE frame caused stream-data loss; confusing reserved frames with H2 smuggling frames opens a smuggling backdoor)
zh-signals: 审计 HTTP/3 实现对 GREASE/保留帧类型、保留 SETTINGS 标识、未知单向流类型的容忍义务是否按 RFC 9114 §9/§7.2.8——未知帧必须按长度跳过不得拒绝，H2 保留帧 0x02/0x06/0x08/0x09 必须炸连接不得当 GREASE 跳过；拒绝 GREASE 即前向兼容断点（关联实证：aioquic <1.6 流尾 GREASE 帧导致流数据丢失；保留帧与 H2 走私帧边界混淆即走私暗道面）
rfc: RFC 9114 §9（Extensions/未知帧容忍）/ §7.2.8（保留帧类型 0x1f·N+0x21 与 H2 保留帧）/ §7.2.4.1（SETTINGS 未知标识容忍）/ §6.2（未知单向流类型）/ RFC 8701（QUIC 传输层 GREASE，对照：QUIC 层无可忽略帧类型 RFC 9000 §12.4）
license: Apache-2.0
---

# RFC 9114 §9/§7.2.8 GREASE & Reserved-Frame Tolerance Obligations Audit

## 1. Normative Clauses (Original Sources)

RFC 9114 §9 / §7.2.8 (key points, cross-corroborated):
> Unknown frame types (including reserved GREASE types 0x1f * N + 0x21) MUST be ignored by length skipping — reserved frame types exist precisely to catch implementations that do not.

RFC 9114 §7.2.8 (H2 reserved-frame boundary, original text, key points):
> Frame types 0x02 (PRIORITY), 0x06 (PING), 0x08 (WINDOW_UPDATE), 0x09 (CONTINUATION) are permanently reserved in H3; receipt MUST be treated as connection error H3_FRAME_UNEXPECTED — **they are "known-forbidden", not "unknown"; skipping them as GREASE = silently swallowing H2 frames smuggled onto H3**.

RFC 9114 §7.2.4.1 (SETTINGS tolerance, key points):
> Unknown / reserved SETTINGS identifiers MUST be ignored (grease tolerance), never triggering SETTINGS_ERROR.

RFC 9114 §6.2 (unknown unidirectional stream types, key points):
> Unrecognized unidirectional stream types MUST be ignored (read and discarded), never closing the connection.

RFC 9000 §12.4 (comparison baseline):
> The QUIC transport layer reserves no "ignorable frame types" — an unknown frame at the transport layer is a protocol error; the ignore obligation is an H3-layer one. Do not conflate the two layers' tolerance semantics during the audit.

Core pattern in one sentence: **GREASE is a landmine the protocol buries for itself — erroring on GREASE is an advance notice of breaking future extensions; tolerating H2 reserved frames as unknown opens a smuggling backdoor at the "unknown vs known-forbidden" boundary. Bidirectional precision of the tolerance obligation is what this clause tests.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| GR-1 | Send reserved GREASE frames (0x21, 0x40, 0x1f·N+0x21 family) with valid lengths on a request/control stream | Connection closed/error → violates §9 (forward-compatibility break); silently skipped → compliant |
| GR-2 | Send H2 reserved frames 0x02/0x06/0x08/0x09 on any stream | Skipped as unknown → violates §7.2.8 (smuggling backdoor surface); correctly killed with H3_FRAME_UNEXPECTED → compliant |
| GR-3 | SETTINGS frame carrying reserved/unknown identifiers (e.g. 0x1f·N+0x21 family identifiers) | Triggers SETTINGS_ERROR/connection close → violates §7.2.4.1 |
| GR-4 | Open a unidirectional stream of unknown type and send data | Connection closed → violates §6.2; data discarded while operation continues → compliant |
| GR-5 | Stream-tail GREASE variant: make the ignored frame the last frame of the stream (aioquic <1.6 evidenced scenario) | Stream-tail data loss / peer timeout → implementation-level bug (skip logic swallowed the stream-end boundary) |

Method: aioquic frame-level construction (type/length/position variants); each probe class on an independent port to avoid endpoint-level config cross-contamination.

## 3. Attack-Surface Hypotheses

- **H2→H3 smuggling backdoor**: GR-2 — inject H2 frames into an H3 connection through a proxy; tolerant implementations silently swallow frames, splitting frontend/backend parsing (an H3 variant of the smuggler-desync family)
- **Forward-compatibility break / fingerprinting surface**: GR-1/GR-3 — implementations rejecting GREASE both expose their stack version and become failure points when real extensions land
- **Parsing split**: GR-5 — skip implementations' differing handling of the stream-tail boundary can be used for request/response truncation confusion

## 4. Related Historical CVEs

| CVE / Evidence | Implementation | Root cause |
|---|---|---|
| **aioquic < 1.6 stream-tail loss evidence** (disclosed via the pqcrypta-proxy conformance suite) | aioquic (affected downstreams incl. dnspython DoH) | When the last frame on a stream is of an ignored type, the stream's end boundary is lost and the client waits until timeout even after receiving the full response — an evidenced anchor for GREASE-tolerance implementation-detail bugs |
| Same methodology family as the sharing session | QUIC-FUZZ / interop-runner family | Reserved-frame/unknown-type paths are the core area of extensibility testing; interop history repeatedly found implementations over- or under-responding to this obligation |
| H2 reserved-frame boundary confusion (blind-spot declaration of this Skill) | Implementations under test | No standalone CVE for 0x02/0x06/0x08/0x09 — a high-variance blind-spot clause; once combined with a proxy conversion layer (H2 in, H3 out), it escalates to a smuggling-grade vulnerability; marked as a directed-audit signal |

## 5. Differential Verification

Control group: strictly two-sided implementations (GREASE skip / H2 reserved-frame kill) — reference the irontraffic design doc and the RFC 9114 §7.2.8 judgment; latest quiche/quic-go.
Comparison fields: GR-1/GR-3/GR-4 tolerance, GR-2 error-code correctness (must be H3_FRAME_UNEXPECTED, not H3_FRAME_ERROR), GR-5 stream integrity.
False-positive exclusion: transport-layer unknown frames erroring (per RFC 9000 §12.4) is correct behavior, not a violation; H2 reserved frames on an H2 connection are normal (audit target is the H3/QUIC endpoint).

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (GREASE/reserved-frame position and length fuzz), `dharma-grammar-fuzz` (frame-sequence variant generation)
- Tool layer (with what): aioquic (frame-level construction and injection), h3-conformance-style test suites (full GR-1~GR-5 item set), proxy conversion chains (GR-2 smuggling reproduction requires an H2→H3 proxy)
- Post-hit actions: GR-2 hit → immediately verify smuggling feasibility along the "proxy parsing split" route (hand off to `smuggler-desync`) → extract a minimal stream sequence for GR-5 and report to the implementation side

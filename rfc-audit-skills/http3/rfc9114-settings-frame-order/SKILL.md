---
name: rfc9114-settings-frame-order
description: Audit whether HTTP/3 implementations enforce SETTINGS-frame strictness per RFC 9114 §7.2.1 — SETTINGS must be the first frame on each control stream, and a duplicate SETTINGS must be treated as an H3_FRAME_UNEXPECTED connection error (blind-spot clause, no public CVE yet)
zh-signals: 审计 HTTP/3 实现对 SETTINGS 帧严格性是否按 RFC 9114 §7.2.1——SETTINGS 必须是每个 control stream 的第一帧，重复 SETTINGS 必须按 H3_FRAME_UNEXPECTED 连接错误处理（盲区条款，暂无公开 CVE）
rfc: RFC 9114 §7.2.1（SETTINGS 帧）
license: Apache-2.0
---

# RFC 9114 §7.2.1 SETTINGS Frame Order & Uniqueness Audit

## 1. Normative Clauses (Original Sources)

RFC 9114 §7.2.1 (original text, key points):
> The SETTINGS frame MUST be the first frame on the control stream.
> An endpoint MUST NOT send a SETTINGS frame after the first SETTINGS frame; an endpoint that receives such a frame MUST treat it as a connection error of type H3_FRAME_UNEXPECTED.
> Before the SETTINGS frame is received, an endpoint must not send request/response traffic that requires SETTINGS to take effect before it can be interpreted.

Core pattern in one sentence: **SETTINGS is the "protocol version & capability negotiation anchor" of the HTTP/3 control stream; its position (first frame) and uniqueness (exactly once) are the preconditions for all subsequent semantic parsing — loosen the anchor and everything parsed afterwards is undefined behavior.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| SO-1 | Send a non-SETTINGS frame (e.g. DATA/HEADERS/GREASE) as the first frame on the control stream and observe the peer | Connection not terminated with H3_MISSING_SETTINGS or H3_FRAME_UNEXPECTED → violation |
| SO-2 | After a normal SETTINGS, send a second SETTINGS frame (one with valid values, one with conflicting values) | Connection not terminated with H3_FRAME_UNEXPECTED → violation; if the second value is accepted → negotiation-hijack surface |
| SO-3 | Send an empty SETTINGS (all key items such as QPACK dynamic-table capacity at defaults) and observe whether the peer handles the negotiated defaults correctly per RFC | Default handling inconsistent with RFC → violation |
| SO-4 | Before receiving the peer's SETTINGS, send frames that depend on negotiation results (e.g. HEADERS encoded with a large dynamic table) and observe whether they are correctly rejected | Not rejected / no buffering protection → violation |
| SO-5 | Craft an incomplete SETTINGS on the control stream (frame header declares a length > actual payload, i.e. the stream ends mid-SETTINGS) | Not treated as H3_FRAME_ERROR and survives → violation |

Method: aioquic / quic-go custom peer with frame-level control of the control-stream content; h3i `send_frames_before_settings`-style scenarios.

## 3. Attack-Surface Hypotheses

- **Capability-negotiation hijacking**: SO-2 — if the implementation accepts a second SETTINGS, an attacker can override QPACK dynamic-table capacity, H3_DATAGRAM negotiation results and other capability bits, misaligning all subsequent parsing
- **Parsing-precondition bypass**: SO-1/SO-4 — frames injected before the anchor is established may be parsed in an "uninitialized state", producing type confusion or null-pointer paths
- **Half-open connection resource consumption**: SO-5 — an incomplete SETTINGS leaves the peer waiting indefinitely for the control stream to establish; multiplied across connections, this becomes resource exhaustion

## 4. Related Historical CVEs

This clause has **no public CVE yet** — a typical "constraint without disclosure" blind-spot clause: the RFC is explicit, every implementation claims support, but "is duplicate SETTINGS strictly rejected" and "is a non-SETTINGS first frame strictly terminated" have long been missing from mainstream test coverage. Per this layer's methodology, this is exactly a high-value directed-audit signal.

## 5. Differential Verification

Control group: quic-go, nghttp3 / nghttp2's H3 side, Cloudflare quiche.
Comparison fields: error codes and termination behavior for SO-1~SO-5 individually; pay special attention to consistency of the "connection error vs stream error" level.
False-positive exclusion: an implementation that "logs and continues" after an illegal SETTINGS sequence with behavior provably equivalent to termination is compliant; flag only "second SETTINGS takes effect" and "pre-anchor frames are parsed".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (control-stream frame-sequence fuzz), `h2csmuggler-http2` (H3 adaptation of the same-family precondition-confusion approach)
- Tool layer (with what): aioquic, h3i
- Post-hit actions: confirm whether the second SETTINGS takes effect → if yes, assess the negotiation-hijack chain; if it merely fails to terminate, record as a compliance gap

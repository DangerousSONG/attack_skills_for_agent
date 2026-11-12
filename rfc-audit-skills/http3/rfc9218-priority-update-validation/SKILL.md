---
name: rfc9218-priority-update-validation
description: Audit whether HTTP/3 implementations' validation of the PRIORITY_UPDATE frame (RFC 9218 §7.2) is complete — frame position, target stream type, out-of-limit stream IDs, push-stream references, and priority field-value parse failures are all connection-error obligations whose absence is a blind-spot clause (erlang_quic Strict PRIORITY_UPDATE parsing fix as evidence)
zh-signals: 审计 HTTP/3 实现对 PRIORITY_UPDATE 帧（RFC 9218 §7.2）的校验是否完备——帧位置、目标流类型、越限流 ID、推送流引用、优先级字段值解析错误即连接错误处理义务缺失（盲区条款；erlang_quic Strict PRIORITY_UPDATE parsing 修复实证）
rfc: RFC 9218 §7（PRIORITY_UPDATE 帧）/ §4（urgency 与 incremental 参数）
license: Apache-2.0
---

# RFC 9218 §7 PRIORITY_UPDATE Frame Validation Completeness Audit

## 1. Normative Clauses (Original Sources)

RFC 9218 §7.2 (original text, key points):
> The PRIORITY_UPDATE frame MUST be sent on the client control stream... Receiving a PRIORITY_UPDATE frame on a stream other than the client control stream MUST be treated as a connection error of type H3_FRAME_UNEXPECTED.
> The request-stream variant (0xF0700) MUST reference a request stream. If a server receives PRIORITY_UPDATE (0xF0700) for a stream ID that is not a request stream, this MUST be treated as a connection error of type H3_ID_ERROR. The stream ID MUST be within the client-initiated bidirectional stream limit. If a server receives PRIORITY_UPDATE (0xF0700) with a stream ID beyond the stream limits, this SHOULD be treated as a connection error of type H3_ID_ERROR.
> The push-stream variant (0xF0701) MUST reference a promised push stream. If a server receives PRIORITY_UPDATE (0xF0701) with a push ID greater than the maximum push ID or that has not yet been promised, this MUST be treated as a connection error of type H3_ID_ERROR.

RFC 9218 §4: priority field values use HTTP Structured Fields encoding; urgency ranges 0-7, out-of-range values must be ignored/handled per protocol (parameter parse failures must not drive the connection into an undefined state).

Core pattern in one sentence: **PRIORITY_UPDATE hands scheduling-decision power to the peer; the frame references "which stream should be scheduled how" — loosen any link of reference validation (position/type/range/existence) and you hand the write pointer of the scheduling state machine to the attacker.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| PU-1 | Send PRIORITY_UPDATE on a request stream / push stream / server control stream (instead of the client control stream) | Not terminated with H3_FRAME_UNEXPECTED → violation |
| PU-2 | Send 0xF0700 targeting a server-initiated stream ID / non-bidirectional stream ID | Not terminated with H3_ID_ERROR → violation |
| PU-3 | Send 0xF0700 with a target stream ID beyond the current concurrent-stream limit | Not treated as H3_ID_ERROR (SHOULD-level, flagged as a gap) → violation |
| PU-4 | Send 0xF0701 with an un-promised push ID / a push ID exceeding MAX_PUSH_ID | Not terminated with H3_ID_ERROR → violation |
| PU-5 | Craft a malformed Structured Fields Priority Field Value (urgency=99, nested disorder, illegal characters) and an over-long field value | Parse crash / scheduling-state pollution / connection hang → violation; malformed value ignored → compliant |

Method: h3i frame-by-frame construction; aioquic custom control stream; inspect scheduling logs to observe whether the target stream's priority is polluted.

## 3. Attack-Surface Hypotheses

- **Scheduling-priority pollution**: PU-2/PU-3 — forged high-priority references let an attacker's connection seize bandwidth (the reverse side of low-priority starvation DoS), or starve critical streams
- **Parse-crash surface**: PU-5 — Structured Fields parsers vary widely between implementations (RFC 8941 parsing corner cases abound); malformed values triggering assertion/recursion-depth issues are a high-frequency fuzz hit area
- **Complicity of missing connection-error obligations**: PU-1/PU-4 — violations that should terminate are tolerated, compounding with other frame-handling flaws into stepping stones for smuggling/confusion chains

## 4. Related Historical CVEs / Evidence

| Evidence | Implementation | Root cause |
|---|---|---|
| erlang_quic 1.0.0 changelog | erlang_quic | Explicitly fixed "Strict PRIORITY_UPDATE frame parsing per RFC 9218" — showing mainstream implementations were long lenient on this frame's parsing |
| No standalone CVE for this clause yet | — | RFC 9218 is relatively new (2022); PRIORITY_UPDATE is an extension frame and implementations mostly fall back to the "unknown frame ignored" path, which bypasses every MUST exactly — blind-spot clause |

## 5. Differential Verification

Control group: quic-go ≥ 0.60, nghttp3, erlang_quic ≥ 1.0.0.
Comparison fields: error codes and termination behavior for PU-1~PU-5 individually; pay special attention to whether the "extension frame ignored by default" path swallows PRIORITY_UPDATE.
False-positive exclusion: an implementation that does not support RFC 9218 (not declared in SETTINGS) handling PRIORITY_UPDATE as an unknown frame is compliant; flag only "declares support but validation missing".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (control-stream frame-sequence fuzz), `dharma-grammar-fuzz` (Structured Fields value grammar generation)
- Tool layer (with what): h3i, aioquic
- Post-hit actions: confirm validation gap → construct priority-pollution sequences and assess scheduling-fairness breakage → or minimize a parse-crash reproduction

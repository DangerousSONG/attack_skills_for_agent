---
name: rfc9000-transport-parameter-validation
description: Audit whether QUIC implementations validate transport-parameter integrity and consistency per RFC 9000 §18.2/§7.3 — missing/mismatched CID-related parameters, client carrying server-only parameters, illegal values not rejected (pre-authentication attack surface and MITM CID-injection surface; blind-spot clause; CVE-2025-54939 lsquic QUIC-LEAK evidences the same path)
zh-signals: 审计 QUIC 实现对传输参数完整性与一致性校验是否按 RFC 9000 §18.2/§7.3——CID 相关参数缺失/错配、服务端专用参数被客户端携带、非法值未拒绝即握手前无认证攻击面与中间人注入 CID 面（盲区条款；CVE-2025-54939 lsquic QUIC-LEAK 同路径实证）
rfc: RFC 9000 §18.2（Transport Parameter 定义）/ §7.3（使用 CID 参数的验证义务）
license: Apache-2.0
---

# RFC 9000 §18.2 Transport-Parameter Validation Completeness Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §7.3/§18.2 (original text, key points):
> An endpoint MUST treat the absence of the initial_source_connection_id transport parameter from either endpoint or the absence of the original_destination_connection_id transport parameter from the server as a connection error of type TRANSPORT_PARAMETER_ERROR.
> An endpoint MUST treat the following as a connection error of type TRANSPORT_PARAMETER_ERROR or PROTOCOL_VIOLATION: absence of the retry_source_connection_id transport parameter from the server after receiving a Retry packet; presence of the retry_source_connection_id transport parameter when no Retry packet was received; or a mismatch between values received from a peer in these transport parameters and the value sent in the corresponding Destination or Source Connection ID fields of Initial packets.
> A client MUST NOT include any server-only transport parameter: original_destination_connection_id, preferred_address, retry_source_connection_id, or stateless_reset_token. A server MUST treat receipt of any of these transport parameters as a connection error of type TRANSPORT_PARAMETER_ERROR.
> A server that chooses a zero-length connection ID MUST NOT provide a preferred address. Similarly, a server MUST NOT include a zero-length connection ID in this transport parameter. A client MUST treat a violation of these requirements as a connection error of type TRANSPORT_PARAMETER_ERROR.
> A max_udp_payload_size value below 1200 is invalid.

Core pattern in one sentence: **CID-related transport parameters are the only anchor binding "the CID seen on the wire" to "the CID negotiated in the handshake" — a missing or mismatched anchor means the Initial during the handshake can be injected and replaced; the connection's identity may be attacker-chosen from the very first handshake packet.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| TP-1 | Remove initial_source_connection_id (or, on the server side, original_destination_connection_id) and complete the handshake | Not terminated with TRANSPORT_PARAMETER_ERROR → violation |
| TP-2 | Carry retry_source_connection_id without a Retry / omit it after a Retry / make its value mismatch the Retry packet SCID | Not terminated → violation |
| TP-3 | Client Initial carries any server-only parameter (original_destination_connection_id / preferred_address / retry_source_connection_id / stateless_reset_token) | Server does not terminate → violation |
| TP-4 | Craft transport-parameter values inconsistent with the CID fields of the on-wire Initial packets (rewrite DCID and replay) | Not detected → MITM CID injection confirmed |
| TP-5 | Send max_udp_payload_size < 1200 / preferred_address containing a zero-length CID / zero-length-CID server carrying preferred_address | Not terminated with TRANSPORT_PARAMETER_ERROR → violation |

Method: per-parameter tampering with aioquic (transport parameters live in encrypted extensions; requires a custom TLS layer or a stack supporting extension injection); observe the validation path via quic-go debug logs.

## 3. Attack-Surface Hypotheses

- **CID injection (MITM)**: TP-4 — inject an Initial with an attacker-chosen CID during the handshake; if validation is missing, connection identity is hijacked and subsequent routing/stateless-reset tokens are all displaced
- **Pre-authentication handshake crash**: transport-parameter parsing sits on the pre-authentication path; malformed parameters are the entry point of the same "smuggled packet triggers memory allocation" class as LSQUIC QUIC-LEAK (CVE-2025-54939)
- **preferred_address with zero-length CID**: can drive the connection-ID state machine on migration paths into an undefined branch

## 4. Related Historical CVEs / Evidence

| CVE / Evidence | Implementation | Root cause |
|---|---|---|
| **CVE-2025-54939** (QUIC-LEAK, HIGH) | lsquic | Memory allocated on the pre-authentication path for malformed/oversized packets never freed — transport-parameter parsing and Initial handling share this unauthenticated pre-handshake path; TP-1~TP-5 of this Skill are the parameter-level systematic expansion of that path |
| No standalone CVE for parameter validation yet | — | §18.2 validation is scattered across §7.3/§18.2 in multiple paragraphs; implementations often validate only "parses" but not "values are consistent" — blind-spot clause |

## 5. Differential Verification

Control group: quic-go ≥ 0.60, msquic, ngtcp2.
Comparison fields: error codes and termination behavior for TP-1~TP-5 individually; focus on whether "parse succeeded but value validation" exists as an independent check.
False-positive exclusion: distinguish "ignore unknown parameters" (compliant; RFC allows) from "reject illegal values" (mandatory); flag only missing MUST-level validation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (transport-parameter byte fuzz), `tlsfuzzer-fuzz` (TLS-layer extension parameter mutation)
- Tool layer (with what): aioquic (custom transport parameters), hand-written TLS ClientHello mutation scripts
- Post-hit actions: if TP-4 holds → verify the impact chain of CID injection on routing layer / reset tokens; for TP-1~TP-3 → extend fuzzing against the pre-handshake crash surface

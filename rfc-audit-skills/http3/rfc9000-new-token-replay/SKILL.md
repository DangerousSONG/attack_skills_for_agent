---
name: rfc9000-new-token-replay
description: Audit QUIC implementations' protection of NEW_TOKEN frames and cross-connection token replay per RFC 9000 §19.7/§8.1.4 — single-use constraints, the IP-binding MUST, and unlimited replay would let the address-validation system be bypassed (blind-spot clause; format custom + scattered MUSTs = high-variance surface)
zh-signals: 审计 QUIC 实现对 NEW_TOKEN 帧与令牌跨连接重放的防护是否按 RFC 9000 §19.7/§8.1.4——令牌单用约束、IP 绑定 MUST、重放未限即地址验证体系被绕过（盲区条款；格式自定 + MUST 分散的高 variance 面）
rfc: RFC 9000 §19.7（NEW_TOKEN 帧）/ §8.1.4（地址验证令牌完整性）
license: Apache-2.0
---

# RFC 9000 §19.7 NEW_TOKEN Lifecycle and Replay-Protection Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §8.1.4 (verbatim):
> Tokens sent in NEW_TOKEN frames MUST include information that allows the server to verify that the client IP address has not changed from when the token was issued... Attackers could replay tokens to use servers as amplifiers in DDoS attacks. To protect against such attacks, **servers MUST ensure that replay of tokens is prevented or limited**. Tokens that are provided in NEW_TOKEN frames need to be valid for longer but SHOULD NOT be accepted multiple times.

RFC 9000 §19.7 (key points): the NEW_TOKEN frame is sent by the server after the handshake to issue a token that can skip address validation in **future connections**; **a client must never send a NEW_TOKEN frame**; tokens must be distinguishable from Retry tokens ("context distinguisher").

Core pattern in one sentence: **NEW_TOKEN is a performance optimization that amortizes address-validation cost onto future connections — but every reusable token issued is a forward-dated check pre-signed with "this address is trustworthy"; the check is bearer-style and resellable, and when it is cashed the server pays for a third party's forged source address.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| NT-1 | A client sends a NEW_TOKEN frame to the server | Server does not terminate with FRAME_ENCODING_ERROR / PROTOCOL_VIOLATION → violation |
| NT-2 | Obtain a token on connection A, then initiate connections B1, B2… N times from the **same IP** with the same token | All accepted with address validation skipped → violates SHOULD-NOT-accept-multiple-times; any single acceptance plus no server-side anti-replay state → flagged high-risk |
| NT-3 | Cross-IP replay of the token (same token from another source address) | Accepted → violates the IP-binding MUST |
| NT-4 | Token / Retry-token confusion: put a NEW_TOKEN token into the echo field of the Initial after receiving a Retry | Accepted → missing context distinguisher → violation |
| NT-5 | Observe the server's token issuance rate and volume: how many valid tokens can a single connection extract in batch | No cap / no expiry → the replay surface scales linearly with the token-pool size, recorded as a gap |

Method: aioquic two-connection sequence; scripted token replay after capture; server-behavior differential (responses with token vs without token on the Initial).

## 3. Attack-Surface Hypotheses

- **Address-validation-system bypass**: NT-2/NT-3 — an attacker bulk-extracts tokens and combines them with source-address spoofing, turning the server into a high-multiplier UDP amplifier (the endgame of lifting the 3x anti-amplification limit)
- **NAT sharing surface**: §8.1.4 itself notes that IP binding "might not be sufficient to protect other hosts behind the same NAT" — the token is equally valid for other hosts behind the NAT, a lateral amplification
- **Token-pool pollution**: NT-5 — the total stock of replayable tokens accumulated by a long-running server is the attacker's ammunition depot

## 4. Related Historical CVEs / Empirical Findings

| Evidence | Implementation | Root Cause |
|---|---|---|
| No standalone NEW_TOKEN CVE yet | — | The token format is server-defined (the RFC deliberately does not specify a format); validation quality depends on each implementation — a "custom format + scattered MUSTs" high-variance blind-spot clause |
| CVE-2023-49295 / CVE-2024-22189 (same-family pattern) | quic-go et al. | The same "protocol obligations (response/accounting) not enforced → resource asymmetry" pattern; address-validation obligation bypass is its resource-surface variant |
| RFC 9000 §8.1.4 NAT self-noted risk | Protocol layer | The standard itself admits IP-binding validation is insufficient under NAT — a protocol-level residual risk; the audit focus is whether implementations add further constraints on top |

## 5. Differential Verification

Control group: quic-go ≥ 0.60, msquic, nginx-quic.
Comparison fields: NT-1 termination behavior, NT-2 single-use, NT-3 IP binding, NT-4 context distinguishment.
False-positive exclusion: an implementation choosing "never send NEW_TOKEN" (not enabling the optimization at all) is the strictest compliant form; only flag "issues tokens without anti-replay / without IP binding".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (post-bypass amplification verification), `fuzzowski-network-fuzz` (token-field fuzzing)
- Tool layer (what to attack with): aioquic (token extraction and replay scripts)
- Post-hit actions: NT-2/NT-3 established → measure the amplification ratio after lifting the anti-amplification limit → assess feasibility as a reflection amplifier

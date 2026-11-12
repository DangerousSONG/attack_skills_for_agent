---
name: rfc9001-retry-integrity-tag
description: Audit whether QUIC implementations handle Retry-packet integrity and token lifecycle per RFC 9000 §8.1.4/§17.2.5 and RFC 9001 §5.8 — unverified integrity tag, replayable tokens, unguarded multi-Retry loops (pre-authentication attack surface; blind-spot clause; warpsock added §17.2.5.1/§17.2.5.2 loop guards as evidence)
zh-signals: 审计 QUIC 实现对 Retry 包完整性与令牌生命周期的处理是否按 RFC 9000 §8.1.4/§17.2.5 与 RFC 9001 §5.8——完整性标签未验证、令牌可重放、多 Retry 循环未防护即握手前无认证攻击面（盲区条款；warpsock 补齐 §17.2.5.1/§17.2.5.2 loop guards 实证）
rfc: RFC 9000 §8.1.4（令牌完整性）/ §17.2.5（Retry 包）/ RFC 9001 §5.8（Retry Integrity Tag）
license: Apache-2.0
---

# RFC 9001 §5.8 Retry Integrity & Token Lifecycle Audit

## 1. Normative Clauses (Original Sources)

RFC 9001 §5.8: a Retry packet carries a 128-bit integrity tag computed with a **publicly fixed** AES-128-GCM key and nonce (v1 constants are public; v2 constants are specified separately in RFC 9369 §3.3.3) — the client **must** verify this tag before accepting a Retry (the tag provides no server authentication, only tamper/forgery protection).

RFC 9000 §8.1.4 (original text, key points):
> Address-validation tokens MUST be hard to guess and MUST have integrity protection against client forgery; Retry tokens SHOULD be short-lived and usable only for immediate echo; **servers MUST ensure that replay of tokens is prevented or limited**.
> If a server receives an Initial containing an invalid Retry token, it SHOULD immediately close the connection with INVALID_TOKEN.

RFC 9000 §17.2.5: a client MUST NOT accept more than one Retry for the same connection attempt (an attacker can use unlimited Retries for amplification/delay); a Retry arriving after the client has received the server's Initial MUST be discarded.

Core pattern in one sentence: **Retry turns "prove you received my challenge" into a stateless, verifiable token — but the integrity-tag key is public and the token is client-replayable, so all security weight rests on three switches: verify tag, limit count, limit lifetime. Miss one switch and you have a pre-handshake DoS backdoor.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| RT-1 | Tamper with the Retry packet's DCID/token, append any recomputed 16-byte tail (or flip any tag bit), and send it to the client | Client accepts the Retry → integrity tag not verified → violation |
| RT-2 | Attempt to inject two Retries in a row for the same connection (the second carrying the first's token) | Client accepts the second / enters a loop → violates the §17.2.5 single-Retry constraint |
| RT-3 | Inject a delayed Retry after the client has received the server's Initial/Handshake | Client accepts → violates the late-arrival discard constraint |
| RT-4 | Replay the same token across connections (token obtained in connection A used to open connection B) and observe the server | Accepted, skipping address validation → violates the MUST anti-replay; combined with source-address spoofing it becomes an amplifier |
| RT-5 | Echo an expired/address-mismatched token (if token contents can be injected and observed) | Accepted → token not bound to source address/timestamp |

Method: aioquic acting as a malicious client/MITM injecting Retries; token replay needs dual connections from the same IP; timing control via raw UDP injection.

## 3. Attack-Surface Hypotheses

- **Pre-handshake amplification/delay DoS**: RT-2/RT-3 — unlimited Retry loops force the client to repeatedly recompute Initial keys (each Retry changes DCID, requiring re-derivation), CPU amplification
- **Address-validation bypass → reflection amplification**: RT-4 — token replay + source-address spoofing makes the server treat an unvalidated address as validated, lifting the 3× anti-amplification limit
- **Downgrade chaining**: forged Retries interacting with version negotiation/migration can serve as a trigger for QUIC-LEAK-class pre-handshake memory consumption

## 4. Related Historical CVEs / Evidence

| Evidence | Implementation | Root cause |
|---|---|---|
| warpsock changelog fix record | warpsock | Explicitly added "RFC 9000 §17.2.5.1/§17.2.5.2 loop guards (one accepted Retry per attempt, late Retry discard once an Initial or Handshake is opened)" with dedicated regression tests — showing multi-Retry and late-Retry are real implementation pitfalls |
| CVE-2025-54939 (corroborating path) | lsquic | The pre-handshake path (Initial/Retry handling) is unauthenticated and historically error-prone in memory management — RT-1~RT-5 of this Skill all land on that path |
| No standalone CVE for Retry yet | — | The public tag key in RFC 9001 §5.8 is by design (tamper protection only, no forgery protection); implementations generally verify the tag but coverage of the count/lifetime/anti-replay switches varies — blind-spot clause |

## 5. Differential Verification

Control group: quic-go ≥ 0.60, msquic, warpsock (version with loop guards).
Comparison fields: RT-1 tag verification, RT-2 single-Retry enforcement, RT-3 late-arrival discard, RT-4 cross-connection replay rejection.
False-positive exclusion: an implementation choosing "accept no Retry at all" (disable_retry) is compliant; flag only "verifies tag but unlimited count", "accepts late Retry", "replay accepted".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (Retry/Initial interaction-sequence fuzz), `slowhttptest-dos` (pre-handshake resource-consumption cadence)
- Tool layer (with what): aioquic (Retry injection), raw UDP timing scripts
- Post-hit actions: if RT-4 holds → assess the reflection amplification ratio (send ceiling after address-validation bypass); if RT-2 holds → quantify the per-connection CPU amplification factor

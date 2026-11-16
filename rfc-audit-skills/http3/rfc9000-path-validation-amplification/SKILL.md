---
name: rfc9000-path-validation-amplification
description: Audit QUIC implementations' enforcement of path validation and anti-amplification limits per RFC 9000 §8.1/§8.2.1/§9 — missing PATH_CHALLENGE/PATH_RESPONSE obligations or unenforced anti-amplification limits become an unauthenticated DoS amplification primitive (related CVE-2023-49295 quic-go, HIGH)
zh-signals: 审计 QUIC 实现对路径验证与反放大限制的强制执行是否按 RFC 9000 §8.1/§8.2.1/§9——PATH_CHALLENGE/PATH_RESPONSE 义务缺失或反放大限制未强制即未认证 DoS 放大原语（关联 CVE-2023-49295 quic-go，HIGH）
rfc: RFC 9000 §8.1（地址验证与反放大）/ §8.2.1（PATH_CHALLENGE/PATH_RESPONSE）/ §9（NAT 重绑定）
license: Apache-2.0
---

# RFC 9000 §8 Path Validation and Anti-Amplification Limit Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §8.1: before **completing address validation**, a server must not send more bytes than **3 times** the bytes received from that address (anti-amplification limit). No implementation may break this ceiling on the grounds of "expecting to respond".

RFC 9000 §8.2.1: an endpoint **must** send a PATH_CHALLENGE on a new path and wait for the corresponding PATH_RESPONSE before treating the path as validated; the PATH_RESPONSE payload must echo the corresponding PATH_CHALLENGE data byte for byte.

RFC 9000 §9: NAT rebinding (abrupt peer address-port change) triggers the path-validation flow; unlimited sending on the new path is forbidden until validation completes.

Core pattern in one sentence: **the anti-amplification limit and path validation are the two mandatory gates QUIC raises against "small-beats-big" DoS — the gates themselves are protocol obligations, not optional optimizations; any implementation missing either lets an attacker pry open the peer's downstream bandwidth and memory with minimal uplink traffic.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| PV-1 | As a client from an unvalidated address, observe whether the server's cumulative bytes sent before completing address validation stay strictly ≤ 3× bytes received | Sending beyond the limit → anti-amplification violation (usable as a UDP amplifier) |
| PV-2 | Flood PATH_CHALLENGEs (spoofed source addresses, high concurrency); observe whether the peer maintains pending-response state per challenge | State accumulates without a cap → memory-exhaustion surface (CVE-2023-49295 pattern) |
| PV-3 | Send PATH_RESPONSEs while suppressing/dropping the peer's PATH_CHALLENGEs (or vice versa); observe whether the peer's path-validation state machine waits forever or misjudges validation success | Obligation asymmetry → availability destruction |
| PV-4 | Simulate NAT-rebinding timing: start sending high-volume traffic immediately after the abrupt new-address change; observe whether the peer accepts it before validation completes | Accepted without validation → source-address trust-hijacking surface |
| PV-5 | Tamper with the PATH_RESPONSE payload (not echoing the original challenge data) | Accepted → validation is a formality |

Method: aioquic spoofed-source-address scenario scripts; quic-go debug counters to observe the anti-amplification window; multi-connection stress to watch the challenge state-table growth.

## 3. Attack-Surface Hypotheses

- **UDP reflection amplification**: PV-1 — turning a QUIC-supporting server into a reflection amplifier (3x is the protocol's hard ceiling; an implementation breaking it becomes an amplifier)
- **Unauthenticated memory exhaustion**: PV-2 — a single attacker forces the peer to build state for massive numbers of forged challenges with minimal traffic; 1:N resource asymmetry
- **Targeted connection-availability destruction**: PV-3/PV-4 — suppressing validation responses keeps legitimate connections stuck in the validating state forever, or hijacks the rebinding window to take over connection routing

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2023-49295** (HIGH) | quic-go < 0.37.7 / 0.38.2 / 0.39.4 | The attacker floods PATH_CHALLENGEs while suppressing the congestion window so PATH_RESPONSE sends fail; quic-go keeps allocating state per challenge until memory exhaustion — a live instance of the PV-2 + PV-3 obligation asymmetry |
| **CVE-2024-22189** (corroborating pattern) | Multiple QUIC-ecosystem implementations | NEW_CONNECTION_ID flooding + RETIRE suppression — the same "request-obligation/response-obligation asymmetry" structure as PV-2 |

## 5. Differential Verification

Control group: quic-go ≥ 0.39.4 (patched), msquic, ngtcp2.
Comparison fields: PV-1 byte-count hard ceiling, PV-2 challenge state-table cap and eviction policy, PV-3 wait-timeout, PV-5 echo validation.
False-positive exclusion: an implementation choosing "strict 3x hard limit + fixed-length state table until validation completes" is compliant; only flag "sending beyond limit", "unbounded state", and "non-echo responses accepted".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (slow obligation-suppression mode: suppressing PATH_RESPONSEs), `fuzzowski-network-fuzz` (path-validation frame-timing fuzzing)
- Tool layer (what to attack with): aioquic (spoofed addresses + frame-level timing), multi-source concurrent stress scripts
- Post-hit actions: measure the amplification ratio (uplink:downlink, attack traffic:target memory) → confirm as a reflection amplifier or memory-exhaustion primitive → assess the exposure surface in combination with CDN/QUIC front ends

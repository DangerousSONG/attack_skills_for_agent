---
name: rfc9000-migration-congestion-window
description: Audit whether QUIC implementations violate the RFC 9000 §8.1 anti-amplification 3x limit and §9.4 pre-validation rate-limiting obligations during connection migration / NAT rebinding — sending at full speed to an unvalidated address opens a UDP reflection-amplification and traffic-hijacking attack surface (related CVE-2026-35191 OpenSSL QUIC non-validating-mode accounting error violating 3x; TMA 2025: 20% of IPv4 servers violate the amplification limit; HAProxy#3329 disable_active_migration over-interpretation empirical finding)
zh-signals: 审计 QUIC 实现在连接迁移/NAT 重绑定时是否违反 RFC 9000 §8.1 反放大 3 倍限制与 §9.4 路径验证前限速义务——未验证新地址即全速发送即 UDP 反射放大与流量劫持攻击面（关联 CVE-2026-35191 OpenSSL QUIC 非验证模式记账错误违反 3x；TMA 2025：20% IPv4 服务器违反放大限制；HAProxy#3329 disable_active_migration 过度解释实证）
rfc: RFC 9000 §8.1 / §9.2 / §9.4（连接迁移与拥塞控制恢复）/ §18.2（disable_active_migration 语义）
license: Apache-2.0
---

# RFC 9000 §9.4 Connection-Migration Congestion Control and Anti-Amplification Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §8.1 (verbatim):
> an endpoint MUST limit the amount of data it sends to the unvalidated address to three times the amount of data received from that address.

RFC 9000 §18.2 (key points, disable_active_migration transport parameter):
> even when a server sets disable_active_migration, it can still respond to packets from a new peer address. This parameter only forbids actively initiating migration; it does not exempt the endpoint from the obligation to respond to new addresses.

RFC 9000 §9.2 / §9.4 (key points):
- A new path MUST be validated via PATH_CHALLENGE / PATH_RESPONSE before it is considered usable;
- §9.4: the congestion-control window MUST stay conservative (initial-window level) until path validation completes; only after validation may the old path's congestion state be restored — **congestion-window restoration is a reward after validation, not the default**;
- Only "the non-probing frame with the largest packet number" may trigger address-change handling (probing frames: PATH_CHALLENGE/PATH_RESPONSE/PADDING/NEW_CONNECTION_ID).

Core pattern in one sentence: **connection migration hands the "where to send" decision to the peer's packets — sending at full speed to an unvalidated address turns the server into an amplifier for any claimed address; restoring the congestion window to its old value before validation renders the 3x gate toothless.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| MI-1 | After completing the handshake, send a single packet (containing a non-probing frame) from a spoofed source address; measure the total bytes the server sends back | Response > 3× received → violates §8.1 (TMA 2025 measured 20% of IPv4 servers violating) |
| MI-2 | Datagrams carrying multiple QUIC packets (smuggled Initial): observe the amplification-accounting caliber | Accounting by whole-datagram length instead of per-packet occupancy → inflated accounting violates the 3x (same class as CVE-2026-35191) |
| MI-3 | After NAT rebinding (source-port change), detect whether the server keeps sending STREAM data before PATH_CHALLENGE validation | Sending non-ACK/CRYPTO data without validation → violates §9.2/§9.4 |
| MI-4 | Initiate passive migration against a target with disable_active_migration set | Server completely ignores packets from the new address and the connection stalls → violates the §18.2 response obligation (HAProxy#3329 empirical); the opposite direction: accepting migration without path validation → amplification vulnerability |
| MI-5 | Detect the pre-validation congestion window: measure the server's send-rate slope on the new path | Rate quickly climbs to the old path's cwnd level without validation → §9.4 violation |

Method: dual-address client (aioquic custom + source-spoofing UDP socket); control-group rate curves + packet-capture amplification-ratio statistics.

## 3. Attack-Surface Hypotheses

- **UDP reflection amplification**: MI-1/MI-2 — after the handshake completes, a spoofed address makes the server send at full speed to the victim; 3x-accounting errors inflate the amplification factor (OpenSSL QUIC non-validating mode empirical)
- **Traffic hijacking / redirection**: an on-path attacker who changes the source address first and arrives → the server routes the stream to the attacker's address (a risk explicitly noted by the RFC design)
- **DoS resource consumption**: the PATH_CHALLENGE state table is flooded by massive forged migrations (path validation itself is double-edged as an attack surface; an IETF QUIC WG protocol-level weakness has been disclosed)

## 4. Related Historical CVEs

| CVE / Empirical Finding | Implementation | Root Cause |
|---|---|---|
| **CVE-2026-35191** | OpenSSL QUIC (non-validating mode) | When handling datagrams containing multiple QUIC packets, the whole datagram length is counted into the unvalidated address's amplification quota, violating the 3x limit (disclosed by Tenable 2026-09; Linux distributions unpatched) |
| **TMA 2025 (Buchet/Pelsser, UCLouvain)** | 450K+ IPv4 measured | Two classes of amplification attacks (handshake and migration): 20% of IPv4 servers violate the amplification limit; most migration-capable servers enforce path validation, but some reply with data directly |
| **HAProxy#3329** (2026-04, quic-interop-runner empirical) | HAProxy QUIC | After setting disable_active_migration, address-change handling stops entirely and NAT rebinding drops the connection — parameter semantics over-interpreted, the §18.2 obligation swallowed |
| IETF QUIC WG disclosure (2023-12, seemann.io) | quic-go / quiche / quicly all affected | PATH_CHALLENGE/PATH_RESPONSE validation state can be induced into unbounded memory consumption — protocol-level weakness (fixed on the implementation side; check against it during audits) |

## 5. Differential Verification

Control group: latest quic-go (strict 3x + conservative cwnd pre-validation), OpenSSL QUIC with validating mode enabled.
Comparison fields: MI-1 amplification ratio, MI-3 pre-validation data frames, MI-5 rate slope, MI-4 bidirectional behavior (neither ignore nor blindly trust).
False-positive exclusion: a server sending only ACK/CRYPTO during PATH_CHALLENGE is doing compliant probing responses, not counted as a violation; scenarios where a load balancer forwards by CID and ignores source addresses are marked "migration terminated at the LB" and the audit target becomes the LB.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (low-rate migration-deception amplification), `fuzzowski-network-fuzz` (multi-packet datagram / source-address combination fuzzing)
- Tool layer (what to attack with): aioquic (custom PATH_CHALLENGE timing), source-spoofing UDP socket, quic-interop-runner (NAT rebinding scenarios)
- Post-hit actions: quantify the amplification ratio (>3x is violation evidence) → assess reflection-DoS feasibility (spoofed source + large response streams) → minimize the MI-2 accounting path separately

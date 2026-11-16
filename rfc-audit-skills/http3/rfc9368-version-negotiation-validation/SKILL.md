---
name: rfc9368-version-negotiation-validation
description: Audit whether QUIC implementations handle version negotiation and downgrade protection per RFC 8999 §6 and RFC 9368 §4 — Version Negotiation packet invariants and the full set of Version Information validation MUSTs; their absence is a version-downgrade and parse-crash attack surface (evidence: QUIC-FUZZ xquic VN-event crash; CVE-2024-45396 Quicly same-family pattern)
zh-signals: 审计 QUIC 实现对版本协商与降级防护是否按 RFC 8999 §6 与 RFC 9368 §4——Version Negotiation 包不变量、Version Information 校验全套 MUST 缺失即版本降级与解析崩溃攻击面（实证：QUIC-FUZZ xquic VN 事件崩溃；CVE-2024-45396 Quicly 同类模式）
rfc: RFC 8999 §6（Version Negotiation 包不变量）/ RFC 9368 §4（Version Downgrade Prevention）/ RFC 9369 §3（v2 义务）
license: Apache-2.0
---

# RFC 9368 §4 Version Negotiation & Downgrade-Protection Audit

## 1. Normative Clauses (Original Sources)

RFC 8999 §6 (original text, key points):
> Packets with a short header do not trigger version negotiation. (Short headers do not trigger VN.)
> An endpoint MUST ignore a packet that contains no Supported Version fields or contains a truncated Supported Version value. (Empty/truncated version lists must be ignored.)
> An endpoint MUST include the value from the Source Connection ID field of the packet it receives in the Destination Connection ID field. (CID echo obligation.)
> Version Negotiation packets do not use integrity or confidentiality protection. (VN packets have no integrity protection — downgrade defense rests entirely on endpoint validation.)

RFC 9368 §4 (original text, key points):
> Clients MUST ignore any received Version Negotiation packets that contain the Original Version. (VN packets containing the original version must be ignored.)
> Both endpoints MUST parse their peer's Version Information during the handshake... [on parse failure] the endpoint MUST close the connection; if the connection was using QUIC version 1, that connection closure MUST use a transport error of type TRANSPORT_PARAMETER_ERROR. (Version Information parse failure must close the connection.)
> If an endpoint receives a Chosen Version equal to zero, or any Available Version equal to zero, it MUST treat it as a parsing failure. (Zero version numbers are parse failures.)
> If a server receives Version Information where the Chosen Version is not included in Available Versions, it MUST treat it as a parsing failure.
> When the server then processes the client's Version Information, the server MUST validate that the client's Chosen Version matches the version in use for the connection. If the two differ, the server MUST close the connection with a version negotiation error.
> Clients MUST NOT complete the handshake if they are reacting to a Version Negotiation packet and the server's Version Information is missing... MUST close the connection with a version negotiation error.
> If a client has reacted to a Version Negotiation packet, the client MUST validate the server's Available Versions field... If the client would have selected a different version, the client MUST close the connection with a version negotiation error.
> Clients MUST validate that the server's Chosen Version is equal to the Negotiated Version; if they do not match, the client MUST close the connection with a version negotiation error.

RFC 9369 §3: endpoints supporting QUIC v2 MUST send, process, and validate the version_information transport parameter.

Core pattern in one sentence: **VN packets are plaintext with no integrity protection — the entire weight of downgrade defense rests on a string of MUST validations on the endpoint side; these validations are typical "safety-guardrail" code that doesn't break immediately when missing, but silently downgrades the connection or crashes it when attacked.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| VN-1 | Server responds to a **short-header** packet with a Version Negotiation packet | Sending VN → violates the invariant (short headers do not trigger) |
| VN-2 | Inject a VN packet containing the client's Original Version into the client (MITM/out-of-order replay) | Client switches version and reconnects per the VN → violates MUST-ignore |
| VN-3 | Craft malformed Version Information transport-parameter values (too short / not a multiple of 4 bytes / Chosen Version or any Available Version equal to 0 / server-side Chosen not in Available) | Peer fails to close the connection (and, under v1, fails to use TRANSPORT_PARAMETER_ERROR) → violation |
| VN-4 | After the client responded to a VN, the server's Version Information is missing / Available Versions empty / the client would have selected a different version per its selection algorithm | Client completes the handshake → violation |
| VN-5 | Server Chosen Version inconsistent with the long-header negotiated-version field (compatible-negotiation path) | Client fails to close with a version-negotiation error → violation |
| VN-6 | Send the server an Initial with an **unsupported version number** (the legitimate VN-triggering path); observe the CID echo and version-list integrity of the server's VN response | CID not echoed / empty list / truncated list processed anyway → violation; server parse-event-handling crash (xquic evidence) → crash surface |

Method: aioquic with custom version numbers + raw UDP injection of VN packets; quic-go debug logs to observe version-negotiation events.

## 3. Attack-Surface Hypotheses

- **Version downgrade**: VN-2/VN-4 — downgrade the connection to an older or draft version with weaker protections (draft versions differ widely in key derivation and handshake validation), an entry point for cross-version attacks
- **Unauthenticated parse crash**: VN-6 — version-negotiation events sit on the unauthenticated pre-handshake path; QUIC-FUZZ has evidenced a NULL-pointer dereference crash in xquic's VN-event logging
- **Transport-parameter parse pollution**: VN-3 — Version Information coexists with transport parameters in the same parse path; malformed values become a fuzz entry into the transport-parameter parser

## 4. Related Historical CVEs / Evidence

| Evidence | Implementation | Root cause |
|---|---|---|
| QUIC-FUZZ (arXiv:2503.19402) measured vulnerability | xquic | Sending an Initial with a wrong version triggers a Version Negotiation event; the logging function receives a NULL network-path pointer → server crash DoS. Version-negotiation event handling is an unauthenticated attack surface — the empirical basis of VN-6 in this Skill |
| QUIC-FUZZ measured vulnerability | Quicly | Pre-handshake-path assertion-failure crash (CVE-2024-45396) — the same-family "unauthenticated pre-handshake path" pattern |
| No standalone CVE for VN validation yet | — | RFC 9368 was only standardized in 2023; mainstream implementations mostly sit at "support v1 + skip validation", and the full MUST set is almost completely unimplemented — a typical blind-spot clause |

## 5. Differential Verification

Control group: quic-go ≥ 0.60, msquic, xquic ≥ fixed version.
Comparison fields: response behavior for VN-1~VN-6 individually; specifically compare "does it really re-select a version after receiving a VN" vs "is Version Information validation complete".
False-positive exclusion: an implementation supporting only v1 and adopting an "ignore and continue" policy toward VN (equivalent to the strictest form of MUST-ignore) is compliant; flag only "switches version per VN but validation missing" and "parse failure without close".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (transport-parameter/VN packet fuzz), `grammarinator-gen-fuzz` (Version Information grammar generation)
- Tool layer (with what): aioquic (custom versions + raw UDP injection), hand-written VN-packet construction scripts
- Post-hit actions: confirm downgrade feasibility → assess known weaknesses of the target version (draft/v2) → confirm crash path → minimize an unauthenticated crash reproduction sequence

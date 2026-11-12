---
name: protocol-reverse
description: "Authorized reverse engineering of custom binary protocols, Protobuf/gRPC schemas, WebSocket frames, and PCAP-driven protocol recovery."
zh-signals: "对自定义二进制协议、Protobuf/gRPC、WebSocket 帧与 PCAP 流量进行协议逆向还原。信号:协议逆向,二进制协议,Protobuf,gRPC,WebSocket,PCAP"
when-to-use: "Use when documenting an undocumented wire protocol from captures or decoding structured traffic during an authorized analysis of custom TCP/UDP, Protobuf/gRPC, WebSocket, or MQTT protocols."
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# Protocol Reverse Engineering
## When to Use

- Documenting an undocumented wire protocol from captures.
- Decoding structured traffic during an authorized analysis.


## Applicable Scenarios

- Custom TCP/UDP binary protocols
- Protobuf / gRPC / FlatBuffers / MessagePack
- WebSocket / MQTT / private RPC
- Recovering fields and state machines from PCAP / PCAPNG
- Client-server validation checks, sequence numbers, encrypted frame headers

## Not Applicable to This Skill

| Situation | Where to go |
|------|------|
| HTTP parameter signing / JS encryption only | `js-reverse/` |
| TLS certificate issues only | `pentest-tools/` or a browser proxy |
| Deep dive into a firmware protocol stack + emulation | `firmware-pentest/` first, then come back to this skill |

## Workflow

### Phase 1 — Collection and Triage

```text
□ Got the sample: PCAP / proxy export / client logs / binary
□ Mark the direction: C→S / S→C; is there a handshake, heartbeat, reconnect
□ Fixed header? Magic number? Length field? TLV? Fixed length?
□ Is it compressed (zlib/gzip/lz4) or encrypted (AES/ChaCha in-frame)
□ tshark -r cap.pcap -T fields -e frame.number -e ip.src -e tcp.payload
```

### Phase 2 — Frame Layout Reconstruction

```text
□ Align multiple messages of the same kind, find invariant bytes / incrementing sequence numbers
□ Length field: big-endian/little-endian, with or without the header
□ Checksums: CRC16/32, checksum, HMAC position
□ Draw the state machine: Connect → Auth → Ready → Request/Response → Close
□ Tools: Wireshark custom dissector draft / ImHex / 010 Editor templates / Kaitai Struct
```

### Phase 3 — Serialization and Encryption

```text
□ Protobuf: .proto recovery (blackboxprotobuf / pbtk / protoc --decode_raw)
□ gRPC: HTTP/2 headers + protobuf body
□ Encryption: find key derivation (client so/dll/JS) → combine with ida-reverse / js-reverse / apk-reverse
□ Replay: only within the authorized scope; harmless fields first, then sensitive operations
```

### Phase 4 — Deliverables

```text
MUST deliver:
- Message type table (name / opcode / fields)
- At least 1 reproducible decode command or script
- Evidence: raw hex excerpts + decode results (desensitized)
```

## Toolchain

| Tool | Required | Purpose | Bootstrap |
|------|------|------|------|
| tshark / Wireshark | Strongly recommended | PCAP parsing | Manual / winget |
| Python3 | Yes | Decode scripts | System |
| blackboxprotobuf | Optional | Unknown protobuf | pip |
| ImHex / 010 | Optional | Structure templates | Manual |
| IDA / r2 / Ghidra | On demand | Client serialization functions | See the corresponding skill |

## References

- `references/protocol-workflow.md` — frame layout and Protobuf quick reference
- Related: `../ida-reverse/` `../js-reverse/` `../firmware-pentest/` `../pentest-tools/`

## Routing Context

**Upstream**: `MASTER-ROUTING` R21 · `routing.md`  
**Downstream**: needs client algorithms → `ida-reverse`/`js-reverse`; needs exploit replay → `pentest-tools`/`api-security`  
**Sibling**: `malware-analysis` (C2 protocols), `digital-forensics` (traffic forensics)

## Task Completion Self-Check

- [ ] Have you reconstructed the message layout or state machine (rather than just pasting hex)?
- [ ] Do you have a reproducible decode command?
- [ ] Have you respected the scope / desensitization requirements?
- [ ] Have you written back to the field-journal / report checklist?

## Limitations

- Encrypted or session-keyed protocols need key material first.
- Stateful protocols may require long, varied capture sessions.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).

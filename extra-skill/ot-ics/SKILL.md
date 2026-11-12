---
name: ot-ics
description: "Authorized OT/ICS security assessment: Purdue-model zoning review, PLC/SCADA exposure, industrial protocol discovery, and passive-first evaluation discipline."
zh-signals: "授权 OT/ICS 安全评估，覆盖 Purdue 模型分区审查、PLC/SCADA 暴露、工控协议发现与被动优先原则。信号:OT安全,ICS,SCADA,Purdue模型,工控协议"
when-to-use: >-
  Use for authorized OT/ICS security assessments — Purdue-model zoning review,
  PLC/SCADA exposure, and industrial protocol discovery with a passive-first approach.
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

> **Mandatory confirmation gate**
> Before running any command that probes, exploits, changes, persists on, extracts data from, or attempts credential access against a target:
> 1. Ask the user to state the exact target URL, IP, account, or resource.
> 2. Ask the user to confirm written authorization and the permitted scope.
> 3. Show the exact command(s) and explain their expected effect.
> 4. Wait for explicit confirmation in the current conversation.
>
> Without that confirmation, remain read-only and provide defensive guidance only. Prefer a sandbox, disposable VM, or controlled lab.

# OT / ICS Security
## When to Use

- Passive assessment of industrial networks within an approved scope.
- Documenting PLC/SCADA exposure and zoning violations.


## Applicable Scenarios

- OT/SCADA/DCS security assessment (authorized)
- Purdue model zoning and cross-zone conduits
- Protocol exposure for Modbus/DNP3/S7/EtherNet-IP and similar protocols
- Engineering stations, HMIs, historian databases, jump hosts
- IT/OT convergence boundaries (firewall rules, one-way diode)

## Safety Rules (MUST)

```text
MUST NOT, unless explicitly permitted:
- Write coils/registers to PLCs
- High-rate scan production OT across the whole network
- Interrupt paths related to the Safety Instrumented System (SIS)
Prefer: read-only identification, traffic mirroring, offline firmware/configuration analysis
```

## Workflow

### Phase 1 — Zoning and Assets

```text
□ Purdue L0–L5 sketch: field devices → control → supervision → site DMZ → enterprise
□ Asset inventory: PLC/RTU/HMI/engineering station/historian/jump host
□ Protocol and port baseline (authorized network segments only)
```

### Phase 2 — Passive and Read-Only

```text
□ SPAN/mirrored PCAP → protocol-reverse / Wireshark industrial dissectors
□ Offline audit of configurations and engineering files (TIA/RSLogix exports, etc.)
□ Record default credentials and cleartext protocols (Modbus has no authentication) as a Finding, do not write to disk or change values
```

### Phase 3 — Restricted Active (Authorized Only)

```text
□ Low-rate identification, within the maintenance window
□ Read-only function codes first
□ Evidence for every step; stop and report immediately on anomalies
```

### Phase 4 — Firmware/Patch Surface

```text
□ Controller firmware versions → CVE mapping (do not blindly flash firmware)
□ Coordinate with firmware-pentest for offline image analysis
```

## Toolchain

| Tool | Purpose | Notes |
|------|------|------|
| Wireshark industrial dissectors | Passive parsing | Mirrored traffic |
| Nmap NSE (restricted) | Identification | Rate and time window |
| Claroty/Nozomi and similar | Asset discovery | Commercial/on-site |
| PLC vendor engineering software | Configuration audit | Offline first |
| binwalk / Ghidra | Firmware | Offline |

## References

- `references/ot-safe-assessment.md`
- `../firmware-pentest/` `../protocol-reverse/` `../network` via pentest-tools

## Routing Context

**Upstream**: MASTER R28  
**Downstream**: firmware deep dive `firmware-pentest`; protocol `protocol-reverse`; IT lateral movement `windows-ad`/`attack-chain`  
**Peer level**: do not run generic web scans with default parameters against OT

## Task Completion Self-Check

- [ ] Did you default to passive/read-only and record the authorization boundary?
- [ ] Did you avoid write operations on control loops (unless explicitly permitted)?
- [ ] Do the findings describe physical/process impact?
- [ ] Checklist / journal?

## Limitations

- Active scanning can crash PLCs; default to passive capture.
- Specialized protocols need vendor documentation rarely available publicly.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).

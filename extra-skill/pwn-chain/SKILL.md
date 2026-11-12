---
name: pwn-chain
description: "Go from reverse engineering to a working exploit: stack/heap/kernel pwn workflows with pwntools, libc-database, ROP, and stabilization from CTF to authorized remote targets."
zh-signals: "从逆向到可用 exploit，覆盖栈/堆/内核 pwn 工作流、pwntools、ROP 与远程稳定化。信号:pwn,栈溢出,堆利用,内核提权,ROP,pwntools"
when-to-use: "Use when a binary vulnerability is already understood and needs a reliable exploit, when porting a CTF exploit to an authorized target, or when exploiting a Linux kernel ioctl bug for privilege escalation."
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

- A binary vulnerability is understood and needs a reliable exploit.
- Porting a CTF-style exploit to an authorized real-world target.

## Scope of Applicability

Use this skill when the task falls into the following scenarios:

1. **Got the binary + a known vulnerability point** — static analysis/audit/fuzzing has already located an overflow/UAF/double free, and you need to go from triggering it to getting a shell
2. **The CTF challenge works locally but fails remotely** — differences in the remote environment break the script, so it needs stabilization
3. **Binary exploitation against a real target** — in SRC / red team scenarios, a memory corruption vulnerability has already been identified and RCE must be constructed
4. **Linux kernel driver ioctl bug** — triggered from user space, with the goal of escalating to root

**Prerequisite**: you already know "where it blows up". This skill is not responsible for finding vulnerabilities (that is fuzzing / auditing), only for "writing an exploit from the vulnerability point".

### Division of Labor with Other Skills

| Scenario | What to Use |
|------|--------|
| Identify a custom VM / anti-debug / complex obfuscation | `reverse-engineering/` |
| Open a binary from scratch for static analysis | `ida-reverse/` or `radare2/` |
| **Have a vulnerability point, write an exploit to reach the remote target** | **This skill** |
| Integrate the shell obtained through pwn into a complete attack chain | `attack-chain/` (downstream) |

`reverse-engineering/` focuses on "understanding what the program does" (pattern recognition, protocol restoration, working out the weird mechanisms in CTF challenges); this skill focuses on "turning an already understood vulnerability into an executable attack". The two are often used together, but their division of labor is clear.

## Core Workflow

```text
Step 1: Confirm the vulnerability type + the mitigation mechanisms
   ├─ checksec ./vuln (NX / Canary / PIE / RELRO / Fortify)
   ├─ file ./vuln  + readelf -d ./vuln
   ├─ Vulnerability class: stack overflow / format string / heap (UAF/DF/OF) / integer / race / kernel
   └─ → decide which references/ to use

Step 2: Choose the exploitation strategy
   ├─ NX off + no ASLR → direct shellcode
   ├─ NX on + libc provided → ret2libc / one_gadget
   ├─ NX on + no libc provided → leak first, then look it up in libc-database
   ├─ Heap → pick the technique matching the glibc version (tcache/fastbin/unsorted/large)
   └─ Kernel → commit_creds / modprobe_path / core_pattern

Step 3: Prepare libc + gadgets
   ├─ libc-database: ./find puts 0x6f0
   ├─ ROPgadget --binary ./libc.so.6 --only "pop|ret"
   ├─ one_gadget ./libc.so.6
   └─ Compute the base: leak_addr - libc.sym['puts']

Step 4: Write the pwntools template (local process)
   ├─ context.binary = ELF('./vuln')
   ├─ p = process('./vuln')  /  p = gdb.debug('./vuln','b *main+xx')
   ├─ payload = cyclic(N) + p64(ret) + ...
   └─ p.interactive()

Step 5: Get it working locally
   ├─ Repeatedly attach + inspect registers + tune the offset
   ├─ Use pwndbg/GEF's vmmap / heap / bins / telescope
   └─ Once it works, switch to remote()

Step 6: Stabilize for the remote target
   ├─ libc offset: use the leak to look it up in libc-database, never guess
   ├─ Stack alignment: 16-byte misalignment → movaps crashes → add a ret gadget
   ├─ Remote network latency → recvuntil with an exact anchor string, disable fuzzy sleeps
   ├─ Remote buffering: sendlineafter is more reliable than sendline
   ├─ Heap spray success rate: increase the spray count + keep padding chunks to prevent consolidation
   └─ Run repeatedly: wrap in while True and verify a success rate ≥ 95%
```

## Typical Scenarios

### Scenario 1: Remote 64-bit binary (NX+PIE+canary, libc provided)

```text
Available: ./vuln (64-bit ELF, NX, PIE, canary) + ./libc.so.6 + nc host port
Vulnerability: read(buf, 0x200) but buf is only 0x40 bytes → stack overflow
Mitigations: the canary blocks it, PIE randomizes .text

Strategy:
1. Leak the canary first (stack / format string / partial read)
2. Then leak a libc function address (puts@got)
3. Compute the libc base with libc.address = leaked - libc.sym['puts']
4. Run one_gadget ./libc.so.6 and pick a magic gadget whose constraints can be satisfied
5. payload = padding + canary + saved_rbp + (pop_rdi + bin_sh + system) or a direct one_gadget
6. Add a ret gadget to fix stack alignment (critical!)
```

For the full template see `references/stack-pwn.md`.

### Scenario 2: Linux kernel driver ioctl out-of-bounds write → root

```text
Available: vmlinux + bzImage + initramfs.cpio.gz + a custom vuln.ko
Vulnerability: controllable length in copy_from_user inside ioctl(0x1337, ptr) → kernel heap overflow (kmalloc-64 slab)
Mitigations: SMEP, SMAP, KASLR, KPTI

Strategy:
1. Modify the init script to get a root shell (CTF), or leak the KASLR base first and continue (real world)
2. Leak the kernel base through /proc/kallsyms (may be restricted) or via an uninitialized heap spray
3. Spray tty_struct / msg_msg / pipe_buffer objects into the kmalloc-64 slab
4. Overwrite the vtable pointer to point to user space → won't work (SMEP), switch to stack pivot + kernel ROP
5. ROP chain: prepare_kernel_cred(0) → commit_creds → swapgs+iretq → user-space execve("/bin/sh")
6. Or simpler: overwrite modprobe_path with "/tmp/x", write a /tmp/x, then trigger modprobe
```

For the full template see `references/kernel-pwn.md`.

## On-Demand Bootstrap

### Tool Dependencies

| Tool | Purpose | Installation |
|------|------|---------|
| pwntools | Exploit development framework | `pip install pwntools` |
| GEF | gdb enhancement (recommended for kernel + user space) | `git clone https://github.com/bata24/gef` (actively maintained fork) |
| pwndbg | gdb enhancement (best heap debugging experience) | `git clone https://github.com/pwndbg/pwndbg && ./setup.sh` |
| ROPgadget | Gadget search | `pip install ropgadget` |
| Ropper | Gadget search (alternative, supports many architectures) | `pip install ropper` |
| one_gadget | libc magic gadget finder | `gem install one_gadget` (requires ruby) |
| libc-database | libc fingerprint lookup | `git clone https://github.com/niklasb/libc-database && ./get` |
| qemu-system-x86_64 | Kernel challenge debugging | `apt install qemu-system-x86` |
| binwalk / cpio | initramfs unpacking | `apt install binwalk cpio` |
| patchelf | Switching libc versions | `apt install patchelf` |

### Bootstrap Check Script

```bash
# One-shot check + install of the core tools
for t in pwntools ropgadget ropper; do
  pip show $t >/dev/null 2>&1 || pip install $t
done

command -v one_gadget >/dev/null || gem install one_gadget

[ -d ~/tools/libc-database ] || git clone https://github.com/niklasb/libc-database ~/tools/libc-database
[ -d ~/tools/libc-database/db ] || (cd ~/tools/libc-database && ./get ubuntu debian)

[ -d ~/tools/pwndbg ] || (git clone https://github.com/pwndbg/pwndbg ~/tools/pwndbg && cd ~/tools/pwndbg && ./setup.sh)
```

### After 2 Failed Automatic Install Attempts of the Same Tool

Stop retrying and output structured manual installation steps (pip mirror / gem mirror / git domestic mirror / apt mirror) for the user to confirm.

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Trigger condition**: a binary plus an identified vulnerability point, an exploit needs to be written

**Upstream skills (use them first, then come back to this skill)**:
- Still don't understand what the binary does → `reverse-engineering/`
- Need detailed static analysis → `ida-reverse/`
- Quick reconnaissance to confirm the architecture/mitigations → `radare2/`

**Downstream skills (after obtaining a shell)**:
- Integrate into a complete attack chain (lateral movement, privilege escalation, persistence) → `attack-chain/`

**Sub-module navigation**:
- Stack exploitation (ret2libc / ret2csu / one_gadget / stack alignment) → `references/stack-pwn.md`
- Heap exploitation (tcache / fastbin / unsorted / large bin / FILE struct) → `references/heap-pwn.md`
- Kernel pwn (kROP / SMEP-SMAP bypass / KASLR leak / modprobe_path) → `references/kernel-pwn.md`

## Notes

- **Do not stop at a working local exploit** — the local libc / ASLR / network environment all differ from the remote one, so you must run in remote mode at least 20 times in a row to verify stability
- **The libc version must be confirmed** — use a leak + libc-database lookup, do not assume the Ubuntu 22.04 default libc
- **Stack alignment is a common 64-bit pitfall** — `movaps xmm0, [rsp]` faults when rsp is not 16-byte aligned; add an empty `ret` gadget to fix it
- **Heap exploitation is extremely sensitive to the glibc version** — tcache was introduced in 2.27, safe-linking in 2.32, hooks were removed in 2.34, and each version has a different exploitation path
- **Kernel pwn requires checking the CPU flags first** — whether the qemu boot arguments include +smep +smap +pku directly determines how the ROP chain is written
- **One KASLR leak is enough** — once you have a kernel address all other addresses are offsets, do not leak repeatedly

## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?

## Limitations

- Exploit development only on systems you are authorized to attack.
- Mitigations (full RELRO, CFI, MTE) raise difficulty substantially.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).

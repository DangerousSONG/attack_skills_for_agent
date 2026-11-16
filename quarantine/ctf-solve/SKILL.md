---
name: ctf-solve
description: "CTF general-purpose solve orchestrator. Use when facing a CTF challenge of unknown type and you need to automatically analyze the challenge type and select the correct solving path. It automatically dispatches the matching specialized skill (pwn/crypto/web/reverse/forensics/osint/malware/misc), which suits scenarios where you are given challenge files or a service endpoint but cannot tell which category it belongs to"
zh-signals: "CTF 综合解题编排，先分类挑战再调度 pwn/crypto/web/reverse/forensics/osint/malware/misc 专项技能。信号:CTF,解题编排,挑战分类,多类型挑战"
when-to-use: >-
  Use when facing an unknown-type CTF challenge, given challenge files or a service
  endpoint but unsure which category it belongs to, and you need to classify it and
  dispatch the right specialized skill.
metadata:
  tags: "ctf,solve,orchestration,orchestrator,challenge,solving"
  category: "ctf"
---

# CTF General-Purpose Solve Orchestrator

## Phase 1: Solving Workflow

### 1.1 Reconnaissance

```bash
file *                          # Identify file types
strings binary | grep -i flag   # Quick string search
xxd binary | head -20           # Hex header
binwalk -e firmware.bin         # Extract embedded files
checksec --file=binary          # Check protections
nc host port                    # Connect to a remote service
```

### 1.2 Classification and Skill Dispatch

**By file type:**

| File type | Category | Dispatch Skill |
|----------|------|-----------|
| .pcap/.evtx/.raw/.dd | Forensics | ctf-forensics |
| ELF/PE + remote service | Pwn | ctf-pwn |
| ELF/PE/APK/.pyc/WASM | Reverse | ctf-reverse |
| .py/.sage + numbers | Cryptography | ctf-crypto |
| Web URL/HTML/JS/PHP | Web | ctf-web-methodology |
| Image/audio/PDF (no obvious content) | Steganography forensics | ctf-forensics |

**By keyword:**

| Keyword | Category |
|--------|------|
| overflow/ROP/shellcode/heap | ctf-pwn |
| RSA/AES/cipher/lattice/LWE | ctf-crypto |
| XSS/SQLi/JWT/SSRF | ctf-web-methodology |
| disk image/memory dump/registry | ctf-forensics |
| find/locate/identify/who/where | ctf-osint |
| obfuscated/C2/malware/beacon | ctf-malware |
| jail/sandbox/encoding/game | ctf-misc |

### 1.3 Pivot When Stuck

1. **Reclassify** — many challenges span categories (Web+Crypto, Forensics+Crypto, Reverse+Pwn)
2. **Check for missed items** — hidden files, backup ports, response headers, comments, metadata
3. **Simplify** — check whether a simpler path exists (default credentials, known CVEs, logic flaws)

**Common cross-category patterns:**
- Forensics + Cryptography: encrypted data inside PCAP/disk images
- Web + Reverse: WASM or obfuscated JS
- Web + Cryptography: JWT forgery, custom signatures
- Reverse + Pwn: reverse first, then exploit
- OSINT + Steganography: social media Unicode homoglyphs

## Phase 2: Supporting Information

### 2.1 Flag Format

Common: `flag{...}` / `CTF{...}` / custom prefixes (`ENO{...}` / `HTB{...}`)

```bash
grep -rniE '(flag|ctf|eno|htb|pico)\{' .
strings output.bin | grep -iE '\{.*\}'
```

### 2.2 Strategy When Stuck
- Fall back to reconnaissance: robots.txt, .git, backup files, directory scanning

### 2.3 File Type Identification
- SQLite database file: open it with the sqlite3 command and use .tables to query the schema

---
name: coding-mastery
description: Use when writing security tooling, exploits, scanners, or C2 in Python/C/Go/Rust/ASM — systems & network programming, automation, cryptography implementation
when-to-use: Use when writing security tooling, exploits, scanners, or C2 in Python/C/Go/Rust/ASM — systems & network programming, automation, cryptography implementation
metadata:
  type: utility
  phase: any
kill_chain:
  phase: [weaponize]
  step: [2]
  attck_tactics: [TA0042]
depends_on: []
feeds_into: [exploit-development, shellcode-dev, edr-evasion]
inputs: [tool_requirements]
outputs: [custom_tooling, exploit_code]
---

# Coding Mastery

## When to Activate

- Writing exploit code, PoCs, or security tools
- Developing automation scripts for pentesting workflows
- Implementing network protocols or custom C2
- Building security analysis tools
- Cryptographic implementation or analysis
- Performance-critical systems programming

## Languages & Use Cases

### Python (Primary — Offensive Tooling)
```python
# Exploit development with pwntools
from pwn import *
context(arch='amd64', os='linux')

# Network programming
import socket, ssl, struct
import asyncio, aiohttp  # async operations

# Web exploitation
import requests, urllib3
from bs4 import BeautifulSoup

# Crypto
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
import hashlib, hmac

# Binary analysis
import struct, ctypes
from capstone import *  # disassembly
from unicorn import *   # emulation
from keystone import *  # assembly
```

### C/C++ (Systems & Exploit Dev)
```c
// Shellcode development
// Position-independent code, null-free
// Syscall-based (avoid libc dependency)

// Kernel module development
#include <linux/module.h>
#include <linux/kernel.h>

// Windows API abuse
#include <windows.h>
#include <winternl.h>
// Direct syscalls, NTAPI

// Memory manipulation
// Custom allocators, heap spray, ROP gadget finders
```

### Go (Offensive Tooling & C2)
```go
// Implant development (cross-compile, static binary)
// C2 communication (HTTP/DNS/named pipes)
// Network scanning and enumeration
// Proxy/tunnel tools (chisel-like)

// Advantages: single binary, cross-platform, fast, good crypto stdlib
```

### Rust (High-Performance Security Tools)
```rust
// Memory-safe exploit tooling
// High-performance scanners
// Custom protocol implementations
// Fuzzing harnesses
```

### PowerShell (Windows Post-Exploitation)
```powershell
# AMSI bypass, ETW patching
# In-memory execution (reflection)
# AD enumeration and exploitation
# Fileless malware techniques
```

### Assembly (x86/x64/ARM)
```nasm
; Shellcode
; ROP gadgets
; Anti-debugging
; Kernel exploitation
; Architecture-specific tricks
```

## Design Patterns for Security Tools

### Scanner Architecture
```python
import asyncio
from dataclasses import dataclass
from typing import AsyncIterator

@dataclass
class Finding:
    severity: str
    target: str
    vulnerability: str
    evidence: str

class Scanner:
    def __init__(self, targets: list[str], concurrency: int = 50):
        self.targets = targets
        self.semaphore = asyncio.Semaphore(concurrency)
    
    async def scan_target(self, target: str) -> list[Finding]:
        async with self.semaphore:
            # Implement scan logic
            pass
    
    async def run(self) -> AsyncIterator[Finding]:
        tasks = [self.scan_target(t) for t in self.targets]
        for coro in asyncio.as_completed(tasks):
            findings = await coro
            for f in findings:
                yield f
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

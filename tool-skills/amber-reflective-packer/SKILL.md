---
name: amber-reflective-packer
description: "Amber: uses reflective loading to evade disk scanning. Signals: process injection, dll injection, preserve PE header, static compilation"
zh-signals: "Amber: 反射加载规避磁盘扫描。信号:进程注入,dll注入,保留 PE 头,静态编译。"
when-to-use: >-
  Use when you need to convert a Windows PE into a reflective shellcode loader to
  evade static disk scanning; supports preserving the PE header and static
  compilation, though dynamic EDR detection still requires testing.
---

# Amber

- Attack Category: C22 Process Injection and In-Memory Execution
- Upstream Repository: https://github.com/EgeBalci/Amber
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/EgeBalci/Amber@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `amber payload.exe` | Reflectively pack into a shellcode loader |
| `-k` | Preserve the PE header |
| `-s` | Static compilation |
| `amber -l payload.bin` | Output shellcode only |

## Attack Scenario Playbook

### Reflective loading to evade disk scanning

```bash
amber agent.exe -o packed.exe
# The packed artifact reflectively loads the original PE from memory at runtime, making static detection hard
```

## Notes

Converts an exe into a reflective shellcode loader; the output still needs testing against the target EDR's dynamic detection.

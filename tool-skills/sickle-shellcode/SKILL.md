---
name: sickle-shellcode
description: "Sickle: shellcode analysis. Signals: reverse engineering, disassembly, bad characters, comparison."
zh-signals: "Sickle: shellcode 分析。信号:逆向,反汇编,坏字符,对比。"
when-to-use: >-
  Use when analyzing shellcode during reverse engineering: disassemble it,
  identify bad characters, and diff variants.
---

# Sickle

- Attack Category: C47 Reverse Engineering
- Upstream Repository: https://github.com/wetw0rk/Sickle
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/wetw0rk/Sickle && cd Sickle && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sickle -f shellcode.bin -m disassemble` | Shellcode disassembly |
| `-f bin -f badchars '\x00'` | Bad characters |
| `-m diff` | Comparison |

## Attack Scenario Playbook

### Shellcode analysis

```bash
sickle -f payload.bin -m disassemble
# Disassembly + bad character detection
```

## Notes

A shellcode analysis tool for disassembly and extraction.

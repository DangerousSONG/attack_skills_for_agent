---
name: shellnoob-shellcode
description: "shellnoob: fast assembly and shellcode conversion. Signals: payload development, weaponization, disassembly, format conversion, architecture."
zh-signals: "shellnoob: 汇编↔shellcode 快速互转。信号:载荷开发,武器化,反汇编,格式转换,架构。"
when-to-use: >-
  Use when developing or converting shellcode for CTF, teaching, or exploit
  development, especially to assemble or disassemble snippets and switch output
  formats and architectures.
---

# shellnoob

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/reyammer/shellnoob
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install shellnoob or git clone https://github.com/reyammer/shellnoob
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `shellnoob -c 'exec /bin/sh'` | Assembly ↔ shellcode conversion |
| `-i shellcode.txt` | Disassembly |
| `-f input.txt -o output` | Format conversion |
| `-32 / -64` | Architecture |

## Attack Scenario Playbook

### Fast Assembly ↔ Shellcode Conversion

```bash
shellnoob -c 'xor eax,eax; push 0x68732f2f; push 0x6e69622f; mov ebx,esp; ...'
# Handy for teaching/CTF shellcode work
```

## Notes

Long-standing teaching tool from the Python 2 era; for complex shellcode prefer nasm+objdump or pwntools.

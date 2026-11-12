---
name: armscgen-shellcode
description: "ARMSCGen: generates ARM/embedded shellcode. Signals: pwn, binary exploitation, reverse shell, list"
zh-signals: "ARMSCGen: ARM/嵌入式 shellcode。信号:pwn,二进制利用,反向 shell,列表。"
when-to-use: >-
  Use when exploiting ARM or embedded Linux targets and you need architecture-specific shellcode
  such as reverse shells or egghunters.
---

# ARMSCGen

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/alexpark07/ARMSCGen
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/alexpark07/ARMSCGen
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 ARMSCGen.py -f sc_flimsy` | ARM shellcode generation |
| `-f sc_reverse_tcp` | Reverse shell |
| `-l` | List |

## Attack Scenario Playbook

### ARM/Embedded Shellcode

```bash
python3 ARMSCGen.py -f sc_egghunter
# ARM architecture shellcode
```

## Notes

An ARM shellcode generator.

---
name: exe2hexbat-payload-transfer
description: "exe2hex: transfer binaries without file landing. Signals: reverse engineering, disassembly, C code format."
zh-signals: "exe2hex: 无文件落地传二进制。信号:逆向,反汇编,C 代码格式。"
when-to-use: >-
  Use when you need to transfer a Windows binary to a target without dropping a
  file, converting the executable into a self-decoding BAT/TXT or C/PowerShell
  script.
---

# exe2hex

- Attack Category: C47 Reverse Engineering Assistance
- Upstream Repository: https://github.com/g0tmi1k/exe2hex
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/g0tmi1k/exe2hex && cd exe2hex
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `bash exe2hex.sh -x /usr/share/windows-binaries/nc.exe -e nc.cmd` | exe→BAT/TXT transfer |
| `-b` | PowerShell/BAT hybrid |
| `-cc` | C code format |

## Attack Scenario Playbook

### Fileless binary transfer

```bash
bash exe2hex.sh -x procdump.exe -e dump.cmd
# Encode the exe into a cmd script that echoes it back together, bypassing allowlists
```

## Notes

By g0tmi1k; converts a binary into a BAT/PowerShell script that rebuilds it, ideal for payload delivery where uploads are blocked.

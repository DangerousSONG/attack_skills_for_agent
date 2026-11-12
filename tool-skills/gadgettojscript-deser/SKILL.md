---
name: gadgettojscript-deser
description: "GadgetToJScript builds Office macro deserialization payloads. Signals: payload development, weaponization, .NET serialized payloads, VBS output, obfuscation."
zh-signals: "GadgetToJScript: Office 宏反序列化。信号:载荷开发,武器化,.NET 序列化载荷,VBS 输出,混淆。"
when-to-use: >-
  Use when weaponizing .NET serialized payloads into Office macros or VBS/VBA
  scripts, optionally obfuscated, for authorized payload development.
---

# GadgetToJScript

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/med0x2e/GadgetToJScript
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/med0x2e/GadgetToJScript && cd GadgetToJScript && dotnet build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `GadgetToJScript.exe -b -c -e binary -w vba -o macro` | .NET serialized payload |
| `-e binary -w vbs` | VBS output |
| `-c` | Obfuscation |

## Attack Scenario Playbook

### Office macro deserialization

```bash
GadgetToJScript.exe -b -e shellcode -w vba -o invoice
# .NET deserialization executes inside the macro
```

## Notes

Embeds .NET serialized payloads in Office documents.

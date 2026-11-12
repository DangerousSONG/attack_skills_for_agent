---
name: evilclippy-macro-hide
description: "EvilClippy: macro document evasion. Signals: malware development, evasion development, GUI obfuscation, remove macro VBA project, inject URL into macro."
zh-signals: "EvilClippy: 宏文档免杀。信号:恶意软件开发,免杀开发,GUI 混淆,移除宏 VBA 项目,URL 注入宏。"
when-to-use: >-
  Use when weaponizing Office macro documents, to apply VBA stomping and GUI
  obfuscation that evades static AV and sandbox inspection.
---

# EvilClippy

- Attack Category: C45 AV Evasion and Payload Delivery
- Upstream Repository: https://github.com/outflanknl/EvilClippy
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/outflanknl/EvilClippy && build with mono/xbuild
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `EvilClippy.exe -s fakecode.vba macro.doc` | VBA code deception (analyzers see the wrong code) |
| `-g` | GUI obfuscation |
| `-r` | Remove the macro VBA project |
| `-u` | Inject a URL into the macro |
| `-st` | VBA stomping |

## Attack Scenario Playbook

### Macro Document AV Evasion

```bash
EvilClippy.exe -s benign.vba payload.docm
# Preview/sandbox sees the benign macro while the stomped p-code actually executes
```

## Notes

From Outflank, weaponizing Office macros: VBA stomping (separating source from p-code) plus GUI camouflage bypasses static AV detection in most products.

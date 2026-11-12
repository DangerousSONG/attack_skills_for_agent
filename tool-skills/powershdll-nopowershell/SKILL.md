---
name: powershdll-nopowershell
description: "Windows local privilege escalation scenario. Signals: Windows privilege escalation, UAC bypass, single command, registry mode."
zh-signals: "PowerShdll: Windows本地提权场景。信号:windows提权,uac绕过,单条命令,注册表模式。"
when-to-use: "Use when powershell.exe is blocked or PowerShell is locked in Constrained Language Mode on a Windows host and you need to run PowerShell scripts or cmdlets through rundll32 or regsvr32 for privilege escalation and AppLocker bypass."
---

# PowerShdll

- Attack Category: C17 Windows Local Privilege Escalation
- Upstream Repository: https://github.com/p3nt4/PowerShdll
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/p3nt4/PowerShdll && cd into the dll directory and call it directly with rundll32
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `rundll32 PowerShdll.dll,main -s <script.ps1>` | Run scripts without powershell.exe |
| `rundll32 PowerShdll.dll,main -c <cmdlet>` | Single command |
| `regsvr32 /s PowerShdll.dll` | Registry mode |
| `InstallUtil mode bypasses AppLocker` | Description |

## Attack Scenario Playbook

### Constrained Language Mode Bypass

```bash
rundll32 PowerShdll.dll,main -s enum.ps1
# Run PowerShell through rundll32 when powershell.exe is blocked or CLM is locked down
```

## Notes

Runs PowerShell through the rundll32/regsvr32 hosts, bypassing disabled powershell.exe, AppLocker and CLM restrictions.

---
name: seatbelt-host-survey
description: "Seatbelt: Enumerates Windows privilege escalation surface. Signals: Windows privilege escalation, UAC bypass, full host reconnaissance, by group, system groups."
zh-signals: "Seatbelt: Windows 提权面系统枚举。信号:windows提权,uac绕过,全量主机侦察,按组,系统组。"
when-to-use: >-
  Use after gaining a foothold on Windows when you need a comprehensive host
  survey to identify privilege escalation paths such as unquoted service paths,
  writable services, AlwaysInstallElevated, and UAC settings.
---

# Seatbelt

- Attack Category: C17 Windows Local Privilege Escalation
- Upstream Repository: https://github.com/GhostPack/Seatbelt
- Upstream License: BSD-3-Clause(GhostPack) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
release download Seatbelt.exe or dotnet build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `Seatbelt.exe` | Full host reconnaissance |
| `Seatbelt.exe -group=user` | By group |
| `-group=system` | System groups |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Systematic enumeration of the Windows privilege escalation surface

```bash
Seatbelt.exe -group=user -group=system
# Output: browser credentials / unquoted service paths / writable services / AlwaysInstallElevated / UAC configuration
```

## Notes

By GhostPack, 90+ checks; captures every privilege escalation lead at once, and the output directly guides the privesc path.

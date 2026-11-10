---
name: conducting-internal-reconnaissance-with-bloodhound-ce
description: "Use BloodHound CE with SharpHound (AD) and AzureHound (Entra ID) collectors for internal AD reconnaissance and attack-path mapping. Signals: BloodHound, SharpHound."
zh-signals: "用 BloodHound CE 图数据库 + SharpHound(AD)/AzureHound(Entra ID)采集器做内网 AD 侦察,把 AC信号:bloodhound,sharphound。"
when-to-use: Conduct internal Active Directory reconnaissance using BloodHound Community Edition's graph database with the SharpHound (AD) and AzureHound (Entra ID) collectors, mapping ACLs, sessions, and group me
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- reconnaissance
- bloodhound
- active-directory
- attack-paths
- privilege-escalation
- graph-analysis
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
- T1087.002
- T1069.002
- T1482
- T1018
---
# Conducting Internal Reconnaissance with BloodHound CE


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Overview

BloodHound Community Edition (CE) is a modern, web-based Active Directory reconnaissance platform developed by SpecterOps that uses graph theory to reveal hidden relationships and attack paths within AD environments. Unlike the legacy BloodHound application, BloodHound CE uses a PostgreSQL backend with a dedicated graph database, providing improved performance, a modern web UI, and enhanced API capabilities. Red teams use BloodHound CE to collect AD objects, ACLs, sessions, group memberships, and trust relationships, then visualize attack paths from compromised low-privileged accounts to high-value targets like Domain Admins. The SharpHound collector (v2 for CE) gathers data from Active Directory, while AzureHound collects from Azure AD / Entra ID environments.


## When to Use

- When conducting security assessments that involve conducting internal reconnaissance with bloodhound ce
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Familiarity with red teaming concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Objectives

- Deploy BloodHound CE server using Docker Compose
- Collect AD data using SharpHound v2 or BloodHound.py
- Import collected data into BloodHound CE for graph analysis
- Identify shortest attack paths from owned principals to Domain Admins
- Discover ACL-based attack paths, Kerberoastable accounts, and delegation abuse
- Execute custom Cypher queries for advanced attack path analysis
- Generate attack path reports for engagement documentation

## MITRE ATT&CK Mapping

- **T1087.002** - Account Discovery: Domain Account
- **T1069.002** - Permission Groups Discovery: Domain Groups
- **T1482** - Domain Trust Discovery
- **T1615** - Group Policy Discovery
- **T1018** - Remote System Discovery
- **T1033** - System Owner/User Discovery
- **T1016** - System Network Configuration Discovery

## Workflow

### Phase 1: BloodHound CE Deployment
1. Deploy BloodHound CE using Docker Compose:
   ```bash
   curl -L https://ghst.ly/getbhce -o docker-compose.yml
   docker compose pull
   docker compose up -d
   ```
2. Access the web interface at https://localhost:8080
3. Log in with the default admin credentials (displayed in Docker logs):
   ```bash
   docker compose logs | grep "Initial Password"
   ```
4. Change the default admin password immediately

### Phase 2: Data Collection with SharpHound v2
1. Transfer SharpHound v2 to the compromised Windows host:
   ```powershell
   # Execute full collection
   .\SharpHound.exe -c All --outputdirectory C:\Temp

   # DCOnly collection (LDAP only, stealthier)
   .\SharpHound.exe -c DCOnly

   # Session collection for logged-on user mapping
   .\SharpHound.exe -c Session --loop --loopduration 02:00:00

   # Collect from specific domain
   .\SharpHound.exe -c All -d child.domain.local
   ```
2. Alternative: Use BloodHound.py from Linux:
   ```bash
   bloodhound-python -u user -p 'Password123' -d domain.local -ns 10.10.10.1 -c All
   ```
3. Exfiltrate the generated ZIP file to the analysis workstation

### Phase 3: Data Import and Initial Analysis
1. Upload collected data via the BloodHound CE web interface (File Ingest)
2. Mark compromised accounts as "Owned" in the interface
3. Run built-in analysis queries:
   - Shortest Path to Domain Admin
   - Kerberoastable Users with Path to DA
   - AS-REP Roastable Users
   - Users with DCSync Rights
   - Computers with Unconstrained Delegation

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

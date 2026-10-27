---
name: performing-credential-access-with-lazagne
description: "Extract stored credentials from compromised endpoints using the LaZagne 信号:本地凭据,浏览器窃取,chrome密码。"
when-to-use: Extract stored credentials from compromised endpoints using the LaZagne
  post-exploitation tool to recover passwords from browsers, databases, system vaults,
  and applications during authorized red team operations.
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- credential-access
- lazagne
- post-exploitation
- password-recovery
- credential-dumping
- lateral-movement
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
- Platform Hardening
- File Format Verification
nist_csf:
- ID.RA-01
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1595
- T1190
- T1059
- T1078
- T1021
mitre_f3:
  version: '1.1'
  tactics:
  - reconnaissance
  - positioning
  - initial-access
  techniques:
  - id: T1555
    name: Credentials from Password Stores
    tactic: reconnaissance
    source: attack
  - id: T1555.003
    name: 'Credentials from Password Stores: Credentials from Web Browsers'
    tactic: reconnaissance
    source: attack
  - id: T1555.005
    name: 'Credentials from Password Stores: Password Managers'
    tactic: reconnaissance
    source: attack
  - id: T1539
    name: Steal Web Session Cookie
    tactic: positioning
    source: attack
  - id: F1006.002
    name: 'Account Takeover: Exposed Login Credential'
    tactic: initial-access
    source: f3
  - id: F1006
    name: Account Takeover
    tactic: initial-access
    source: f3
---
# Performing Credential Access with LaZagne

## Overview

LaZagne is an open-source post-exploitation tool designed to retrieve credentials stored on local systems. It supports Windows, Linux, and macOS, with the most extensive module library for Windows. LaZagne recovers passwords from browsers (Chrome, Firefox, Edge, Opera), email clients (Outlook, Thunderbird), databases (PostgreSQL, MySQL, SQLite), system stores (Windows Credential Manager, LSA secrets, DPAPI), Wi-Fi profiles, Git credentials, and dozens of other applications. The tool is categorized under MITRE ATT&CK T1555 (Credentials from Password Stores) and is listed as software S0349. Red teams use LaZagne after gaining initial access to harvest stored credentials that enable lateral movement and privilege escalation.


## When to Use

- When conducting security assessments that involve performing credential access with lazagne
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Familiarity with red teaming concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Objectives

- Deploy LaZagne on compromised Windows, Linux, or macOS endpoints
- Extract credentials from all supported password stores
- Parse and prioritize recovered credentials for lateral movement
- Identify high-value credentials (domain admin, service accounts, cloud access)
- Document credential harvesting results with appropriate evidence handling
- Correlate recovered credentials with BloodHound attack paths

## MITRE ATT&CK Mapping

- **T1555** - Credentials from Password Stores
- **T1555.003** - Credentials from Password Stores: Credentials from Web Browsers
- **T1555.004** - Credentials from Password Stores: Windows Credential Manager
- **T1552.001** - Unsecured Credentials: Credentials In Files
- **T1552.002** - Unsecured Credentials: Credentials in Registry
- **T1003.004** - OS Credential Dumping: LSA Secrets
- **T1539** - Steal Web Session Cookie

## Workflow

### Phase 1: LaZagne Deployment
1. Transfer LaZagne to the compromised host:
   ```powershell
   # Pre-compiled executable (Windows)
   # Transfer lazagne.exe via C2 channel or file upload

   # Python version (requires Python on target)
   git clone https://github.com/AlessandroZ/LaZagne.git
   cd LaZagne
   pip install -r requirements.txt
   ```
2. Verify execution capability and privileges:
   ```powershell
   # Check current user context
   whoami /priv

   # LaZagne works with standard user privileges for user-level stores
   # SYSTEM/Admin privileges needed for DPAPI master keys, LSA secrets, SAM
   ```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

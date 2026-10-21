---
name: performing-thick-client-application-penetration-test
description: Conduct a thick client application penetration test to identify insecure
when-to-use: Conduct a thick client application penetration test to identify insecure
  local storage, hardcoded credentials, DLL hijacking, memory manipulation, and insecure
  API communication in desktop applications using dnSpy, Procmon, and Burp Suite.
domain: cybersecurity
subdomain: penetration-testing
tags:
- thick-client
- desktop-application
- dnSpy
- Procmon
- DLL-hijacking
- binary-analysis
- API-interception
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
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
- T1003
---

# Performing Thick Client Application Penetration Test

## Overview

Thick client (fat client) penetration testing assesses the security of desktop applications that run locally on user machines and communicate with backend servers. Unlike web applications, thick clients present a broader attack surface including local file storage, binary analysis, memory manipulation, DLL injection, process interception, and client-server communication. Common targets include banking applications, ERP clients (SAP GUI), trading platforms, healthcare systems, and legacy enterprise software.


## When to Use

- When conducting security assessments that involve performing thick client application penetration test
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Application installer and valid credentials
- Windows/Linux test machine (isolated)
- Tools: dnSpy, Procmon, Process Hacker, Wireshark, Burp Suite, Echo Mirage, Fiddler, IDA Pro/Ghidra
- Administrative access to test machine


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Phase 1 — Information Gathering

### Static Analysis

```powershell
# Identify application technology
# Check file properties, signatures, framework (.NET, Java, C++, Electron)
file application.exe
# .NET -> dnSpy, JetBrains dotPeek
# Java -> JD-GUI, JADX
# C/C++ -> Ghidra, IDA Pro
# Electron -> extract asar archive

# Check for .NET framework
Get-ChildItem -Path "C:\Program Files\TargetApp" -Recurse -Filter "*.dll" |
  ForEach-Object { [System.Reflection.AssemblyName]::GetAssemblyName($_.FullName).FullName }

# Strings analysis
strings application.exe | findstr -i "password\|secret\|api\|key\|token\|jdbc\|connection"

# Check for hardcoded credentials
strings application.exe | findstr -i "username\|user=\|pass=\|pwd=\|admin"

# Review configuration files
type "C:\Program Files\TargetApp\app.config"
type "C:\Program Files\TargetApp\settings.xml"
type "%APPDATA%\TargetApp\config.json"

# Check for certificate pinning
strings application.exe | findstr -i "cert\|pin\|ssl\|tls"
```

### .NET Decompilation with dnSpy

```
# Open application in dnSpy
1. Launch dnSpy
2. File > Open > Select application.exe and DLLs
3. Search for:
   - "password", "secret", "connectionString"
   - Authentication methods
   - Encryption/decryption functions
   - API endpoints and keys
   - License validation logic

# Look for:
- Hardcoded credentials in source
- Insecure encryption (DES, MD5, base64 "encryption")
- SQL queries (potential injection)
- Disabled certificate validation
- Debug/verbose logging with sensitive data
```

## Phase 2 — Dynamic Analysis

### Process Monitoring

```powershell
# Monitor file system activity with Procmon
# Filters:
#   Process Name = application.exe
#   Operation = CreateFile, WriteFile, ReadFile, RegSetValue

# Key observations:
# - Where does the app store data? (AppData, temp, registry)
# - Does it write credentials to disk?
# - Does it create temporary files with sensitive data?
# - What registry keys does it access?

# Monitor with Process Hacker
# Check: loaded DLLs, network connections, handles, tokens

# Monitor network traffic
# Wireshark filter: ip.addr == <server_ip>
# Check for: unencrypted credentials, API keys, tokens
```

### Traffic Interception

```bash
# Intercept HTTP/HTTPS traffic with Burp Suite
# Configure system proxy: 127.0.0.1:8080
# Install Burp CA certificate in Windows certificate store

# For non-HTTP protocols, use Echo Mirage

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

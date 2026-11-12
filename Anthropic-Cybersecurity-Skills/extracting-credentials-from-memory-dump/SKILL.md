---
name: extracting-credentials-from-memory-dump
description: "Extract cached credentials, password hashes, Kerberos tickets, and other secrets. Signals: Kerberos, ticket attack, golden ticket."
zh-signals: "Extracts cached credentials, password hashes, Kerberos tickets, and 信号:kerberos,票据攻击,黄金票据。"
when-to-use: Extracts cached credentials, password hashes, Kerberos tickets, and
  authentication tokens from Windows memory dumps using Volatility 3, Mimikatz,
  and pypykatz. Use when performing memory forensics or incident response on an
  LSASS or full memory dump and you need to recover credentials or Kerberos material
  for investigation.
domain: cybersecurity
subdomain: digital-forensics
tags:
- forensics
- credential-extraction
- memory-forensics
- volatility
- mimikatz
- password-hashes
- incident-response
mitre_attack:
- T1005
- T1074
- T1119
- T1070
- T1003
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
  - id: T1539
    name: Steal Web Session Cookie
    tactic: positioning
    source: attack
  - id: F1006
    name: Account Takeover
    tactic: initial-access
    source: f3
  - id: F1006.002
    name: 'Account Takeover: Exposed Login Credential'
    tactic: initial-access
    source: f3
  - id: F1006.001
    name: 'Account Takeover: Exposed API Key'
    tactic: initial-access
    source: f3
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-03
- DE.AE-02
- RS.MA-01
---

# Extracting Credentials from Memory Dump

## When to Use
- During incident response to determine what credentials an attacker had access to
- When assessing the scope of credential compromise after a breach
- For identifying accounts that need immediate password resets
- When investigating lateral movement and pass-the-hash/pass-the-ticket attacks
- For recovering encryption keys or authentication tokens from process memory

## Prerequisites
- Memory dump in raw, ELF, or crash dump format
- Volatility 3 with Windows symbol tables
- Mimikatz (for offline analysis of extracted LSASS dumps)
- pypykatz (Python implementation of Mimikatz for Linux-based analysis)
- Understanding of Windows authentication (NTLM, Kerberos, DPAPI)
- Appropriate legal authorization for credential extraction

## Workflow

### Step 1: Prepare Tools and Verify Memory Dump

```bash
# Install analysis tools
pip install volatility3 pypykatz

# Verify memory dump integrity
sha256sum /cases/case-2024-001/memory/memory.raw

# Identify the OS version
vol -f /cases/case-2024-001/memory/memory.raw windows.info

# Verify LSASS process exists in memory
vol -f /cases/case-2024-001/memory/memory.raw windows.pslist | grep -i lsass

# Output:
# PID    PPID   ImageFileName   Offset(V)        Threads  Handles  SessionId
# 684    564    lsass.exe       0xffffe00123456   35       1234     0
```

### Step 2: Extract Credential Hashes with Volatility

```bash
# Dump SAM database hashes from memory
vol -f /cases/case-2024-001/memory/memory.raw windows.hashdump \
   | tee /cases/case-2024-001/analysis/hashdump.txt

# Output format:
# User           RID    LM Hash                          NTLM Hash
# Administrator  500    aad3b435b51404eeaad3b435b51404ee  fc525c9683e8fe067095ba2ddc971889
# Guest          501    aad3b435b51404eeaad3b435b51404ee  31d6cfe0d16ae931b73c59d7e0c089c0
# DefaultAccount 503    aad3b435b51404eeaad3b435b51404ee  31d6cfe0d16ae931b73c59d7e0c089c0
# svcbackup      1001   aad3b435b51404eeaad3b435b51404ee  2b576acbe6bcfda7294d6bd18041b8fe

# Extract LSA secrets
vol -f /cases/case-2024-001/memory/memory.raw windows.lsadump \
   | tee /cases/case-2024-001/analysis/lsadump.txt

# Extract cached domain credentials
vol -f /cases/case-2024-001/memory/memory.raw windows.cachedump \
   | tee /cases/case-2024-001/analysis/cachedump.txt
```

### Step 3: Dump LSASS Process Memory for Detailed Analysis

```bash
# Dump LSASS process memory (PID from Step 1)
vol -f /cases/case-2024-001/memory/memory.raw windows.memmap --pid 684 --dump \
   -o /cases/case-2024-001/analysis/lsass_dump/

# Alternative: Dump all files associated with LSASS
vol -f /cases/case-2024-001/memory/memory.raw windows.dumpfiles --pid 684 \
   -o /cases/case-2024-001/analysis/lsass_files/

# Use procdump plugin for cleaner process dump
vol -f /cases/case-2024-001/memory/memory.raw windows.dumpfiles \
   --pid 684 -o /cases/case-2024-001/analysis/

# Rename the dump file for pypykatz/mimikatz
mv /cases/case-2024-001/analysis/lsass_dump/pid.684.dmp \
   /cases/case-2024-001/analysis/lsass.dmp
```

### Step 4: Extract Credentials with pypykatz

```bash

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

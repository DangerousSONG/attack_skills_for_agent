---
name: conducting-social-engineering-pretext-call
description: "Plan and execute authorized vishing (voice phishing) pretext calls to 信号:钓鱼,社会工程,钓鱼邮件。"
when-to-use: Plan and execute authorized vishing (voice phishing) pretext calls to
  assess employee susceptibility to social engineering and evaluate security awareness
  controls.
domain: cybersecurity
subdomain: red-teaming
tags:
- social-engineering
- vishing
- pretext-call
- security-awareness
- red-team
- phishing
- human-risk
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0088
- AML.T0052
nist_ai_rmf:
- GOVERN-6.2
- MAP-5.2
d3fend_techniques:
- File Metadata Consistency Validation
- Application Protocol Command Analysis
- Identifier Analysis
- Content Format Conversion
- Message Analysis
nist_csf:
- ID.RA-01
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1598.004
- T1566.004
- T1589
- T1591
- T1598
mitre_f3:
  version: '1.1'
  tactics:
  - reconnaissance
  - initial-access
  - stealth
  techniques:
  - id: T1598
    name: Phishing for Information
    tactic: reconnaissance
    source: attack
  - id: F1034
    name: Interactive Voice Response Mapping
    tactic: reconnaissance
    source: f3
  - id: F1029
    name: Gather Customer Information
    tactic: reconnaissance
    source: f3
  - id: F1032
    name: Impersonate Official
    tactic: initial-access
    source: f3
  - id: F1040
    name: Phone Number Spoofing
    tactic: stealth
    source: f3
  - id: F1040.002
    name: 'Phone Number Spoofing: Official Phone Number Spoofing'
    tactic: stealth
    source: f3
---

# Conducting Social Engineering Pretext Call

## Overview

A pretext call (vishing) is a social engineering technique where an attacker impersonates a trusted authority figure over the phone to manipulate targets into divulging sensitive information, performing actions, or granting access. In red team engagements, pretext calls test the human element of security controls, measuring employee adherence to verification procedures and security awareness training effectiveness. MITRE ATT&CK maps this to T1566.004 (Phishing for Information: Voice) and T1598 (Phishing for Information).


## When to Use

- When conducting security assessments that involve conducting social engineering pretext call
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Written authorization specifying social engineering scope and boundaries
- List of approved target employees (usually provided by client)
- OSINT research on targets and organization
- Spoofed caller ID capability (authorized for testing)
- Call recording equipment (with legal consent as required)
- Pretext scenarios approved by client

## MITRE ATT&CK Mapping

| Technique ID | Name | Tactic |
|---|---|---|
| T1566.004 | Phishing: Voice | Initial Access |
| T1598 | Phishing for Information | Reconnaissance |
| T1598.003 | Phishing for Information: Spearphishing Voice | Reconnaissance |
| T1589 | Gather Victim Identity Information | Reconnaissance |
| T1591 | Gather Victim Org Information | Reconnaissance |

## Phase 1: OSINT and Target Research

```bash
# LinkedIn employee enumeration
theHarvester -d targetcorp.com -b linkedin -l 200

# Company org chart and employee roles
# Review LinkedIn, corporate website "About Us" / "Team" pages

# Technology stack identification
# Check job postings for technology references (VPN vendor, email, helpdesk tool)

# Phone system identification
# Call main line, note IVR options, department names, extension patterns
```

Key intelligence to gather:
- Internal helpdesk phone number and procedures
- IT department names and staff
- VPN/remote access vendor (Cisco AnyConnect, Fortinet, Pulse Secure)
- Corporate email format (first.last, flast, etc.)
- Recent events (mergers, office moves, system upgrades)
- Employee names, titles, departments

## Phase 2: Pretext Development

### Common Pretext Scenarios

**IT Helpdesk Impersonation (Most Effective):**
> "Hi, this is [name] from the IT Service Desk. We're migrating everyone to the new VPN client this week, and I see your account hasn't been updated yet. I need to verify your current credentials to ensure the migration goes smoothly. Can you confirm your username and current password?"

**Vendor/Contractor:**
> "Hi, I'm [name] from [known vendor]. We're doing an emergency patch deployment for [product] and I need remote access to your system. Could you help me connect via TeamViewer?"

**Executive Assistant (Authority):**
> "This is [name] calling on behalf of [CFO name]. [He/She] needs an urgent wire transfer processed for a deal that's closing today. I'll email you the details, but we need this done in the next hour."

**Building/Facilities:**
> "Hi, this is [name] from facilities management. We're updating the badge access system this weekend. I need to confirm your employee ID and current badge number so your access isn't interrupted."

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

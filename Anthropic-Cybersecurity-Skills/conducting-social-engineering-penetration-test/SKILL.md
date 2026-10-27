---
name: conducting-social-engineering-penetration-test
description: "OSINT 画像驱动的社会工程渗透测试:钓鱼/语音钓鱼/短信钓鱼/物理伪装,用 GoPhish、SET、Evilginx 度量人员安全韧性。信号:社会工程,钓鱼测试,vishing,smishing。"
when-to-use: Design and execute a social engineering penetration test combining OSINT-driven target profiling with phishing, vishing, smishing, and physical pretexting campaigns using tools like GoPhish, the Socia
domain: cybersecurity
subdomain: penetration-testing
tags:
- social-engineering
- phishing
- vishing
- pretexting
- GoPhish
- SET
- OSINT
- security-awareness
- red-team
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0088
- AML.T0052
nist_ai_rmf:
- GOVERN-6.2
- MAP-5.2
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1566
- T1598
- T1566.004
- T1204.001
- T1589
mitre_f3:
  version: '1.1'
  tactics:
  - reconnaissance
  - initial-access
  - resource-development
  techniques:
  - id: T1598
    name: Phishing for Information
    tactic: reconnaissance
    source: attack
  - id: T1660
    name: Phishing
    tactic: initial-access
    source: attack
  - id: F1029
    name: Gather Customer Information
    tactic: reconnaissance
    source: f3
  - id: F1032
    name: Impersonate Official
    tactic: initial-access
    source: f3
  - id: T1557
    name: Adversary-in-the-Middle
    tactic: initial-access
    source: attack
  - id: F1020.002
    name: 'Create Fake Materials: Fake Website'
    tactic: resource-development
    source: f3
---

# Conducting Social Engineering Penetration Test

## Overview

Social engineering penetration testing assesses an organization's human attack surface through controlled simulation of real-world deception techniques. According to Verizon DBIR 2024, the human element is involved in approximately 68% of all breaches, with phishing remaining the dominant initial access vector. This skill covers phishing, vishing (voice phishing), smishing (SMS phishing), and physical pretexting campaigns using tools like GoPhish, the Social Engineer Toolkit (SET), and Evilginx.


## When to Use

- When conducting security assessments that involve conducting social engineering penetration test
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Written authorization from senior management (CISO/CTO)
- Legal review confirming compliance with local laws (CFAA, GDPR, etc.)
- Defined scope: target employee groups, attack types, exclusions
- GoPhish server, domain for phishing infrastructure, VPS
- OSINT tools: Maltego, theHarvester, LinkedIn scraping tools
- Coordination with HR and Legal for employee notification post-test

## Phase 1 — OSINT and Target Profiling

### Employee Reconnaissance

```bash
# Email harvesting
theHarvester -d targetcorp.com -b all -l 500 -f harvester_results

# LinkedIn OSINT (manual + tools)
# Gather: names, roles, departments, email format
# Identify: new hires, IT admins, finance team, executives

# Email format discovery
# Check: first.last@, flast@, firstl@
# Verify with: hunter.io, phonebook.cz, email-checker.net

# Social media OSINT
# Twitter/X: employees posting about work tools/frustrations
# Facebook: corporate event photos, office layout
# GitHub: employee repos with corporate email addresses

# Domain intelligence
dig targetcorp.com MX +short
dig targetcorp.com TXT +short
# Check for SPF, DKIM, DMARC records
# Weak DMARC = easier email spoofing

# Check breach databases (authorized)
# HaveIBeenPwned API for corporate emails
# Identify employees with compromised credentials
```

### Target Selection Matrix

| Group | Count | Pretext | Attack Vector |
|-------|-------|---------|--------------|
| Finance | 15 | Invoice approval | Phishing (credential harvest) |
| IT Help Desk | 8 | Password reset | Vishing |
| Executives | 5 | Board meeting update | Spear phishing |
| New Hires (< 90 days) | 12 | HR onboarding form | Phishing (payload) |
| All Employees | 200 | IT security update | Broad phishing |

## Phase 2 — Phishing Campaign

### Infrastructure Setup

```bash
# Register lookalike domain
# targetcorp.com -> targetc0rp.com, targetcorp-secure.com, targetcorp.net

# Set up GoPhish server
sudo apt install gophish
# Edit config.json for admin and phishing server ports
gophish

# Configure sending profile in GoPhish
# SMTP server: mail.attackdomain.com

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

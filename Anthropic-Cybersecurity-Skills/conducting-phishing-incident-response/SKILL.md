---
name: conducting-phishing-incident-response
description: "Respond to phishing incidents by analyzing reported emails, extracting IOCs, sandboxing URLs/attachments, assessing credential compromise, and remediating accounts. Signals: phishing response, incident response, IOC, email analysis, credential compromise."
zh-signals: "钓鱼事件响应:分析举报邮件、提取 IOC、沙箱跑 URL/附件、评估凭据泄露、全组织隔离清除与账户修复。信号:钓鱼响应,事件响应,ioc,邮件分析,凭据泄露。"
when-to-use: Respond to phishing incidents by analyzing reported emails, extracting indicators, sandboxing URLs/attachments, assessing credential compromise, quarantining malicious messages organization-wide, and 
domain: cybersecurity
subdomain: incident-response
tags:
- phishing-response
- email-security
- credential-compromise
- email-header-analysis
- mailbox-remediation
mitre_attack:
- T1566.001
- T1566.002
- T1204.002
- T1204.001
- T1114
- T1056.003
mitre_f3:
  version: '1.1'
  tactics:
  - initial-access
  - reconnaissance
  - resource-development
  - positioning
  techniques:
  - id: T1660
    name: Phishing
    tactic: initial-access
    source: attack
  - id: T1598
    name: Phishing for Information
    tactic: reconnaissance
    source: attack
  - id: F1020.002
    name: 'Create Fake Materials: Fake Website'
    tactic: resource-development
    source: f3
  - id: T1557
    name: Adversary-in-the-Middle
    tactic: positioning
    source: attack
  - id: F1004
    name: Access with Stolen Session Cookie
    tactic: initial-access
    source: f3
  - id: F1006.002
    name: 'Account Takeover: Exposed Login Credential'
    tactic: initial-access
    source: f3
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---

# Conducting Phishing Incident Response

## When to Use

- A user reports receiving a suspicious email via the phishing report button or abuse mailbox
- Email gateway detects a malicious email that bypassed initial filtering
- Threat intelligence indicates an active phishing campaign targeting the organization
- A user confirms they clicked a link or opened an attachment from a suspicious email
- Credentials have been entered on a suspected phishing page

**Do not use** for business email compromise (BEC) involving compromised internal accounts; use BEC response procedures which focus on account takeover investigation.

## Prerequisites

- Email security gateway with message trace and quarantine capabilities (Microsoft Defender for Office 365, Proofpoint, Mimecast)
- Microsoft 365 admin access or Google Workspace admin for mailbox search and purge
- Malware sandbox for attachment and URL analysis (ANY.RUN, Joe Sandbox, Hybrid Analysis)
- Email header analysis tools (MXToolbox Header Analyzer, Google Admin Toolbox)
- Identity provider access for account remediation (Azure AD, Okta, Duo)
- Phishing report intake process (dedicated mailbox or integrated report button)

## Workflow

### Step 1: Receive and Triage the Phishing Report

Evaluate the reported email to determine if it is malicious:

- Extract the email as an .EML or .MSG file (preserves headers)
- Analyze email headers to determine the true sender, relay path, and authentication results

```
Email Header Analysis Checklist:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Return-Path:     billing@spoofed-domain[.]com
From:            "IT Support" <support@corp-lookalike[.]com>
Reply-To:        attacker@gmail[.]com (different from From)
SPF:             FAIL (sender IP not authorized for domain)
DKIM:            FAIL (signature invalid)
DMARC:           FAIL (policy: none - no enforcement)
Received:        from mail.attacker-infra[.]net [45.33.x.x]
X-Originating-IP: 45.33.x.x
Message-ID:      <random@attacker-infra.net>
```

Classification criteria:
- **Confirmed Phishing**: Malicious URL/attachment, spoofed sender, credential harvesting page
- **Suspicious**: Anomalous headers but no confirmed malicious content
- **Spam/Marketing**: Unwanted but not malicious
- **Legitimate**: Not a phishing email (false report)

### Step 2: Analyze Malicious Content

Examine URLs and attachments in a safe environment:

**URL Analysis:**
- Check URL against VirusTotal, URLscan.io, and Google Safe Browsing
- Open URL in a sandbox browser to capture the landing page
- Check if the URL redirects to a credential harvesting page
- Identify the phishing kit type (Microsoft 365 login clone, Okta clone, generic)
- Determine if the phishing page is still active

**Attachment Analysis:**
- Calculate file hash (SHA-256) and check against VirusTotal
- Detonate in sandbox (ANY.RUN, Joe Sandbox)
- Analyze document for macros (olevba for Office files)
- Check for embedded exploits (CVE exploitation in document parsers)

### Step 3: Determine Scope of Impact

Identify all recipients and assess who interacted with the phishing email:

```
Scope Assessment:
━━━━━━━━━━━━━━━━
Total Recipients:     47 users
Delivered to Inbox:   38 users (9 caught by email gateway)
Opened Email:         24 users (email tracking pixel data)
Clicked Link:         8 users (proxy/firewall logs)
Entered Credentials:  3 users (phishing page submitted form data)
Opened Attachment:    2 users (EDR process execution telemetry)
```

Search methods:
- Microsoft 365: Use Threat Explorer or Content Search to find all instances of the email
- Google Workspace: Use Admin Console > Investigation tool for message search
- Proxy logs: Search for connections to the phishing URL from internal IPs
- EDR: Search for attachment file hash execution across all endpoints

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

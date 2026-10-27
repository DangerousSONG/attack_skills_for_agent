---
name: investigating-phishing-email-incident
description: "Investigates phishing email incidents from initial user report through 信号:钓鱼,社会工程,钓鱼邮件。"
when-to-use: 'Investigates phishing email incidents from initial user report through
  header analysis, URL/attachment detonation, impacted user identification, and containment
  actions using SOC tools like Splunk, Microsoft Defender, and sandbox analysis platforms.
  Use when a reported phishing email requires full incident investigation to determine
  scope and impact.

  '
domain: cybersecurity
subdomain: soc-operations
tags:
- soc
- phishing
- incident-response
- email-security
- splunk
- defender
- sandbox
mitre_attack:
- T1078
- T1685.002
- T1685.005
- T1566
- T1598
mitre_f3:
  version: '1.1'
  tactics:
  - reconnaissance
  - resource-development
  - initial-access
  - stealth
  - positioning
  techniques:
  - id: T1598
    name: Phishing for Information
    tactic: reconnaissance
    source: attack
  - id: T1660
    name: Phishing
    tactic: initial-access
    source: attack
  - id: T1672
    name: Email Spoofing
    tactic: stealth
    source: attack
  - id: F1020.002
    name: 'Create Fake Materials: Fake Website'
    tactic: resource-development
    source: f3
  - id: T1539
    name: Steal Web Session Cookie
    tactic: positioning
    source: attack
  - id: F1006.002
    name: 'Account Takeover: Exposed Login Credential'
    tactic: initial-access
    source: f3
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
---
# Investigating Phishing Email Incident

## When to Use

Use this skill when:
- A user reports a suspicious email via the phishing report button or helpdesk ticket
- Email security gateway flags a message that bypassed initial filters
- Automated detection identifies credential harvesting URLs or malicious attachments
- A phishing campaign targeting the organization requires scope assessment

**Do not use** for spam or marketing emails without malicious intent — route those to email administration for filter tuning.

## Prerequisites

- Access to email gateway logs (Proofpoint, Mimecast, or Microsoft Defender for Office 365)
- Splunk or SIEM with email log ingestion (O365 Message Trace, Exchange tracking logs)
- Sandbox access (Any.Run, Joe Sandbox, or Hybrid Analysis) for URL/attachment detonation
- Microsoft Graph API or Exchange Admin Center for email search and purge operations
- URLScan.io and VirusTotal API keys

## Workflow

### Step 1: Extract and Analyze Email Headers

Obtain the full email headers (`.eml` file) from the reported message:

```python
import email
from email import policy

with open("phishing_sample.eml", "rb") as f:
    msg = email.message_from_binary_file(f, policy=policy.default)

# Extract key headers
print(f"From: {msg['From']}")
print(f"Return-Path: {msg['Return-Path']}")
print(f"Reply-To: {msg['Reply-To']}")
print(f"Subject: {msg['Subject']}")
print(f"Message-ID: {msg['Message-ID']}")
print(f"X-Originating-IP: {msg['X-Originating-IP']}")

# Parse Received headers (bottom-up for true origin)
for header in reversed(msg.get_all('Received', [])):
    print(f"Received: {header[:120]}")

# Check authentication results
print(f"Authentication-Results: {msg['Authentication-Results']}")
print(f"DKIM-Signature: {msg.get('DKIM-Signature', 'NONE')[:80]}")
```

Key checks:
- **SPF**: Does `Return-Path` domain match sending IP? Look for `spf=pass` or `spf=fail`
- **DKIM**: Is the signature valid? `dkim=pass` confirms the email was not modified in transit
- **DMARC**: Does the `From` domain align with SPF/DKIM domains? `dmarc=fail` indicates spoofing

### Step 2: Analyze URLs and Attachments

**URL Analysis:**

```python
import requests

# Submit URL to URLScan.io
url_to_scan = "https://evil-login.example.com/office365"
response = requests.post(
    "https://urlscan.io/api/v1/scan/",
    headers={"API-Key": "YOUR_KEY", "Content-Type": "application/json"},
    json={"url": url_to_scan, "visibility": "unlisted"}
)
scan_id = response.json()["uuid"]
print(f"Scan URL: https://urlscan.io/result/{scan_id}/")

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

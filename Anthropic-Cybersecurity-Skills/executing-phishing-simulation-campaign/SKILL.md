---
name: executing-phishing-simulation-campaign
description: "Execute authorized phishing simulation campaigns to assess an organization's security posture. Signals: phishing, social engineering, phishing email."
zh-signals: "Executes authorized phishing simulation campaigns to assess an organization''s 信号:钓鱼,社会工程,钓鱼邮件。"
when-to-use: 'Executes authorized phishing simulation campaigns to assess an organization''s
  susceptibility to email-based social engineering attacks. The tester designs realistic
  phishing scenarios, builds credential harvesting infrastructure, sends targeted
  phishing emails, and tracks open rates, click-through rates, and credential submission
  rates to measure human security awareness. Activates for requests involving phishing
  simulation, social engineering assessment, email security testing, or security awareness
  measurement.

  '
domain: cybersecurity
subdomain: penetration-testing
tags:
- phishing-simulation
- social-engineering
- GoPhish
- email-security
- security-awareness
version: 1.0.0
author: mahipal
license: Apache-2.0
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
mitre_f3:
  version: '1.1'
  tactics:
  - reconnaissance
  - resource-development
  - initial-access
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
  - id: F1020.002
    name: 'Create Fake Materials: Fake Website'
    tactic: resource-development
    source: f3
  - id: T1583.001
    name: 'Acquire Infrastructure: Domains'
    tactic: resource-development
    source: attack
  - id: T1557
    name: Adversary-in-the-Middle
    tactic: initial-access
    source: attack
  - id: F1004
    name: Access with Stolen Session Cookie
    tactic: initial-access
    source: f3
---
# Executing Phishing Simulation Campaign

## When to Use

- Measuring employee susceptibility to phishing attacks as part of a security awareness program
- Testing the effectiveness of email security controls (secure email gateway, DMARC, SPF, DKIM)
- Conducting the social engineering component of a red team exercise to gain initial access
- Establishing a baseline for phishing susceptibility before deploying security awareness training
- Validating that incident response procedures work when employees report suspicious emails

**Do not use** without explicit written authorization from the organization's leadership, for actual credential theft beyond the authorized scope, for targeting individuals personally rather than professionally, or for sending phishing emails that could cause psychological harm or legal liability.

## Prerequisites

- Written authorization from executive leadership specifying the campaign scope, target groups, and escalation procedures
- Coordination with the IT/security team to whitelist the sending infrastructure (or test whether it bypasses controls, depending on scope)
- GoPhish or equivalent phishing platform configured with a sending domain, SMTP relay, and landing page infrastructure
- Phishing domain registered and configured with SPF, DKIM, and DMARC records to maximize deliverability
- Employee email list from HR, organized by department for targeted campaigns
- Incident response team briefed on the campaign timeline and escalation procedures

## Workflow

### Step 1: Campaign Planning and Pretext Development

Design realistic phishing scenarios based on threats relevant to the target organization:

- **Pretext selection**: Choose scenarios that mirror real-world attacks:
  - IT support: Password expiration notice requiring immediate action
  - HR department: Benefits enrollment, policy acknowledgment, W-2/tax document
  - Executive impersonation: Urgent request from CEO/CFO to review a document
  - Vendor/supplier: Invoice requiring review, delivery notification
  - Cloud services: Microsoft 365 shared document, Google Drive access, Zoom meeting invitation
- **Target segmentation**: Divide employees into groups by department, role, or access level. High-value targets (finance, IT admin, executives) may receive more sophisticated pretexts.
- **Timing**: Schedule sends during business hours, preferably Tuesday-Thursday when email engagement is highest. Avoid holidays, mass layoff periods, or other sensitive times.
- **Success metrics**: Define what constitutes campaign success: email open rate, link click rate, credential submission rate, report rate (employees who report the phish to IT)

### Step 2: Infrastructure Setup

Configure the phishing infrastructure:

- **Domain registration**: Register a domain that resembles the target organization's domain (typosquatting, homograph, or brand-adjacent). Examples: `target-corp.com`, `targetcorp-portal.com`, `targetsupport.net`
- **SSL certificate**: Obtain a TLS certificate for the phishing domain (Let's Encrypt) to display the padlock icon
- **GoPhish configuration**:
  - Set up the GoPhish server on a VPS with the phishing domain
  - Configure the SMTP sending profile with the phishing domain's mail server
  - Create the email template with tracking pixel and link to the landing page
  - Build the credential harvesting landing page that mirrors the target's login portal
  - Import the target email list and create user groups
- **Email authentication**: Configure SPF, DKIM, and DMARC records for the phishing domain to pass email authentication checks and improve delivery rates
- **Test delivery**: Send test emails to a controlled inbox to verify rendering, link tracking, and landing page functionality

### Step 3: Campaign Execution

Launch the phishing campaign:

- Send emails in batches to avoid triggering rate limits or spam filters (e.g., 50 emails per hour)
- Monitor GoPhish dashboard in real-time for delivery failures, bounces, and early interactions
- Track metrics as they come in: emails sent, emails opened (tracking pixel fired), links clicked, credentials submitted
- If the IT security team or SOC detects the campaign (if this is part of the test), document the detection time and response actions
- Maintain an emergency stop procedure: if an employee becomes distressed or the campaign creates unintended consequences, pause immediately
- Run the campaign for 48-72 hours before closing the landing page, as most interactions occur within the first 24 hours

### Step 4: Credential Capture and Access Demonstration

Process captured credentials to demonstrate impact (if authorized):

- Review all captured credentials in GoPhish. Do not test credentials against real systems unless explicitly authorized.
- If authorized for full exploitation: test captured credentials against the organization's actual login portal (VPN, OWA, SSO)
- Document any accounts that were successfully compromised, what data they could access, and whether MFA was present
- If MFA blocks access, document that MFA prevented the compromise and recommend maintaining MFA enforcement
- Identify patterns in credential submissions: which departments, roles, or locations are most susceptible

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

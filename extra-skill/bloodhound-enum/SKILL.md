---
name: bloodhound-enum
description: "Active Directory information gathering with BloodHound.py. Use when you need to enumerate domain users, groups, computers, sessions, ACLs, and trust relationships, or to analyze domain attack paths. BloodHound.py is the Python collector for BloodHound; it collects AD data over LDAP/DNS/Kerberos and outputs JSON for analysis in the BloodHound GUI. Use this skill for any scenario involving domain penetration, AD enumeration, or attack path analysis"
zh-signals: "使用 BloodHound.py 采集 Active Directory 信息，枚举用户、组、计算机、会话、ACL 与信任关系并分析域内攻击路径。信号:BloodHound,AD枚举,攻击路径,ACL,域渗透,Kerberos"
when-to-use: "Use when you need to enumerate Active Directory users, groups, computers, sessions, ACLs, and trust relationships, or analyze domain attack paths with BloodHound.py."
metadata:
  tags: "bloodhound,AD,domain penetration,Active Directory,LDAP,Kerberos,enumeration,ACL,trust relationship,attack path,domain controller"
  category: "tool"
---

# BloodHound.py AD Information Gathering Methodology

BloodHound.py is the Python collector for BloodHound. Core advantages: **no execution on the target** (collects remotely over LDAP/DNS) + **broad coverage** (users/groups/computers/sessions/ACLs/trust relationships) + **JSON output** (import into the BloodHound GUI to analyze attack paths).

Project URL: https://github.com/dirkjanm/BloodHound.py

## Phase 1: Basic Collection

```bash
# Full collection (most common)
bloodhound-python -d corp.local -u user -p 'P@ssw0rd' -c All

# Specify the domain controller IP
bloodhound-python -d corp.local -u user -p 'P@ssw0rd' -c All -dc 10.0.0.1

# Specify the DNS server
bloodhound-python -d corp.local -u user -p 'P@ssw0rd' -c All -ns 10.0.0.1

# Output a compressed archive
bloodhound-python -d corp.local -u user -p 'P@ssw0rd' -c All --zip
```

## Phase 2: Authentication Methods

```bash
# Password authentication
bloodhound-python -d corp.local -u user -p 'P@ssw0rd' -c All

# NTLM hash authentication (pass-the-hash)
bloodhound-python -d corp.local -u user --hashes aad3b435b51404eeaad3b435b51404ee:hash -c All

# Kerberos authentication
bloodhound-python -d corp.local -u user -p 'P@ssw0rd' -c All -k

# Use a ccache ticket
export KRB5CCNAME=/tmp/krb5cc_user
bloodhound-python -d corp.local -u user -c All -k --auth-method kerberos
```

## Phase 3: Choosing a Collection Method

```bash
# Default collection (Group + LocalAdmin + Session + Trusts)
bloodhound-python -d corp.local -u user -p pass -c Default

# Group membership only
bloodhound-python -d corp.local -u user -p pass -c Group

# Local admins only
bloodhound-python -d corp.local -u user -p pass -c LocalAdmin

# Session information only
bloodhound-python -d corp.local -u user -p pass -c Session

# ACL collection (to analyze permission relationships)
bloodhound-python -d corp.local -u user -p pass -c ACL

# Trust relationships
bloodhound-python -d corp.local -u user -p pass -c Trusts
```

## Phase 4: Import and Analysis

After collection finishes, import the JSON/ZIP file into the BloodHound GUI:

```bash
# Start Neo4j (the BloodHound backend)
sudo neo4j start

# Open the BloodHound GUI and drag the JSON/ZIP file in to import it
# Common queries:
# - Find all Domain Admins
# - Shortest Path to Domain Admins
# - Find Kerberoastable Users
# - Find AS-REP Roastable Users
```

## Common Penetration Testing Scenarios

| Scenario | Command |
|------|------|
| Full collection | `bloodhound-python -d corp.local -u user -p pass -c All --zip` |
| PtH collection | `bloodhound-python -d corp.local -u user --hashes LM:NT -c All` |
| ACL analysis only | `bloodhound-python -d corp.local -u user -p pass -c ACL` |
| Specify the DC | `bloodhound-python -d corp.local -u user -p pass -c All -dc 10.0.0.1 -ns 10.0.0.1` |

---
name: adinfo-enum
description: "Use Adinfo for Active Directory information gathering. Use when you have obtained domain user credentials and need to quickly collect domain environment information. Adinfo is a fast AD information gathering tool that outputs the domain controller list, domain admin accounts, trust relationships, GPOs, SPNs, delegation configuration, and other key information with a single command — far faster than manual LDAP queries. Use this skill for the first information gathering step after discovering a domain environment"
zh-signals: "使用 Adinfo 一条命令完成 Active Directory 信息收集，覆盖域控、域管、信任、GPO、SPN 与委派配置。信号:Adinfo,AD信息收集,域控枚举,SPN,委派,GPO。"
when-to-use: >-
  Use when you have obtained domain user credentials and need fast Active Directory reconnaissance — domain controllers, domain admins, trust relationships, GPOs, SPNs, or delegation — as the first collection step after discovering a domain environment.
metadata:
  tags: "adinfo,ad,domain,ldap,ad-enumeration,information-gathering,domain-controller,domain-admin,SPN,delegation,GPO,active-directory"
  category: "tool"
---

# Adinfo Fast AD Information Gathering

The value of Adinfo lies in **collecting a full picture of the domain environment with one command** — domain controllers, domain admins, trusts, SPNs, delegation, GPOs, and other key information all get printed, saving you the trouble of writing LDAP queries by hand.

Project address: https://github.com/lzzbb/Adinfo

## Basic Usage

```bash
# Collect with domain user credentials
adinfo -d DOMAIN -u user -p password -dc DC_IP

# Use an NTLM hash
adinfo -d DOMAIN -u user -H NTLM_HASH -dc DC_IP
```

## Output Contents

Adinfo automatically collects and outputs the following information:

| Category | Content |
|------|------|
| Basic information | Domain name, domain SID, functional level |
| Domain controller list | Hostname and IP of every DC |
| Domain admin accounts | Domain Admins / Enterprise Admins members |
| Trust relationships | Domain trust types and direction |
| Password policy | Minimum length, complexity, lockout threshold |
| SPN accounts | Service accounts vulnerable to Kerberoasting |
| Delegation configuration | Unconstrained delegation / constrained delegation / RBCD |
| AS-REP | Accounts that do not require pre-authentication |
| GPO | Group Policy list |
| OU structure | Organizational unit hierarchy |
| Computer accounts | List of computers in the domain |

## Operational Workflow

```
After obtaining domain user credentials:
│
├─ 1. adinfo quickly collects the full picture
│     └→ Identify domain admins, SPN accounts, delegation configuration
│
├─ 2. Choose the attack path based on the adinfo output
│     ├─ SPN accounts present → Kerberoast (GetUserSPNs.py)
│     ├─ AS-REP accounts present → AS-REP Roast (GetNPUsers.py)
│     ├─ Unconstrained delegation present → delegation attack
│     ├─ Trust relationships present → cross-domain attack
│     └─ Weak password policy → password spraying
│
├─ 3. Deep enumeration (when more detail is needed)
│     ├─ BloodHound → visualize attack paths
│     ├─ nxc ldap → specific LDAP queries
│     └─ ldapsearch → custom filters
│
└─ 4. Lateral movement + privilege escalation
```

## Comparison with Other AD Tools

| Tool | Advantage | Applicable scenario |
|------|------|---------|
| Adinfo | One command for the full picture, concise output | Initial domain information gathering |
| BloodHound | Visualized attack paths | Path analysis in complex domain environments |
| nxc ldap | Flexible queries, rich module set | Targeted information queries |
| ldapsearch | Native LDAP, maximum flexibility | Custom complex queries |

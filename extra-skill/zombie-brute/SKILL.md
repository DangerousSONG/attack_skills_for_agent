---
name: zombie-brute
description: "Multi-protocol brute force with zombie. zombie is a high-performance brute-force tool from chainreactors that supports 20+ protocols including SSH/FTP/MySQL/MSSQL/PostgreSQL/Redis/SMB/RDP/SNMP/LDAP/VNC, with built-in smart dictionary generation and a distributed mode. Compared with hydra: zombie supports more protocols, faster concurrency, and rule-based dictionary generation. Use this skill when you need bulk weak credential detection or credential spraying"
zh-signals: "使用 zombie 进行多协议暴力破解与凭据喷洒，支持 20+ 协议、智能字典与分布式模式。信号:zombie,暴力破解,凭据喷洒,弱口令,多协议"
when-to-use: >-
  Use when performing authorized brute force, weak-password detection, or
  credential spraying across SSH, RDP, MySQL, Redis, SMB, and other protocols.
metadata:
  tags: "zombie,brute,bruteforce,brute force,weak credentials,password,ssh,rdp,mysql,redis,smb,chainreactors,hydra"
  category: "tool"
---

# zombie Multi-Protocol Brute Force

zombie focuses on the **efficiency and coverage of brute force** — supporting 20+ protocols, building in smart dictionary generation, and supporting a credential spraying mode (one password against all users, avoiding lockouts).

Project URL: https://github.com/chainreactors/zombie

## Basic Usage

```bash
# SSH brute force
zombie -i 10.0.0.1 -s ssh -u root -P passwords.txt

# Specify the username and password files
zombie -i 10.0.0.1 -s ssh -U users.txt -P passwords.txt

# MySQL brute force
zombie -i 10.0.0.1 -s mysql -u root -P passwords.txt

# Redis unauthenticated access + password check
zombie -i 10.0.0.1 -s redis -P passwords.txt

# RDP brute force
zombie -i 10.0.0.1 -s rdp -u administrator -P passwords.txt
```

## Batch Targets

```bash
# Read targets from a file (one ip:port per line)
zombie -l targets.txt -s ssh -U users.txt -P passwords.txt

# Network segment scan + brute force
zombie -i 10.0.0.0/24 -s ssh -u root -p admin123

# Brute force multiple protocols at once
zombie -i 10.0.0.1 -s ssh,mysql,redis,ftp -U users.txt -P passwords.txt
```

## Credential Spraying Mode

Credential spraying (one password against all users) is safer than traditional brute force (one user against all passwords) — it is less likely to trigger account lockouts:

```bash
# Spray mode
zombie -i 10.0.0.0/24 -s smb -U domain_users.txt -p 'P@ssw0rd' --spray

# Multi-password spray (one password per round)
zombie -i 10.0.0.0/24 -s smb -U domain_users.txt -P top10.txt --spray
```

## Concurrency and Timeout

```bash
# Adjust the concurrency threads (default 10)
zombie -i 10.0.0.0/24 -s ssh -u root -P passwords.txt -t 50

# Timeout setting (seconds)
zombie -i 10.0.0.1 -s rdp -u admin -P passwords.txt --timeout 10

# Stop on success
zombie -i 10.0.0.1 -s ssh -u root -P passwords.txt --stop-on-success
```

## Supported Protocols

SSH, FTP, MySQL, MSSQL, PostgreSQL, Redis, MongoDB, Memcached, SMB, RDP, VNC, SNMP, LDAP, SMTP, POP3, IMAP, HTTP-Basic, HTTP-Form, Telnet, Oracle

## Decision Tree

```
What do you need to brute force?
├─ Single protocol + simple scenario → zombie / hydra both work
├─ Multi-protocol batch + large scale → zombie (faster, broader protocol support)
├─ Credential spraying in a domain environment → zombie --spray or nxc
├─ Need integrated internal scanning + weak credentials → fscan (integrated scan + brute force)
└─ Web form brute force → zombie / hydra / ffuf
```

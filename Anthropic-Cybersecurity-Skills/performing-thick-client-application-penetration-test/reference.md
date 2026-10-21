# performing-thick-client-application-penetration-test — 详细参考（由 SKILL.md 拆分）

# Inject into process and intercept TCP/UDP traffic

# For HTTPS with certificate pinning:
# Method 1: Patch certificate validation in dnSpy
# Method 2: Use Frida to hook SSL validation
frida -l bypass_ssl_pinning.js -f application.exe

# Fiddler for .NET applications
# Enable HTTPS decryption
# Monitor API calls, request/response bodies
```

## Phase 3 — Vulnerability Testing

### Authentication Bypass

```
# Test local authentication bypass
1. Open dnSpy, find authentication method
2. Set breakpoint on credential validation
3. Modify return value to bypass (Debug > Set Next Statement)
4. Or: Patch binary to always return true

# Test for credential storage
# Check: registry, config files, SQLite databases, Windows Credential Manager
reg query "HKCU\Software\TargetApp" /s
type "%APPDATA%\TargetApp\user.db"
# SQLite: sqlite3 user.db ".dump"
```

### DLL Hijacking

```powershell
# Identify DLL search order vulnerability
# Use Procmon to find DLLs loaded from writable paths
# Filter: Result = NAME NOT FOUND, Path ends with .dll

# Create malicious DLL
# msfvenom -p windows/exec CMD=calc.exe -f dll -o hijacked.dll
# Place in application directory or writable PATH directory

# DLL sideloading
# If app loads DLL without full path:
# 1. Create DLL with same exports
# 2. Place in app directory
# 3. DLL loads before legitimate version
```

### Memory Analysis

```powershell
# Dump process memory
# Use Process Hacker > Process > Properties > Memory
# Search for plaintext credentials, tokens, session IDs

# Strings from memory dump
strings process_dump.dmp | findstr -i "password\|token\|session\|bearer"

# Modify memory values (license bypass, privilege escalation)
# Use Cheat Engine or x64dbg to:
# 1. Find memory address of authorization variable
# 2. Modify value (e.g., isAdmin = 0 -> isAdmin = 1)
```

### Input Validation

```
# SQL Injection in local database
# Test input fields with: ' OR 1=1--
# If app uses local SQLite/SQL Server Express

# Command injection
# Test fields that interact with OS:
# File paths: ..\..\..\..\windows\system32\cmd.exe
# Print/export: | calc.exe

# Buffer overflow
# Send oversized input to text fields
# Monitor with x64dbg for crashes
# Check for SEH-based or stack-based overflows
```

## Phase 4 — API Security Testing

```bash
# Capture API calls from thick client
# In Burp Suite, analyze:

# IDOR (Insecure Direct Object Reference)
# Change user IDs in requests to access other users' data
# GET /api/users/1001 -> GET /api/users/1002

# Authorization bypass
# Remove or modify JWT tokens
# Test role escalation: change role claim from "user" to "admin"

# Mass assignment
# Add additional parameters to API requests
# POST /api/profile {"name": "test", "isAdmin": true}

# Rate limiting
# Test for brute-force protection on login API
# Test for account lockout bypass
```

## Findings Template

| Finding | Severity | CVSS | Remediation |
|---------|----------|------|-------------|
| Hardcoded database credentials in binary | Critical | 9.1 | Use secure credential storage (DPAPI, vault) |
| DLL hijacking via writable app directory | High | 7.8 | Use full DLL paths, validate DLL signatures |
| Plaintext credentials in memory | High | 7.5 | Zero memory after use, use SecureString |
| No certificate pinning | Medium | 6.5 | Implement certificate pinning |
| Local SQLite DB with cleartext passwords | Critical | 9.0 | Use bcrypt/Argon2 hashing |
| Disabled SSL validation in code | High | 8.1 | Enable proper certificate validation |

## References

- dnSpy: https://github.com/dnSpy/dnSpy
- Procmon: https://learn.microsoft.com/en-us/sysinternals/downloads/procmon
- OWASP Thick Client Testing Guide: https://owasp.org/www-project-thick-client-top-10/
- Ghidra: https://ghidra-sre.org/
- Echo Mirage: https://sourceforge.net/projects/echomirage/

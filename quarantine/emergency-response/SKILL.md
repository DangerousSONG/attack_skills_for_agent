---
name: emergency-response
description: "Incident response methodology. Use when a target host is suspected of being compromised, when you need to hunt for backdoors, trojans, anomalous processes or anomalous accounts, or when you need to trace a security incident. Covers account auditing, process triage, network connection analysis, startup item and scheduled task checks, log analysis, and rootkit detection on both Linux and Windows"
zh-signals: "面向 Linux 与 Windows 主机的入侵排查与应急响应，覆盖账户、进程、网络与日志溯源。信号:应急响应,入侵排查,后门检测,日志分析,Rootkit"
when-to-use: >-
  Use when a host is suspected of compromise and you need incident triage, backdoor or
  malware hunting, anomalous process or account review, and forensic analysis on Linux
  or Windows.
metadata:
  tags: "emergency response,incident response,IR,host compromise triage,backdoor detection,rootkit,log analysis,process triage,account audit,linux,windows,blue team"
  category: "dfir"
---

# Incident Response Methodology

> Linux + Windows dual-platform intrusion triage playbook. Advance phase by phase, and only move to the next step after each step yields a clear conclusion.

---

## Phase 1: Initial Response Decision

```
Host suspected of being compromised?
├─ 1. Confirm the scope of the incident
│   ├─ Single host → triage directly
│   └─ Multiple/unknown hosts → isolate the network first, then triage host by host
├─ 2. Determine the operating system
│   ├─ Linux → Phase 2
│   └─ Windows → Phase 3
├─ 3. Confirm the current privileges
│   ├─ root/Administrator → full triage is possible
│   └─ Regular user → escalate privileges first or coordinate administrator access
└─ 4. Preserve evidence (before triage)
    ├─ Memory snapshot (if feasible)
    ├─ Disk image (critical servers)
    └─ Record the current timestamp and annotate the time on every later finding
```

**Key principles**:
- Collect first, analyze second, clean up last — never delete suspicious files during triage
- Record findings at every step to build a timeline
- Prioritize high-threat items: accounts → processes/network → persistence → files → logs

---

## Phase 2: Linux Incident Triage

### 2.1 Account Audit

**Triage checklist**:

```bash
# 1. Find privileged users (only root should have uid=0)
awk -F: '$3==0{print $1}' /etc/passwd

# 2. Find accounts that can log in remotely (accounts with a password hash)
awk '/\$1|\$6/{print $1}' /etc/shadow

# 3. Check for abnormal sudo grants (non-admins should not have ALL)
grep -v "^#\|^$" /etc/sudoers | grep "ALL=(ALL)"
cat /etc/sudoers.d/*

# 4. Check SSH authorized keys (attackers often plant public keys)
find / -name "authorized_keys" -exec ls -la {} \; -exec cat {} \;

# 5. Review recent login records
lastlog           # Last login time for all users
last              # Historical login/logout records
lastb             # Failed login records (brute-force traces)
```

**Triage criteria**:

| Finding | Risk level | Action |
|------|---------|------|
| Non-root user with uid=0 | High | Disable immediately: `usermod -L <user>` |
| Unknown user holding sudo ALL | High | Remove the sudoers entry |
| Unknown SSH public key | High | Record the key fingerprint, then delete it |
| Logon records at unusual hours | Medium | Correlate the IP for attribution |

### 2.2 Processes and Network

```bash
# 1. Check for anomalous network connections (focus on ESTABLISHED and LISTEN)
netstat -antlp | grep -E "ESTABLISHED|LISTEN"
# or
ss -antlp

# 2. Locate the process behind a suspicious connection by PID
ls -la /proc/<PID>/exe        # Executable backing the process
cat /proc/<PID>/cmdline       # Full command line
ls -la /proc/<PID>/fd         # Open file descriptors

# 3. Check for anomalous processes
ps aux --sort=-%cpu | head -20    # Sort by CPU usage (mining detection)
ps aux --sort=-%mem | head -20    # Sort by memory usage

# 4. Check for hidden processes (names starting with . or masquerading as kernel threads)
ps -ef | grep -E "^\S+\s+\d+.*\[.*\]" | grep -v "\[kworker"
```

**Triage criteria**:
- ESTABLISHED connections to non-business IPs → highly suspicious (C2 traffic)
- Process executable under /tmp, /dev/shm, /var/tmp → highly suspicious
- Process executable deleted (`/proc/PID/exe -> (deleted)`) → malicious process resident in memory

### 2.3 Startup Items and Scheduled Tasks

```bash
# 1. Check crontab (all users)
for user in $(cut -f1 -d: /etc/passwd); do
  crontab -l -u $user 2>/dev/null && echo "=== $user ==="
done
cat /etc/crontab
ls -la /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ /etc/cron.monthly/ /etc/cron.weekly/

# 2. Check systemd services (focus on unofficial and recently modified ones)
systemctl list-unit-files --type=service | grep enabled
find /etc/systemd/system/ /usr/lib/systemd/system/ -name "*.service" -mtime -7

# 3. Check rc.local and init.d
cat /etc/rc.local
ls -la /etc/init.d/
ls -la /etc/rc.d/rc*.d/ 2>/dev/null

# 4. Check bashrc/profile tampering
grep -r "curl\|wget\|python\|bash -i\|/dev/tcp" /etc/profile* /etc/bashrc /root/.bashrc /home/*/.bashrc 2>/dev/null
```

**Focus on**:
- Newly added cron jobs (correlate creation time against the intrusion time window)
- Service files in non-standard paths (/tmp, user home directories)
- Suspicious scripts inside rc.local

### 2.4 File System Triage

```bash
# 1. Find recently modified files (3 days as an example, adjust to the incident timeline)
find / -mtime -3 -type f -not -path "/proc/*" -not -path "/sys/*" | head -100

# 2. Find SUID/SGID files (a common privilege escalation backdoor)
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null

# 3. Check /tmp and hidden directories
ls -la /tmp/ /var/tmp/ /dev/shm/
find / -name ".. " -o -name "..." -o -name ".hidden" 2>/dev/null

# 4. Webshell detection (web server directories)
find /var/www/ -name "*.php" -mtime -7
grep -rl "eval\|system\|exec\|passthru\|shell_exec\|base64_decode" /var/www/ 2>/dev/null

# 5. Check for timestamp tampering (mtime inconsistent with ctime)
stat <suspicious-file>   # Compare the Modify and Change times
```

### 2.5 Log Analysis

| Log file | Purpose | How to view |
|----------|------|---------|
| /var/log/auth.log or /var/log/secure | SSH logins, sudo, su | `grep "Accepted\|Failed" /var/log/auth.log` |
| /var/log/wtmp | Login/logout records | `last -f /var/log/wtmp` |
| /var/log/btmp | Failed logins | `lastb -f /var/log/btmp` |
| /var/log/cron | Scheduled task execution records | `cat /var/log/cron` |
| /var/log/messages or /var/log/syslog | System events | `grep -i "error\|warning\|fail" /var/log/messages` |
| ~/.bash_history | Command history | `cat /root/.bash_history` |

```bash
# Brute-force detection: count failed login IPs
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -20

# Successful logon triage: watch for unusual IPs and time slots
grep "Accepted" /var/log/auth.log | awk '{print $1,$2,$3,$9,$11}'

# Privilege escalation detection
grep "sudo:" /var/log/auth.log | grep -v "session opened\|session closed"
```

### 2.6 Rootkit Detection

```bash
# Method 1: chkrootkit
apt install chkrootkit -y   # or yum install chkrootkit
chkrootkit

# Method 2: rkhunter
apt install rkhunter -y     # or yum install rkhunter
rkhunter --update
rkhunter --check --sk

# Method 3: manual checks (when the tooling cannot be trusted)
# Compare system command hashes (against a known clean baseline)
md5sum /usr/bin/ps /usr/bin/netstat /usr/bin/ls /usr/bin/find /usr/bin/top
# Check for LD_PRELOAD hijacking
echo $LD_PRELOAD
cat /etc/ld.so.preload
# Inspect kernel modules
lsmod | grep -v "^Module"
```

---

## Phase 3: Windows Incident Triage

### 3.1 Account Audit

```cmd
:: 1. View the current logon sessions
query user

:: 2. List all users and the members of the administrators group
net user
net localgroup administrators

:: 3. Check for hidden/cloned accounts
:: Hidden account names end with $
wmic useraccount list full
:: Compare the registry SAM against the net user output
:: HKLM\SAM\SAM\Domains\Account\Users (requires SYSTEM privileges)

:: 4. Log off suspicious sessions
logoff <SessionID>
```

**Supporting tools**:
- D-Shield: detect hidden and cloned accounts
- Review SID history: `wmic useraccount get name,sid` — administrators whose SID does not end in 500/501 must be verified

### 3.2 Processes and Network

```cmd
:: 1. List all network connections and the owning processes
netstat -ano | findstr "ESTABLISHED LISTENING"

:: 2. Look up process information by PID
tasklist /FI "PID eq <PID>" /V
wmic process where processid=<PID> get name,executablepath,commandline

:: 3. Check for suspicious processes
tasklist /V
wmic process get name,processid,executablepath,commandline /format:list

:: 4. Review the proxy configuration (check whether it was tampered with)
REG QUERY "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings"

:: 5. View the routing table
→route print
```

**Triage criteria**:
- Executable path under %TEMP%, %APPDATA%, or the user's Downloads folder → suspicious
- Process name mimics a system process (e.g. svchost.exe outside C:\Windows\System32) → highly suspicious
- ESTABLISHED connections to unusual outbound IPs → correlate with threat intelligence

### 3.3 Startup Items and Services

```cmd
:: 1. Check registry startup items
REG QUERY "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
REG QUERY "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
REG QUERY "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
REG QUERY "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"

:: 2. Check scheduled tasks
schtasks /query /fo LIST /v

:: 3. Check the Startup folders
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
dir "%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup"

:: 4. Check services (focus on non-standard and recently created ones)
wmic service list brief
wmic service get name,displayname,pathname,startmode | findstr /i "auto"

:: 5. Check startup entries
wmic startup get command,caption
```

**Focus on**:
- Run/RunOnce entries pointing at temporary directories or non-standard paths
- Scheduled tasks that execute PowerShell, cmd /c, mshta, and similar
- Service executable paths containing spaces without quotes (Unquoted Service Path)

### 3.4 File System Triage

```cmd
:: 1. List recently accessed files
dir %USERPROFILE%\Recent /a /o:-d

:: 2. Check the temporary directories
dir %TEMP% /a /o:-d
dir %SYSTEMROOT%\Temp /a /o:-d

:: 3. Check the browser download directories
dir "%USERPROFILE%\Downloads" /a /o:-d

:: 4. Inspect the Recycle Bin
dir C:\$Recycle.Bin /s /a

:: 5. Check for ADS (alternate data streams, which can hide malicious code)
dir /r <suspicious-directory>
```

**Check prefetch files**:
- Path: `C:\Windows\Prefetch\`
- Recovers program execution history even after the executable has been deleted

### 3.5 Log Analysis

Open Event Viewer: `eventvwr.msc`

**Log locations**:

| Log type | Default path | What to look for |
|----------|---------|---------|
| Security log | `%SystemRoot%\System32\Winevt\Logs\Security.evtx` | Logon events, account management, privileged use |
| System log | `%SystemRoot%\System32\Winevt\Logs\System.evtx` | Service installs, driver loads, system errors |
| Application log | `%SystemRoot%\System32\Winevt\Logs\Application.evtx` | Application crashes, program errors |

**Key Event IDs**:

| Event ID | Meaning | Triage value |
|----------|------|---------|
| 4624 | Successful logon | Determine the attack method together with the logon type |
| 4625 | Failed logon | Brute-force traces |
| 4634 | Logoff | Session duration analysis |
| 4672 | Special privileges assigned | Administrator logon events |
| 4720 | User account created | Backdoor account detection |
| 7045 | Service installed | Persistence/lateral movement traces |

**Logon type reference**:

| Type | Description | Common scenario |
|------|------|---------|
| 2 | Interactive | Local console logon |
| 3 | Network | Shared folders, PsExec |
| 4 | Batch | Scheduled task |
| 5 | Service | Service start |
| 7 | Unlock | Screen saver unlock |
| 10 | RemoteInteractive | RDP remote desktop |

```powershell
# PowerShell: query the security log (filter failed logons)
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4625} |
  Select-Object TimeCreated,@{N='IP';E={$_.Properties[19].Value}} |
  Group-Object IP | Sort-Object Count -Descending

# Query newly created account events
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4720} |
  Format-List TimeCreated,Message
```

---

## Phase 4: Attribution and Hardening

### 4.1 Timeline Reconstruction

```
Collect all findings → sort by time → build the attack chain:
1. Initial compromise time (the earliest anomaly)
2. Attack path (how it spread from the entry point)
3. Persistence mechanisms (which backdoors were left behind)
4. Data exfiltration (whether large volumes of data left the host)
```

### 4.2 IOC Extraction

Extract the following indicators during triage for threat intelligence correlation:

| IOC type | Source | Use |
|----------|------|------|
| Malicious IP/domain | Network connections, logs | Blocking + intelligence lookup |
| File hash | MD5/SHA256 of suspicious files | VirusTotal/Venustech lookup |
| Attacker account | Newly created or anomalous accounts | Lateral movement triage across the internal network |
| Malicious file path | File system triage | Sweep the whole estate for identical files |

### 4.3 Hardening Recommendations

**Immediate actions**:
- Change the password of every affected account
- Remove the persistence mechanisms planted by the attacker (scheduled tasks, services, startup items, SSH keys)
- Block malicious IPs (firewall/security group)
- Patch the vulnerability exploited for the initial access

**Long-term hardening**:
- Enable centralized log collection (prevents local logs from being wiped)
- Deploy HIDS/EDR monitoring
- Enforce the principle of least privilege
- Audit accounts and services regularly

## Notes

- Never reboot the server during triage — in-memory malicious processes and network connection details will be lost
- Never delete suspicious files outright — back them up for evidence, then clean them up
- If system commands (ps/netstat/ls) are suspected of being replaced (rootkit), triage with a statically linked busybox or with tools copied from a trusted source
- Logs may have been cleared or tampered with by the attacker — cross-validate across multiple sources (system logs + network device logs + application logs)

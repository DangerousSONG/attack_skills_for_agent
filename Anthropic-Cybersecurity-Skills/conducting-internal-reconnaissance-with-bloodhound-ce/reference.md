# conducting-internal-reconnaissance-with-bloodhound-ce — 详细参考（由 SKILL.md 拆分）

### Phase 4: Custom Cypher Queries
1. Execute custom Cypher queries in the BloodHound CE search bar:
   ```cypher
   // Find shortest path from owned principals to Domain Admins
   MATCH p=shortestPath((n {owned:true})-[*1..]->(m:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
   RETURN p

   // Find Kerberoastable users with path to DA
   MATCH (u:User {hasspn:true})
   MATCH p=shortestPath((u)-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
   RETURN p

   // Find computers with sessions of DA members
   MATCH (c:Computer)-[:HasSession]->(u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
   RETURN c.name, u.name

   // Find ACL-based attack paths (GenericAll, WriteDACL, GenericWrite)
   MATCH p=(u:User)-[:GenericAll|GenericWrite|WriteDacl|WriteOwner|ForceChangePassword*1..]->(t)
   WHERE u.owned = true
   RETURN p

   // Find users who can DCSync
   MATCH (u)-[:MemberOf*0..]->()-[:DCSync|GetChanges|GetChangesAll*1..]->(d:Domain)
   RETURN u.name, d.name

   // Find computers with LAPS but readable by non-admins
   MATCH (c:Computer {haslaps:true})
   MATCH p=(u:User)-[:ReadLAPSPassword]->(c)
   RETURN p
   ```

### Phase 5: Attack Path Prioritization
1. Score identified attack paths by:
   - Number of hops (shorter = higher priority)
   - Stealth requirements (avoid noisy techniques)
   - Tool availability for each hop
   - Likelihood of detection at each step
2. Create an execution plan for the highest-priority paths
3. Identify required tools for each step in the chain
4. Plan OPSEC considerations for each technique

## Tools and Resources

| Tool | Purpose | Platform |
|------|---------|----------|
| BloodHound CE | Web-based graph analysis platform | Docker |
| SharpHound v2 | AD data collection (.NET, for CE) | Windows |
| BloodHound.py | AD data collection (Python) | Linux |
| AzureHound | Azure AD / Entra ID data collection | Cross-platform |
| PlumHound | Automated BloodHound reporting | Python |
| BloodHound Query Library | Community Cypher query repository | Web |

## Key Attack Path Types

| Path Type | Description | Example |
|-----------|-------------|---------|
| ACL Abuse | Exploit misconfigured ACLs | GenericAll on DA group |
| Kerberoasting | Crack service account passwords | SPN account → DA |
| AS-REP Roasting | Attack accounts without pre-auth | No-preauth user → password crack |
| Delegation Abuse | Exploit unconstrained/constrained delegation | Computer → impersonate DA |
| GPO Abuse | Modify GPOs applied to privileged OUs | GPO write → code execution on DA |
| Session Hijack | Leverage DA sessions on compromised hosts | Admin session → token theft |

## Validation Criteria

- [ ] BloodHound CE deployed and accessible
- [ ] SharpHound v2 data collected from all domains in scope
- [ ] Data successfully imported into BloodHound CE
- [ ] Owned principals marked in the interface
- [ ] Shortest paths to Domain Admin identified
- [ ] ACL-based attack paths documented
- [ ] Kerberoastable and AS-REP roastable accounts listed
- [ ] Custom Cypher queries executed for advanced analysis
- [ ] Attack paths prioritized by feasibility and stealth
- [ ] Report generated with all identified paths and evidence

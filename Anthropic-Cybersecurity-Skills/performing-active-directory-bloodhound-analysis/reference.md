# performing-active-directory-bloodhound-analysis — 详细参考（由 SKILL.md 拆分）

### Pre-Built Queries (Most Critical)

```cypher
-- Find all Domain Admins
MATCH (n:Group) WHERE n.name =~ '(?i).*domain admins.*' RETURN n

-- Shortest path from owned user to Domain Admin
MATCH p=shortestPath((u:User {owned:true})-[*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'}))
RETURN p

-- Find Kerberoastable users with path to DA
MATCH (u:User {hasspn:true})
MATCH p=shortestPath((u)-[*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'}))
RETURN p

-- Find AS-REP Roastable users
MATCH (u:User {dontreqpreauth:true}) RETURN u.name, u.displayname

-- Users with DCSync rights
MATCH p=(n1)-[:MemberOf|GetChanges*1..]->(u:Domain)
MATCH p2=(n1)-[:MemberOf|GetChangesAll*1..]->(u)
RETURN n1.name

-- Find computers where Domain Users are local admin
MATCH p=(m:Group {name:'DOMAIN USERS@CORP.LOCAL'})-[:AdminTo]->(c:Computer) RETURN p

-- Find unconstrained delegation computers
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

-- Find constrained delegation abuse paths
MATCH (u) WHERE u.allowedtodelegate IS NOT NULL RETURN u.name, u.allowedtodelegate

-- GPO abuse paths
MATCH p=(g:GPO)-[r:GpLink]->(ou:OU)-[r2:Contains*1..]->(c:Computer)
RETURN p LIMIT 50

-- Find all sessions on high-value targets
MATCH (c:Computer)-[:HasSession]->(u:User)-[:MemberOf*1..]->(g:Group {highvalue:true})
RETURN c.name, u.name, g.name
```

### Custom Cypher Queries

```cypher
-- Find users with GenericAll on other users (password reset path)
MATCH p=(u1:User)-[:GenericAll]->(u2:User) RETURN u1.name, u2.name

-- Find WriteDACL paths (ACL abuse)
MATCH p=(n)-[:WriteDacl]->(m) WHERE n<>m RETURN p LIMIT 50

-- Find AddMember rights to privileged groups
MATCH p=(n)-[:AddMember]->(g:Group {highvalue:true}) RETURN n.name, g.name

-- Map trust relationships
MATCH p=(d1:Domain)-[:TrustedBy]->(d2:Domain) RETURN d1.name, d2.name

-- Find service accounts with admin access
MATCH (u:User {hasspn:true})-[:AdminTo]->(c:Computer) RETURN u.name, c.name
```

## Step 4: Common Attack Paths

### Path 1: Kerberoasting to DA
```
User (owned) -> Kerberoastable SVC Account -> Crack Hash -> SVC is AdminTo Server ->
Server HasSession DA -> Steal Token -> Domain Admin
```

### Path 2: ACL Abuse Chain
```
User (owned) -> GenericAll on User2 -> Reset Password -> User2 MemberOf ->
IT Admins -> AdminTo DC -> Domain Admin
```

### Path 3: Unconstrained Delegation
```
User (owned) -> AdminTo Server (Unconstrained Delegation) ->
Coerce DC Auth (PrinterBug/PetitPotam) -> Capture TGT -> DCSync
```

### Path 4: GPO Abuse
```
User (owned) -> GenericWrite on GPO -> Modify GPO -> Scheduled Task on OU Computers ->
Code Execution as SYSTEM
```

## Step 5: Remediation Recommendations

| Finding | Risk | Remediation |
|---|---|---|
| Kerberoastable DA | Critical | Use gMSA, rotate passwords, AES-only |
| Unconstrained Delegation | Critical | Migrate to constrained/RBCD delegation |
| Domain Users local admin | High | Remove DA from local admin, use LAPS |
| Excessive ACL permissions | High | Audit and reduce GenericAll/WriteDACL |
| Stale admin sessions | Medium | Implement session cleanup, restrict RDP |
| Cross-domain trust abuse | High | Review trust direction and SID filtering |

## References

- BloodHound GitHub: https://github.com/BloodHoundAD/BloodHound
- BloodHound CE: https://github.com/SpecterOps/BloodHound
- SharpHound: https://github.com/BloodHoundAD/SharpHound
- MITRE ATT&CK S0521: https://attack.mitre.org/software/S0521/
- SpecterOps BloodHound Documentation: https://bloodhound.readthedocs.io/

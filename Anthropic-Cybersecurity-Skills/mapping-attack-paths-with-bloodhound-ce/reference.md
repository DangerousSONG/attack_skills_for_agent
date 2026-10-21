# mapping-attack-paths-with-bloodhound-ce — 详细参考（由 SKILL.md 拆分）

# Start a file-upload job, then PUT the collector ZIP/JSON to it
JOB=$(curl -s -X POST http://localhost:8080/api/v2/file-upload/start \
  -H "Authorization: Bearer $TOKEN" | python -c "import sys,json;print(json.load(sys.stdin)['data']['id'])")
curl -s -X PUT "http://localhost:8080/api/v2/file-upload/$JOB" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/zip' \
  --data-binary @C:/Temp/BloodHound.zip
curl -s -X POST "http://localhost:8080/api/v2/file-upload/$JOB/end" \
  -H "Authorization: Bearer $TOKEN"
```

### Step 5: Mark owned principals
In the UI, search for each compromised account/computer, open the node, and toggle **Mark as Owned**. Owned principals seed pathfinding queries (`{owned:true}`).

### Step 6: Run built-in analysis queries
Open the **Cypher** tab or use the pre-built queries in the search panel:

- Shortest Path to Domain Admins
- Kerberoastable accounts with a path to high value
- AS-REP roastable users
- Principals with DCSync rights
- ADCS misconfigurations (ESC1-ESC8 edges in CE)
- Computers with unconstrained delegation

### Step 7: Author custom Cypher for bespoke paths
Use Cypher for paths the built-ins do not cover, including hybrid AD-to-Entra chains.

```cypher
// Shortest path from any owned principal to Domain Admins
MATCH p=shortestPath((n {owned:true})-[*1..]->(g:Group))
WHERE g.objectid ENDS WITH "-512"
RETURN p

// Kerberoastable users (SPN set) with a path to Domain Admins
MATCH (u:User {hasspn:true})
MATCH p=shortestPath((u)-[*1..]->(g:Group))
WHERE g.objectid ENDS WITH "-512"
RETURN p

// Principals who can DCSync the domain
MATCH (n)-[:MemberOf*0..]->()-[:DCSync|GetChanges|GetChangesAll*1..]->(d:Domain)
RETURN n.name, d.name

// ACL abuse from owned principals (GenericAll/WriteDacl/WriteOwner/ForceChangePassword)
MATCH p=(n {owned:true})-[:GenericAll|GenericWrite|WriteDacl|WriteOwner|ForceChangePassword*1..]->(t)
RETURN p

// Hybrid: on-prem user synced to an Entra account holding a privileged directory role
MATCH p=(u:User)-[:SyncedToEntraUser]->(:AZUser)-[:AZHasRole|AZGlobalAdmin*1..]->(r)
RETURN p
```

### Step 8: Prioritize and document
Rank paths by hop count, stealth (avoid noisy edges like HasSession requiring host touch), and tooling availability. Record each path with the principals, edges, required actions, and a remediation note (e.g., remove the abusable ACL, tier the account).

## Tools and Resources

| Tool | Purpose | Source |
|------|---------|--------|
| BloodHound CE | Graph attack-path platform (Docker stack) | https://github.com/SpecterOps/BloodHound |
| SharpHound (CE) | On-prem AD collector | https://github.com/SpecterOps/SharpHound |
| AzureHound | Entra ID / Azure RM collector | https://github.com/SpecterOps/AzureHound |
| bloodhound-ce-python | Linux Python AD collector | https://github.com/dirkjanm/BloodHound.py |
| CE Quickstart | Official deployment docs | https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart |
| BloodHound Cypher refs | Edge/query documentation | https://bloodhound.specterops.io/ |

## Key Edge / Path Types

| Edge / Path | Meaning | Escalation example |
|-------------|---------|--------------------|
| MemberOf | Group membership | Nested group reaches Domain Admins |
| GenericAll / WriteDacl | Full/ACL control over an object | Reset a privileged user's password |
| ForceChangePassword | Can reset another principal's password | Take over a Tier-0 account |
| HasSession | A user is logged into a computer | Steal a DA token from a compromised host |
| ADCSESC1..ESC8 | Certificate services misconfig | Enroll a cert as a privileged principal |
| SyncedToEntraUser / AZGlobalAdmin | Hybrid identity edges | On-prem foothold -> cloud Global Admin |

## Validation Criteria

- [ ] BloodHound CE deployed and reachable; default admin password rotated
- [ ] SharpHound data collected from all in-scope domains
- [ ] AzureHound JSON collected for the in-scope tenant (if hybrid/cloud in scope)
- [ ] Both datasets ingested successfully (no failed upload jobs)
- [ ] Compromised principals marked as Owned
- [ ] Shortest paths to Domain Admins / Global Administrator identified
- [ ] ADCS and ACL-abuse paths enumerated
- [ ] At least one custom Cypher query (including a hybrid query where applicable) executed
- [ ] Paths prioritized by hops/stealth and documented with remediation

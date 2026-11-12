---
name: windows-ad
description: Use for authorized Active Directory and Windows identity attacks including Kerberos, AD CS, BloodHound paths, NTLM relay, and domain privilege escalation research.
zh-signals: "面向授权的 Active Directory 与 Windows 身份攻击，覆盖 Kerberos、AD CS、BloodHound、NTLM 中继与域提权。信号:Active Directory,Kerberos,AD CS,BloodHound,NTLM中继"
when-to-use: "Use for authorized AD and Windows identity attack testing — Kerberos abuse, AD CS, BloodHound paths, NTLM relay, or domain privilege escalation research."
---

# Windows / Active Directory Security

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../field-journal/precedent-pentest.md`
2. `NOW`: **domain/AD testing must have an explicit authorized scope** (including DCs, and whether poisoning/relay is allowed)
3. `NOW`: case-init; write down the network_profile and the prohibited actions
4. `NEXT`: tool-index (impacket/certipy/bloodhound and similar tools are often invoked manually)
5. `ACT`: start with identity enumeration and the BloodHound graph, do not jump to destructive exploitation

## Applicable Scenarios

- Domain penetration, Kerberoasting, AS-REP, delegation
- AD CS (ESC1–ESC8 and similar) certificate attacks
- BloodHound / SharpHound attack paths
- NTLM Relay / Coercer forced authentication
- Local privilege escalation into domain paths (Potato and similar as pivots)

## Relationship to attack-chain

- **Multi-stage path from external network to domain controller** → PRIMARY can still be `attack-chain/`, this skill is the **AD specialization**
- **Already in-domain and focused on identity** → PRIMARY = this skill

## Workflow

### 1. Enumeration

```bash
# Sample Impacket / built-in commands (credentials and authorization required)
nxc smb <range> -u user -p pass
bloodhound-python -d domain.local -u user -p pass -c All -ns <DC>
```

### 2. Common paths (map first, then shoot)

```text
□ Kerberoast / AS-REP → offline cracking
□ ACL abuse (GenericAll/WriteDacl)
□ Delegation (unconstrained/constrained/resource-based)
□ AD CS template misconfiguration → Certipy
□ Relay: LLMNR/NBT-NS + ntlmrelayx (confirm authorization)
```

### 3. Credentials and lateral movement

```text
□ secretsdump / lsassy / mimikatz (strict authorization and cleanup)
□ PtH / PtT / Golden Ticket only within the authorized red team scope
□ Record Evidence at every step; confirm with the user before high-risk actions
```

## Toolchain

| Tool | Purpose |
|------|------|
| BloodHound / SharpHound | Path mapping |
| Certipy | AD CS |
| Impacket / NetExec | Lateral movement and enumeration |
| Rubeus / Mimikatz | Tickets and credentials (authorized) |
| Coercer / Responder | Forced authentication / poisoning |

## References

- `references/ad-attack-paths.md`
- `../pentest-tools/references/network-attack-defense.md`
- `../attack-chain/`
- seeds: `field-journal/seed-005_ad-certipy-esc1.md` `seed-007_ntlm-relay-coercer.md` `seed-013_kerberoasting-spn.md`

## Routing Context

**Upstream**: MASTER R24  
**Downstream**: reporting `docs-generator`; for EDR research `edr-bypass-re`  
**MUST NOT**: DCSync without authorization / Golden Ticket attacks on production

## Task Completion Self-Check

- [ ] Did you build the graph/enumerate before exploiting?
- [ ] Did you record reproducible commands and redact sensitive data?
- [ ] Did you respect the scope prohibitions?
- [ ] Checklist?
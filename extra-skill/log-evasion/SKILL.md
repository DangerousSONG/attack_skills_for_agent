---
name: log-evasion
description: "Log analysis and log evasion methodology. Understand how the blue team tracks attacker behavior through logs (SIEM/Event Log/Syslog), and how the red team evades logging or precisely removes traces. Use when you need to design trace-free operations or analyze log monitoring coverage"
zh-signals: "分析蓝队日志检测覆盖并设计红队日志规避与痕迹清理策略。信号:日志逃逸,Event Log,Sysmon,SIEM,痕迹清除"
when-to-use: >-
  Use when designing low-trace operations or assessing log monitoring coverage across Windows Event Log, Syslog, and SIEM.
metadata:
  tags: "log,evasion,event-log,syslog,siem,etw,anti-log,trace-cleanup,audit,detection"
  category: "dfir"
  mitre_attack: "T1070.001,T1070.002,T1562.002,T1562.001,T1562.006"
---

# Log Analysis and Log Evasion

> **Core principle**: the best anti-log strategy is to never generate logs in the first place, rather than deleting them afterwards

## ⛔ Further Reading

- Detailed Windows Event Log ID mapping and clearing → [references/windows-eventlog.md](references/windows-eventlog.md)
- Linux audit/syslog bypass techniques → [references/linux-log-evasion.md](references/linux-log-evasion.md)

---

## Part A: Blue Team Perspective — Key Log Detection Points

### Key Windows Event IDs

| Event ID | Log Source | Meaning | Red Team Action Triggered |
|----------|--------|------|-------------|
| 4624 | Security | Successful logon | PTH/PTT/RDP |
| 4625 | Security | Failed logon | Password spraying |
| 4648 | Security | Logon with explicit credentials | runas/PsExec |
| 4672 | Security | Special privileges assigned | Privilege escalation |
| 4688 | Security | New process created | Tool execution |
| 4698 | Security | Scheduled task created | Persistence |
| 4720 | Security | User account created | Backdoor account |
| 5140 | Security | Network share accessed | Lateral movement |
| 5156 | Security | Network connection | C2 communication |
| 7045 | System | Service installed | Persistence/PsExec |
| 1102 | Security | Log cleared | ⛔ Anti-forensics exposure! |
| 4104 | PowerShell | Script block logging | PS attack tooling |
| 4103 | PowerShell | Module logging | PS command execution |
| 1 | Sysmon | Process create (with hash) | All tool execution |
| 3 | Sysmon | Network connection | C2 communication |
| 8 | Sysmon | CreateRemoteThread | Process injection |
| 10 | Sysmon | Process access | LSASS dump |
| 11 | Sysmon | File created | Tool written to disk |

### Key Linux Logs

| Log | Location | Contents |
|------|------|---------|
| auth.log/secure | /var/log/ | SSH logins, sudo, su |
| wtmp | /var/log/ | Logon/logoff records |
| btmp | /var/log/ | Failed logins |
| lastlog | /var/log/ | Last login time |
| audit.log | /var/log/audit/ | auditd rule matches |
| syslog/messages | /var/log/ | System events |
| journal | /var/log/journal/ | systemd logs |
| .bash_history | ~/ | Command history |

### Common SIEM Detection Rules (that you need to bypass)

```
Sigma rule examples (deployed by the blue team):
├─ Process injection: Sysmon EventID 8 (CreateRemoteThread to lsass)
├─ Credential dump: EventID 10 (OpenProcess to lsass)
├─ Lateral movement: EventID 4648 + 4624 LogonType 3
├─ Persistence: EventID 7045 (new service) / 4698 (new scheduled task)
├─ Log clearing: EventID 1102 / 104 → high-priority alert!
└─ PowerShell: EventID 4104 containing "IEX" / "Invoke-" / "-enc"
```

---

## Part B: Red Team Perspective — Log Evasion

### Strategy 1: Prevent Logs From Being Generated (Optimal)

```
Windows:
├─ Disable ETW Provider → block PowerShell/AMS logging
│   patch ntdll!EtwEventWrite → ret
│   or NtTraceEvent hook
├─ Turn off ScriptBlock Logging
│   reg: HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging → 0
├─ Use .NET to avoid PowerShell logging
│   Call .NET directly from C# → does not go through the PS engine → no 4104
├─ Thread detach from ETW
│   patch the ETW context of the current thread → no more events generated
└─ Sysmon bypass
    unload sysmon driver / patch the event callback

Linux:
├─ Before the operation: unset HISTFILE; export HISTSIZE=0; export HISTFILESIZE=0
├─ Or: set +o history
├─ Prefix commands with a space (bash HISTCONTROL=ignorespace)
├─ kill -9 auditd (requires root, generates a stop log)
└─ auditctl -e 0 (disable auditing, more covert)
```

### Strategy 2: Bypass Logging (Without Triggering Detection Rules)

```
Bypass Sysmon:
├─ Process injection: avoid CreateRemoteThread → use APC/Callback/Early Bird
├─ LSASS access: avoid direct OpenProcess → use handle duplication/MiniDump
├─ Network: use raw sockets → Sysmon EID 3 may not capture them
└─ Files: use existing file names/paths → do not trigger new-file rules

Bypass PowerShell logging:
├─ Downgrade the attack: powershell -version 2 (no ScriptBlock logging)
├─ Use C#/.NET: call via reflection directly → no PS logging
├─ AMSI bypass → prevent script content from being recorded
└─ Use WMI/COM → does not go through the PowerShell engine

Bypass 4688 process creation:
├─ Process name masquerading: execute a copy of a legitimate program
├─ Use LOLBins: rundll32/mshta/certutil → legitimate processes
├─ Parent process spoofing: set PPID to a normal process
└─ Command line obfuscation: environment variable expansion, special characters
```

### Strategy 3: Precise Clearing (Remediation After Logs Exist)

```
⛔ NEVER empty the entire log → EventID 1102 triggers an immediate alert!
⛔ ALWAYS delete specific entries precisely

Windows precise clearing:
├─ Method 1: stop the EventLog service → modify the .evtx file → restart the service
│   net stop eventlog (requires SYSTEM)
│   Modify the evtx binary structure to delete specific records
│   net start eventlog
├─ Method 2: Danderspritz eventlogedit (NSA tool)
│   Precisely delete records of a given EventID and repair the file checksum
├─ Method 3: Invoke-Phant0m
│   Kill all threads of the EventLog service → the service runs but writes no logs
└─ Method 4: MiniNT registry key
    HKLM\SYSTEM\CurrentControlSet\Control\MiniNT → blocks log writes

Linux precise clearing:
├─ auth.log: sed -i '/specific-IP/d' /var/log/auth.log
├─ wtmp: utmpdump /var/log/wtmp > tmp.txt
│         edit out the specific lines
│         utmpdump -r < tmp.txt > /var/log/wtmp
├─ lastlog: use a tool to modify the lastlog record of a specific user
├─ audit.log: confirm the record with aureport → delete with sed
└─ journal: journalctl --vacuum-time=1s (⛔ clears everything)
```

### Strategy 4: Countering Real-Time Log Forwarding

```
Modern enterprises forward logs to a SIEM in real time → local deletion is useless!

Countermeasures:
├─ Never generate logs in the first place (Strategy 1) → optimal
├─ Bypass Sysmon/ETW (Strategy 2) → do not generate the specific events
├─ Use an SSH tunnel/DNS tunnel → blend into legitimate traffic in network logs
├─ Choose the timing of operations → early morning/holidays → slow SOC response
└─ Understand SIEM rule thresholds → operate below the alerting threshold
    Example: password spray lockout threshold is 5 attempts → try only 2 per user
```

## Comparison Table

| Blue Team Monitoring | Trigger Condition | Red Team Countermeasure |
|----------|---------|---------|
| EventID 4624 | Any logon | Normal hours + legitimate usernames |
| EventID 4688 | New process | LOLBins / PPID spoofing |
| EventID 4104 | PS script | .NET / AMSI bypass / PS v2 |
| Sysmon EID 1 | Process + hash | Modify known allowlisted programs |
| Sysmon EID 8 | Remote thread | APC / Timer callback |
| Sysmon EID 10 | Process access | Handle duplicate |
| auditd | Syscall auditing | Disable auditd / direct syscall |
| Network logs | Connection records | Domain fronting / CDN / legitimate services |

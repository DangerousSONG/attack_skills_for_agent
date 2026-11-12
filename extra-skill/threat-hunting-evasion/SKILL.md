---
name: threat-hunting-evasion
description: "Threat hunting principles and evasion methodology. Understand how the blue team hunts proactively (hypothesis-driven / IOC-driven / analytics-driven), and how the red team designs behavior to stay undetected. Use when you need to assess whether your own operations could be discovered by threat hunting"
zh-signals: "理解威胁猎杀原理并设计规避检测的行为。信号:威胁猎杀,检测规避,sigma,yara,edr"
when-to-use: "Use when assessing whether your operations could be discovered by threat hunting, or when studying Sigma/YARA rules and EDR detection logic for evasion."
metadata:
  tags: "threat-hunting,detection,evasion,sigma,yara,hypothesis,detection-rules"
  category: "threat-intel"
  mitre_attack: "T1562,T1070,T1036,T1027,T1055"
---

# Threat Hunting Principles and Evasion

> **The red team must understand how hunters think in order to stay ahead of them**

## Deep Reference (Load on Demand)

The references below are large. Do not pre-read them when you only need the general hunting methodology; open a specific file only when the task explicitly involves rule dissection, EDR logic, or evasion validation.

- Need to analyze Sigma/YARA rules, rule bypasses, or detection condition decomposition -> [references/detection-rules-bypass.md](references/detection-rules-bypass.md)
- Need to analyze mainstream EDR detection logic, telemetry sources, or behavior chains -> [references/edr-detection-logic.md](references/edr-detection-logic.md)

---

## Part A: Threat Hunting Methodology (Blue Team Perspective)

### Three Hunting Paradigms

```
1. Hypothesis-driven
   "If APT29 breaches us, they will use a PowerShell downloader"
   -> Search: EventID 4104 + "IEX" + "DownloadString"

2. IOC-driven
   "Threat intelligence shows this IP is C2"
   -> Search: all hosts connecting to that IP

3. Analytics-driven
   "A normal user does not run whoami at 3 AM"
   -> Search: unusual time + reconnaissance command combination
```

### Common Hunting Queries (That You Need to Evade)

```
# Sigma rule examples

# 1. Suspicious PowerShell download
title: Suspicious PowerShell Download
detection:
  selection:
    EventID: 4104
    ScriptBlockText|contains:
      - 'IEX'
      - 'Invoke-Expression'
      - 'DownloadString'
      - 'Net.WebClient'

# 2. LSASS access
title: LSASS Memory Access
detection:
  selection:
    EventID: 10
    TargetImage: 'C:\Windows\System32\lsass.exe'
    GrantedAccess|contains:
      - '0x1010'
      - '0x1410'

# 3. Abnormal parent-child process
title: Suspicious Parent-Child
detection:
  selection:
    ParentImage|endswith: '\outlook.exe'
    Image|endswith:
      - '\cmd.exe'
      - '\powershell.exe'
      - '\mshta.exe'

# 4. Enumeration command combination (3+ recon commands within 5 minutes)
title: Reconnaissance Commands
detection:
  selection:
    CommandLine|contains:
      - 'whoami'
      - 'net user'
      - 'net group'
      - 'ipconfig'
      - 'systeminfo'
    timeframe: 5m
    condition: selection | count() >= 3
```

### Hunting Data Sources

| Data Source | Hunting Target |
|--------|---------|
| Sysmon | Process creation/injection/network/file |
| PowerShell Logging | Script execution content |
| Windows Security | Authentication/permissions/policy |
| DNS Logs | C2 domains/DGA/tunneling |
| Proxy/Firewall | Anomalous outbound connections/large transfers |
| EDR Telemetry | Behavior chains |
| NetFlow | Traffic pattern anomalies |
| LDAP Logs | AD enumeration |

---

## Part B: Red Team Perspective — Evading Threat Hunting

### Strategy 1: Do Not Match Known Detection Rules

```
Analyze public rules in Sigma repositories -> ensure your activity does not hit them

Common rule bypasses:
├─ "IEX(DownloadString)" detection
│   Bypass: call .NET WebClient directly, stay out of PowerShell
│   Or: use certutil / bitsadmin / curl instead
│
├─ "cmd.exe spawned by outlook.exe" detection
│   Bypass: execute through COM objects, spawn no child process
│   Or: call WMI via VBA -> wmiprvse.exe becomes the parent process
│
├─ "lsass.exe access" detection
│   Bypass: use handle duplication (no direct OpenProcess)
│   Or: use NanoDump's MiniDumpWriteDump alternative
│
└─ "Reconnaissance command burst" detection
    Bypass: spread execution out (10+ minutes between each command)
    Or: use WMI/LDAP queries instead of command line tools
```

### Strategy 2: Normalize Behavior Patterns

```
Principle: make your activity look like normal business activity

Network behavior normalization:
├─ Conduct C2 traffic during business hours (9am-6pm)
├─ Match heartbeat intervals to normal HTTP polling (not too regular)
├─ Match traffic volume to normal API calls
├─ Use the target's existing SaaS domains (mimic Slack/Teams API traffic)
└─ Avoid bulk data transfers in the middle of the night

Host behavior normalization:
├─ Do not run multiple reconnaissance commands in a short window
├─ Use tools already present in the target environment (LOLBins)
├─ Make process names/paths match legitimate programs
├─ Do not create obviously unusual usernames (admin123/test)
└─ Mimic human pacing between operations
```

### Strategy 3: YARA Rule Bypass

```
YARA matching principle: byte sequences + conditional logic

Bypass approaches:
├─ String signatures -> XOR/AES encrypt the key strings
├─ Byte sequences -> use a different compiler / compilation options
├─ File structure -> modify the PE header / Rich header
├─ Entry point pattern -> change the stub / use a legitimate packer
└─ Behavior signatures -> change the order/manner of API calls

Verification:
yara -r sigma_rules/ my_payload.exe  # self-test before deploying
```

### Strategy 4: EDR Behavior Detection Evasion

```
Modern EDR looks beyond signatures, it looks at behavior chains:
├─ Process Chain: email->CMD->PowerShell->network connection = malicious
├─ Memory Pattern: RWX + PE header + remote thread = injection
├─ File Pattern: write->execute->delete = dropper
└─ Network Pattern: DNS over HTTPS + fixed interval = C2

Red team countermeasures:
├─ Break the behavior chain -> do not complete all steps in the same process
├─ Space out timing -> Sleep for longer between each step
├─ Use legitimate workflows -> execute through COM/WMI/scheduled tasks
├─ Avoid known-bad combinations -> study the target EDR's detection logic
└─ Test -> rehearse in a similar EDR environment
```

### Strategy 5: Exploit the Hunter's Blind Spots

```
Common hunter blind spots (exploitable):
├─ Weekends/holidays -> thin staffing, slow response
├─ Normal business traffic -> blending into legitimate API calls is hard to distinguish
├─ Non-standard data sources -> invisible if the logs are not collected
├─ Encrypted traffic -> TLS contents are invisible (unless TLS decryption is available)
├─ Cloud environments -> fragmented logs, hard to correlate across platforms
├─ Legitimate tools -> logs from LOLBins are identical to normal administrative actions
└─ Alert fatigue -> high-risk activity hides among many low-priority alerts
```

## Red Team Self-Check Checklist

```
Pre-operation self-check:
[ ] Do public Sigma rules hit my TTP?
[ ] Can my C2 traffic be fingerprinted by JA3/JARM?
[ ] Does my process chain contain abnormal parent-child relationships?
[ ] Does my network pattern have fixed intervals/sizes?
[ ] Did I run multiple reconnaissance commands within a short window?
[ ] Is my tool already flagged on VirusTotal?
[ ] Does the target deploy Sysmon? Which rules are configured?
[ ] What is the target EDR? Have I tested in a similar environment?
```

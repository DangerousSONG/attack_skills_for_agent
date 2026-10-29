---
name: performing-purple-team-exercise
description: "Performs purple team exercises coordinating red team adversary emulation. Signals: red team, methodology, penetration testing workflow."
zh-signals: "Performs purple team exercises by coordinating red team adversary emulation 信号:红队,方法论,渗透流程。"
when-to-use: 'Performs purple team exercises by coordinating red team adversary emulation
  with blue team detection validation using MITRE ATT&CK-mapped attack scenarios,
  real-time detection testing, and collaborative gap remediation. Use when SOC teams
  need to validate detection capabilities, improve analyst skills, and close detection
  gaps through structured offensive-defensive collaboration.

  '
domain: cybersecurity
subdomain: soc-operations
tags:
- soc
- purple-team
- red-team
- blue-team
- mitre-attack
- adversary-emulation
- detection-validation
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- File Metadata Consistency Validation
- Application Protocol Command Analysis
- Identifier Analysis
- Content Format Conversion
- Message Analysis
nist_csf:
- DE.CM-01
- DE.AE-02
- RS.MA-01
- DE.AE-06
mitre_attack:
- T1078
- T1685.002
- T1685.005
- T1566
---
# Performing Purple Team Exercise

## When to Use

Use this skill when:
- SOC teams need to validate that detection rules actually fire for the threats they target
- Red team assessments produced findings that need translation into detection improvements
- New detection tools or SIEM migrations require validation of detection coverage
- Analyst training requires hands-on experience with real attack techniques and SIEM responses
- Quarterly or semi-annual detection validation cycles are scheduled

**Do not use** for unannounced red team engagements — purple team exercises require explicit coordination between offensive and defensive teams with real-time collaboration.

## Prerequisites

- Red team capability: internal team or contracted purple team operator
- Attack simulation tools: Atomic Red Team, MITRE Caldera, or C2 framework (authorized)
- SIEM access for real-time alert monitoring during exercise
- ATT&CK-mapped detection rule inventory with expected alert names
- Isolated test environment or approved production scope with change management approval
- Communication channel (Slack/Teams) for real-time red-blue coordination

## Workflow

### Step 1: Define Exercise Scope and Objectives

Document exercise parameters:

```yaml
purple_team_exercise:
  exercise_id: PT-2024-Q1
  date: 2024-03-20
  duration: 8 hours (09:00-17:00 UTC)
  scope:
    environment: Production (Finance VLAN, 10.0.5.0/24)
    systems_in_scope:
      - WORKSTATION-TEST01 (10.0.5.100) — Test endpoint
      - DC-TEST (10.0.5.200) — Test domain controller
      - FILESERVER-TEST (10.0.5.201) — Test file server
    systems_excluded:
      - All production domain controllers
      - Customer-facing systems
  objectives:
    - Validate 15 detection rules mapped to FIN7 TTPs
    - Test SOC analyst response to real attack indicators
    - Identify detection gaps for credential access and lateral movement
    - Measure detection latency for each technique
  threat_scenario: FIN7 campaign targeting financial data via spearphishing
  authorization: Approved by CISO, Change Request CR-2024-0567
  communication: #purple-team-2024q1 Slack channel
```

### Step 2: Build ATT&CK-Mapped Test Plan

Create technique-by-technique test matrix:

| # | ATT&CK ID | Technique | Test Tool | Expected Detection | Blue Team Metric |
|---|-----------|-----------|-----------|-------------------|------------------|
| 1 | T1566.001 | Spearphishing Attachment | Manual email | Email gateway alert | Detection Y/N, latency |
| 2 | T1204.002 | User Execution | Macro document | Sysmon process creation | Detection Y/N, latency |
| 3 | T1059.001 | PowerShell | Atomic RT #1-3 | PowerShell execution alert | Detection Y/N, latency |
| 4 | T1053.005 | Scheduled Task | Atomic RT | Scheduled task creation alert | Detection Y/N, latency |
| 5 | T1547.001 | Registry Run Keys | Atomic RT | Registry modification alert | Detection Y/N, latency |
| 6 | T1003.001 | LSASS Memory | Mimikatz | Credential dumping alert | Detection Y/N, latency |
| 7 | T1550.002 | Pass-the-Hash | Mimikatz | NTLM anomaly detection | Detection Y/N, latency |
| 8 | T1021.002 | SMB/PsExec | PsExec | PsExec service creation alert | Detection Y/N, latency |
| 9 | T1047 | WMI | wmic /node | WMI remote execution alert | Detection Y/N, latency |
| 10| T1021.001 | RDP | xfreerdp | RDP lateral movement alert | Detection Y/N, latency |
| 11| T1071.001 | Web C2 | Cobalt Strike | C2 beacon detection | Detection Y/N, latency |
| 12| T1041 | Exfiltration C2 | Rclone | Data exfiltration alert | Detection Y/N, latency |
| 13| T1490 | Inhibit Recovery | vssadmin | Shadow copy deletion alert | Detection Y/N, latency |
| 14| T1486 | Data Encrypted | Test encryption | Mass encryption detection | Detection Y/N, latency |
| 15| T1070.001 | Clear Logs | wevtutil | Log clearing detection | Detection Y/N, latency |

### Step 3: Execute Red Team Techniques

Run each technique with Atomic Red Team (or manual execution):

```powershell
# Install Atomic Red Team
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing)
Install-AtomicRedTeam -getAtomics

# Test 1: T1059.001 — PowerShell Execution
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Executing T1059.001 - PowerShell"
Invoke-AtomicTest T1059.001 -TestNumbers 1
# Notify blue team: "T1059.001 executed at $(Get-Date)"

# Test 2: T1053.005 — Scheduled Task Creation
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Executing T1053.005 - Scheduled Task"
Invoke-AtomicTest T1053.005 -TestNumbers 1

# Test 3: T1547.001 — Registry Run Key
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Executing T1547.001 - Registry Persistence"
Invoke-AtomicTest T1547.001 -TestNumbers 1,2

# Test 4: T1003.001 — Credential Dumping
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Executing T1003.001 - LSASS Access"
Invoke-AtomicTest T1003.001 -TestNumbers 1,2

# Test 5: T1490 — Shadow Copy Deletion
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Executing T1490 - Inhibit Recovery"
Invoke-AtomicTest T1490 -TestNumbers 1

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

---
name: performing-lateral-movement-detection
description: "Detect lateral movement techniques including Pass-the-Hash, PsExec, and WMIExec. Signals: lateral movement, psexec, wmiexec."
zh-signals: "Detects lateral movement techniques including Pass-the-Hash, PsExec 信号:横向移动,psexec,wmiexec。"
when-to-use: 'Detects lateral movement techniques including Pass-the-Hash, PsExec,
  WMI execution, RDP pivoting, and SMB-based spreading by correlating Windows Security/Sysmon
  event logs, network flow data (NetFlow/Zeek), and endpoint telemetry in a SIEM,
  mapped to MITRE ATT&CK Lateral Movement (TA0008) techniques with sample SPL detection
  queries. Use when a SOC team needs to detect attackers pivoting between internal
  systems after initial compromise, trace an attacker''s movement path during an
  incident investigation, or build detection engineering rules for TA0008; not for
  detecting initial access or external attacks.

  '
domain: cybersecurity
subdomain: soc-operations
tags:
- soc
- lateral-movement
- mitre-attack
- pass-the-hash
- psexec
- wmi
- rdp
- smb
- detection
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Token Binding
- Execution Isolation
- Restore Access
- Application Protocol Command Analysis
- Process Termination
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
- T1021
---
# Performing Lateral Movement Detection

## When to Use

Use this skill when:
- SOC teams need to detect attackers pivoting between systems after initial compromise
- Incident investigations require tracking an attacker's movement path through the network
- Detection engineering needs lateral movement rules mapped to ATT&CK TA0008 techniques
- Red/purple team exercises identify lateral movement detection gaps

**Do not use** for detecting initial access or external attacks — lateral movement detection focuses on internal host-to-host pivot activity.

## Prerequisites

- Windows Security Event Logs (EventCode 4624, 4625, 4648, 4672) from all endpoints and servers
- Sysmon deployed with process creation (EventCode 1), network connections (EventCode 3), and named pipe (EventCode 17/18)
- Network flow data (NetFlow/sFlow, Zeek connection logs) for internal traffic analysis
- SIEM with cross-source correlation capability
- Baseline of normal internal authentication patterns

## Workflow

### Step 1: Detect Pass-the-Hash / Pass-the-Ticket (T1550)

**Pass-the-Hash Detection (EventCode 4624 with NTLM):**
```spl
index=wineventlog sourcetype="WinEventLog:Security" EventCode=4624 Logon_Type=3
AuthenticationPackageName="NTLM"
| where TargetUserName!="ANONYMOUS LOGON" AND TargetUserName!="$"
| stats count, dc(ComputerName) AS unique_targets, values(ComputerName) AS targets
  by src_ip, TargetUserName
| where unique_targets > 3
| eval alert = "Possible Pass-the-Hash: NTLM network logon to ".unique_targets." hosts"
| sort - unique_targets
| table src_ip, TargetUserName, unique_targets, count, targets, alert
```

**Overpass-the-Hash Detection (Kerberos with RC4):**
```spl
index=wineventlog sourcetype="WinEventLog:Security" EventCode=4769
TicketEncryptionType="0x17"
| where ServiceName!="krbtgt" AND ServiceName!="$"
| stats count, dc(ServiceName) AS unique_services by src_ip, TargetUserName
| where count > 5
| eval alert = "Possible Overpass-the-Hash: RC4 Kerberos tickets from ".src_ip
| table _time, src_ip, TargetUserName, unique_services, count, alert
```

**Golden/Silver Ticket Detection (T1558):**
```spl
index=wineventlog sourcetype="WinEventLog:Security" EventCode=4769
| where TicketOptions="0x40810000" OR TicketOptions="0x40800000"
| eval ticket_lifetime = TicketExpireTime - TicketIssueTime
| where ticket_lifetime > 36000  --- >10 hours (abnormal)
| stats count by src_ip, TargetUserName, ServiceName, TicketEncryptionType, TicketOptions
| eval alert = "Possible Golden/Silver Ticket: Abnormal ticket properties"
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

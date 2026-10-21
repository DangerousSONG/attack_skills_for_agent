# performing-purple-team-exercise — 详细参考（由 SKILL.md 拆分）

# Cleanup after each test
Invoke-AtomicTest T1059.001 -TestNumbers 1 -Cleanup
Invoke-AtomicTest T1053.005 -TestNumbers 1 -Cleanup
Invoke-AtomicTest T1547.001 -TestNumbers 1,2 -Cleanup
```

### Step 4: Monitor Blue Team Detection in Real-Time

Blue team monitors SIEM during execution:

```spl
--- Real-time purple team monitoring dashboard
index=notable earliest=-1h
| where Computer IN ("WORKSTATION-TEST01", "DC-TEST", "FILESERVER-TEST")
  OR src IN ("10.0.5.100", "10.0.5.200", "10.0.5.201")
| eval detection_latency = _time - orig_time
| eval latency_seconds = round(detection_latency, 0)
| sort _time
| table _time, rule_name, urgency, src, dest, user, latency_seconds

--- Check specific technique detection
index=sysmon Computer="WORKSTATION-TEST01" earliest=-15m
(EventCode=1 OR EventCode=3 OR EventCode=10 OR EventCode=11 OR EventCode=13)
| sort _time
| table _time, EventCode, Image, CommandLine, TargetFilename, TargetObject
```

Record results in real-time:

```python
exercise_results = {
    "exercise_id": "PT-2024-Q1",
    "results": [
        {
            "technique": "T1059.001",
            "name": "PowerShell Execution",
            "execution_time": "09:15:00",
            "detected": True,
            "alert_name": "Suspicious PowerShell Encoded Command",
            "detection_time": "09:15:47",
            "latency_seconds": 47,
            "notes": "Detected via Sysmon EventCode 1 with encoded command pattern"
        },
        {
            "technique": "T1003.001",
            "name": "LSASS Memory Access",
            "execution_time": "10:30:00",
            "detected": False,
            "alert_name": None,
            "detection_time": None,
            "latency_seconds": None,
            "notes": "GAP: No detection rule for LSASS access. Sysmon EventCode 10 present but no correlation rule."
        }
    ]
}
```

### Step 5: Collaborative Gap Remediation

For each gap, the blue team builds detection rules immediately:

```spl
--- Gap: T1003.001 — No LSASS access detection
--- Build rule during exercise
index=sysmon EventCode=10 TargetImage="*\\lsass.exe"
GrantedAccess IN ("0x1010", "0x1038", "0x1fffff", "0x40")
NOT SourceImage IN ("*\\svchost.exe", "*\\csrss.exe", "*\\MsMpEng.exe")
| stats count by Computer, SourceImage, SourceUser, GrantedAccess
| where count > 0
```

After building, re-test:
```
Red Team: "Re-executing T1003.001 at 11:45"
Blue Team: "Confirmed — alert 'LSASS Memory Access Detected' fired at 11:45:32 (32s latency)"
Result: GAP CLOSED
```

### Step 6: Generate Exercise Report

```python
def generate_purple_team_report(results):
    total = len(results["results"])
    detected = sum(1 for r in results["results"] if r["detected"])
    gaps = sum(1 for r in results["results"] if not r["detected"])
    avg_latency = sum(r["latency_seconds"] for r in results["results"]
                      if r["latency_seconds"]) / max(detected, 1)

    report = f"""
PURPLE TEAM EXERCISE REPORT — {results['exercise_id']}
{'=' * 60}

SUMMARY:
  Techniques Tested:     {total}
  Detected:              {detected} ({detected/total*100:.0f}%)
  Gaps Identified:       {gaps} ({gaps/total*100:.0f}%)
  Avg Detection Latency: {avg_latency:.0f} seconds

DETAILED RESULTS:
"""
    for r in results["results"]:
        status = "DETECTED" if r["detected"] else "GAP"
        latency = f"{r['latency_seconds']}s" if r["latency_seconds"] else "N/A"
        report += f"  [{status}] {r['technique']} — {r['name']} (Latency: {latency})\n"
        if not r["detected"]:
            report += f"          Action: {r['notes']}\n"

    return report
```

## Key Concepts

| Term | Definition |
|------|-----------|
| **Purple Team** | Collaborative exercise where red (offensive) and blue (defensive) teams work together to validate and improve detection |
| **Adversary Emulation** | Structured simulation of specific threat actor TTPs for testing defensive capabilities |
| **Detection Validation** | Process of confirming that detection rules fire correctly when the targeted technique is executed |
| **Detection Latency** | Time between technique execution and SIEM alert generation — measured during purple team exercises |
| **Gap Remediation** | Immediate creation or tuning of detection rules for techniques that were not detected during testing |
| **Atomic Red Team** | Open-source library of small, focused tests for individual ATT&CK techniques |

## Tools & Systems

- **Atomic Red Team**: Open-source attack test library from Red Canary for technique-by-technique validation
- **MITRE Caldera**: Automated adversary emulation platform supporting ATT&CK-mapped attack chains
- **Vectr**: Purple team management platform for tracking exercise results and detection coverage improvements
- **Prelude Operator**: Adversary emulation tool supporting automated multi-step attack scenarios
- **AttackIQ**: Breach and Attack Simulation (BAS) platform for continuous detection validation

## Common Scenarios

- **Quarterly Validation**: Test top 20 detection rules against ATT&CK techniques to ensure continued effectiveness
- **New Tool Validation**: After deploying new EDR, validate detection coverage against baseline techniques
- **Analyst Training**: Junior analysts observe real attacks in real-time with expert guidance on SIEM investigation
- **Post-Incident Validation**: After a real incident, emulate the attack chain to verify detection improvements
- **Compliance Evidence**: Document detection validation results for SOC 2, ISO 27001, or PCI DSS audits

## Output Format

```
PURPLE TEAM EXERCISE REPORT — PT-2024-Q1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date:         2024-03-20 (09:00-17:00 UTC)
Scenario:     FIN7 Financial Sector Campaign
Scope:        Finance VLAN (10.0.5.0/24)

RESULTS:
  Techniques Tested:     15
  Detected:              11 (73%)
  Gaps Identified:       4 (27%)
  Gaps Remediated Same Day: 3
  Avg Detection Latency: 38 seconds

DETAILED RESULTS:
  [PASS]  T1566.001 Spearphishing Attachment      — 12s latency
  [PASS]  T1204.002 User Execution (Macro)         — 8s latency
  [PASS]  T1059.001 PowerShell Execution            — 47s latency
  [PASS]  T1053.005 Scheduled Task                  — 23s latency
  [PASS]  T1547.001 Registry Run Keys               — 31s latency
  [FAIL]  T1003.001 LSASS Memory Access             — REMEDIATED during exercise
  [FAIL]  T1550.002 Pass-the-Hash                   — REMEDIATED during exercise
  [PASS]  T1021.002 PsExec                          — 15s latency
  [PASS]  T1047 WMI Remote Execution                — 42s latency
  [PASS]  T1021.001 RDP Lateral Movement            — 28s latency
  [FAIL]  T1071.001 Web C2 Beaconing                — REMEDIATED during exercise
  [PASS]  T1041 Exfiltration over C2                — 67s latency
  [PASS]  T1490 Shadow Copy Deletion                — 5s latency
  [FAIL]  T1486 Data Encryption for Impact          — OPEN — requires endpoint telemetry
  [PASS]  T1070.001 Event Log Clearing              — 11s latency

POST-EXERCISE COVERAGE: 93% (14/15) — up from 73% at start
REMAINING GAP: T1486 requires EDR file monitoring enhancement
```

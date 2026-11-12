---
name: apt-emulation
description: "APT emulation and intelligence-driven red team methodology. Design red team operation plans around the TTPs of known APT groups (MITRE ATT&CK). Use when you need to emulate a specific threat actor, design a high-fidelity adversary exercise, or build an attack strategy from threat intelligence"
zh-signals: "基于已知 APT 组织的 MITRE ATT&CK TTP 设计高仿真红队攻击演练与行动计划。信号:APT模拟,威胁情报,红队,MITRE ATT&CK,TTP"
when-to-use: >-
  Use when emulating a specific threat actor, designing a high-fidelity adversary
  exercise, or building an attack strategy from threat intelligence.
metadata:
  tags: "apt,emulation,mitre,attack,red-team,adversary,ttp,threat emulation,APT emulation,purple team"
  category: "threat-intel"
  mitre_attack: "TA0001-TA0011"
---

# APT Emulation and Intelligence-Driven Red Teaming

> **Goal**: not random attacks, but the complete attack chain of a real threat actor, used to test the organization's defensive capability

## ⛔ Further Reading

- Attack emulation frameworks and resources → [references/emulation-frameworks.md](references/emulation-frameworks.md)

---

## Phase 1: Threat Intelligence Collection — choosing the emulation target

### 1.1 Identify the relevant threat actor

```
Select the APT based on the target industry:
├─ Finance → APT38 (Lazarus), FIN7, Carbanak
├─ Government/defense → APT29 (Cozy Bear), APT28 (Fancy Bear), Turla
├─ Energy/ICS → Sandworm, Dragonfly, Triton
├─ Technology/telecom → APT41 (Double Dragon), Salt Typhoon
├─ Healthcare → APT10 (Stone Panda), FIN12
└─ Cross-industry → Lazarus, APT41, FIN7
```

### 1.2 Intelligence sources

```
TTP intelligence gathering:
├─ MITRE ATT&CK Groups → attack.mitre.org/groups/
├─ Vendor reports → Mandiant/CrowdStrike/Kaspersky APT reports
├─ CISA Advisory → US cybersecurity agency advisories
├─ Threat intelligence platforms → MISP/OpenCTI/AlienVault OTX
└─ Academic research → APT deception papers
```

## Phase 2: TTP Mapping and Attack Planning

### 2.1 Attack chain design template

```
Example emulating APT29 (Cozy Bear):

Initial Access:
├─ T1566.001 - Spearphishing with ISO attachment
└─ T1566.002 - Link to watering hole site

Execution:
├─ T1059.001 - PowerShell
└─ T1204.002 - User opens malicious file

Persistence:
├─ T1547.001 - Registry Run Keys
└─ T1053.005 - Scheduled Task

Privilege Escalation:
└─ T1548.002 - UAC Bypass

Defense Evasion:
├─ T1027.005 - Indicator Removal (obfuscation)
├─ T1055.012 - Process Hollowing
└─ T1497.001 - Sandbox evasion

Credential Access:
├─ T1003.001 - LSASS Memory
└─ T1558.003 - Kerberoasting

Discovery:
├─ T1087 - Account Discovery
└─ T1018 - Remote System Discovery

Lateral Movement:
├─ T1021.006 - WinRM
└─ T1550.002 - Pass the Hash

Collection:
└─ T1560.001 - Archive via Utility (7z)

Exfiltration:
└─ T1041 - Exfil over C2 Channel (HTTPS)
```

### 2.2 Rules of Engagement

```
⛔ Must be confirmed before emulation:
├─ Written authorization (executive sign-off)
├─ Scope definition (in-scope / out-of-scope systems)
├─ Emergency contacts (when a real intrusion is found)
├─ Stop conditions (when business is impacted)
├─ Time window
└─ Data handling rules (do not exfiltrate real sensitive data)
```

## Phase 3: Attack Execution

### 3.1 Infrastructure Setup

```
Match the infrastructure profile of the target APT:
├─ APT29 → HTTPS C2, legitimate domain masquerading, cloud services as redirector
├─ APT28 → multi-layer proxies, VPN nodes, disposable infrastructure
├─ Lazarus → compromised legitimate websites as pivots, custom C2 protocol
└─ FIN7 → large-scale phishing infrastructure, Carbanak/Cobalt Strike
```

### 3.2 Tool Selection Mapping

| APT group | Real tools | Red team emulation substitute |
|----------|---------|-------------|
| APT29 | SUNBURST, EnvyScout | Cobalt Strike + custom loader |
| APT28 | X-Agent, X-Tunnel | Sliver + custom tunnel |
| Lazarus | BLINDINGCAN, DRATzarus | Havoc + custom backdoor |
| FIN7 | GRIFFON, BIRDDOG | Cobalt Strike + BAT2EXE |
| APT41 | ShadowPad, Winnti | PlugX loader reimplementation |

### 3.3 Execution Tempo

```
Emulate the timing pattern of a real APT:
├─ Day 1-3: reconnaissance + phishing delivery
├─ Day 4-7: initial foothold + persistence
├─ Day 7-14: internal network enumeration + privilege escalation
├─ Day 14-21: lateral movement + target location
├─ Day 21-28: data collection + exfiltration
└─ ⛔ Do not complete every phase in one day → it does not match a real APT tempo

Sleep pattern:
├─ Operate during working hours (match the APT time zone)
├─ Keep beacons sleeping outside working hours
├─ Simulate holiday pauses (APTs take holidays too)
└─ Some infrastructure is detected → assess whether to pause
```

## Phase 4: Detection Gap Analysis

### 4.1 Record the detection status of every step

```
| Attack step | MITRE ID | Executed | Detected | Blocked | Notes |
|----------|----------|---------|--------|--------|------|
| Phishing delivery | T1566.001 | ✓ | ✗ | ✗ | Not caught by the email gateway |
| PS execution | T1059.001 | ✓ | ✓ | ✗ | EDR alerted but did not block |
| Persistence | T1053.005 | ✓ | ✗ | ✗ | No Sysmon rule |
| LSASS dump | T1003.001 | ✗ | ✓ | ✓ | Credential Guard |
| Lateral PTH | T1550.002 | ✓ | ✓ | ✗ | Detection delayed 4h |
```

### 4.2 Report Structure

```
Report framework:
├─ Executive summary (for management)
├─ Threat intelligence background (the emulated APT)
├─ Attack chain timeline (each step + timing)
├─ Detection coverage matrix (detected/missed ratio)
├─ Key findings (high-risk vulnerabilities)
├─ Recommended remediation (by priority)
└─ ATT&CK Navigator heatmap (coverage vs gaps)
```

## Resources and Tools

| Resource | Purpose |
|------|------|
| MITRE ATT&CK Navigator | Visualize TTP coverage |
| Atomic Red Team | Atomic attack testing |
| MITRE CALDERA | Automated attack emulation |
| Red Canary Reports | Annual threat reports |
| ATT&CK Evaluations | Vendor detection capability comparison |
| Threat Actor Playbooks (SCYTHE) | Pre-built attack playbooks |

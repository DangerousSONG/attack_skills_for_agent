---
name: performing-purple-team-atomic-testing
description: "Executes Atomic Red Team tests mapped to MITRE ATT&CK via Invoke-AtomicRedTeam 信号:红队,方法论,渗透流程。"
when-to-use: 'Executes Atomic Red Team tests mapped to MITRE ATT&CK via Invoke-AtomicRedTeam
  PowerShell, generates ATT&CK Navigator coverage heatmaps, correlates results against
  Sigma rules, and runs detection validation loops to measure blue team visibility.
  Use for purple team exercises, atomic test execution, ATT&CK coverage assessment,
  or detection engineering validation.

  '
domain: cybersecurity
subdomain: purple-team
tags:
- purple-team
- atomic-red-team
- mitre-attack
- detection-engineering
- adversary-emulation
version: 1.0.0
author: mukul975
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
d3fend_techniques:
- Executable Denylisting
- Execution Isolation
- File Metadata Consistency Validation
- Content Format Conversion
- File Content Analysis
nist_csf:
- ID.RA-01
- DE.AE-07
- GV.OV-02
mitre_attack:
- T1078
- T1190
- T1059
---

# Performing Purple Team Atomic Testing

## When to Use

- Validating detection coverage against specific MITRE ATT&CK techniques
- Running purple team exercises using Atomic Red Team test library
- Performing ATT&CK coverage gap analysis to identify blind spots in SIEM/EDR
- Building a detection validation loop: execute atomic test, check SIEM, tune rule, retest
- Generating ATT&CK Navigator heatmap layers for executive reporting
- Automating continuous atomic testing in CI/CD or scheduled pipelines
- Mapping threat intelligence reports to executable atomic tests

**Do not use** for full-scope red team engagements requiring custom implants or live adversary simulation beyond atomic tests; use Caldera, SCYTHE, or Cobalt Strike for advanced adversary emulation.

**DISCLAIMER**: Atomic Red Team tests execute real attack techniques. Run only on systems you own or have explicit written authorization to test. Many tests modify system state, create artifacts, or trigger security alerts. Always execute cleanup commands after testing. Never run atomic tests in production without risk acceptance from stakeholders.

## Prerequisites

- Windows host with PowerShell 5.1+ or PowerShell Core 7+ (Linux/macOS supported for cross-platform atomics)
- Invoke-AtomicRedTeam PowerShell module installed from PSGallery
- Atomic Red Team atomics repository cloned locally
- SIEM/EDR with log ingestion from test endpoints (Splunk, Elastic, Microsoft Sentinel, CrowdStrike)
- MITRE ATT&CK Navigator (web-based or local instance) for layer visualization
- Python 3.9+ with `mitreattack-python`, `pyyaml`, and `requests` for automation scripts
- Sigma rules repository for detection correlation
- Administrative/root access on test endpoints
- Isolated test environment (lab, sandbox, or dedicated test range)

## Workflow

### Step 1: Install and Configure Invoke-AtomicRedTeam

Set up the execution framework and download the atomics library:

```powershell
# Install the PowerShell execution module
Install-Module -Name invoke-atomicredteam -Scope CurrentUser -Force
Install-Module -Name powershell-yaml -Scope CurrentUser -Force

# Import the module
Import-Module invoke-atomicredteam

# Install atomics to default location (C:\AtomicRedTeam\atomics)
IEX (IEX (New-Object System.Net.WebClient).DownloadString(
    'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1'
)); Install-AtomicRedTeam -getAtomics -Force

# Verify installation - list available techniques
$atomicsPath = "C:\AtomicRedTeam\atomics"
$techniques = Get-ChildItem $atomicsPath -Directory | Where-Object { $_.Name -match '^T\d{4}' }
Write-Host "Available techniques: $($techniques.Count)"

# Configure execution logging
$env:ARTLOG = "C:\AtomicRedTeam\logs"
if (-not (Test-Path $env:ARTLOG)) { New-Item -Path $env:ARTLOG -ItemType Directory }
```

### Step 2: Enumerate and Select Atomic Tests

Inventory available tests and select targets based on threat intelligence or gap analysis:

```powershell
# List all tests for a specific technique
Invoke-AtomicTest T1059.001 -ShowDetailsBrief

# Show full details including attack commands and cleanup
Invoke-AtomicTest T1059.001 -ShowDetails

# List tests for a tactic (e.g., Persistence)
$persistenceTechniques = @(
    "T1547.001",  # Boot or Logon Autostart - Registry Run Keys
    "T1053.005",  # Scheduled Task
    "T1136.001",  # Create Account - Local Account
    "T1543.003",  # Create or Modify System Process - Windows Service
    "T1546.001",  # Event Triggered Execution - Change Default File Association
    "T1574.001",  # Hijack Execution Flow - DLL Search Order Hijacking
    "T1197"       # BITS Jobs
)

foreach ($tech in $persistenceTechniques) {
    Write-Host "`n=== $tech ===" -ForegroundColor Cyan
    try {
        Invoke-AtomicTest $tech -ShowDetailsBrief
    } catch {
        Write-Host "  No tests available" -ForegroundColor Yellow
    }
}

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

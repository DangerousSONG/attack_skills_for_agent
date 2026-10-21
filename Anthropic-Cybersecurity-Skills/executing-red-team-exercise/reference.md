# executing-red-team-exercise — 详细参考（由 SKILL.md 拆分）

### Scenario: Adversary Emulation of FIN7 Against a Retail Company

**Context**: A national retail chain wants to test its defenses against FIN7, a financially motivated threat group known for targeting retail and hospitality organizations with point-of-sale malware, phishing, and data exfiltration.

**Approach**:
1. Emulate FIN7 TTPs: spear-phishing with malicious document containing VBA macros that execute PowerShell
2. Initial access achieved through spear-phishing a marketing employee; macro drops Cobalt Strike beacon using rundll32 proxy execution
3. Internal reconnaissance with BloodHound reveals a path from the compromised user to a service account with access to the POS management server
4. Kerberoast the service account, crack the password, and move laterally to the POS management system
5. Demonstrate data access to cardholder data environment, staging simulated card data for exfiltration
6. Exfiltrate staged data over DNS C2 channel to simulate data theft
7. SOC detected the lateral movement at hour 47 but did not detect the initial phishing, macro execution, or Kerberoasting

**Pitfalls**:
- Operating too aggressively and getting detected immediately, providing no value for testing Blue Team's advanced detection capabilities
- Using exclusively custom tools instead of living-off-the-land techniques that real adversaries prefer
- Not recording detailed timestamps for every action, making post-exercise analysis and detection gap mapping impossible
- Failing to establish backup C2 channels, getting burned by a single detection, and losing access without completing objectives

## Output Format

```
## Red Team Exercise Report - FIN7 Adversary Emulation

### Exercise Summary
**Duration**: November 4-22, 2025 (15 business days)
**Objective**: Access cardholder data environment and demonstrate data exfiltration capability
**Outcome**: OBJECTIVE ACHIEVED - Red team accessed POS management system and staged cardholder data for exfiltration

### ATT&CK Technique Coverage
| Technique | ID | Status | Detected? | MTTD |
|-----------|----|--------|-----------|------|
| Spear-Phishing Attachment | T1566.001 | Executed | No | - |
| Visual Basic Macro | T1059.005 | Executed | No | - |
| Process Injection | T1055 | Executed | No | - |
| Kerberoasting | T1558.003 | Executed | No | - |
| Remote Desktop Protocol | T1021.001 | Executed | YES | 47h |
| Data Staged | T1074 | Executed | No | - |
| Exfiltration Over C2 | T1041 | Executed | No | - |

### Detection Summary
- **Techniques Executed**: 14
- **Techniques Detected**: 3 (21.4%)
- **Mean Time to Detect**: 47 hours (for detected techniques)
- **Mean Time to Respond**: 4 hours (from detection to containment)

### Priority Recommendations
1. Deploy email detonation sandboxing for macro-enabled document analysis
2. Implement Kerberoasting detection via Windows Event ID 4769 monitoring
3. Enhance PowerShell logging (Script Block Logging, Module Logging)
4. Deploy memory-scanning EDR capability to detect process injection
```

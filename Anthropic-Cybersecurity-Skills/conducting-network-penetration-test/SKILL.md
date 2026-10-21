---
name: conducting-network-penetration-test
description: 'Conducts comprehensive network penetration tests against authorized
when-to-use: 'Conducts comprehensive network penetration tests against authorized
  target environments by performing host discovery, port scanning, service enumeration,
  vulnerability identification, and controlled exploitation to assess the security
  posture of network infrastructure. The tester follows PTES methodology from reconnaissance
  through post-exploitation and reporting. Activates for requests involving network
  pentest, infrastructure security assessment, internal network testing, or external
  perimeter testing.

  '
domain: cybersecurity
subdomain: penetration-testing
tags:
- network-pentest
- Nmap
- Metasploit
- vulnerability-exploitation
- infrastructure-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1046
- T1595.002
- T1190
- T1210
- T1021
- T1078
---
# Conducting Network Penetration Test

## When to Use

- Assessing the security posture of internal or external network infrastructure before or after deployment
- Validating firewall rules, network segmentation, and access controls under realistic attack conditions
- Identifying exploitable vulnerabilities in network services, protocols, and configurations
- Meeting compliance requirements for PCI-DSS, HIPAA, SOC 2, or ISO 27001 that mandate periodic penetration testing
- Evaluating the effectiveness of IDS/IPS, SIEM, and SOC detection capabilities against real attack traffic

**Do not use** for testing networks without explicit written authorization from the asset owner, against production systems without a pre-approved change window and rollback plan, or for denial-of-service testing unless explicitly scoped and authorized.

## Prerequisites

- Signed Rules of Engagement (RoE) document specifying target IP ranges, excluded hosts, testing hours, and emergency contacts
- Written authorization letter (get-out-of-jail letter) from the network owner
- Dedicated testing laptop with Kali Linux or equivalent distribution with up-to-date tools
- VPN or direct network access to the target scope as defined in the RoE
- Out-of-band communication channel with the client's incident response team
- Scope document listing in-scope IP ranges, domains, and any explicitly excluded systems (medical devices, SCADA, critical infrastructure)

## Workflow

### Step 1: Pre-Engagement and Scope Validation

Validate the scope by confirming IP ranges with the client. Verify that all IP addresses in scope are owned by the client using ARIN/RIPE WHOIS lookups. Confirm testing windows, escalation procedures, and any sensitivity constraints. Set up the testing environment with a dedicated VM, VPN connection, and logging enabled on all tools. Create a timestamped activity log that records every command executed, every scan launched, and every exploit attempted throughout the engagement.

### Step 2: Host Discovery and Network Mapping

Identify live hosts within the authorized scope using layered discovery techniques:

- **ICMP sweep**: `nmap -sn -PE -PP -PM 10.10.0.0/16 -oA discovery_icmp` to find hosts responding to ping
- **ARP scan** (internal networks): `nmap -sn -PR 10.10.0.0/24 -oA discovery_arp` or `arp-scan -l` for local subnet enumeration
- **TCP SYN discovery**: `nmap -sn -PS21,22,25,80,443,445,3389,8080 10.10.0.0/16 -oA discovery_tcp` to find hosts with ICMP blocked
- **UDP discovery**: `nmap -sn -PU53,161,500 10.10.0.0/16 -oA discovery_udp` for hosts only responding on UDP

Consolidate live hosts into a target list. Map the network topology by identifying gateways, VLAN boundaries, and trust relationships using traceroute and SNMP community string guessing where authorized.

### Step 3: Port Scanning and Service Enumeration

Perform detailed port scanning on discovered hosts:

- **Full TCP scan**: `nmap -sS -p- --min-rate 1000 -T4 -oA full_tcp <target>` to identify all open TCP ports
- **Top UDP ports**: `nmap -sU --top-ports 200 -T4 -oA top_udp <target>` for commonly exploitable UDP services
- **Service version detection**: `nmap -sV -sC -p <open_ports> -oA service_enum <target>` to fingerprint service versions and run default NSE scripts
- **OS fingerprinting**: `nmap -O --osscan-guess -oA os_detection <target>` to identify operating systems

Enumerate discovered services in depth using protocol-specific tools:
- SMB: `enum4linux -a <target>`, `crackmapexec smb <target> --shares`
- SNMP: `snmpwalk -v2c -c public <target>`
- DNS: `dig axfr @<dns_server> <domain>` for zone transfer attempts
- LDAP: `ldapsearch -x -H ldap://<target> -b "dc=example,dc=com"`

### Step 4: Vulnerability Identification

Correlate discovered service versions against known vulnerability databases:

- Run `nmap --script vuln -p <ports> <target>` for NSE vulnerability scripts
- Use `searchsploit <service> <version>` to query the Exploit-DB offline database
- Cross-reference with NVD (National Vulnerability Database) and CVE records for confirmed vulnerabilities
- Check for default credentials on management interfaces (Tomcat Manager, Jenkins, phpMyAdmin, database consoles)
- Test for common misconfigurations: anonymous FTP, open SMTP relays, unrestricted SNMP communities, NFS exports without authentication

Prioritize vulnerabilities by CVSS score, exploitability, and business impact. Document each finding with CVE identifier, affected host, service, and version.

### Step 5: Exploitation

Attempt controlled exploitation of validated vulnerabilities using the principle of minimum necessary access:

- **Metasploit Framework**: `msfconsole` with appropriate exploit modules matched to confirmed vulnerabilities. Set RHOSTS, RPORT, and payload options. Prefer bind/reverse TCP Meterpreter for post-exploitation flexibility.
- **Manual exploitation**: Use public proof-of-concept exploits from Exploit-DB after code review. Compile and modify as needed for the target environment.
- **Credential attacks**: Use `hydra` or `crackmapexec` for password spraying against discovered services (SSH, RDP, SMB, HTTP basic auth) using common credential lists. Respect lockout policies.
- **Pass-the-hash / relay**: If NTLM hashes are obtained, attempt pass-the-hash with `impacket-psexec` or relay attacks with `impacket-ntlmrelayx` where SMB signing is disabled.

Document every exploitation attempt including failures. Capture screenshots of successful compromises showing hostname, IP, current user, and privilege level.

### Step 6: Post-Exploitation and Pivoting

After gaining access to a host, demonstrate business impact:

- **Privilege escalation**: Check for local privilege escalation paths using `linpeas.sh` (Linux) or `winPEAS.exe` (Windows). Look for misconfigured services, SUID binaries, unquoted service paths, or kernel exploits.
- **Credential harvesting**: Extract stored credentials from memory (`mimikatz`), files (config files, browser stores), or cached hashes (`hashdump`).
- **Lateral movement**: Use obtained credentials to pivot to additional systems. Test network segmentation by attempting to reach out-of-scope networks from compromised hosts.
- **Data access demonstration**: Identify sensitive data accessible from compromised systems (PII databases, file shares, backup files) and document access without exfiltrating actual data.

Maintain detailed notes on every pivot point, credential obtained, and system accessed to build the attack chain narrative.

### Step 7: Cleanup and Reporting

Remove all testing artifacts from compromised systems:

- Delete uploaded tools, shells, and temporary files
- Remove any accounts created during testing
- Revert configuration changes made during exploitation
- Verify cleanup by re-scanning affected hosts

Prepare the penetration test report with executive summary, methodology description, finding details with CVSS scores, proof-of-concept evidence, and prioritized remediation recommendations.

## Key Concepts

| Term | Definition |
|------|------------|
| **Rules of Engagement (RoE)** | Formal document defining the scope, boundaries, testing hours, authorized actions, and escalation procedures for a penetration test |
| **Pivot** | Using a compromised host as a relay point to access additional network segments not directly reachable from the tester's position |
| **Service Enumeration** | The process of identifying running services, their versions, and configurations on discovered hosts to map the attack surface |
| **Credential Spraying** | Testing a small number of commonly used passwords against many accounts simultaneously to avoid account lockout thresholds |
| **CVSS** | Common Vulnerability Scoring System; an industry-standard framework for rating the severity of vulnerabilities on a 0-10 scale |
| **Lateral Movement** | Techniques used to move from one compromised system to another within a network, expanding the scope of access |
| **Post-Exploitation** | Activities performed after initial compromise including privilege escalation, persistence, credential harvesting, and data access |

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

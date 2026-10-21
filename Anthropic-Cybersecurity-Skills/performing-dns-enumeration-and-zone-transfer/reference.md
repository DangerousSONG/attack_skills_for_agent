# performing-dns-enumeration-and-zone-transfer — 详细参考（由 SKILL.md 拆分）

# Use Nmap for reverse DNS on a subnet
nmap -sL 10.10.0.0/24 | grep "(" | awk '{print $5, $6}'

# Check for DNS cache snooping (information about queried domains)
dig @ns1.example.com www.competitor.com +norecurse
```

### Step 5: Analyze DNS Security Configuration

```bash
# Check DNSSEC validation
dig example.com +dnssec +short
dig DNSKEY example.com +short
dig DS example.com +short

# Test for DNS rebinding vulnerability
# Check if the DNS server has a short TTL that could enable rebinding
dig example.com +noall +answer | grep -i ttl

# Check for open recursive resolver (misconfiguration)
dig @ns1.example.com google.com +recurse
# If it resolves, the server is an open resolver

# Check for wildcard DNS records
dig nonexistent-subdomain-xyz123.example.com +short
# If it resolves, a wildcard record exists

# Test DNS over HTTPS/TLS support
# DoH test
curl -s -H 'accept: application/dns-json' 'https://dns.google/resolve?name=example.com&type=A'

# Verify SPF record for email security
dig TXT example.com +short | grep "v=spf1"
# Check for overly permissive SPF (+all, ?all)
```

### Step 6: Resolve and Map All Discovered Subdomains

```bash
# Resolve all discovered subdomains to IP addresses
while read subdomain; do
  ip=$(dig +short A "$subdomain" | head -1)
  if [ -n "$ip" ]; then
    echo "$subdomain,$ip"
  fi
done < all_subdomains.txt > resolved_subdomains.csv

# Identify unique IP addresses and their locations
cut -d',' -f2 resolved_subdomains.csv | sort -u > unique_ips.txt

# Check for internal IP addresses leaked via DNS
grep -E "^10\.|^172\.(1[6-9]|2[0-9]|3[01])\.|^192\.168\." resolved_subdomains.csv > internal_ip_leaks.txt

# Use httpx to probe web services on discovered subdomains
cat all_subdomains.txt | httpx -title -status-code -tech-detect -o httpx_results.txt

# Screenshot web services for documentation
cat all_subdomains.txt | httpx -screenshot -o screenshots/
```

## Key Concepts

| Term | Definition |
|------|------------|
| **Zone Transfer (AXFR)** | DNS mechanism that replicates the complete zone file from a primary to secondary server; unauthorized transfers expose all records in the zone |
| **Subdomain Enumeration** | Process of discovering valid subdomains through brute force, certificate transparency logs, search engines, and passive DNS databases |
| **DNSSEC** | DNS Security Extensions that add cryptographic signatures to DNS responses, preventing cache poisoning and spoofing attacks |
| **SPF/DKIM/DMARC** | Email authentication protocols defined in DNS TXT records that prevent email spoofing and domain impersonation |
| **Wildcard DNS** | A DNS record using an asterisk (*) that matches any query for non-existent subdomains, potentially masking enumeration results |
| **PTR Record** | Reverse DNS record that maps an IP address to a hostname, often revealing internal naming conventions and server roles |

## Tools & Systems

- **dig**: Standard DNS lookup utility with full support for all record types, DNSSEC validation, and zone transfer queries
- **dnsrecon**: Comprehensive DNS enumeration tool supporting zone transfers, brute force, reverse lookup, cache snooping, and Google dork queries
- **subfinder**: Fast passive subdomain discovery tool that queries certificate transparency logs, search engines, and DNS databases
- **Amass (OWASP)**: Advanced attack surface mapping tool with both passive and active DNS enumeration, graph analysis, and data source integration
- **gobuster**: Fast brute-force tool for DNS subdomain enumeration using configurable wordlists and concurrent threads

## Common Scenarios

### Scenario: External Reconnaissance for a Web Application Penetration Test

**Context**: A security consultant is performing external reconnaissance for a web application penetration test. The client's primary domain is example.com, and the scope includes all subdomains and related infrastructure. The consultant has authorization to enumerate DNS records and probe discovered web services.

**Approach**:
1. Query NS, MX, TXT, and SOA records for example.com to map the DNS infrastructure
2. Attempt zone transfers against both nameservers -- ns2 succeeds, revealing 347 DNS records including internal staging environments
3. Run subfinder and amass in passive mode to discover 89 additional subdomains from certificate transparency logs
4. Brute-force subdomains with a 20,000-word list using gobuster, discovering 12 more subdomains not found in passive sources
5. Resolve all subdomains and identify 15 that resolve to internal RFC1918 addresses (information disclosure)
6. Probe all web-accessible subdomains with httpx, discovering a staging environment (staging.example.com) with default credentials
7. Report zone transfer vulnerability, internal IP disclosure, and exposed staging environment to the client

**Pitfalls**:
- Sending thousands of DNS queries per second and triggering rate limiting or DNS-based DDoS protection
- Not checking for wildcard DNS records, resulting in false positive subdomain discoveries
- Missing subdomains that use separate DNS providers or CDN-specific CNAME records
- Overlooking TXT records that contain API keys, verification tokens, or internal comments

## Output Format

```
## DNS Enumeration Report

**Target Domain**: example.com
**Authorized Nameservers**: ns1.example.com (203.0.113.10), ns2.example.com (203.0.113.11)

### Zone Transfer Status
| Nameserver | AXFR Result | Records Obtained |
|------------|-------------|------------------|
| ns1.example.com | REFUSED | 0 |
| ns2.example.com | SUCCESS | 347 records |

### Subdomain Discovery Summary
| Method | Subdomains Found |
|--------|-----------------|
| Zone Transfer | 347 |
| Passive (subfinder + amass) | 89 |
| Active Brute Force | 12 |
| **Total Unique** | **412** |

### Critical Findings
1. **Zone Transfer Allowed** (High): ns2.example.com allows AXFR from any source
2. **Internal IP Disclosure** (Medium): 15 subdomains resolve to RFC1918 addresses
3. **Exposed Staging Environment** (High): staging.example.com accessible with default credentials
4. **Missing DMARC Policy** (Medium): No DMARC record found, enabling email spoofing
5. **Weak SPF Record** (Low): SPF uses ~all (soft fail) instead of -all (hard fail)
```

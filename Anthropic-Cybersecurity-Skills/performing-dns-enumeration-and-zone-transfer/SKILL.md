---
name: performing-dns-enumeration-and-zone-transfer
description: "Enumerate DNS records, attempt zone transfers, and brute-force subdomains. Signals: subdomain, domain enumeration, dns enumeration."
zh-signals: "Enumerates DNS records, attempts zone transfers, brute-forces subdomains 信号:子域名,域名枚举,dns枚举。"
when-to-use: 'Enumerates DNS records, attempts zone transfers, brute-forces subdomains,
  and maps DNS infrastructure during authorized reconnaissance to identify attack
  surface, misconfigurations, and information disclosure in target domains.

  '
domain: cybersecurity
subdomain: network-security
tags:
- network-security
- dns
- enumeration
- zone-transfer
- reconnaissance
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
mitre_attack:
- T1046
- T1040
- T1557
- T1071
- T1595
---
# Performing DNS Enumeration and Zone Transfer

## When to Use

- Mapping the external attack surface of a target organization during authorized penetration tests
- Discovering hidden subdomains, internal hostnames, and IP addresses exposed via DNS records
- Testing whether DNS servers allow unauthorized zone transfers that leak the entire zone file
- Identifying mail servers, name servers, and service records for further targeted testing
- Validating DNS security configurations including DNSSEC, SPF, DKIM, and DMARC

**Do not use** against domains you do not have authorization to test, for DNS amplification or reflection attacks, or to overwhelm DNS servers with excessive query volumes.

## Prerequisites

- Written authorization to perform DNS enumeration against the target domain
- DNS enumeration tools installed: dig, nslookup, host, dnsrecon, dnsenum, subfinder, amass
- Network access to the target's DNS servers (UDP/TCP port 53)
- Wordlist for subdomain brute-forcing (SecLists dns-wordlist or similar)
- Understanding of DNS record types (A, AAAA, CNAME, MX, NS, TXT, SOA, SRV, PTR)

## Workflow

### Step 1: Identify DNS Servers and Basic Records

```bash
# Find authoritative name servers
dig NS example.com +short
# ns1.example.com.
# ns2.example.com.

# Get SOA record for zone metadata
dig SOA example.com +short
# ns1.example.com. admin.example.com. 2024031501 3600 900 604800 86400

# Enumerate all common record types
dig example.com ANY +noall +answer

# Get MX records (mail servers)
dig MX example.com +short
# 10 mail.example.com.
# 20 mail-backup.example.com.

# Get TXT records (SPF, DKIM, DMARC, verification)
dig TXT example.com +short

# Check for DMARC policy
dig TXT _dmarc.example.com +short

# Check for DKIM selectors
dig TXT default._domainkey.example.com +short
dig TXT selector1._domainkey.example.com +short
dig TXT google._domainkey.example.com +short

# Get SRV records for common services
dig SRV _sip._tcp.example.com +short
dig SRV _ldap._tcp.example.com +short
dig SRV _kerberos._tcp.example.com +short
```

### Step 2: Attempt Zone Transfers

```bash
# Attempt AXFR zone transfer against each name server
dig AXFR example.com @ns1.example.com
dig AXFR example.com @ns2.example.com

# Use host command for zone transfer
host -t axfr example.com ns1.example.com

# Use dnsrecon for automated zone transfer attempts
dnsrecon -d example.com -t axfr

# If zone transfer succeeds, save the output
dig AXFR example.com @ns1.example.com > zone_transfer_results.txt

# Test for IXFR (incremental zone transfer)
dig IXFR=2024031500 example.com @ns1.example.com
```

### Step 3: Subdomain Enumeration via Brute Force

```bash
# Use dnsenum for comprehensive enumeration
dnsenum --dnsserver ns1.example.com --enum -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -r example.com -o dnsenum_output.xml

# Use dnsrecon with brute force
dnsrecon -d example.com -t brt -D /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Use gobuster for fast DNS brute forcing
gobuster dns -d example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -t 50 -o gobuster_dns.txt

# Use subfinder for passive subdomain discovery
subfinder -d example.com -all -o subfinder_results.txt

# Use amass for comprehensive enumeration (passive + active)
amass enum -d example.com -passive -o amass_passive.txt
amass enum -d example.com -active -brute -o amass_active.txt

# Combine and deduplicate results
cat subfinder_results.txt amass_passive.txt amass_active.txt gobuster_dns.txt | sort -u > all_subdomains.txt
```

### Step 4: Reverse DNS and PTR Enumeration

```bash
# Reverse DNS lookup on discovered IP ranges
dnsrecon -d example.com -t rvl -r 10.10.0.0/24

# PTR record enumeration for IP range
for ip in $(seq 1 254); do
  result=$(dig -x 10.10.1.$ip +short 2>/dev/null)
  if [ -n "$result" ]; then
    echo "10.10.1.$ip -> $result"
  fi
done

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

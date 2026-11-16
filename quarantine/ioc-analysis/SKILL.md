---
name: ioc-analysis
description: "IOC (indicator of compromise) analysis and counter-adversary methodology. Blue team perspective: how to collect, enrich, and correlate IOCs for threat hunting. Red team perspective: how to avoid generating identifiable IOCs from your own infrastructure and tooling, and how to make IOCs expire quickly. Use when a red team needs to assess its own exposure or plan C2 infrastructure"
zh-signals: "从蓝队与红队双视角分析失陷指标，讲解 IOC 收集富化关联及红队规避可识别 IOC 的基础设施对抗。信号:IOC,威胁情报,OPSEC,C2基础设施,归因"
when-to-use: >-
  Use when a red team needs to assess its own exposure or plan C2 infrastructure, or
  when analyzing and enriching IOCs for threat hunting from a blue-team perspective.
metadata:
  tags: "ioc,indicator,threat-intel,c2-infrastructure,opsec,threat-intelligence,indicator-of-compromise,infrastructure,attribution"
  category: "threat-intel"
  mitre_attack: "T1583,T1584,T1588,T1608,T1071"
---

# IOC Analysis and Counter-Adversary Operations

> **Red team positioning**: understand how the blue team tracks you → design short-lived, non-correlatable infrastructure

## ⛔ Further Reading

- C2 infrastructure OPSEC checklist → [references/c2-infra-opsec.md](references/c2-infra-opsec.md)
- IOC types and lifecycle management → [references/ioc-lifecycle.md](references/ioc-lifecycle.md)

---

## IOC Pyramid (Pyramid of Pain)

```
Hard to change                 High value to defenders
   ▲
   │  TTPs (tactics/techniques/procedures)  ← hardest to change
   │  Tool signatures (Imphash/YARA)         ← requires recompilation
   │  Network/host artifacts                 ← requires behavior change
   │  Domains                                ← requires new registration
   │  IP addresses                           ← easiest to swap
   │  Hash values                            ← one byte change breaks it
   ▼
Easy to change                 Low value to defenders
```

**Red team strategy: keep your own IOCs at the bottom of the pyramid (easy to change) and avoid exposing the top (immutable TTPs)**

## Part A: Blue Team Perspective — IOC Collection and Analysis

### IOC Types

| Type | Example | Collection Source |
|------|---------|---------|
| File hash | MD5/SHA256 | Endpoint/sandbox/VirusTotal |
| IP address | C2 server IP | Network logs/PCAP |
| Domain | C2/phishing domain | DNS logs/certificate transparency |
| URL/URI | C2 path | Proxy logs/HTTP logs |
| Email | Sender/attachment name | Mail gateway |
| Registry | Persistence key | Endpoint detection |
| Process | Process name/command line | EDR/Sysmon |
| File path | Malicious file location | Endpoint detection |
| Certificate | SSL certificate hash | JA3/JARM |
| Network signature | JA3/JA3S/JARM | Traffic analysis |

### IOC Enrichment Workflow

```
Raw IOC → Enrichment → Correlation
├─ File hash → VirusTotal/MalwareBazaar → family/origin/related samples
├─ IP → Shodan/Censys/GreyNoise → services/ports/history
├─ Domain → PassiveDNS/Whois/CT Logs → registration info/related domains
├─ Certificate → crt.sh/Censys → related domains/IPs
└─ JA3 → JA3er → client fingerprinting
```

---

## Part B: Red Team Perspective — IOC Counter-Adversary Operations

### Strategy 1: Infrastructure Separation and Rotation

```
C2 infrastructure design principles:
├─ Tiered architecture:
│   Attacker → Redirector (multiple/rotating) → TeamServer (hidden)
│   Only the Redirector is discovered → swapping the IP is enough
│
├─ Domain strategy:
│   ├─ Register domains older than 30 days (new domains carry risk scores)
│   ├─ Use domains with legitimate categories (not newly registered / not flagged)
│   ├─ Domain fronting → the real C2 hides behind a CDN
│   └─ Use hijacked legitimate subdomains (more trusted)
│
├─ IP strategy:
│   ├─ Use cloud provider IPs (AWS/Azure/GCP) → hard to block
│   ├─ Create a new VPS per operation → never reuse an IP
│   └─ Use a CDN/reverse proxy → hide the real IP
│
└─ Certificate strategy:
    ├─ Use Let's Encrypt certificates (most common, not distinctive)
    ├─ Or buy a commercial certificate of the same type as the target
    └─ ⛔ NEVER use self-signed certificates → obvious JA3S/JARM signatures
```

### Strategy 2: Tool Signature Elimination

```
File-level IOC counter-adversary measures:
├─ Recompile for every operation → SHA256 changes
├─ Use Garble/Shikata polymorphic encoding → YARA rules fail
├─ Modify the Rich Header / compile timestamp → Imphash changes
├─ Replace resource signatures → looks like legitimate software
└─ Code obfuscation/virtualization → static analysis fails

Network-level IOC counter-adversary measures:
├─ JA3 fingerprint → use a legitimate browser TLS library/configuration
├─ User-Agent → match the real browser of the target environment
├─ URI pattern → mimic a legitimate SaaS API (/api/v1/events)
├─ Heartbeat interval → increase jitter (30-50%), never a fixed interval
└─ Data size → add padding to avoid a fixed packet size
```

### Strategy 3: Attribution Counter-Adversary Measures

```
Prevent correlation to the same organization/operation:
├─ Use completely independent infrastructure for different operations
├─ Recompile tools (different compiler/options/timestamp)
├─ Never reuse C2 Profile / Malleable templates
├─ Use disposable emails + different registrars for registration info
├─ Pay with cryptocurrency → Monero is better than Bitcoin
└─ Randomize timezone/language fingerprints
```

### Strategy 4: Shorten IOC Lifecycles

```
Make the IOCs collected by the blue team go stale quickly:
├─ Short-lived C2 domains → rotate after 48h
├─ One-time payloads → compile uniquely per target
├─ Short-lived VPS → destroy as soon as the operation ends
├─ Fast phase switching → initial access ≠ persistence ≠ data exfiltration
└─ Payload self-destruction → delete itself after execution
```

## Red Team C2 Infrastructure Checklist

```
Pre-deployment checks:
[ ] Domain registered > 30 days ago + categorized
[ ] SSL certificate is LE or a commercial certificate (not self-signed)
[ ] Redirector configured (Apache/Nginx/Cloudflare)
[ ] TeamServer has no direct public exposure
[ ] JA3 fingerprint matches a legitimate client
[ ] JARM fingerprint does not match a known C2 framework
[ ] User-Agent matches the target environment
[ ] Whois privacy protection enabled for the domain
[ ] IP is not on any known malicious IP list (check via VirusTotal/AbuseIPDB)
[ ] DNS records show no anomalies (no TXT payload / multiple A records)

During the operation:
[ ] Monitor the VT detection rate of C2 domains/IPs
[ ] No anomalous scanning in Redirector logs
[ ] Backup C2 channel tested
[ ] Rotation plan confirmed

After the operation:
[ ] Destroy all VPS instances
[ ] Destroy all Redirectors
[ ] Confirm no DNS records remain pointing to destroyed IPs
```

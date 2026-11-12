---
name: gobuster-dir-dns
description: "gobuster discovers directories, admin panels, and subdomains for asset mapping. Signals: web scanning, vulnerability scanning, directory/file brute-forcing, virtual host brute-forcing."
zh-signals: "gobuster: 目录与后台发现、子域名枚举接资产梳理。信号:web扫描,漏洞扫描,目录/文件爆破,虚拟主机爆破。"
when-to-use: >-
  Use when discovering directories, virtual hosts, DNS subdomains, or fuzzable
  paths during web or asset reconnaissance; select the appropriate mode and
  wordlist, and use wildcard handling for DNS.
---

# gobuster

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/OJ/gobuster
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/OJ/gobuster/v3@latest
# or apt install gobuster (bundled with Kali)
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dir -u URL -w wordlist.txt` | Directory / file brute force |
| `dns -d target.com -w subdomains.txt` | Subdomain enumeration |
| `vhost -u URL -w vhosts.txt` | Virtual host brute force |
| `fuzz -u URL/FUZZ -w params.txt` | Parameter / path point fuzzing |
| `-t 50` | Number of threads |
| `-x php,txt,bak` | Append extensions in directory mode |
| `-s 200,204,301,302,307` | Only show these status codes |
| `-k` | Ignore HTTPS certificate errors |
| `--wildcard` | Handle wildcard resolution in DNS mode |
| `-o result.txt` | Write output to a file |

## Attack Scenario Playbook

### Directory and admin panel discovery

```bash
gobuster dir -u https://target.com -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,html,bak -t 80 -o dirs.txt
```

### Subdomain enumeration feeding asset mapping

```bash
gobuster dns -d target.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -o subs.txt
cat subs.txt | awk '{print $2}' | sort -u
```

### Hidden virtual host and parameter point discovery

```bash
gobuster vhost -u https://target.com -w vhost-wordlist.txt -t 50
gobuster fuzz -u "https://target.com/api/FUZZ" -w api-endpoints.txt -mc 200,401,403
```

## Notes

When its functionality overlaps with dirsearch/feroxbuster, prefer it for DNS and vhost modes; in DNS mode remember to add `--wildcard` to exclude wildcard resolution from polluting the results.

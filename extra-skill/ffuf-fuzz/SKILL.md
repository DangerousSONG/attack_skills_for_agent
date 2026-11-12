---
name: ffuf-fuzz
description: "Complete reference for the ffuf fuzzing tool. Used for directory/file discovery, parameter fuzzing, virtual host enumeration, POST data fuzzing, and multi-position fuzzing. Use when you need to brute-force web application paths, discover parameters, or enumerate subdomains. More flexible than gobuster/dirsearch — it supports multiple FUZZ positions and custom filters. Use this skill for any scenario requiring web path or parameter brute-force enumeration"
zh-signals: "使用 ffuf 进行目录/文件发现、参数 Fuzz、虚拟主机枚举与多位置模糊测试。信号:ffuf,模糊测试,目录扫描,参数发现,虚拟主机"
when-to-use: "Use when performing web path brute force, parameter discovery, virtual-host enumeration, or multi-position fuzzing with ffuf."
metadata:
  tags: "ffuf,fuzz,directory,brute force,parameter,vhost,wordlist,web,directory scanning,parameter discovery,fuzzing"
  category: "tool"
---

# ffuf Fuzzing Tool Complete Reference

ffuf (Fuzz Faster U Fool) is the most flexible web fuzzing tool. Core concept: mark the positions to be replaced with the `FUZZ` keyword.

## Phase 1: Directory/File Discovery (most common)

```bash
# Basic directory scan
ffuf -u http://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

# Specify extensions
ffuf -u http://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt \
    -e .php,.html,.txt,.bak,.zip

# Recursive scan (keep digging after a directory is found)
ffuf -u http://target/FUZZ -w wordlist.txt -recursion -recursion-depth 2

# Deep scan with a large wordlist
ffuf -u http://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
    -e .php,.asp,.jsp -t 50
```

### Wordlist Selection

| Scenario | Recommended wordlist |
|------|----------|
| Quick scan | `Discovery/Web-Content/common.txt` (4660) |
| Medium scan | `Discovery/Web-Content/directory-list-2.3-small.txt` (87k) |
| Deep scan | `Discovery/Web-Content/directory-list-2.3-medium.txt` (220k) |
| Backup files | `Discovery/Web-Content/common-and-backup.txt` |
| API paths | `Discovery/Web-Content/api/api-endpoints.txt` |
| Common in CTFs | `/pentest/AboutSecurity/Dic/Web/CTF/` |

---

## Phase 2: Parameter Fuzzing (finding hidden parameters)

```bash
# GET parameter discovery
ffuf -u 'http://target/page.php?FUZZ=test' \
    -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
    -fs 4242  # filter out the default response size

# GET parameter value fuzzing
ffuf -u 'http://target/page.php?id=FUZZ' \
    -w /usr/share/seclists/Fuzzing/integers-1-1000.txt

# POST parameter discovery
ffuf -u 'http://target/api' -X POST \
    -d 'FUZZ=test' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
    -fs 4242

# JSON parameter fuzzing
ffuf -u 'http://target/api' -X POST \
    -d '{"FUZZ":"test"}' \
    -H 'Content-Type: application/json' \
    -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
    -fs 4242
```

**CTF-specific parameter wordlist**: `/pentest/AboutSecurity/Dic/Web/CTF/Fuzz_param.txt`

---

## Phase 3: Virtual Host / Subdomain Enumeration

```bash
# Virtual host enumeration (via the Host header)
ffuf -u http://target/ -H 'Host: FUZZ.target.com' \
    -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
    -fs 4242  # filter out the default page size
```

---

## Phase 4: Multi-Position Fuzzing

ffuf supports multiple FUZZ keywords (distinguished by different names):

```bash
# Username + password brute force
ffuf -u http://target/login -X POST \
    -d 'username=HFUZZ&password=WFUZZ' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -w users.txt:HFUZZ -w passwords.txt:WFUZZ \
    -fc 401  # filter out 401 responses

# Directory + extension combinations
ffuf -u http://target/W1FUZZ.W2FUZZ \
    -w dirs.txt:W1FUZZ -w extensions.txt:W2FUZZ \
    -mode clusterbomb  # all combinations (cartesian product)
```

### Fuzz Modes

| Mode | Description | Scenario |
|------|------|------|
| `clusterbomb` | All combinations (default) | Username × password |
| `pitchfork` | One-to-one pairing | Known paired credentials |
| `sniper` | Single wordlist per position | One parameter in multiple positions |

---

## Phase 5: Filtering and Matching (critical!)

ffuf displays all responses by default, so you need to filter out the noise:

### Filtering (exclude what you do not want)

| Parameter | Purpose | Example |
|------|------|------|
| `-fc` | Filter status codes | `-fc 404,403,500` |
| `-fs` | Filter response size | `-fs 4242` |
| `-fw` | Filter response word count | `-fw 12` |
| `-fl` | Filter response line count | `-fl 5` |
| `-fr` | Filter regex match | `-fr 'not found'` |
| `-ft` | Filter response time | `-ft '>3000'` (>3 seconds) |

### Matching (show only what you want)

| Parameter | Purpose | Example |
|------|------|------|
| `-mc` | Match status codes | `-mc 200,301,302` |
| `-ms` | Match response size | `-ms 1234` |
| `-mw` | Match response word count | `-mw 100-500` |
| `-mr` | Match regex | `-mr 'flag\{.*\}'` |

**Tip**: run it once without any filter first, observe the default response size, then filter it out with `-fs`.

---

## Phase 6: Common Options

```bash
# Number of threads (default 40, can be raised)
-t 100

# Delay (to avoid bans, in seconds; 0.1 = 100ms)
-p 0.1

# Request rate limit (requests per second)
-rate 50

# Custom cookie
-b 'session=abc123; token=xyz'

# Custom header
-H 'Authorization: Bearer TOKEN'
-H 'X-Forwarded-For: 127.0.0.1'

# Proxy
-x http://127.0.0.1:8080
-x socks5://127.0.0.1:1080

# Output to file
-o results.json -of json
-o results.csv -of csv
-o results.html -of html

# Auto-calibration (automatically detects the filter baseline)
-ac

# Follow redirects
-r

# Timeout (seconds)
-timeout 10

# Quiet mode (output only the results)
-s
```

---

## Practical Scenario Quick Reference

| Scenario | Command |
|------|------|
| Quick directory scan | `ffuf -u URL/FUZZ -w common.txt -mc 200,301,302` |
| Scan for PHP files | `ffuf -u URL/FUZZ -w common.txt -e .php -mc 200` |
| Find hidden parameters | `ffuf -u 'URL?FUZZ=1' -w burp-parameter-names.txt -fs SIZE` |
| LFI parameter fuzzing | `ffuf -u 'URL?FUZZ=../../../etc/passwd' -w Fuzz_param.txt -mr 'root:'` |
| Subdomain enumeration | `ffuf -u URL -H 'Host: FUZZ.target' -w subdomains.txt -fs SIZE` |
| Brute-force login | `ffuf -u URL -X POST -d 'user=admin&pass=FUZZ' -w passwords.txt -fc 401` |
| API endpoint discovery | `ffuf -u URL/api/FUZZ -w api-endpoints.txt -mc 200,401,403` |
| Backup file search | `ffuf -u URL/FUZZ -w common.txt -e .bak,.zip,.tar.gz,.sql -mc 200` |

## Notes

- **`-ac` auto-calibration** is very useful — it automatically detects the default response and filters it, saving you the trouble of setting `-fs` manually
- ffuf defaults to 40 threads, which may be too fast for weak targets and trigger 429/bans; lower it to `-t 10 -p 0.1`
- Wordlist paths: SecLists is usually at `/usr/share/seclists/`, the AboutSecurity wordlists are at `/pentest/AboutSecurity/Dic/`
- POST fuzzing must specify the Content-Type header, otherwise the server may not parse the body
- Multi-position fuzzing defaults to clusterbomb (cartesian product), so large wordlists explode the combination count — watch the wordlist size

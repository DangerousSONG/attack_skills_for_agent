---
name: performing-clickjacking-attack-test
description: "Test web applications for clickjacking vulnerabilities by assessing frame embedding controls. Signals: web vulnerability, injection, sql injection."
zh-signals: "Testing web applications for clickjacking vulnerabilities by assessing 信号:web漏洞,注入,sql注入。"
when-to-use: Testing web applications for clickjacking vulnerabilities by assessing
  frame embedding controls and crafting proof-of-concept overlay attacks during authorized
  security assessments.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- clickjacking
- ui-redressing
- web-security
- owasp
- x-frame-options
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0024
- AML.T0035
nist_ai_rmf:
- MEASURE-2.8
- MAP-5.1
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

# Performing Clickjacking Attack Test

## When to Use

- During authorized penetration tests when assessing UI redressing vulnerabilities
- When testing whether sensitive actions (delete account, transfer funds, change settings) can be performed via clickjacking
- For evaluating the effectiveness of X-Frame-Options and Content-Security-Policy frame-ancestors directives
- When assessing applications that process one-click actions without additional confirmation
- During security audits of applications handling financial transactions or account management

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Web browser**: Modern browser for testing iframe embedding
- **Local web server**: Python `http.server` or similar for hosting PoC pages
- **Burp Suite**: For examining response headers
- **HTML/CSS knowledge**: For crafting clickjacking overlay pages
- **curl**: For checking framing headers on target pages


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Check Frame Embedding Protections

Examine response headers for anti-clickjacking defenses.

```bash
# Check X-Frame-Options header
curl -s -I "https://target.example.com/" | grep -i "x-frame-options"
# Expected values:
# X-Frame-Options: DENY (blocks all framing)
# X-Frame-Options: SAMEORIGIN (allows same-origin framing)
# X-Frame-Options: ALLOW-FROM https://trusted.com (deprecated, limited support)

# Check Content-Security-Policy frame-ancestors directive
curl -s -I "https://target.example.com/" | grep -i "content-security-policy"
# Look for: frame-ancestors 'none' or frame-ancestors 'self'
# frame-ancestors 'none' = equivalent to DENY
# frame-ancestors 'self' = equivalent to SAMEORIGIN

# Test multiple sensitive pages
for page in / /account/settings /account/delete /transfer \
  /admin/dashboard /change-password /change-email; do
  echo -n "$page: "
  headers=$(curl -s -I "https://target.example.com$page")
  xfo=$(echo "$headers" | grep -i "x-frame-options" | tr -d '\r')
  csp=$(echo "$headers" | grep -i "content-security-policy" | grep -o "frame-ancestors[^;]*" | tr -d '\r')
  if [ -z "$xfo" ] && [ -z "$csp" ]; then
    echo "NO PROTECTION"
  else
    echo "${xfo:-none} | ${csp:-none}"
  fi
done

# Check if JavaScript frame-busting is used (weak protection)
curl -s "https://target.example.com/" | grep -i "top.location\|parent.location\|frameElement"
```

### Step 2: Test Basic Iframe Embedding

Attempt to embed the target page in an iframe to confirm vulnerability.

```html
<!-- basic-frame-test.html -->
<html>
<head><title>Clickjacking Frame Test</title></head>
<body>
<h1>Frame Embedding Test</h1>
<p>If the target page loads below, it is vulnerable to clickjacking.</p>

<!-- Test basic framing -->
<iframe src="https://target.example.com/account/settings"
        width="800" height="600"
        style="border: 2px solid red;">
</iframe>

<p>If you see "Refused to display" in console or blank iframe,
   the page has frame protection.</p>
</body>
</html>
```

```bash
# Host the test page
cd /tmp
cat > frame-test.html << 'EOF'
<html>
<body>
<h1>Clickjacking Test</h1>
<iframe src="https://target.example.com/account/settings"
        width="800" height="600"></iframe>
</body>
</html>
EOF
python3 -m http.server 8888
# Open http://localhost:8888/frame-test.html in browser
# Check browser console for framing errors
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

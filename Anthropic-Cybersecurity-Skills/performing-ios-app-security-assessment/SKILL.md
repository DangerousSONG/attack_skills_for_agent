---
name: performing-ios-app-security-assessment
description: "Perform comprehensive iOS application security assessments using Frida and related tooling. Signals: mobile, android attack, ios attack."
zh-signals: "Performs comprehensive iOS application security assessments using Frida 信号:移动端,android攻击,ios攻击。"
when-to-use: 'Performs comprehensive iOS application security assessments using Frida
  for dynamic instrumentation, Objection for runtime exploration, SSL pinning bypass
  for traffic interception, keychain extraction for credential analysis, and IPA static
  analysis for binary-level review. Use when conducting authorized iOS penetration
  tests, evaluating mobile app security posture against OWASP MASTG, or assessing
  iOS app data protection and transport security controls. Activates for requests
  involving iOS app pentesting, Frida-based iOS instrumentation, mobile app SSL pinning
  bypass, or IPA reverse engineering.

  '
domain: cybersecurity
subdomain: mobile-security
author: mukul975
tags:
- mobile-security
- ios
- frida
- objection
- ssl-pinning
- keychain
- ipa-analysis
- owasp-mastg
version: 1.0.0
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.AA-05
- ID.RA-01
- DE.CM-09
mitre_attack:
- T1059
- T1056
- T1036
- T1078
- T1003
---
# Performing iOS App Security Assessment

## Disclaimer

This skill is intended for authorized security testing, penetration testing engagements, CTF competitions, and educational purposes only. Unauthorized access to applications or devices is illegal. Always obtain written authorization before performing any security assessment. Misuse of these techniques may violate computer fraud and abuse laws in your jurisdiction.

## When to Use

Use this skill when:
- Conducting authorized penetration tests of iOS applications against OWASP MASVS/MASTG criteria
- Performing dynamic analysis of iOS apps using Frida instrumentation and Objection runtime exploration
- Bypassing SSL/TLS certificate pinning to intercept and analyze app network traffic through a proxy
- Extracting and auditing iOS Keychain contents for insecure credential storage practices
- Performing static analysis of IPA packages to identify hardcoded secrets, entitlements, and binary protections
- Assessing jailbreak detection and anti-tampering controls in iOS applications

**Do not use** against applications without explicit written authorization. Do not use on production devices containing real user data unless the engagement scope permits it.

## Prerequisites

- Python 3.10+ with pip
- Frida toolkit: `pip install frida-tools frida`
- Objection: `pip install objection`
- Target iOS device (jailbroken with frida-server, or non-jailbroken with patched IPA)
- macOS with Xcode command-line tools (recommended for code signing and ideviceinstaller)
- Burp Suite or mitmproxy for traffic interception after SSL pinning bypass
- For jailbroken devices: SSH access and frida-server running on the device
- For non-jailbroken devices: Apple Developer certificate for IPA re-signing

## Workflow

### Step 1: IPA Static Analysis

Extract and analyze the IPA binary before runtime testing:

```bash
# Unzip IPA for static analysis
unzip target.ipa -d target_app/

# Check binary architectures and protections
otool -hv target_app/Payload/*.app/AppExecutable
otool -l target_app/Payload/*.app/AppExecutable | grep -A4 LC_ENCRYPTION

# Extract Info.plist for entitlements and URL schemes
plutil -p target_app/Payload/*.app/Info.plist

# Search for hardcoded secrets in binary strings
strings target_app/Payload/*.app/AppExecutable | grep -iE "api[_-]?key|secret|password|token|firebase"

# Check embedded provisioning profile
security cms -D -i target_app/Payload/*.app/embedded.mobileprovision

# Identify linked frameworks
otool -L target_app/Payload/*.app/AppExecutable
```

### Step 2: Environment Setup and Frida Attachment

```bash
# For jailbroken device: verify Frida server is running
frida-ps -U

# Spawn target app with Frida
frida -U -f com.target.app --no-pause

# For non-jailbroken device: patch IPA with Frida Gadget
objection patchipa --source target.ipa --codesign-signature "Apple Development: tester@example.com"

# Install patched IPA
ideviceinstaller -i target-patched.ipa

# Attach Objection to running app
objection --gadget "com.target.app" explore
```

### Step 3: SSL Pinning Bypass

Bypass certificate pinning to enable traffic interception:

```bash
# Using Objection's built-in bypass
objection --gadget "com.target.app" explore --startup-command "ios sslpinning disable"

# Using Frida script for more comprehensive bypass
frida -U -f com.target.app -l ssl_pinning_bypass.js --no-pause

# Verify bypass by configuring device proxy to Burp Suite
# Device Settings -> Wi-Fi -> HTTP Proxy -> Manual -> <burp_ip>:8080
# Install Burp CA certificate on device via http://<burp_ip>:8080/cert
```

The Frida SSL pinning bypass script hooks into NSURLSession, NSURLConnection, and
AFNetworking/Alamofire trust evaluation delegates to override certificate validation
at the TLS handshake level.

### Step 4: Keychain Extraction and Credential Analysis

```bash
# Dump all accessible keychain items via Objection
ios keychain dump

# Dump keychain with raw data output
ios keychain dump --json

# Check keychain item accessibility attributes
# Items with kSecAttrAccessibleAlways or kSecAttrAccessibleAfterFirstUnlock
# are accessible without device unlock - this is a finding

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

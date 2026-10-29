---
name: performing-mobile-app-certificate-pinning-bypass
description: "Bypasses SSL/TLS certificate pinning in Android. Signals: mobile, Android attacks, iOS attacks."
zh-signals: "Bypasses SSL/TLS certificate pinning implementations in Android and 信号:移动端,android攻击,ios攻击。"
when-to-use: 'Bypasses SSL/TLS certificate pinning implementations in Android and
  iOS applications to enable traffic interception during authorized security assessments.
  Covers OkHttp, TrustManager, NSURLSession, and third-party pinning library bypass
  techniques using Frida, Objection, and custom scripts. Activates for requests involving
  certificate pinning bypass, SSL pinning defeat, mobile TLS interception, or proxy-resistant
  app testing.

  '
domain: cybersecurity
subdomain: mobile-security
author: mahipal
tags:
- mobile-security
- android
- ios
- certificate-pinning
- frida
- penetration-testing
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
- T1027
---
# Performing Mobile App Certificate Pinning Bypass

## When to Use

Use this skill when:
- Mobile app refuses connections through a proxy due to certificate pinning
- Performing authorized security testing requiring HTTPS traffic interception
- Assessing the strength and bypass difficulty of pinning implementations
- Evaluating defense-in-depth of mobile app network security

**Do not use** to bypass pinning on apps without explicit testing authorization.

## Prerequisites

- Burp Suite configured as proxy with listener on all interfaces
- Rooted Android device or jailbroken iOS device
- Frida server running on target device
- Objection installed (`pip install objection`)
- Target app installed and reproducing the pinning behavior

## Workflow

### Step 1: Identify Pinning Implementation

**Android pinning methods to identify:**
```
1. Network Security Config (res/xml/network_security_config.xml)
   <pin-set> with certificate hash pins

2. OkHttp CertificatePinner
   CertificatePinner.Builder().add("api.target.com", "sha256/...")

3. Custom TrustManager
   X509TrustManager overrides in code

4. Third-party libraries
   - TrustKit
   - Certificate Transparency checks
```

**iOS pinning methods:**
```
1. NSURLSession delegate (URLSession:didReceiveChallenge:)
2. ATS (App Transport Security) with custom trust evaluation
3. TrustKit framework
4. Alamofire ServerTrustPolicy
5. Custom SecTrust evaluation
```

### Step 2: Bypass with Objection (Quickest Approach)

```bash
# Android
objection --gadget com.target.app explore
android sslpinning disable

# iOS
objection --gadget com.target.app explore
ios sslpinning disable
```

Objection hooks common pinning implementations including OkHttp CertificatePinner, TrustManagerImpl, NSURLSession delegate methods, and SecTrust evaluation.

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

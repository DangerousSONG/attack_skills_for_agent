---
name: conducting-mobile-app-penetration-test
description: "Conducts penetration testing of iOS and Android mobile applications 信号:移动端,android攻击,ios攻击。"
when-to-use: 'Conducts penetration testing of iOS and Android mobile applications
  following the OWASP Mobile Application Security Testing Guide (MASTG) to identify
  vulnerabilities in data storage, network communication, authentication, cryptography,
  and platform-specific security controls. The tester performs static analysis of
  application binaries, dynamic analysis at runtime, and API security testing to evaluate
  the complete mobile attack surface. Activates for requests involving mobile app
  pentest, iOS security assessment, Android security testing, or OWASP MASTG assessment.

  '
domain: cybersecurity
subdomain: penetration-testing
tags:
- mobile-pentest
- OWASP-MASTG
- Android-security
- iOS-security
- mobile-application-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1426
- T1409
- T1521.003
- T1633
- T1417
- T1422
---
# Conducting Mobile App Penetration Test

## When to Use

- Testing mobile applications before release to identify security vulnerabilities and data protection issues
- Conducting compliance assessments against OWASP MASVS (Mobile Application Security Verification Standard) levels L1 and L2
- Evaluating the security of mobile banking, healthcare, or government applications handling sensitive data
- Testing mobile apps that interact with backend APIs to assess the end-to-end security of the mobile ecosystem
- Assessing mobile application resistance to reverse engineering, tampering, and runtime manipulation

**Do not use** against mobile applications without written authorization from the application owner, for distributing modified or repackaged applications, or for testing apps on the public app stores without a separate test build.

## Prerequisites

- Target application IPA (iOS) and APK (Android) files or access to download from a private distribution channel
- Rooted Android device or emulator (Genymotion, Android Studio AVD) with Frida, Objection, and Magisk installed
- Jailbroken iOS device or Corellium virtual device with Frida, Objection, and SSL Kill Switch installed
- Static analysis tools: jadx (Android decompilation), Hopper/Ghidra (iOS binary analysis), MobSF (automated scanning)
- Burp Suite Professional configured as proxy for intercepting mobile app traffic with CA certificate installed on the test device


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Static Analysis

Analyze the application binary without executing it:

**Android Static Analysis:**
- Decompile the APK: `jadx -d output/ target.apk` to obtain Java/Kotlin source code
- Review `AndroidManifest.xml` for exported components (activities, services, receivers, content providers), permissions, and debuggable flag
- Search for hardcoded secrets: `grep -rn "api_key\|password\|secret\|token\|aws_" output/`
- Identify insecure data storage patterns: SharedPreferences with sensitive data, SQLite databases without encryption, files in external storage
- Check for WebView vulnerabilities: `setJavaScriptEnabled(true)`, `addJavascriptInterface()`, and loading untrusted content
- Run MobSF automated scan: `python manage.py runserver` and upload the APK for automated static analysis

**iOS Static Analysis:**
- Extract the IPA and locate the Mach-O binary
- Use `otool -L <binary>` to list linked frameworks and identify third-party libraries
- Analyze with Ghidra or Hopper for hardcoded URLs, API endpoints, and embedded credentials
- Check Info.plist for App Transport Security (ATS) exceptions that allow insecure HTTP connections
- Review embedded entitlements for excessive capabilities

### Step 2: Network Security Testing

Intercept and analyze all network communications:

- Configure Burp Suite as proxy on the test device and install the Burp CA certificate
- Exercise all application functionality while Burp captures API traffic
- **SSL/TLS validation**: Verify the app validates server certificates properly. If the app fails to connect through the proxy, it may implement certificate pinning.
- **Certificate pinning bypass**:
  - Android: Use Frida script: `frida -U -f com.target.app -l ssl-pinning-bypass.js --no-pause`
  - iOS: Use SSL Kill Switch or Objection: `objection -g "Target App" explore --startup-command "ios sslpinning disable"`
- **API traffic analysis**: Review all API calls for:
  - Sensitive data transmitted without encryption
  - Authentication tokens in URL parameters (visible in logs)
  - Excessive data in API responses beyond what the UI displays
  - Missing or weak authentication on API endpoints
- **WebSocket and custom protocols**: Check for non-HTTP communication channels that may bypass standard proxy interception

### Step 3: Data Storage Analysis

Test for insecure local data storage:

**Android Data Storage:**
- Access app data directory: `/data/data/com.target.app/`
- Check SharedPreferences XML files for stored credentials, tokens, and PII
- Examine SQLite databases: `sqlite3 /data/data/com.target.app/databases/*.db ".dump"`
- Check for sensitive data in application logs: `logcat -d | grep -i "password\|token\|key"`
- Verify that application data is excluded from backups: `android:allowBackup="false"` in AndroidManifest.xml
- Check clipboard for sensitive data leakage

**iOS Data Storage:**
- Examine the Keychain for stored credentials: `objection -g "Target App" explore` then `ios keychain dump`
- Check NSUserDefaults/plist files: `find /var/mobile/Containers/Data/Application/ -name "*.plist" -exec plutil -p {} \;`
- Inspect SQLite databases and Core Data stores for unencrypted sensitive data
- Check for data leaking through screenshots (iOS captures screenshots during app backgrounding)
- Verify data protection class: sensitive files should use NSFileProtectionComplete

### Step 4: Authentication and Session Management

Test mobile-specific authentication controls:

- **Biometric bypass**: Test if biometric authentication can be bypassed by hooking the authentication callback with Frida to always return success
- **Token storage**: Verify that authentication tokens are stored in the Keychain (iOS) or Android Keystore, not in SharedPreferences or files
- **Session timeout**: Verify that sessions expire after a reasonable idle timeout and that tokens are invalidated server-side on logout
- **Root/jailbreak detection bypass**: Test if the app detects rooted/jailbroken devices and if the detection can be bypassed with Frida or Magisk Hide
- **Deep link abuse**: Test if custom URL schemes or universal links can be used to bypass authentication or access restricted functionality

### Step 5: Runtime Manipulation

Test the application's resistance to runtime attacks:

- **Frida hooking**: Use Frida to hook and modify application functions at runtime:
  - Bypass root detection: hook the detection function to return false
  - Modify return values of authentication checks
  - Intercept encryption functions to capture plaintext data before encryption
  - Bypass certificate pinning by hooking SSL verification
- **Method swizzling** (iOS): Use Frida to replace Objective-C method implementations
- **Intent manipulation** (Android): Send crafted intents to exported components: `adb shell am start -n com.target.app/.InternalActivity -e "user_id" "admin"`
- **Tampering detection**: Modify the APK/IPA (add code, change resources), re-sign, and install. Verify whether the app detects tampering.

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

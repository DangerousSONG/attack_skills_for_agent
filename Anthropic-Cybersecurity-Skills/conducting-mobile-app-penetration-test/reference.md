# conducting-mobile-app-penetration-test — 详细参考（由 SKILL.md 拆分）

## Key Concepts

| Term | Definition |
|------|------------|
| **OWASP MASTG** | Mobile Application Security Testing Guide; comprehensive manual for mobile app security testing covering both iOS and Android platforms |
| **Certificate Pinning** | A mobile security control that restricts which TLS certificates the app trusts, preventing man-in-the-middle attacks through proxy interception |
| **Frida** | Dynamic instrumentation toolkit that allows injection of JavaScript into running processes to hook functions, modify behavior, and bypass security controls |
| **Root/Jailbreak Detection** | Application-level checks to detect if the device has been modified to grant root access, typically blocking app usage on compromised devices |
| **Android Keystore** | Hardware-backed credential storage on Android that protects cryptographic keys and secrets from extraction even on rooted devices |
| **App Transport Security (ATS)** | iOS security feature that enforces HTTPS connections by default; ATS exceptions may indicate insecure network communication |
| **Deep Links** | URL schemes that open specific screens within a mobile application, which may bypass normal navigation and authentication flows if not properly validated |

## Tools & Systems

- **Frida / Objection**: Dynamic instrumentation tools for hooking functions, bypassing security controls, and manipulating application behavior at runtime
- **MobSF (Mobile Security Framework)**: Automated static and dynamic analysis platform for Android and iOS applications
- **jadx**: Android decompiler that converts APK bytecode to readable Java source code for manual code review
- **Burp Suite Professional**: HTTP proxy for intercepting and modifying mobile app API traffic after bypassing certificate pinning

## Common Scenarios

### Scenario: Mobile Banking Application Security Assessment

**Context**: A bank is launching a new mobile banking app for iOS and Android. The app handles account viewing, fund transfers, bill payment, and check deposit. OWASP MASVS L2 compliance is required due to the financial data handled.

**Approach**:
1. Static analysis of the Android APK reveals API endpoints, a hardcoded staging server URL, and an AWS API key in a configuration file
2. Certificate pinning is implemented but bypassed with Frida SSL pinning bypass script
3. API traffic analysis reveals that the balance check endpoint returns all account numbers associated with the user, not just the requested account
4. Local data storage analysis finds that the app caches the last 10 transactions in an unencrypted SQLite database
5. Biometric authentication bypass: Frida hook on the biometric callback always returns success, granting access without fingerprint
6. Root detection is present but bypassed with Magisk Hide module, allowing the app to run on a rooted device with full data access

**Pitfalls**:
- Testing only on an emulator and missing hardware-specific security features (Android Keystore hardware backing, iOS Secure Enclave)
- Not testing both iOS and Android versions, as they may have different implementations and different vulnerabilities
- Ignoring the backend API security because it was "tested separately" when the mobile app may call API endpoints differently than the web app
- Failing to test certificate pinning bypass, resulting in an incomplete network analysis

## Output Format

```
## Finding: Biometric Authentication Bypass via Frida Instrumentation

**ID**: MOB-003
**Severity**: High (CVSS 7.7)
**Platform**: Android and iOS
**OWASP MASVS**: MASVS-AUTH-2 (Biometric Authentication)

**Description**:
The mobile banking app's biometric authentication can be bypassed using Frida
dynamic instrumentation. The authentication callback function accepts a boolean
result from the biometric API, which can be hooked and forced to return true
without presenting a valid fingerprint or face scan.

**Proof of Concept (Android)**:
frida -U -f com.bank.mobileapp -l bypass-biometric.js --no-pause

// bypass-biometric.js
Java.perform(function() {
  var BiometricCallback = Java.use("com.bank.mobileapp.auth.BiometricCallback");
  BiometricCallback.onAuthenticationSucceeded.implementation = function(result) {
    console.log("[*] Biometric bypassed");
    this.onAuthenticationSucceeded(result);
  };
});

**Impact**:
An attacker with physical access to an unlocked device can bypass biometric
authentication and access the victim's bank accounts, initiate transfers,
and view financial data without biometric verification.

**Remediation**:
1. Implement server-side biometric verification using Android BiometricPrompt
   CryptoObject tied to a Keystore key
2. Require the biometric operation to decrypt a server-side challenge, making
   client-side bypass ineffective
3. Add runtime integrity checks to detect Frida and other instrumentation frameworks
4. Implement step-up authentication for high-risk operations (transfers > threshold)
```

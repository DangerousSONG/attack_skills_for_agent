---
name: performing-dynamic-analysis-of-android-app
description: "Perform runtime dynamic analysis of Android applications using Frida. Signals: mobile, android attack, ios attack."
zh-signals: "Performs runtime dynamic analysis of Android applications using Frida 信号:移动端,android攻击,ios攻击。"
when-to-use: 'Performs runtime dynamic analysis of Android applications using Frida,
  Objection, and Android Debug Bridge to observe application behavior during execution,
  intercept function calls, modify runtime values, and identify vulnerabilities that
  static analysis misses. Use when testing Android apps for runtime security flaws,
  hooking sensitive methods, bypassing client-side protections, or analyzing obfuscated
  applications. Activates for requests involving Android dynamic analysis, runtime
  hooking, Frida Android instrumentation, or live app behavior analysis.

  '
domain: cybersecurity
subdomain: mobile-security
author: mahipal
tags:
- mobile-security
- android
- frida
- dynamic-analysis
- owasp-mobile
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
# Performing Dynamic Analysis of Android App

## When to Use

Use this skill when:
- Static analysis results need runtime validation on an actual Android device
- The target app uses obfuscation (DexGuard, custom packers) that prevents effective static analysis
- Testing requires observing actual API calls, decrypted data, or runtime-generated values
- Assessing root detection, tamper detection, or anti-debugging implementations

**Do not use** this skill on production environments without authorization -- dynamic instrumentation can alter app behavior and trigger security alerts.

## Prerequisites

- Rooted Android device or emulator (Genymotion, Android Studio AVD with writable system)
- Frida server installed on device matching the architecture (arm64, x86_64)
- Python 3.10+ with `frida-tools` and `objection` packages
- ADB configured and device connected
- Target APK installed on device

## Workflow

### Step 1: Setup Frida Server on Android Device

```bash
# Check device architecture
adb shell getprop ro.product.cpu.abi
# Output: arm64-v8a

# Download matching Frida server from GitHub releases
# https://github.com/frida/frida/releases
# Push to device
adb push frida-server-16.x.x-android-arm64 /data/local/tmp/frida-server
adb shell chmod 755 /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &

# Verify Frida connection
frida-ps -U
```

### Step 2: Enumerate Application Attack Surface

```bash
# List all packages
frida-ps -U -a

# Attach Objection for high-level exploration
objection --gadget com.target.app explore

# List activities, services, receivers
android hooking list activities
android hooking list services
android hooking list receivers

# List loaded classes
android hooking list classes
android hooking search classes com.target.app
```

### Step 3: Hook Sensitive Methods

```bash
# Hook all methods of a class
android hooking watch class com.target.app.auth.LoginManager

# Hook specific method with argument dumping
android hooking watch class_method com.target.app.auth.LoginManager.authenticate --dump-args --dump-return

# Hook crypto operations
android hooking watch class javax.crypto.Cipher --dump-args
android hooking watch class java.security.MessageDigest --dump-args

# Hook network calls
android hooking watch class okhttp3.OkHttpClient --dump-args
android hooking watch class java.net.URL --dump-args
```

### Step 4: Write Custom Frida Scripts for Deep Analysis

```javascript
// hook_crypto.js - Intercept encryption/decryption operations
Java.perform(function() {
    var Cipher = Java.use("javax.crypto.Cipher");

    Cipher.doFinal.overload("[B").implementation = function(input) {
        var mode = this.getAlgorithm();
        console.log("[Cipher] Algorithm: " + mode);
        console.log("[Cipher] Input: " + bytesToHex(input));

        var result = this.doFinal(input);
        console.log("[Cipher] Output: " + bytesToHex(result));
        return result;
    };

    function bytesToHex(bytes) {
        var hex = [];
        for (var i = 0; i < bytes.length; i++) {
            hex.push(("0" + (bytes[i] & 0xFF).toString(16)).slice(-2));
        }
        return hex.join("");
    }
});
```

```bash
# Execute custom Frida script
frida -U -f com.target.app -l hook_crypto.js --no-pause
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

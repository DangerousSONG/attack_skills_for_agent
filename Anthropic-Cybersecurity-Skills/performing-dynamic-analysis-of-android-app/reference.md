# performing-dynamic-analysis-of-android-app — 详细参考（由 SKILL.md 拆分）

### Step 5: Bypass Root Detection

```javascript
// root_bypass.js - Common root detection bypass
Java.perform(function() {
    // Bypass RootBeer library
    var RootBeer = Java.use("com.scottyab.rootbeer.RootBeer");
    RootBeer.isRooted.implementation = function() {
        console.log("[RootBeer] isRooted() bypassed");
        return false;
    };

    // Bypass generic file-based root checks
    var File = Java.use("java.io.File");
    var originalExists = File.exists;
    File.exists.implementation = function() {
        var path = this.getAbsolutePath();
        var rootPaths = ["/system/app/Superuser.apk", "/system/xbin/su",
                         "/sbin/su", "/system/bin/su", "/data/local/bin/su"];
        if (rootPaths.indexOf(path) >= 0) {
            console.log("[Root] Blocked check for: " + path);
            return false;
        }
        return originalExists.call(this);
    };

    // Bypass SafetyNet/Play Integrity
    try {
        var SafetyNet = Java.use("com.google.android.gms.safetynet.SafetyNetApi");
        console.log("[SafetyNet] Class found - may need additional bypass");
    } catch(e) {}
});
```

### Step 6: Analyze Network Communication at Runtime

```javascript
// network_monitor.js - Monitor all HTTP requests
Java.perform(function() {
    // Hook OkHttp3
    try {
        var OkHttpClient = Java.use("okhttp3.OkHttpClient");
        var Interceptor = Java.use("okhttp3.Interceptor");
        var Chain = Java.use("okhttp3.Interceptor$Chain");

        console.log("[OkHttp] Monitoring network requests...");

        var Request = Java.use("okhttp3.Request");
        Request.url.implementation = function() {
            var url = this.url();
            console.log("[OkHttp] URL: " + url.toString());
            return url;
        };
    } catch(e) {
        console.log("[OkHttp] Not found, trying HttpURLConnection");
    }

    // Hook HttpURLConnection
    var URL = Java.use("java.net.URL");
    URL.openConnection.overload().implementation = function() {
        console.log("[URL] Opening: " + this.toString());
        return this.openConnection();
    };
});
```

### Step 7: Extract Decrypted Data and Secrets

```bash
# Using Objection for quick extraction
objection --gadget com.target.app explore

# Dump Android Keystore entries
android keystore list
android keystore dump

# Search heap for sensitive objects
android heap search instances com.target.app.model.User
android heap evaluate <handle> "JSON.stringify(clazz)"

# Memory string search
memory search "password" --string
memory search "api_key" --string
```

## Key Concepts

| Term | Definition |
|------|-----------|
| **Dynamic Instrumentation** | Modifying application behavior at runtime by injecting code into the running process |
| **Method Hooking** | Replacing or wrapping function implementations to intercept arguments and return values |
| **Frida Server** | Daemon running on the target device that receives instrumentation commands from the host |
| **Dalvik/ART Runtime** | Android runtime environments; Frida hooks at the ART level for Java/Kotlin methods |
| **Heap Inspection** | Examining live objects in the application's memory heap to extract runtime data |

## Tools & Systems

- **Frida**: Dynamic instrumentation toolkit for injecting JavaScript into native Android processes
- **Objection**: Higher-level Frida wrapper with pre-built Android and iOS security testing commands
- **frida-trace**: Automated method tracing utility for quick reconnaissance of app behavior
- **Drozer**: Android security assessment framework for testing IPC and exported components
- **Android Studio Profiler**: Runtime monitoring for CPU, memory, and network activity

## Common Pitfalls

- **Frida version mismatch**: The Frida server on the device must match the frida-tools version on the host. Version mismatches cause connection failures.
- **Anti-Frida detection**: Some apps detect Frida by checking for the Frida server process, scanning memory for Frida signatures, or monitoring `/proc/self/maps`. Use Frida Gadget injection or custom server builds.
- **Obfuscated class names**: When ProGuard/R8 is applied, class and method names are shortened (e.g., `a.b.c.d()`). Use `android hooking search classes` to discover actual runtime names.
- **Multi-DEX apps**: Large apps split across multiple DEX files may not have all classes loaded at startup. Hook class loaders or use `Java.enumerateLoadedClasses()` after app is fully initialized.

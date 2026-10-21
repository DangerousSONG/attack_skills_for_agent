# performing-initial-access-with-evilginx3 — 详细参考（由 SKILL.md 拆分）

### Phase 3: Phishing Delivery
1. Craft a pretext email with the lure URL embedded
2. Use GoPhish or manual SMTP for email delivery:
   ```
   # Integration with EvilGoPhish for combined campaigns
   # Provides GoPhish email tracking + EvilGinx3 credential capture
   ```
3. Implement URL masking or shortening if needed for link obfuscation
4. Deploy landing page with appropriate social engineering pretext

### Phase 4: Session Hijacking
1. Monitor EvilGinx3 for captured sessions:
   ```
   sessions
   sessions <session-id>
   ```
2. Extract captured session cookies from the session:
   ```
   # Session output includes:
   # - Username and password
   # - Session cookies (authentication tokens)
   # - Custom captured parameters
   ```
3. Import session cookies into a browser using a cookie editor extension:
   - Export cookies in JSON format
   - Use Cookie-Editor or EditThisCookie browser extension
   - Navigate to the target service to validate session hijack
4. Establish persistent access by creating application passwords or OAuth tokens

### Phase 5: Post-Access Activities
1. Enumerate mailbox contents, contacts, and shared drives
2. Identify additional targets for lateral phishing
3. Check for access to connected cloud applications (SharePoint, Teams, OneDrive)
4. Document all captured credentials and access achieved

## Tools and Resources

| Tool | Purpose | Platform |
|------|---------|----------|
| EvilGinx3 | AiTM phishing framework | Linux |
| GoPhish | Phishing campaign management | Cross-platform |
| EvilGoPhish | Combined EvilGinx3 + GoPhish integration | Linux |
| Cookie-Editor | Browser cookie import/export | Browser Extension |
| Modlishka | Alternative AiTM proxy framework | Linux |
| Muraena | Alternative AiTM phishing proxy | Linux |

## Phishlet Targets

| Target Service | Phishlet | Captured Data |
|---------------|----------|---------------|
| Microsoft 365 | o365 | Session cookies, credentials |
| Google Workspace | google | Session cookies, credentials |
| Okta | okta | Session tokens, credentials |
| GitHub | github | Session cookies, credentials |
| AWS Console | aws | Session tokens, credentials |

## Detection Indicators

| Indicator | Detection Method |
|-----------|-----------------|
| Newly registered lookalike domains | Domain monitoring and certificate transparency logs |
| SSL certificates for suspicious domains | CT log monitoring (crt.sh, Censys) |
| Unusual login locations after phishing | SIEM correlation of authentication events |
| Session cookie replay from different IP | Conditional access policy alerts |
| AiTM proxy headers in traffic | Network inspection for proxy artifacts |

## Validation Criteria

- [ ] EvilGinx3 deployed with valid SSL certificates
- [ ] Phishlet configured and enabled for target service
- [ ] Lure URL generated and accessible
- [ ] Test credentials captured successfully through phishing flow
- [ ] Session cookies captured and validated for MFA bypass
- [ ] Session hijack demonstrated in browser with stolen cookies
- [ ] Post-authentication access to target service confirmed
- [ ] Evidence documented with screenshots and session logs

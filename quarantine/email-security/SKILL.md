---
name: email-security
description: "Authorized email security review: phishing analysis, SPF/DKIM/DMARC header authentication, BEC pattern investigation, and mailbox token abuse research."
zh-signals: "授权邮件安全审查，分析钓鱼邮件、SPF/DKIM/DMARC 认证、BEC 模式与邮箱令牌滥用。信号:邮件安全,钓鱼分析,SPF/DKIM/DMARC,BEC,邮件认证"
when-to-use: "Use when reviewing an authorized domain's email authentication posture or analyzing suspicious phishing messages and BEC patterns."
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

> **Mandatory confirmation gate**
> Before running any command that probes, exploits, changes, persists on, extracts data from, or attempts credential access against a target:
> 1. Ask the user to state the exact target URL, IP, account, or resource.
> 2. Ask the user to confirm written authorization and the permitted scope.
> 3. Show the exact command(s) and explain their expected effect.
> 4. Wait for explicit confirmation in the current conversation.
>
> Without that confirmation, remain read-only and provide defensive guidance only. Prefer a sandbox, disposable VM, or controlled lab.

# Email Security & Phishing Analysis
## When to Use

- Analyzing suspicious messages or domain spoofing exposure.
- Validating a domain's email authentication posture.


## Applicable Scenarios

- Phishing email teardown and IOCs
- SPF/DKIM/DMARC configuration assessment
- BEC (business email compromise) fraud patterns
- OAuth app phishing / mailbox token abuse (joint with llm/cloud identity)
- Security awareness exercise design (authorized)

## Workflow

```text
□ Full raw headers: Received chain, From/Return-Path consistency
□ SPF/DKIM/DMARC alignment results
□ URL sandboxing and static attachment analysis (joint with malware-analysis)
□ Impersonated brand vs. reply address differences
□ Tenant: anti-phishing policy, external markings, MFA, OAuth app consent
```

## Toolchain

| Tool | Purpose |
|------|------|
| Email client "view source" | headers |
| dig/nslookup | SPF/DMARC records |
| urlscan / sandbox | links and attachments |
| Tenant admin center | policy |

## References

- `references/email-auth-checklist.md`
- `../malware-analysis/` `../attack-chain/` (phishing stage) `../windows-ad/` (tokens)

## Routing Context

**Upstream**: MASTER R36  
**MUST NOT**: bulk phishing testing against third-party domains without authorization

## Task Completion Self-Check

- [ ] Is the header authentication conclusion complete?
- [ ] Are the IOCs detectable (joint with threat-hunting)?
- [ ] Checklist?

## Limitations

- Live mailbox investigation touches personal data; minimize and anonymize.
- Header analysis cannot detect compromise that leaves no mail trail.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).

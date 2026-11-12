---
name: jwtcat-token-crack
description: "jwtcat takes over weak JWT signing keys. Signals: API attack, interface testing, JWT signing key brute force, inline token."
zh-signals: "jwtcat: 弱 JWT 密钥接管。信号:api攻击,接口测试,JWT 签名密钥爆破,直接内联 token。"
when-to-use: >-
  Use when testing APIs that issue JWT tokens and you suspect a weak HMAC signing key; brute-
  force the secret from a wordlist, then forge tokens for other users.
---

# jwtcat

- Attack Category: C10 API and GraphQL Attacks
- Upstream Repository: https://github.com/aress31/jwtcat
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install jwtcat
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `jwtcat -t token.txt -w wordlist.txt` | JWT signing key brute force |
| `-t eyJ... -w rockyou.txt` | Inline token directly |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Weak JWT Key Takeover

```bash
jwtcat -t token.txt -w rockyou.txt
# After brute-forcing a weak HS256 key, forge tokens for arbitrary users
```

## Notes

JWT key dictionary brute force; on a hit, forge an admin token with pyjwt or similar.

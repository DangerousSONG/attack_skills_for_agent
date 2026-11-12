---
name: myjwt-jwt-audit
description: "MyJWT: JWT multi-attack-surface testing. Signals: API attack, interface testing, JWT key brute force, KID injection, JKU bypass."
zh-signals: "MyJWT: JWT 多攻击面测试。信号:api攻击,接口测试,JWT 密钥爆破,KID 注入,JKU 绕过。"
when-to-use: >-
  Use when auditing JWT implementations for multiple weaknesses at once, including weak key brute
  force, KID injection, JKU bypass, and payload tampering.
---

# MyJWT

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/mBouamama/MyJWT
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install myjwt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `myjwt 'eyJ...' --crack /tmp/wordlist.txt` | JWT key brute force |
| `myjwt 'token' --kid injection` | KID injection |
| `--jku bypass` | JKU bypass |
| `--modify-payload 'admin:true'` | Payload tampering |
| `--verify` | Verify the signature |

## Attack Scenario Playbook

### Multi-Attack-Surface JWT Testing

```bash
myjwt $TOKEN --crack rockyou.txt
# Covers weak keys/kid/jku/alg:none in one pass
```

## Notes

A Swiss Army knife for JWT vulnerabilities: cracking/tampering/kid/jku/alg confusion.

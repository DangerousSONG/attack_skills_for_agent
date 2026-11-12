---
name: jwt-tool-token
description: "jwt_tool performs JWT attacks including jku/x5u injection to spoof server keys. Signals: API attack, interface testing, comprehensive token audit, offline dictionary cracking."
zh-signals: "jwt_tool: JWT 五连击、jku/x5u 注入拿服务端公钥欺骗。信号:api攻击,接口测试,令牌全面体检,离线破解字典。"
when-to-use: >-
  Use when auditing JWT implementations, including algorithm confusion, jku/x5u and kid injection, offline secret cracking and token replay during API testing.
---

# jwt_tool

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/ticarpi/jwt_tool
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ticarpi/jwt_tool && cd jwt_tool && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python jwt_tool.py <JWT>` | Comprehensive token audit |
| `-M at` | Tampering (alg none / RS256→HS256) |
| `-C` | Offline dictionary cracking |
| `-X a` | Brute force all |
| `-I` | Injection targets (forged kid/jwk/x5u) |
| `-T` | Token replay |
| `-jw` | JWKS injection |
| `-Q` | Query expiration / not-before |

## Attack Scenario Playbook

### The JWT five-hit combo

```bash
python jwt_tool.py eyJhbG... -M at  # automatically tries alg:none / key confusion / weak signatures
python jwt_tool.py eyJhbG... -C -d secrets.txt  # HS256 key brute force
python jwt_tool.py eyJhbG... -X i -I  # tries kid injection to forge signatures
```

### jku/x5u injection to spoof the server public key

```bash
python jwt_tool.py eyJhbG... -M i  # automatically probes jwks injection points and builds a PoC
```

## Notes

The de facto standard for JWT security testing; supports 30+ attack modes including the confusion and injection surfaces introduced in 2023.

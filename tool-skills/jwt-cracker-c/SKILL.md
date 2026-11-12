---
name: jwt-cracker-c
description: "jwt-cracker brute-forces HS256 keys quickly. Signals: API attack, interface testing, charset brute force, maximum length."
zh-signals: "jwt-cracker: HS256 密钥高速爆破。信号:api攻击,接口测试,字符集爆破,最大长度。"
when-to-use: >-
  Use when you have an HS256-signed JWT and want to recover the weak secret via high-speed C brute force or charset enumeration so you can forge tokens.
---

# jwt-cracker

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/brendan-rius/c-jwt-cracker
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/brendan-rius/c-jwt-cracker && cd c-jwt-cracker && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./jwtcrack <token> /usr/share/wordlists/rockyou.txt` | Ultra-fast C HS256 key brute force |
| `-a charset` | Charset brute force |
| `-m 8` | Maximum length |

## Attack Scenario Playbook

### High-speed HS256 key brute force

```bash
./jwtcrack $TOKEN rockyou.txt  # Multi-threaded C implementation, two orders of magnitude faster than python
```

## Notes

CPU brute forcer with GPU-class throughput; once the key is recovered you can forge tokens at will.

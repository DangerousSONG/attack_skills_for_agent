---
name: jwtcat-token-crack
description: "jwtcat takes over weak JWT signing keys. Signals: API attack, interface testing, JWT signing key brute force, inline token."
zh-signals: "jwtcat: 弱 JWT 密钥接管。信号:api攻击,接口测试,JWT 签名密钥爆破,直接内联 token。"
---

# jwtcat

- 攻击大类:C10 API与GraphQL攻击
- 上游仓库:https://github.com/aress31/jwtcat
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install jwtcat
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `jwtcat -t token.txt -w wordlist.txt` | JWT 签名密钥爆破 |
| `-t eyJ... -w rockyou.txt` | 直接内联 token |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 弱 JWT 密钥接管

```bash
jwtcat -t token.txt -w rockyou.txt
# 弱 HS256 密钥爆破后伪造任意用户 token
```

## 注意事项

JWT 密钥字典爆破,命中后用 pyjwt 等伪造 admin token。

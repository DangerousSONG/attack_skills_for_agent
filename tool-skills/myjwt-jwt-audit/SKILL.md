---
name: myjwt-jwt-audit
description: "MyJWT: JWT multi-attack-surface testing. Signals: API attack, interface testing, JWT key brute force, KID injection, JKU bypass."
zh-signals: "MyJWT: JWT 多攻击面测试。信号:api攻击,接口测试,JWT 密钥爆破,KID 注入,JKU 绕过。"
---

# MyJWT

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/mBouamama/MyJWT
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install myjwt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `myjwt 'eyJ...' --crack /tmp/wordlist.txt` | JWT 密钥爆破 |
| `myjwt 'token' --kid injection` | KID 注入 |
| `--jku bypass` | JKU 绕过 |
| `--modify-payload 'admin:true'` | payload 篡改 |
| `--verify` | 校验签名 |

## 攻击场景 Playbook

### JWT 多攻击面测试

```bash
myjwt $TOKEN --crack rockyou.txt
# 弱密钥/kid/jku/alg:none 全覆盖
```

## 注意事项

JWT 漏洞 Swiss Army: 爆破/篡改/kid/jku/alg confusion。

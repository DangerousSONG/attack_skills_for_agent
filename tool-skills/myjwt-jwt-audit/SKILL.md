---
name: myjwt-jwt-audit
description: 渗透工具 skill:MyJWT 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 MyJWT 时使用。
when-to-use: 渗透工具 skill:MyJWT 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 MyJWT 时使用。
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

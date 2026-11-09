---
name: jwt-hack-token
description: "jwt-hack quickly decodes and brute-forces tokens. Signals: API attack, interface testing, token decoding, key brute force."
zh-signals: "jwt-hack: 快速令牌拆解与爆破。信号:api攻击,接口测试,解码,爆破密钥。"
---

# jwt-hack

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/mboekamp/jwt-hack
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/mboekamp/jwt-hack@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `jwt-hack decode <token>` | 解码 |
| `jwt-hack encode -alg HS256 -payload '{"a":1}'` | 生成 |
| `jwt-hack brute -t <token> -w words.txt` | 爆破密钥 |
| `jwt-hack none -t <token>` | alg:none 攻击 |

## 攻击场景 Playbook

### 快速令牌拆解与爆破

```bash
jwt-hack brute -t $TOKEN -w jwt.secrets.list
jwt-hack none -t $TOKEN
```

## 注意事项

jwt_tool 的轻量 Go 替代;单二进制适合目标机投递。

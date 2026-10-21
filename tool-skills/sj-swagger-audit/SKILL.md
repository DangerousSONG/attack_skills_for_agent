---
name: sj-swagger-audit
description: 渗透工具 skill:sj 的安装、参数速查与攻击场景 playbook。当任务涉及 API与GraphQL攻击 需要调用 sj 时使用。
when-to-use: 渗透工具 skill:sj 的安装、参数速查与攻击场景 playbook。当任务涉及 API与GraphQL攻击 需要调用 sj 时使用。
---

# sj

- 攻击大类:C10 API与GraphQL攻击
- 上游仓库:https://github.com/BishopFox/sj
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/BishopFox/sj@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sj prepare -u https://t.com/swagger.json` | 自动构造 API 请求 |
| `sj brute -u https://t.com/swagger.json -w paths.txt` | 路径爆破 |
| `sj audit -u https://t.com/openapi.json` | 全端点审计 |
| `sj automate -u spec.json` | 半自动渗透 |

## 攻击场景 Playbook

### OpenAPI 规范直连渗透

```bash
sj audit -u https://api.t.com/openapi.json
# 按规范逐个端点发请求,自动检测鉴权缺失
```

## 注意事项

BishopFox 出品,读取 Swagger/OpenAPI 规范自动生成并测试所有 API 端点。

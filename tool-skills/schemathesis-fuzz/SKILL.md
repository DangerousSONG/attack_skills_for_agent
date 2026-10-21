---
name: schemathesis-fuzz
description: 渗透工具 skill:Schemathesis 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 Schemathesis 时使用。
when-to-use: 渗透工具 skill:Schemathesis 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 Schemathesis 时使用。
---

# Schemathesis

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/schemathesis/schemathesis
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install schemathesis
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `st run https://t.com/openapi.json` | 属性化模糊测试 |
| `-H 'Authorization: Bearer x'` | 头 |
| `-E POST /users` | 只测端点 |
| `--checks all` | 全检查 |
| `-o yaml` | 报告格式 |
| `--stateful=links` | 有状态测试 |

## 攻击场景 Playbook

### OpenAPI 规范驱动模糊测试

```bash
st run https://api.target.com/openapi.json -H 'Authorization: Bearer $TOKEN' --checks all
# 自动生成边界值/类型混淆/SQLi 特征输入,输出可复现用例
```

## 注意事项

基于 OpenAPI/Swagger 规范自动生成测试用例;契约违背与 5xx 都是 findings。

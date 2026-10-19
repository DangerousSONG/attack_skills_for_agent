---
name: whoxyrm-reverse-whois
description: 渗透工具 skill:WhoxyRM 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 WhoxyRM 时使用。
---

# WhoxyRM

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/MilindPurswani/whoxyrm
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/MilindPurswani/whoxyrm@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `whoxyrm -company-name 'Target Corp' -api-key X` | 反查注册组织名下域名 |
| `-email admin@target.com` | 按邮箱反查 |

## 攻击场景 Playbook

### WHOIS 反查关联资产

```bash
whoxyrm -company-name 'Target Inc' -api-key $KEY
# 同一注册组织的全部历史域名,影子资产一锅端
```

## 注意事项

Whoxy API 的 CLI;组织名/邮箱/电话反查域名是影子资产发现利器。

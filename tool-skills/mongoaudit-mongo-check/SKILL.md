---
name: mongoaudit-mongo-check
description: 渗透工具 skill:mongoaudit 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 mongoaudit 时使用。
when-to-use: 渗透工具 skill:mongoaudit 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 mongoaudit 时使用。
---

# mongoaudit

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/stampery/mongoaudit
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install mongoaudit
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `mongoaudit -h 10.0.0.5 -p 27017` | MongoDB 审计 |
| `-h host -u user -p pass` | 带认证 |
| `-f out.json` | JSON 输出 |

## 攻击场景 Playbook

### MongoDB 未授权+弱配置

```bash
mongoaudit -h 10.0.0.5
# 未授权访问/弱口令/旧版漏洞
```

## 注意事项

MongoDB 安全审计,10+ 项检测含 CVE。

---
name: dawnscanner-ruby-audit
description: 渗透工具 skill:dawnscanner 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 dawnscanner 时使用。
when-to-use: 渗透工具 skill:dawnscanner 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 dawnscanner 时使用。
---

# dawnscanner

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/thesp0nge/dawnscanner
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install dawnscanner
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dawn -r /path/to/rails/app` | Rails 应用静态审计 |
| `dawn --ruby myapp` | Ruby 版本漏洞 |
| `-K` | 仅知识库模式 |
| `-F txt` | 报告格式 |

## 攻击场景 Playbook

### Rails 应用代码审计

```bash
dawn -r /src/webapp
# 静态分析 Ruby on Rails 已知 CVE 模式
```

## 注意事项

Ruby/Rails 静态安全审计,检测已知 CVE 对应的代码模式。

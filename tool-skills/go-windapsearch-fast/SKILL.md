---
name: go-windapsearch-fast
description: 渗透工具 skill:go-windapsearch 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 go-windapsearch 时使用。
when-to-use: 渗透工具 skill:go-windapsearch 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 go-windapsearch 时使用。
---

# go-windapsearch

- 攻击大类:C29 AD与LDAP枚举
- 上游仓库:https://github.com/ropnop/go-windapsearch
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/ropnop/go-windapsearch@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `windapsearch -d corp.local -u svc -p pass --dc 10.0.0.1 --users` | 枚举用户 |
| `--custom '(&(sAMAccountType=805306368)(adminCount=1))'` | 自定义查询 |
| `--full` | 全属性输出 |
| `--krb5 -k svc.ccache` | 票据认证 |

## 攻击场景 Playbook

### 高速批量 LDAP 枚举

```bash
cat dcs.txt | xargs -I{} windapsearch -d corp.local -u svc -p pass --dc {} --users
# Go 版并发快,跨多 DC 拉用户清单
```

## 注意事项

windapsearch 的 Go 重写版,单文件无依赖+Kerberos 票据认证,适合受限环境。

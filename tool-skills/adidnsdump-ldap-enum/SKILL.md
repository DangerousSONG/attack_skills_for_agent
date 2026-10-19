---
name: adidnsdump-ldap-enum
description: 渗透工具 skill:adidnsdump 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 adidnsdump 时使用。
---

# adidnsdump

- 攻击大类:C29 AD与LDAP枚举
- 上游仓库:https://github.com/dirkjanm/adidnsdump
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install git+https://github.com/dirkjanm/adidnsdump.git 或 apt install adidnsdump
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `adidnsdump -u 'corp.local\svc' -p 'pass' dc01.corp.local` | 导出 AD 集成 DNS 全记录 |
| `-u user@corp.local -p pass --print-zones` | 只列出区域 |
| `-r` | 解析记录获取 IP |
| `--include-tombstoned` | 含已删除记录 |

## 攻击场景 Playbook

### AD DNS 记录收割(发现服务器)

```bash
adidnsdump -u 'corp.local\svc' -p 'Pass1' dc01.corp.local -r
# 得 *.corp.local 全解析,重点看 dev/test/backup 等非生产域
```

## 注意事项

dirkjanm 出品。AD 集成 DNS 往往是域内主机最全清单,含未登记资产,信息收集价值极高。

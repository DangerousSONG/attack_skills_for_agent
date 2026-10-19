---
name: crosslinkedin-osint
description: 渗透工具 skill:CrossLinked 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 CrossLinked 时使用。
---

# CrossLinked

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/m8sec/CrossLinked
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install crosslinked
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `crosslinked -f '{first}.{last}@corp.com' corp` | LinkedIn 员工邮箱生成 |
| `-f fmt -t company` | 格式 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### LinkedIn 员工字典

```bash
crosslinked -f '{first}.{last}@corp.com' 'Target Corp'
# 邮箱喷洒前置
```

## 注意事项

m8sec 出品,LinkedIn 员工信息转邮箱字典。

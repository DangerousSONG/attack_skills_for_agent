---
name: socialscan-username
description: 渗透工具 skill:socialscan 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 socialscan 时使用。
---

# socialscan

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/iojw/socialscan
- 上游 License:MPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install socialscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `socialscan --email victim@x.com` | 邮箱可用性/注册查询 |
| `--username user1 user2` | 用户名批量 |
| `--platform twitter github` | 指定平台 |
| `--json` | JSON 输出 |

## 攻击场景 Playbook

### 凭据组合前置侦察

```bash
socialscan --email a@corp.com --email b@corp.com --username ceo_corp
# 确认常用用户名/邮箱占用情况,构造精准凭据字典
```

## 注意事项

异步并发查询,速度比 holehe 快;结果用于 username-anarchy 生成变形字典。

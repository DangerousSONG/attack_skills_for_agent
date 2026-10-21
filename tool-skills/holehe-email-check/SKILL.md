---
name: holehe-email-check
description: 渗透工具 skill:holehe 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 holehe 时使用。
when-to-use: 渗透工具 skill:holehe 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 holehe 时使用。
---

# holehe

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/megadose/holehe
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install holehe
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `holehe test@gmail.com` | 查邮箱注册站点 |
| `--only-used` | 只显示已注册 |
| `-C creds.json` | 保存 cookies |
| `-p 20` | 并发 |
| `--no-passwords` | 不触发找回逻辑 |

## 攻击场景 Playbook

### 邮箱注册足迹画像

```bash
holehe victim@corp.com --only-used
# 输出 Twitter/Instagram/Adobe 等注册站点,勾勒目标画像
```

## 注意事项

通过忘记密码接口侧信道判断注册状态,不产生登录尝试,隐蔽性好。

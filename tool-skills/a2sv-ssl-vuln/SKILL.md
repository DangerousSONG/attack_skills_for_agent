---
name: a2sv-ssl-vuln
description: 渗透工具 skill:a2sv 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 a2sv 时使用。
when-to-use: 渗透工具 skill:a2sv 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 a2sv 时使用。
---

# a2sv

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/hahwul/a2sv
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hahwul/a2sv && cd a2sv && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python a2sv.py -t t.com` | SSL 漏洞扫描 |
| `-t ip -p 443` | 端口 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### SSL/TLS CVE 检测

```bash
python a2sv.py -t t.com
# Heartbleed/CCS/POODLE 等 17 个 CVE
```

## 注意事项

SSL 漏洞扫描器,覆盖 Heartbleed 等经典 CVE。

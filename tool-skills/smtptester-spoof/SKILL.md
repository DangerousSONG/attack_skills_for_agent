---
name: smtptester-spoof
description: SMTPTester: SPF/DKIM 绕过测试。信号:钓鱼,社会工程,SMTP 伪造测试,TLS。
---

# SMTPTester

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/xFreed0m/SMTPTester
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/xFreed0m/SMTPTester && cd SMTPTester && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 SMTPTester.py -t mail.t.com -f attacker@evil.com -v` | SMTP 伪造测试 |
| `-t target -f from -to victim@corp.com` | 参数 |
| `-s` | TLS |

## 攻击场景 Playbook

### SPF/DKIM 绕过测试

```bash
python3 SMTPTester.py -t mail.t.com -f ceo@corp.com -to finance@corp.com
# 测试邮件伪造
```

## 注意事项

SMTP 开放中继+伪造测试。

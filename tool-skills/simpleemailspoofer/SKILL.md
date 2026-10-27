---
name: simpleemailspoofer
description: SimpleEmailSpoofer: 钓鱼邮件伪造测试。信号:钓鱼,社会工程,指定 SMTP,HTML 模式。
---

# SimpleEmailSpoofer

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/lunarca/SimpleEmailSpoofer
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/lunarca/SimpleEmailSpoofer && cd SimpleEmailSpoofer
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python SimpleEmailSpoofer.py -e attacker@evil.com -t victim@corp.com -s 'Urgent' -m body.txt -f ceo@corp.com` | 邮件伪造 |
| `-e from -t to -s subj -m msg -f spoof` | 参数 |
| `-S server` | 指定 SMTP |
| `-p` | HTML 模式 |

## 攻击场景 Playbook

### 钓鱼邮件伪造测试

```bash
python SimpleEmailSpoofer.py -e x@evil.com -t finance@corp.com -s '发票' -m mail.txt -f ceo@corp.com
# 测 SPF/DKIM/DMARC 绕过,红队钓鱼评估
```

## 注意事项

极简 SMTP 伪造工具,钓鱼演练评估 SPF/DMARC 配置。

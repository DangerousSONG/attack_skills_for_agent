---
name: richsploit-richdesk
description: Richsploit: 富客户端漏洞利用。信号:pwn,二进制利用,列表。
---

# Richsploit

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/redtimmy/Richsploit
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/redtimmy/Richsploit && cd Richsploit
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 richsploit.py -f exploit -t 10.0.0.5` | RichClient 漏洞利用 |
| `-l` | 列表 |
| `-c cmd` | 命令 |

## 攻击场景 Playbook

### 富客户端漏洞利用

```bash
python3 richsploit.py -t target -f rce
# CVE-2020-0932 等
```

## 注意事项

红队富客户端利用框架。

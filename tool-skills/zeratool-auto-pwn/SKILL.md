---
name: zeratool-auto-pwn
description: 渗透工具 skill:Zeratool 的安装、参数速查与攻击场景 playbook。当任务涉及 二进制漏洞利用与Pwn 需要调用 Zeratool 时使用。
---

# Zeratool

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/ChrisTheCoolHut/Zeratool
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ChrisTheCoolHut/Zeratool && cd Zeratool && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 zeratool.py bin chall` | CTF 二进制自动 pwn |
| `-l 1` | 泄漏模式 |
| `-u` | 覆盖 |

## 攻击场景 Playbook

### CTF 自动 exploit

```bash
python3 zeratool.py /pwn/chall
# 自动找溢出+ROP+shell
```

## 注意事项

CTF 二进制自动利用框架,angr 驱动。

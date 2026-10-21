---
name: dirb-dir-scan
description: 渗透工具 skill:dirb 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 dirb 时使用。
when-to-use: 渗透工具 skill:dirb 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 dirb 时使用。
---

# dirb

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://gitlab.com/kalilinux/packages/dirb
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install dirb
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dirb https://target.com` | 标准扫描 |
| `/usr/share/wordlists/dirb/big.txt` | 大字典 |
| `-X .php,.bak` | 扩展名 |
| `-r` | 不递归 |
| `-a UA` | UA 伪装 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 目录枚举经典款

```bash
dirb https://target.com /usr/share/wordlists/dirb/common.txt -X .php,.html,.bak
```

## 注意事项

Kali 预装目录扫描鼻祖;速度一般但稳定,脚本管道友好。

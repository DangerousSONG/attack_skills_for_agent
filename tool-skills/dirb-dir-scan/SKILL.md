---
name: dirb-dir-scan
description: dirb: 目录枚举经典款。信号:web扫描,漏洞扫描,标准扫描,大字典,扩展名。
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
| `big.txt`（未随库分发） | 大字典 |
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

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`big.txt`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。

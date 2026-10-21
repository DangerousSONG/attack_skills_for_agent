---
name: injectus-crlf-openredirect
description: 渗透工具 skill:Injectus 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(CRLF/重定向) 需要调用 Injectus 时使用。
when-to-use: 渗透工具 skill:Injectus 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(CRLF/重定向) 需要调用 Injectus 时使用。
---

# Injectus

- 攻击大类:C09 Web利用(CRLF/重定向)
- 上游仓库:https://github.com/BountyStrike/Injectus
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/BountyStrike/Injectus && cd Injectus && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 injectus.py -u 'https://t.com/?redir=x'` | 扫描 CRLF+开放重定向 |
| `-f urls.txt` | 批量 |
| `--crlf-only` | 仅 CRLF |
| `--redirect-only` | 仅开放重定向 |

## 攻击场景 Playbook

### 开放重定向+CRLF 组合探测

```bash
python3 injectus.py -u 'https://t.com/go?to=https://evil.com'
# 命中 redir 参数 → 钓鱼/令牌窃取链
```

## 注意事项

CRLF 注入与开放重定向批量扫描,适合赏金猎人 workflow。

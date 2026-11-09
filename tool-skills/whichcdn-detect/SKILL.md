---
name: whichcdn-detect
description: "whichCDN: CDN identification for bypass strategy selection. Signals: web vulnerabilities, injection, batch."
zh-signals: "whichCDN: CDN 识别选绕过策略。信号:web漏洞,注入,批量。"
---

# whichCDN

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/Nitr4x/whichCDN
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Nitr4x/whichCDN && cd whichCDN && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python whichCDN.py https://t.com` | CDN 识别 |
| `-i hosts.txt` | 批量 |

## 攻击场景 Playbook

### CDN 识别选绕过策略

```bash
python whichCDN.py https://t.com
# Cloudflare/Akamai/Incapsula 针对性绕过
```

## 注意事项

CDN 识别工具,18+ 服务商指纹。

---
name: socialfish-phish
description: "SocialFish: multi-platform phishing sites. Signals: phishing, social engineering, phishing platform, template."
zh-signals: "SocialFish: 多平台钓鱼站点。信号:钓鱼,社会工程,钓鱼平台,模板。"
---

# SocialFish

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/UndeadSec/SocialFish
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/UndeadSec/SocialFish && cd SocialFish && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 SocialFish.py -u admin -p pass` | 钓鱼平台 |
| `-u u -p p -t` | 模板 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 多平台钓鱼站点

```bash
python3 SocialFish.py
# 60+ 站点模板
```

## 注意事项

UndeadSec 出品,多平台钓鱼框架。

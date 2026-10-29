---
name: secretfinder-js-secrets
description: "SecretFinder: harvests hardcoded secrets from frontend JS. Signals: API attack, interface testing, JS secret extraction, bulk, simultaneous crawling."
zh-signals: "SecretFinder: 前端 JS 硬编码密钥收割。信号:api攻击,接口测试,JS 中秘密提取,批量,同时爬站。"
---

# SecretFinder

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/mazen160/secrets-patterns-db
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/mazen160/secrets-patterns-db 或 SecretFinder 主仓
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python SecretFinder.py -i https://t.com/app.js -o results.txt` | JS 中秘密提取 |
| `-i urls.txt` | 批量 |
| `-e` | 同时爬站 |

## 攻击场景 Playbook

### 前端 JS 硬编码密钥收割

```bash
python SecretFinder.py -i https://target/static/app.js -o keys.txt
# 正则匹配 40+ 模式: AWS key/Slack token/JWT/私钥
```

## 注意事项

前端秘密提取事实工具;与 linkfinder(端点发现)组成 JS 分析双件套。

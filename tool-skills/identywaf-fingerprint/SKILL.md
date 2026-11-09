---
name: identywaf-fingerprint
description: "identYwaf identifies web protections before testing. Signals: web vulnerability, injection, identify WAF brand or model, request file input, random UA."
zh-signals: "identYwaf: 渗透前识别防护。信号:web漏洞,注入,识别 WAF 品牌/型号,从请求文件识别,随机 UA。"
---

# identYwaf

- 攻击大类:C09 Web利用(WAF绕过)
- 上游仓库:https://github.com/stamparm/identYwaf
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/stamparm/identYwaf
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python identYwaf.py -u 'https://t.com'` | 识别 WAF 品牌/型号 |
| `-r req.txt` | 从请求文件识别 |
| `--random-agent` | 随机 UA |
| `--health-check` | 连通性检查 |

## 攻击场景 Playbook

### 渗透前识别防护

```bash
python identYwaf.py -u 'https://t.com'
# 输出如 'Cloudflare (Cloudflare Inc.)' 决定后续绕过策略
```

## 注意事项

Miroslav Stampar(sqlmap 作者)出品,WAF 指纹库大且活跃,识别 80+ 种 WAF。

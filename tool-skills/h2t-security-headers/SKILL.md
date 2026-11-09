---
name: h2t-security-headers
description: "h2t audits HTTP security header configuration. Signals: web vulnerabilities, injection, HTTP security header scanning, insecure configuration detection, remediation recommendations."
zh-signals: "h2t: 安全头配置审计。信号:web漏洞,注入,扫描 HTTP 安全头,检测不安全配置,输出修复建议。"
---

# h2t

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/gildasio/h2t
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/gildasio/h2t && cd h2t
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./h2t.sh -S https://t.com` | 扫描 HTTP 安全头 |
| `-S url -b` | 检测不安全配置 |
| `-H` | 输出修复建议 |

## 攻击场景 Playbook

### 安全头配置审计

```bash
./h2t.sh -S https://t.com
# CSP/HSTS/X-Frame-Options 缺失检测,辅助点击劫持评估
```

## 注意事项

HTTP 安全响应头审计,辅助评估浏览器端攻击面。

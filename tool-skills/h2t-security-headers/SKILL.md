---
name: h2t-security-headers
description: 渗透工具 skill:h2t 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 h2t 时使用。
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

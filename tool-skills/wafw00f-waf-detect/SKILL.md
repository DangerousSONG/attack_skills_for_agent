---
name: wafw00f-waf-detect
description: 渗透工具 skill:WAFW00F 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 WAFW00F 时使用。
when-to-use: 渗透工具 skill:WAFW00F 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 WAFW00F 时使用。
---

# WAFW00F

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/EnableSecurity/wafw00f
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install wafw00f
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `wafw00f target.com` | 识别 WAF |
| `-l` | 列出可识别产品 |
| `-a` | 全量检测模式 |
| `-v` | 详细输出 |
| `--proxy` | 代理 |

## 攻击场景 Playbook

### 打前先探 WAF

```bash
wafw00f api.target.com
# 输出如 'cloudflare'/'aliyun' → 决定后续绕过策略与限速
```

## 注意事项

先探明 WAF 再定打法;识别结果直接指导 whatwaf/手动绕过方案选择。

---
name: hsecscan-header-audit
description: 渗透工具 skill:hsecscan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 hsecscan 时使用。
---

# hsecscan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/riramar/hsecscan
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/riramar/hsecscan && cd hsecscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python hsecscan.py -u https://t.com` | 安全头扫描 |
| `-u url -d` | 详细 |
| `-u url -p` | 被动模式 |

## 攻击场景 Playbook

### OWASP 安全头审计

```bash
python hsecscan.py -u https://t.com
# 全 header 检测
```

## 注意事项

OWASP 安全头项目实现。

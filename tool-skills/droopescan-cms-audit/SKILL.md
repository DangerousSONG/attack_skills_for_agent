---
name: droopescan-cms-audit
description: 渗透工具 skill:droopescan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 droopescan 时使用。
---

# droopescan

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/droope/droopescan
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install droopescan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `droopescan scan drupal -u https://t.com` | Drupal 扫描 |
| `droopescan scan silverstripe -u url` | SilverStripe 扫描 |
| `droopescan scan wordpress -u url` | WordPress 扫描 |
| `-t 8` | 线程 |
| `-e p` | 仅插件枚举 |

## 攻击场景 Playbook

### CMS 漏洞面审计

```bash
droopescan scan drupal -u https://t.com -t 20
# 版本/主题/插件识别→比对 CVE,插件漏洞常一打一中
```

## 注意事项

插件架构扫描 Drupal/SilverStripe/WordPress,速度优于 WPScan 的场景。

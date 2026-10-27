---
name: wpscan-wp-audit
description: WPScan: WordPress 插件漏洞检测。信号:web扫描,漏洞扫描,基础 WP 扫描,激进插件检测,登录爆破。
---

# WPScan

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/wpscanteam/wpscan
- 上游 License:CC BY-NC 4.0(非商业)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install wpscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `wpscan --url https://t.com` | 基础 WP 扫描 |
| `--enumerate vp,vt,tt,cb,dbe,u` | 枚举插件/主题/用户/备份 |
| `--plugins-detection aggressive` | 激进插件检测 |
| `--passwords rockyou.txt --usernames admin` | 登录爆破 |
| `--api-token X` | 漏洞库 API |

## 攻击场景 Playbook

### WordPress 插件漏洞检测

```bash
wpscan --url https://blog.t.com --enumerate vp,vt,u --api-token $WPSCAN_TOKEN
# 出插件 CVE 列表+可爆破用户,接 WP 后台
```

## 注意事项

WordPress 漏洞库最全的工具。注意 License 为 CC BY-NC(非商业),商业使用需获授权。

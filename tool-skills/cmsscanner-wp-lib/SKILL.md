---
name: cmsscanner-wp-lib
description: 渗透工具 skill:CMSScanner 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 CMSScanner 时使用。
when-to-use: 渗透工具 skill:CMSScanner 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 CMSScanner 时使用。
---

# CMSScanner

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/wpscanteam/CMSScanner
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install cms_scanner
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cms_scan -u https://t.com` | 通用 CMS 扫描 |
| `--enumerate p,t,u` | 枚举插件/主题/用户 |
| `-f` | 强制扫描 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### WPScan 引擎二次开发

```bash
cms_scan -u https://t.com -e u
# WPScan 团队的底层库,适合写自定义扫描器
```

## 注意事项

WPScan 底层扫描库,提供统一 API 供二次开发自定义 CMS 扫描器。

---
name: red-hawk-recon
description: RED_HAWK: PHP 一体化信息收集。信号:资产测绘,指纹识别,交互输入目标。
---

# RED_HAWK

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/Tuhinshubhra/RED_HAWK
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Tuhinshubhra/RED_HAWK && cd RED_HAWK
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `php rhawk.php` | 交互输入目标 |
| `选择扫描类型` | 含 CMS/IP/端口/子域 |

## 攻击场景 Playbook

### PHP 一体化信息收集

```bash
php rhawk.php  # 输入域名出 CMS/IP/whois/子域/端口/Nmap 简报
```

## 注意事项

PHP 写的一体式侦察;在只有 PHP 的受限环境也能跑。

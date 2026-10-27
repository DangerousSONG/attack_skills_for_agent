---
name: wpintel-wp-intel
description: WPintel: WP 情报快速收集。信号:web漏洞,注入,WP 情报收集,用户枚举,DB 泄露检查。
---

# WPintel

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/Tuhinshubhra/WPintel
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Tuhinshubhra/WPintel && cd WPintel
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python wpintel.py -u https://t.com` | WP 情报收集 |
| `-u url --enumerate u` | 用户枚举 |
| `-u url --dbcheck` | DB 泄露检查 |

## 攻击场景 Playbook

### WP 情报快速收集

```bash
python wpintel.py -u https://t.com
# 版本/用户/主题/插件/泄露
```

## 注意事项

Chrome 扩展+CLI 双形态,WP 信息收集。

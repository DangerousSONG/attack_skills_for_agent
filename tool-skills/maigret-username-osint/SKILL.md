---
name: maigret-username-osint
description: "Maigret: Full-web username profiling and targeted verification. Signals: email collection, employee information, 6000+ sites username lookup, full mode slow but complete."
zh-signals: "Maigret: 用户名全网画像、定向核验。信号:邮箱收集,员工信息,6000+ 站点查用户名,全量模式(慢但全)。"
---

# Maigret

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/soxoj/maigret
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install maigret
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `maigret username` | 6000+ 站点查用户名 |
| `-a` | 全量模式(慢但全) |
| `-n 20` | 并发站点数 |
| `--pdf` | PDF 报告 |
| `--json simple` | JSON 输出 |
| `-c --site GitHub` | 只查指定站点 |

## 攻击场景 Playbook

### 用户名全网画像

```bash
maigret johndoe2024 --pdf
# 汇总该用户名在社交网络/代码站/论坛的全部公开档案
```

### 定向核验

```bash
maigret suspect -c --site github --site twitter --site telegram
```

## 注意事项

Sherlock 的增强 fork,站点库 6000+;PDF/HTML 报告直接可交付。

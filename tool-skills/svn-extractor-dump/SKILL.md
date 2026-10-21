---
name: svn-extractor-dump
description: 渗透工具 skill:svn-extractor 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 svn-extractor 时使用。
when-to-use: 渗透工具 skill:svn-extractor 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 svn-extractor 时使用。
---

# svn-extractor

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/anantshri/svn-extractor
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/anantshri/svn-extractor && cd svn-extractor
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 svn_extractor.py --url https://t.com/.svn/entries` | SVN 泄露导出 |
| `--url url --output out/` | 输出 |
| `--match '.*.php'` | 过滤 |

## 攻击场景 Playbook

### .svn 泄露源码恢复

```bash
python3 svn_extractor.py --url https://t.com/.svn/entries --output src/
# 同 GitTools 但针对 SVN
```

## 注意事项

SVN 目录泄露利用工具。

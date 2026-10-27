---
name: rapidscan-multi-vuln
description: rapidscan: 多工具结果聚合。信号:web漏洞,注入,一键多工具编排扫描,仅 SSL 模块,排除模块。
---

# rapidscan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/skavngr/rapidscan
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/skavngr/rapidscan && cd rapidscan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 rapidscan.py example.com` | 一键多工具编排扫描 |
| `-s ssl` | 仅 SSL 模块 |
| `-e nikto` | 排除模块 |
| `-o report` | 输出 |

## 攻击场景 Playbook

### 多工具结果聚合

```bash
python3 rapidscan.py t.com
# 编排 nmap/nikto/wafw00f 等 10+ 工具,统一报告
```

## 注意事项

多工具编排扫描器,一次调用跑遍常用工具,自动汇总关键发现。

---
name: datasploit-osint-auto
description: datasploit: 一键 OSINT 综合报告。信号:邮箱收集,员工信息,自动化 OSINT 报告,IP 模式,邮箱模式。
---

# datasploit

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/DataSploit/datasploit
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/DataSploit/datasploit && cd datasploit && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python datasploit.py -i target.com` | 自动化 OSINT 报告 |
| `-i ip` | IP 模式 |
| `-i email` | 邮箱模式 |
| `-o out/` | 输出 |

## 攻击场景 Playbook

### 一键 OSINT 综合报告

```bash
python datasploit.py -i corp.com
# 域名/IP/邮箱/泄露/Github 全维度
```

## 注意事项

自动化 OSINT 框架,输出综合评估报告。

---
name: bbscan-batch-scan
description: "BBScan: batch screens web sensitive paths. Signals: web vulnerability, injection, concurrent processes, custom PoC scripts, collect only, no PoC request"
zh-signals: "BBScan: 批量 Web 敏感路径初筛。信号:web漏洞,注入,并发进程,自定义 PoC 脚本,仅收集,不请求 PoC。"
---

# BBScan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/lijiejie/BBScan
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/lijiejie/BBScan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python BBScan.py -u https://t.com` | 单目标敏感路径+信息泄露扫描 |
| `python BBScan.py -f urls.txt` | 批量 |
| `-p 20` | 并发进程 |
| `--script scripts/` | 自定义 PoC 脚本 |
| `-d` | 仅收集,不请求 PoC |

## 攻击场景 Playbook

### 批量 Web 敏感路径初筛

```bash
python BBScan.py -f subs.txt -p 50
# git/.svn/.env/备份文件/管理后台路径批量探,命中人工深挖
```

## 注意事项

lijiejie 出品轻量批量扫描器,内置 git 泄露/目录穿越/备份文件等敏感路径规则,适合大资产初筛。

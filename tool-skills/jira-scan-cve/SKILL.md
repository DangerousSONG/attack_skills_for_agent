---
name: jira-scan-cve
description: 渗透工具 skill:jira_scan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(CVE利用) 需要调用 jira_scan 时使用。
when-to-use: 渗透工具 skill:jira_scan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(CVE利用) 需要调用 jira_scan 时使用。
---

# jira_scan

- 攻击大类:C09 Web利用(CVE利用)
- 上游仓库:https://github.com/bcoles/jira_scan
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/bcoles/jira_scan && gem install jira_scan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `jira-scan -u 'https://jira.t.com'` | 检测 Jira 未授权/漏洞 CVE-2019-11581 等 |
| `-u url -c` | 检测匿名访问 |
| `-q` | 静默 |

## 攻击场景 Playbook

### Jira 漏洞批量核查

```bash
cat jira_hosts.txt | xargs -I{} jira-scan -u {}
# 命中 CVE-2019-11581(SMTP 注入 RCE)可进一步武器化
```

## 注意事项

Jira/Atlassian 系列 CVE 扫描器,输出受影响版本和可利用端点。

---
name: apachetomcatscanner-tomcat
description: 渗透工具 skill:ApacheTomcatScanner 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 ApacheTomcatScanner 时使用。
when-to-use: 渗透工具 skill:ApacheTomcatScanner 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 ApacheTomcatScanner 时使用。
---

# ApacheTomcatScanner

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/p0dalirius/ApacheTomcatScanner
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install apachetomcatscanner
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `apachetomcatscanner -t 10.0.0.0/24` | Tomcat 扫描 |
| `-t cidr -u admin -p pass` | 弱口令 |
| `-o out.txt` | 输出 |
| `--list-modules` | 模块列表 |

## 攻击场景 Playbook

### Tomcat 全网测绘

```bash
apachetomcatscanner -t 10.0.0.0/24
# 版本/默认路径/弱口令/CVE
```

## 注意事项

p0dalirius 出品,Tomcat 专项扫描。

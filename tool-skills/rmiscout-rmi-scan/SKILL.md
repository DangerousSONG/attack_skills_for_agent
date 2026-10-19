---
name: rmiscout-rmi-scan
description: 渗透工具 skill:rmiscout 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 rmiscout 时使用。
---

# rmiscout

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/BishopFox/rmiscout
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/BishopFox/rmiscout && cd rmiscout && ./gradlew build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `java -jar rmiscout.jar -i 10.0.0.5 -p 1099 wordlist.txt` | RMI 方法爆破 |
| `-f` | fuzz |
| `-e` | 枚举 |

## 攻击场景 Playbook

### Java RMI 不安全方法

```bash
java -jar rmiscout.jar -i 10.0.0.5 -p 1099 /usr/share/wordlists/methods.txt
# 找可滥用方法
```

## 注意事项

BishopFox 出品,RMI 方法枚举攻击。

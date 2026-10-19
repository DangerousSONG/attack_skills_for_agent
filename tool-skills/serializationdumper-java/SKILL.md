---
name: serializationdumper-java
description: 渗透工具 skill:SerializationDumper 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 SerializationDumper 时使用。
---

# SerializationDumper

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/NickstaDB/SerializationDumper
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/NickstaDB/SerializationDumper && cd SerializationDumper && javac *.java
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `java SerializationDumper base64string` | 解析 Java 序列化数据 |
| `-r url` | 从 URL 拉取解析 |
| `-f file` | 从文件解析 |

## 攻击场景 Playbook

### Java 序列化数据分析

```bash
java SerializationDumper rO0ABXNy...
# 反序列化漏洞分析第一步,看清对象结构
```

## 注意事项

Java 序列化字节流解析器,反序列化漏洞研究必备。

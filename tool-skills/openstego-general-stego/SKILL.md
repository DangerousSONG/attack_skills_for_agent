---
name: openstego-general-stego
description: 渗透工具 skill:OpenStego 的安装、参数速查与攻击场景 playbook。当任务涉及 隐写与数据提取 需要调用 OpenStego 时使用。
---

# OpenStego

- 攻击大类:C38 隐写与数据提取
- 上游仓库:https://github.com/syvaidya/openstego
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
下载 release JAR: java -jar openstego.jar
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `java -jar openstego.jar embed -mf secret.txt -cf cover.png -sf out.png` | 嵌入数据 |
| `java -jar openstego.jar extract -sf out.png -xd .` | 提取数据 |
| `java -jar openstego.jar embedmark -cf cover.png -mf watermark.txt -sf signed.png` | 数字水印 |
| `-a lsb` | 算法: LSB/RandomLSB |

## 攻击场景 Playbook

### 通用文件隐写

```bash
java -jar openstego.jar embed -mf creds.txt -cf photo.jpg -sf out.jpg
# 图片带数据过检查;Java 跨平台
```

## 注意事项

Java 跨平台通用隐写工具,支持 LSB 嵌入+数字水印,兼容常见图片格式。

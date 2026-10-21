---
name: simplify-android-deobf
description: 渗透工具 skill:simplify 的安装、参数速查与攻击场景 playbook。当任务涉及 移动平台攻击 需要调用 simplify 时使用。
when-to-use: 渗透工具 skill:simplify 的安装、参数速查与攻击场景 playbook。当任务涉及 移动平台攻击 需要调用 simplify 时使用。
---

# simplify

- 攻击大类:C43 移动平台攻击
- 上游仓库:https://github.com/CalebFenton/simplify
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/CalebFenton/simplify && ./gradlew fatjar
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `java -jar simplify/build/libs/simplify.jar app.apk -o simple.apk` | Android 反混淆 |
| `--include-classes com/corp/**` | 仅处理指定类 |
| `--max-execution-time 30` | 单方法超时 |
| `-it` | 输出中间结果 |

## 攻击场景 Playbook

### Android 恶意/加固样本反混淆

```bash
java -jar simplify.jar packed.apk -o clean.apk
# 常量传播/死代码消除后 jadx 看逻辑顺畅很多
```

## 注意事项

Android dex 反混淆与反虚拟机检测工具,适合分析加壳/混淆样本。

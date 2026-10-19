---
name: qark-android
description: 渗透工具 skill:QARK 的安装、参数速查与攻击场景 playbook。当任务涉及 移动端攻击 需要调用 QARK 时使用。
---

# QARK

- 攻击大类:C43 移动端攻击
- 上游仓库:https://github.com/linkedin/qark
- 上游 License:NOASSERTION(需人工)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install qark
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `qark --apk app.apk` | APK 静态扫描 |
| `--report-type json` | JSON 报告 |
| `--exploit-apk` | 生成可执行 PoC |
| `-o outdir` | 输出 |

## 攻击场景 Playbook

### APK 静态漏洞扫描

```bash
qark --apk target.apk --report-type json
# 检测: 导出组件/弱加密/硬编码密钥/WebView 配置/SDK 漏洞
```

## 注意事项

LinkedIn 出品;报告含漏洞详情与修复建议,适合快速评估。

---
name: apkleaks-endpoint-scan
description: APKLeaks: 移动应用 API 面暴露检查。信号:攻击面,云资产,扫 APK 端点/密钥,自定义规则,JSON 输出。
---

# APKLeaks

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/dwisiswant0/apkleaks
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install apkleaks
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `apkleaks -f app.apk` | 扫 APK 端点/密钥 |
| `-p rules.json` | 自定义规则 |
| `-o out.json` | JSON 输出 |
| `--json` | 强制 JSON |

## 攻击场景 Playbook

### 移动应用 API 面暴露检查

```bash
apkleaks -f target-app.apk -o leaks.json
jq -r '.endpoints[]' leaks.json | sort -u  # 未公开 API/测试域名/硬编码 key
```

## 注意事项

反编译 APK 提取 URL/endpoint/key;移动端的'git 泄露'级常送分。

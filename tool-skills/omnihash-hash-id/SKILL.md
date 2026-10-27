---
name: omnihash-hash-id
description: omnihash: 未知哈希类型识别。信号:密码破解,哈希破解,文件哈希,算法全枚举。
---

# omnihash

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/Miserlou/omnihash
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install omnihash
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `oh '5d41402abc4b2a76b9719d911017c592'` | 哈希类型识别 |
| `oh -f file` | 文件哈希 |
| `-a` | 算法全枚举 |

## 攻击场景 Playbook

### 未知哈希类型识别

```bash
oh 'e10adc3949ba59abbe56e057f20f883e'
# 得类型后选 hashcat 模式
```

## 注意事项

哈希类型自动识别工具。

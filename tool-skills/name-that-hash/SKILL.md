---
name: name-that-hash
description: name-that-hash: 未知哈希类型识别。信号:密码破解,哈希破解,识别哈希,批量文件,静默。
---

# name-that-hash

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/HashPals/Name-That-Hash
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install name-that-hash
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `nth -t '5f4dcc3b5aa765d61d8327deb882cf99'` | 识别哈希 |
| `-f hashes.txt` | 批量文件 |
| `--no-banner` | 静默 |
| `-j` | JSON 输出 |

## 攻击场景 Playbook

### 未知哈希类型识别

```bash
nth -f dumped_hashes.txt -j | jq '.[].hashcat'
# 输出 300+ 算法匹配与对应 hashcat -m 编号,直接送破解
```

## 注意事项

识别 300+ 哈希格式并给出 hashcat/John 参数;跟 hashid 互补双跑。

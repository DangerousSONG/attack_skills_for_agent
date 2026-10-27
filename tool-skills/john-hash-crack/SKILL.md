---
name: john-hash-crack
description: John the Ripper: 破解 Windows NTLM 哈希、破解 Linux 系统口令。信号:密码破解,哈希破解,字典破解,显示已破解结果。
---

# John the Ripper

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/openwall/john
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install john            # 基础版;Kali 自带 jumbo
# 或源码编译 jumbo:git clone https://github.com/openwall/john && cd john/src && ./configure && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `john --wordlist=rockyou.txt hash.txt` | 字典破解 |
| `--format=NT hashes.txt` | 指定哈希类型(NT/LM/md5crypt 等) |
| `--show hashes.txt` | 显示已破解结果 |
| `--rules` | 启用规则变形(大小写/加数字后缀等) |
| `--incremental` | 全字符集暴力模式 |
| `unshadow /etc/passwd /etc/shadow > unix_hashes.txt` | Linux 口令哈希提取 |
| `--fork=8` | 8 进程并行 |
| `--session=name --restore=name` | 断点续跑 |

## 攻击场景 Playbook

### 破解 Windows NTLM 哈希

```bash
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt ntlm_hashes.txt
john --format=NT --show ntlm_hashes.txt
```

### 破解 Linux 系统口令

```bash
unshadow /etc/passwd /etc/shadow > unix.txt
john --wordlist=rockyou.txt --rules unix.txt
```

### 字典+规则跑加密文档/数据库导出

```bash
john --wordlist=custom.txt --rules --fork=$(nproc) backup_hash.txt
```

## 注意事项

与 hashcat 互补:John 规则引擎和模糊格式识别更强,GPU 破解选 hashcat;NTLM 等格式在 jumbo 版里叫 `NT`;跑大任务务必 `--session` 断点续跑。

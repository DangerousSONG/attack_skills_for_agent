---
name: rsactftool
description: 渗透工具 skill:RsaCtfTool 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 RsaCtfTool 时使用。
when-to-use: 渗透工具 skill:RsaCtfTool 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 RsaCtfTool 时使用。
---

# RsaCtfTool

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/Ganapati/RsaCtfTool
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Ganapati/RsaCtfTool && cd RsaCtfTool && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `--publickey key.pub --private` | 公钥反推私钥(多攻击链自动尝试) |
| `-n N -e E --uncipher C` | 已知 n/e/密文解密 |
| `--attack hastad,factordb,wiener` | 指定攻击 |
| `--dumpkey` | 导出中间结果 |
| `--iscong` | 检测参数是否一致 |

## 攻击场景 Playbook

### CTF/弱 RSA 私钥恢复

```bash
python3 RsaCtfTool.py --publickey ./key.pub --private --dumpkey
# 自动跑 factordb/wiener/hastad/smallq 等 20+ 攻击
```

### 已知密文解密

```bash
python3 RsaCtfTool.py -n 12345... -e 65537 --uncipher 0xabcd...
```

## 注意事项

集成 factordb 在线查询;生产环境强密钥(n≥3072)无效,仅限弱 key/CTF。

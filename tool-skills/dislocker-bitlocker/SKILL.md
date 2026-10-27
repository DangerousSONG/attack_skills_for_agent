---
name: dislocker-bitlocker
description: dislocker: 离线 BitLocker 解密。信号:密码破解,哈希破解,恢复密码解密卷,用户密码解密,BEK 密钥文件解密。
---

# dislocker

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/Aorimn/dislocker
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install dislocker 或 cmake 编译
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dislocker -V /dev/sda3 -p123456-789012-... -- /mnt/bitlocker` | 恢复密码解密卷 |
| `dislocker -V /dev/sda3 -u -- /mnt/bitlocker` | 用户密码解密 |
| `dislocker -V /dev/sda3 -k bekfile -- /mnt/bitlocker` | BEK 密钥文件解密 |
| `-f /mnt/img/dislocker-file` | 输出解密后镜像文件 |

## 攻击场景 Playbook

### 离线 BitLocker 解密

```bash
dislocker -V /dev/sdb1 -p048401-529119-389719 -- /mnt/bl && ls /mnt/bl
# 取证场景: 拿到密码或 bek 文件后挂载明文 NTFS
```

## 注意事项

Linux 下解密 BitLocker 卷,支持恢复密码/用户密码/BEK/清晰密钥四种解锁方式。

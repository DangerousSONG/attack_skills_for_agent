---
name: dislocker-bitlocker
description: "dislocker: offline BitLocker decryption. Signals: password cracking, hash cracking, recovery password volume decryption, user password decryption, BEK key file decryption."
zh-signals: "dislocker: 离线 BitLocker 解密。信号:密码破解,哈希破解,恢复密码解密卷,用户密码解密,BEK 密钥文件解密。"
when-to-use: >-
  Use when performing offline forensics on a BitLocker-encrypted volume and you have a recovery
  password, user password, BEK file, or clear key to mount it.
---

# dislocker

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/Aorimn/dislocker
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install dislocker or build with cmake
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dislocker -V /dev/sda3 -p123456-789012-... -- /mnt/bitlocker` | Decrypt the volume with a recovery password |
| `dislocker -V /dev/sda3 -u -- /mnt/bitlocker` | Decrypt with a user password |
| `dislocker -V /dev/sda3 -k bekfile -- /mnt/bitlocker` | Decrypt with a BEK key file |
| `-f /mnt/img/dislocker-file` | Output the decrypted image file |

## Attack Scenario Playbook

### Offline BitLocker Decryption

```bash
dislocker -V /dev/sdb1 -p048401-529119-389719 -- /mnt/bl && ls /mnt/bl
# Forensics scenario: mount the plaintext NTFS once you have the password or BEK file
```

## Notes

Decrypts BitLocker volumes on Linux, supporting four unlocking methods: recovery password, user password, BEK and clear key.

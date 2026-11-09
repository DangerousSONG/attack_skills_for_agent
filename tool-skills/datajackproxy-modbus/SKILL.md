---
name: datajackproxy-modbus
description: "DatajackProxy: Tamper with PLC communications. Signals: man-in-the-middle, MITM, industrial control protocol MITM, debugging."
zh-signals: "DatajackProxy: PLC 通信篡改。信号:中间人,mitm,工控协议中间人,调试。"
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

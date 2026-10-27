---
name: cloakify-exfil
description: cloakify: 敏感数据外传演练(DLP 规避)。信号:隐写,steganography,还原,加噪音混淆统计特征。
---

# cloakify

- 攻击大类:C38 隐写与隐藏通道
- 上游仓库:https://github.com/TryCatchHCF/Cloakify
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/TryCatchHCF/Cloakify && cd Cloakify
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python cloakify.py secret.txt ciphers/dna` | 把文件编码成 DNA 序列外观 |
| `decloakify.py out.txt ciphers/dna` | 还原 |
| `noiseTools/` | 加噪音混淆统计特征 |

## 攻击场景 Playbook

### 敏感数据外传演练(DLP 规避)

```bash
python cloakify.py passwd.zip ciphers/ipAddresses > notes.txt
# notes.txt 外观是一堆 IP 地址,经允许渠道传出后 decloakify 还原
```

## 注意事项

无加密,仅外观混淆;真敏感数据先加密再 cloakify。

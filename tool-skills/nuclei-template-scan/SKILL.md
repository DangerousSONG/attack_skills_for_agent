---
name: nuclei-template-scan
description: nuclei: 全量 CVE 与暴露面扫描、定向验证某组件漏洞。信号:web扫描,漏洞扫描,单目标,批量目标。
---

# nuclei

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/projectdiscovery/nuclei
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -update-templates   # 同步社区模板库
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-u URL` | 单目标 |
| `-l urls.txt` | 批量目标 |
| `-t path/to/template.yaml` | 指定自定义模板 |
| `-tags cve,exposure` | 按标签筛选模板 |
| `-severity critical,high` | 按严重程度筛选 |
| `-rl 150` | 每秒请求限速,防封 |
| `-o result.txt` | 输出到文件 |
| `-nc` | 禁彩色输出,便于日志 |

## 攻击场景 Playbook

### 全量 CVE 与暴露面扫描

```bash
nuclei -l targets.txt -severity critical,high,medium -rl 100 -o nuclei_result.txt
```

### 定向验证某组件漏洞

```bash
nuclei -u https://target.com -tags "apache,spring" -severity critical,high
nuclei -u https://target.com -t ~/nuclei-templates/cves/2024/CVE-2024-xxxx.yaml
```

### 扫描结果联动利用

```bash
cat nuclei_result.txt | grep -oE 'https?://[^ ]+' | sort -u > exposed.txt
```

## 注意事项

误报率低于同类工具,输出可直接喂给利用工具;生产环境务必限速 `-rl`;自定义模板放 `~/nuclei-templates/`。

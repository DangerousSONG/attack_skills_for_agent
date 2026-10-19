---
name: mat-metadata-clean
description: 渗透工具 skill:MAT (Metadata Anonymisation Toolkit) 的安装、参数速查与攻击场景 playbook。当任务涉及 反取证与痕迹清理 需要调用 MAT (Metadata Anonymisation Toolkit) 时使用。
---

# MAT (Metadata Anonymisation Toolkit)

- 攻击大类:C20 反取证与痕迹清理
- 上游仓库:https://0xacab.org/jvoisin/mat2 或 https://gitweb.torproject.org/mat.git
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install mat2 (新版) 或 apt install mat
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `mat2 sensitive.pdf` | 清除单文件全部元数据(作者/时间/GPS) |
| `mat2 --inplace *.jpg` | 批量原地清理 |
| `-l` | 列出元数据不清除 |
| `--check` | 验证 |

## 攻击场景 Playbook

### 外传文件元数据清洗

```bash
mat2 report_draft.docx  # 输出 report_draft.cleaned.docx,Exif/XMP 全清
```

## 注意事项

mat2 是活跃继任;清 PDF/JPG/Office 元数据防溯源;对截图同样有效。

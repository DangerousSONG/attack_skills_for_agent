# 建议合并的重叠 Skill 团（v0.1 · 待人工裁决）

判定标准：同主题、同攻击面、方法论高度重叠（均为"方法论导论"而非不同技术细分）。
排除原则：不同技术面的不并（SQL/Nosql/模板/API 注入、AD 分析/渗透/评估 等保留并行）。

## M01（2 个 · C09 Web应用漏洞利用）

- `performing-web-cache-deception-attack` — mukul975/Anthropic-Cybersecurity-Skills · Apache-2.0 · Executes web cache deception attacks by exploiting path normalization
- `performing-web-cache-poisoning-attack` — mukul975/Anthropic-Cybersecurity-Skills · Apache-2.0 · Exploiting web cache mechanisms to serve malicious content to other users

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M02（2 个 · C46 二进制漏洞利用与Pwn / C50 红队方法论与自动化）

- `offensive-windows-boundaries` — tmenov/Claude-Red-pentest-set · MIT · 
- `offensive-windows-mitigations` — tmenov/Claude-Red-pentest-set · MIT · 

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M03（2 个 · C05 外部攻击面与云资产暴露）

- `offensive-linux-privesc` — tmenov/Claude-Red-pentest-set · MIT · Comprehensive Linux privilege escalation methodology for offensive security engagements. Covers the 
- `offensive-windows-privesc` — tmenov/Claude-Red-pentest-set · MIT · Comprehensive Windows privilege escalation methodology for offensive security engagements. Covers th

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M04（2 个 · C09 Web应用漏洞利用）

- `offensive-waf-bypass` — tmenov/Claude-Red-pentest-set · MIT · 
- `wafninja-waf-bypass` — 改写 · Apache-2.0 (上游 GPL-3.0) · [WAFNinja] payload 库+WAF 指纹识别,被拦时快速定位 WAF 类型并尝试变形绕过。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M05（2 个 · C10 API与业务逻辑攻击 / C50 红队方法论与自动化）

- `file-access-vuln` — yaklang/hack-skills · MIT · Category router for file access testing
- `business-logic-vuln` — yaklang/hack-skills · MIT · Category router for business logic testing

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M06（2 个 · C09 Web应用漏洞利用 / C49 密码学攻击）

- `padbuster-padding-oracle` — 改写 · Apache-2.0 (上游 Apache-2.0) · [PadBuster] 经典 CBC padding oracle 工具;块大小 8/16 自适应,支持自动错误指纹学习。
- `padre-padding-oracle` — 改写 · Apache-2.0 (上游 MIT) · [padre] Rust 编写的高速 padding oracle 攻击工具,自动识别错误信号,字节级恢复 CBC 明文。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M07（2 个 · C10 API与业务逻辑攻击）

- `jwt-tool-token` — 改写 · Apache-2.0 (上游 GPL-3.0) · [jwt_tool] JWT 安全测试事实标准;支持 30+ 攻击模式含 2023 新出的混淆与注入面。
- `jwt-hack-token` — 改写 · Apache-2.0 (上游 MIT) · [jwt-hack] jwt_tool 的轻量 Go 替代;单二进制适合目标机投递。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M08（2 个 · C41 Web漏洞扫描与验证）

- `dirb-dir-scan` — 改写 · Apache-2.0 (上游 GPL-2.0) · [dirb] Kali 预装目录扫描鼻祖;速度一般但稳定,脚本管道友好。
- `dirstalk-dir-scan` — 改写 · Apache-2.0 (上游 MIT) · [dirstalk] Go 目录扫描,支持分布式扫描。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M09（2 个 · C29 内网发现与枚举）

- `adidnsdump-ldap-enum` — 改写 · Apache-2.0 (上游 MIT) · [adidnsdump] dirkjanm 出品。AD 集成 DNS 往往是域内主机最全清单,含未登记资产,信息收集价值极高。
- `ad-ldap-enum-ldap` — 改写 · Apache-2.0 (上游 MIT) · [ad-ldap-enum] CroweCyber 出品,简单直接的 LDAP 枚举。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M10（2 个 · C06 漏洞情报与漏洞库 / C09 Web应用漏洞利用）

- `yasuo-vuln-scan` — 改写 · Apache-2.0 (上游 GPL-3.0) · [yasuo] Web 应用指纹识别+漏洞扫描,适合大 IP 段批量。
- `vulmap-vuln-scan` — 改写 · Apache-2.0 (上游 GPL-3.0) · [Vulmap] Vulmon 出品本地漏洞扫描器。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

---

合计 10 团，若全部采纳减少 10 个 skill（1000 → 979）。

---

# 裁决结果（2026-10-21 · v1.9 已执行）

**并（13 个已移除）**：M01 留 collecting-open-source-intelligence ｜ M02 留 request-smuggling ｜ M03 留 ACS deception+poisoning（投毒独立保留），移除 web-cache-deception ｜ M04 留 boundaries+windows-mitigations，移除 offensive-mitigations（5.8 万字为子集）｜ M05 留 network-protocol-attacks ｜ M07 留 osint-methodology（35k>23k）｜ M08 留 open-redirect ｜ M09 留方法论+WAFNinja，移除 WAFPass ｜ M14 留 fierce ｜ M15 留 webpwn3r（xsspy 为 Python2 EOL）｜ M17 留 rustbuster ｜ M18 留 postenum ｜ M20 留 manspider

**不并（7 个，假阳性或工具互补）**：M06（Linux/Windows 提权不同平台）、M10（文件访问≠业务逻辑）、M16（DNS zone≠LDAP 枚举）、M19（远程 Web 扫描≠本地漏洞扫描）、M11/M12/M13（经典标准工具与现代替代互补，Agent 按场景二选一）

净减 13：1002 → **989**。二级路由同步上线：大类 >40 个 skill 按子标签细分（C09 已分 16 个子类）。

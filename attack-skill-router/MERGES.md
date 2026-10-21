# 建议合并的重叠 Skill 团（v0.1 · 待人工裁决）

判定标准：同主题、同攻击面、方法论高度重叠（均为"方法论导论"而非不同技术细分）。
排除原则：不同技术面的不并（SQL/Nosql/模板/API 注入、AD 分析/渗透/评估 等保留并行）。

## M01（2 个 · C01 资产测绘与指纹识别 / C35 C2框架与远控）

- `collecting-open-source-intelligence` — mukul975/Anthropic-Cybersecurity-Skills · Apache-2.0 · 'Collects and synthesizes open-source intelligence (OSINT) about threat
- `performing-open-source-intelligence-gathering` — mukul975/Anthropic-Cybersecurity-Skills · Apache-2.0 · Open Source Intelligence (OSINT) gathering is the first active phase

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M02（2 个 · C09 Web应用漏洞利用）

- `exploiting-http-request-smuggling` — mukul975/Anthropic-Cybersecurity-Skills · Apache-2.0 · >-
- `request-smuggling` — yaklang/hack-skills · MIT · CL.TE/TE.CL/TE.TE with 8 obfuscation variants, HTTP/2 downgrade, client-side desync

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M03（3 个 · C09 Web应用漏洞利用）

- `performing-web-cache-deception-attack` — mukul975/Anthropic-Cybersecurity-Skills · Apache-2.0 · Executes web cache deception attacks by exploiting path normalization
- `performing-web-cache-poisoning-attack` — mukul975/Anthropic-Cybersecurity-Skills · Apache-2.0 · Exploiting web cache mechanisms to serve malicious content to other users
- `web-cache-deception` — yaklang/hack-skills · MIT · Path confusion, cache key manipulation

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 2 个。

## M04（3 个 · C46 二进制漏洞利用与Pwn / C50 红队方法论与自动化）

- `offensive-mitigations` — tmenov/Claude-Red-pentest-set · MIT · 
- `offensive-windows-boundaries` — tmenov/Claude-Red-pentest-set · MIT · 
- `offensive-windows-mitigations` — tmenov/Claude-Red-pentest-set · MIT · 

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 2 个。

## M05（2 个 · C40 嗅探与中间人攻击）

- `offensive-network-attacks` — tmenov/Claude-Red-pentest-set · MIT · Dense description covering ARP spoofing, LLMNR/NBT-NS/mDNS poisoning, DNS poisoning, MITM attacks, V
- `network-protocol-attacks` — yaklang/hack-skills · MIT · ARP spoofing, DNS poisoning, LLMNR/NBT-NS poisoning, DHCP starvation, IPv6 attacks, protocol-level M

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M06（2 个 · C05 外部攻击面与云资产暴露）

- `offensive-linux-privesc` — tmenov/Claude-Red-pentest-set · MIT · Comprehensive Linux privilege escalation methodology for offensive security engagements. Covers the 
- `offensive-windows-privesc` — tmenov/Claude-Red-pentest-set · MIT · Comprehensive Windows privilege escalation methodology for offensive security engagements. Covers th

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M07（2 个 · C50 红队方法论与自动化）

- `offensive-osint-methodology` — tmenov/Claude-Red-pentest-set · MIT · 
- `osint-methodology` — elementalsouls/Claude-OSINT · MIT(代码)/CC BY 4.0(内容) · 战略+程序化外部侦察方法论：资产图纪律、严重度评分、时间预算、身份结构映射、交付模板

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M08（2 个 · C09 Web应用漏洞利用 / C47 逆向工程）

- `offensive-open-redirect` — tmenov/Claude-Red-pentest-set · MIT · 
- `open-redirect` — yaklang/hack-skills · MIT · Redirect chain abuse, tabnabbing (reverse tabnabbing)

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M09（3 个 · C09 Web应用漏洞利用）

- `offensive-waf-bypass` — tmenov/Claude-Red-pentest-set · MIT · 
- `wafninja-waf-bypass` — 改写 · Apache-2.0 (上游 GPL-3.0) · [WAFNinja] payload 库+WAF 指纹识别,被拦时快速定位 WAF 类型并尝试变形绕过。
- `wafpass-bypass` — 改写 · Apache-2.0 (上游 MIT) · [WAFPass] WAF 绕过测试工具,多技术混淆组合。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 2 个。

## M10（2 个 · C10 API与业务逻辑攻击 / C50 红队方法论与自动化）

- `file-access-vuln` — yaklang/hack-skills · MIT · Category router for file access testing
- `business-logic-vuln` — yaklang/hack-skills · MIT · Category router for business logic testing

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M11（2 个 · C09 Web应用漏洞利用 / C49 密码学攻击）

- `padbuster-padding-oracle` — 改写 · Apache-2.0 (上游 Apache-2.0) · [PadBuster] 经典 CBC padding oracle 工具;块大小 8/16 自适应,支持自动错误指纹学习。
- `padre-padding-oracle` — 改写 · Apache-2.0 (上游 MIT) · [padre] Rust 编写的高速 padding oracle 攻击工具,自动识别错误信号,字节级恢复 CBC 明文。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M12（2 个 · C10 API与业务逻辑攻击）

- `jwt-tool-token` — 改写 · Apache-2.0 (上游 GPL-3.0) · [jwt_tool] JWT 安全测试事实标准;支持 30+ 攻击模式含 2023 新出的混淆与注入面。
- `jwt-hack-token` — 改写 · Apache-2.0 (上游 MIT) · [jwt-hack] jwt_tool 的轻量 Go 替代;单二进制适合目标机投递。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M13（2 个 · C41 Web漏洞扫描与验证）

- `dirb-dir-scan` — 改写 · Apache-2.0 (上游 GPL-2.0) · [dirb] Kali 预装目录扫描鼻祖;速度一般但稳定,脚本管道友好。
- `dirstalk-dir-scan` — 改写 · Apache-2.0 (上游 MIT) · [dirstalk] Go 目录扫描,支持分布式扫描。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M14（2 个 · C01 资产测绘与指纹识别 / C02 域名与DNS侦察）

- `fierce-dns-recon` — 改写 · Apache-2.0 (上游 GPL-3.0) · [Fierce] Perl 时代经典;'域→网段'的推导逻辑至今仍被复用。
- `bluto-dns-recon` — 改写 · Apache-2.0 (上游 GPL-3.0) · [Bluto] DNS 信息收集+子域爆破+邮箱生成。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M15（2 个 · C09 Web应用漏洞利用）

- `xsspy-xss-scan` — 改写 · Apache-2.0 (上游 MIT) · [XssPy] Python2 时代老工具,胜在简单粗暴整站爬;精细验证建议再上 Dalfox(现有)。
- `webpwn3r-xss-scan` — 改写 · Apache-2.0 (上游 GPL-2.0) · [webpwn3r] 参数量级 Web 漏洞扫描。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M16（2 个 · C29 内网发现与枚举）

- `adidnsdump-ldap-enum` — 改写 · Apache-2.0 (上游 MIT) · [adidnsdump] dirkjanm 出品。AD 集成 DNS 往往是域内主机最全清单,含未登记资产,信息收集价值极高。
- `ad-ldap-enum-ldap` — 改写 · Apache-2.0 (上游 MIT) · [ad-ldap-enum] CroweCyber 出品,简单直接的 LDAP 枚举。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M17（2 个 · C09 Web应用漏洞利用 / C41 Web漏洞扫描与验证）

- `rustbuster-content-discover` — 改写 · Apache-2.0 (上游 GPL-3.0) · [rustbuster] Rust 编写,单文件多模式内容发现,速度极快,适合大规模资产。
- `cansina-content-discover` — 改写 · Apache-2.0 (上游 GPL-3.0) · [cansina] 目录扫描器,特色是扫描持久化+多扩展名自动组合。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M18（2 个 · C16 Linux本地提权 / C50 红队方法论与自动化）

- `postenum-linux-audit` — 改写 · Apache-2.0 (上游 MIT) · [postenum] Linux 提权枚举脚本,输出按 MITRE ATT&CK 分类,比 LinPEAS 更轻量。
- `climber-linux-audit` — 改写 · Apache-2.0 (上游 GPL-3.0) · [climber] Linux 提权枚举脚本。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M19（2 个 · C06 漏洞情报与漏洞库 / C09 Web应用漏洞利用）

- `yasuo-vuln-scan` — 改写 · Apache-2.0 (上游 GPL-3.0) · [yasuo] Web 应用指纹识别+漏洞扫描,适合大 IP 段批量。
- `vulmap-vuln-scan` — 改写 · Apache-2.0 (上游 GPL-3.0) · [Vulmap] Vulmon 出品本地漏洞扫描器。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

## M20（2 个 · C29 内网发现与枚举）

- `manspider-smb-spider` — 改写 · Apache-2.0 (上游 AGPL-3.0) · [MANSPIDER] SMB 共享批量爬取+内容匹配,域内凭据发现神器。
- `smbspider-smb-spider` — 改写 · Apache-2.0 (上游 GPL-2.0) · [smbspider] SMB 共享文件内容搜索。

建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 1 个。

---

合计 20 团，若全部采纳减少 23 个 skill（1000 → 978）。

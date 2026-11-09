# HTTP/3 试点总结（25 个 RFC 审计规则 Skill · v1.0）

> 2026-11-09 ｜ 分支 `rfc-audit-skills` ｜ 配套登记：多维表格「RFC审计规则清单（主表 · 随批次追加）」25 条
>
> 一句话结论：**"约束条款 + 历史 CVE 模式"的定点审计方法论已完成 25 个 Skill 的试点落地，全部六字段达标、全部带真实证据锚点，可以进入第 2 步（多实现差分验证）验证收益。**

## 1. 交付总览

| 项 | 数值 |
|---|---|
| 试点目标 | 25 个（P0 · HTTP/3 + QUIC + QPACK） |
| 实际交付 | **25 个（5 批 × 5 个，100%）** |
| 协议覆盖 | RFC 9000（传输）/ 9001（TLS）/ 9114（H3）/ 9204（QPACK）/ 9218（优先级）/ 9297（Capsule）/ 9368/9369（版本协商） |
| 六字段完整率 | 25/25（约束条款 / 违规判定 / 攻击面猜想 / 关联 CVE / 差分验证 / 对接攻击 Skill） |
| 证据锚点 | 25/25（无空锚点） |

## 2. 四子组结构（Router C51 两级路由）

| 子组 | 数量 | 成员 |
|---|---|---|
| H3 消息层 | 7 | content-length-data-mismatch · pseudo-header-field-validation · settings-frame-order · goaway-drain-enforcement · server-push-frame-rejection · trailers-frame-sequence · **grease-reserved-frames** |
| H3 压缩层 | 2 | qpack-decoded-size-limit · qpack-dynamic-table-capacity |
| H3 扩展层 | 2 | capsule-content-length · priority-update-validation |
| QUIC 传输层 | 14 | handshake-done-timing · flow-control-accounting · connection-id-retirement · path-validation-amplification · stateless-reset-token · version-negotiation-validation · ack-range-validation · transport-parameter-validation · retry-integrity-tag · new-token-replay · **migration-congestion-window · close-draining-state · stream-reset-cancel · 0rtt-replay-protection** |

（**加粗**为第 5 批新增；路由按子组收敛后选 1-3 个加载，预算红线单次 ≤3 个审计 Skill。）

## 3. CVE / 证据锚点统计

| 锚点类型 | 条数 | 说明 |
|---|---|---|
| 挂真实 CVE 编号 | 16 | 含同族/同路径模式引用，如 CVE-2025-64702 家族、CVE-2023-44487（H2 Rapid Reset → H3 迁移审计）、CVE-2026-35191（OpenSSL QUIC）、CVE-2024-45396（Quicly draining） |
| issue / changelog / 论文实证 | 7 | quiche#2678（0-RTT 重放已确认）、quic-go#5686、quiche#2700、HAProxy#3329、aioquic<1.6 流尾丢失、ANRW 2025（11/16 实现 OACK 脆弱）、TMA 2025（20% IPv4 违反放大限制） |
| 声明盲区条款 | 2 | settings-frame-order、grease-reserved-frames（H2 保留帧边界）——标记为定向审计信号而非缺陷 |

**方法论价值佐证**：25 条锚点中没有任何一条需要新造漏洞模式——全部来自"RFC MUST 条款 × 已披露 CVE/bug"的交叉，验证了分享会方法论（高质量漏洞模式 = 历史同类漏洞 + RFC 强制约束）的可复制性。

## 4. 攻击面分布（按 ATT&CK）

- **T1498 Network DoS × 17**：压缩放大、内存耗尽、反射放大、重放兑现、Rapid Reset——QUIC 传输层是 DoS 原语富矿
- **T1190 Exploit Public-Facing Application × 8**：请求走私族（CL/DATA、trailer、伪头、Capsule、GREASE 边界）、0-RTT 重放

## 5. 第 2 步：差分验证计划（下一步）

依据建设节奏第 2 步（2 周）：对 ≥2 个开源实现跑差分审计，产出 ≥1 个疑似漏洞或违规点。

**目标实现（任选其二，对照基线另选 1 个已修复版本）**：

| 目标 | 选型理由 |
|---|---|
| quic-go 最新版 | 试点主要对照系，AK/MI/ZR 探测易落地 |
| aioquic <1.6 vs ≥1.6 | GREASE 流尾丢失（GR-5）已知回归，天然 A/B 对照 |
| nginx ngx_http_v3_module | 关闭族（CD-1~CD-5）历史 CVE 密集，复测价值高 |

**优先探测清单（按命中概率排序）**：

1. `rfc9000-ack-range-validation` AK-3（乐观确认）——ANRW 2025 显示 11/16 实现脆弱，命中概率最高
2. `rfc9001-0rtt-replay-protection` ZR-1（同实例重放）——quiche#2678 同款判定法可直接复用
3. `rfc9000-migration-congestion-window` MI-1（迁移放大比）——TMA 2025 实测 20% IPv4 违规，公网复测成本低
4. `rfc9114-grease-reserved-frames` GR-2（H2 保留帧处理）——盲区条款，但一旦命中即走私级

**验收口径**：任一探测产出"可复现的违规点 + 帧级证据"即达标；证据按 Skill 第 5 字段差分格式沉淀回流，标记规则为有效实证或误报。

## 6. 已知边界

- 0-RTT 跨实例重放属 RFC 承认的"不完美防护"残余，不计违规
- 流重置 Skill（RS-1）判定须以"服务端总工作量随取消率线性增长"为准，避免把"允许取消"误报为漏洞
- 迁移审计遇 LB 终结 CID 的场景，审计对象需转为 LB 层并在报告中标注

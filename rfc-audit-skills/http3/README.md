# HTTP/3 + QUIC 试点批次（第 1 批 · 5 个）

按 `../SKILL_TEMPLATE.md` 六字段编写。批次选择逻辑：每个 Skill 对应一个**已被真实 CVE 证实值得查的约束模式**，优先选"有约束、有 CVE、且仍存在未修补实现"的条款——盲区条款（无 CVE）在第一批之后按同模板扩。

| # | Skill | 约束出处 | 攻击面 | 关联 CVE |
|---|---|---|---|---|
| 1 | rfc9114-content-length-data-mismatch | RFC 9114 §4.1.2（CL 必须等于 DATA 帧长之和；中介 MUST NOT 转发 malformed） | H3→H1 跨协议请求走私 | CVE-2026-33555（HAProxy 裸 FIN 绕过） |
| 2 | rfc9114-qpack-decoded-size-limit | RFC 9114 §4.1.1 + RFC 9204（限长须作用于解码后字段区块） | QPACK 压缩放大内存耗尽（≤4000 倍） | CVE-2025-64702 / CVE-2026-40898（quic-go）、CVE-2026-12523（quiche）、CVE-2025-13945（Wireshark）；Bun/h3/aioquic 未修 |
| 3 | rfc9114-pseudo-header-field-validation | RFC 9114 §4.1.2/§4.2/§4.3/§10.3（malformed 判定完备性） | 解析分裂 → H3→H1 走私原语库 | nginx#1043（未修复）；H2 历史模式复刻 |
| 4 | rfc9000-flow-control-accounting | RFC 9000 §4 / §2.1（流控记账与 varint 边界） | 内存耗尽 / 整数回绕 / 可用性破坏 | CVE-2024-22189、CVE-2023-49295（关联模式）；FC-2/FC-4 为无 CVE 盲区 |
| 5 | rfc9000-connection-id-retirement | RFC 9000 §5.1（CID 生命周期义务对称） | 状态堆积内存耗尽 | CVE-2024-22189（7.5 HIGH） |

## 批次自检

- ✅ 五条均含真实 CVE 锚点，无虚构编号
- ✅ 判定条件全部可程序化（探测编号 + 观测指标）
- ✅ 每条标注了对照实现（差分基线）与误报排除规则
- ✅ 均未包含攻击代码，只含判定规则与导航（攻击动作交给技能层 + 工具层）
- ✅ 已接通：5 个 Skill 的「对接的攻击 Skill」已映射库内真实 slug（`smuggler-desync` / `http2smugl-desync` / `fuzzowski-network-fuzz` / `slowhttptest-dos` / `grammarinator-gen-fuzz`）；Router 层新增 **C51 协议审计与RFC合规测试** 类目（两级路由：先审计层命中约束 → 后攻击层执行验证）

## 下一步（第 2 批候选）

GOAWAY / H3_GOAWAY 处理（RFC 9114 §5.2）、SETTINGS 帧顺序与重复约束（§7.2.1）、H3_DATagram/RFC 9297 capsule 与 Content-Length 互斥（分享会未公开案例的同族）、QPACK 动态表容量协商（RFC 9204 §3.2）、路径验证 / NAT 重绑定（RFC 9000 §8 / §9，CVE-2023-49295 同族）。

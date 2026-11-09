# HTTP/3 + QUIC 试点批次（第 1-4 批 · 共 20 个）

按 `../SKILL_TEMPLATE.md` 六字段编写。批次选择逻辑：每个 Skill 对应一个**已被真实 CVE 证实值得查的约束模式**，优先选"有约束、有 CVE、且仍存在未修补实现"的条款——盲区条款（无 CVE）在候选穷尽后按同模板扩。

## 第 1 批（5 个）

| # | Skill | 约束出处 | 攻击面 | 关联 CVE |
|---|---|---|---|---|
| 1 | rfc9114-content-length-data-mismatch | RFC 9114 §4.1.2（CL 必须等于 DATA 帧长之和；中介 MUST NOT 转发 malformed） | H3→H1 跨协议请求走私 | CVE-2026-33555（HAProxy 裸 FIN 绕过） |
| 2 | rfc9114-qpack-decoded-size-limit | RFC 9114 §4.1.1 + RFC 9204（限长须作用于解码后字段区块） | QPACK 压缩放大内存耗尽（≤4000 倍） | CVE-2025-64702 / CVE-2026-40898（quic-go）、CVE-2026-12523（quiche）、CVE-2025-13945（Wireshark）；Bun/h3/aioquic 未修 |
| 3 | rfc9114-pseudo-header-field-validation | RFC 9114 §4.1.2/§4.2/§4.3/§10.3（malformed 判定完备性） | 解析分裂 → H3→H1 走私原语库 | nginx#1043（未修复）；H2 历史模式复刻 |
| 4 | rfc9000-flow-control-accounting | RFC 9000 §4 / §2.1（流控记账与 varint 边界） | 内存耗尽 / 整数回绕 / 可用性破坏 | CVE-2024-22189、CVE-2023-49295（关联模式）；FC-2/FC-4 为无 CVE 盲区 |
| 5 | rfc9000-connection-id-retirement | RFC 9000 §5.1（CID 生命周期义务对称） | 状态堆积内存耗尽 | CVE-2024-22189（7.5 HIGH） |

## 第 2 批（5 个）

| # | Skill | 约束出处 | 攻击面 | 关联 CVE |
|---|---|---|---|---|
| 6 | rfc9000-handshake-done-timing | RFC 9000 §19.20（HANDSHAKE_DONE 双向义务）+ RFC 9001 §4.9.2（密钥丢弃顺序） | 恶意服务端握手期断言崩溃客户端 | CVE-2025-59530（quic-go，野外已观测，7.5 HIGH） |
| 7 | rfc9114-settings-frame-order | RFC 9114 §7.2.1（SETTINGS 必须为首帧且唯一） | 能力协商劫持 / 解析前置条件绕过 | 暂无公开 CVE（盲区条款，定向审计信号） |
| 8 | rfc9297-capsule-content-length | RFC 9297 §2/§3.2/§3.3/§3.5（capsule 与 CL 互斥、解析自洽、未知类型静默丢弃） | HTTP 走私同族（前后端解析分裂）/ 内存耗尽 | 分享会未公开走私案例（同族）；CVE-2025-64702（同族模式） |
| 9 | rfc9204-qpack-dynamic-table-capacity | RFC 9204 §3.2（容量协商、尺寸更新顺序、不得超容量插入） | 幽灵引用头部伪造 / 内存耗尽 | CVE-2025-64702 家族（quic-go） |
| 10 | rfc9000-path-validation-amplification | RFC 9000 §8.1（3 倍反放大）/ §8.2.1（PATH_CHALLENGE/RESPONSE 义务）/ §9（NAT 重绑定） | UDP 反射放大 / 挑战状态表内存耗尽 | CVE-2023-49295（quic-go，HIGH） |

## 第 3 批（5 个）

| # | Skill | 约束出处 | 攻击面 | 关联 CVE / 实证 |
|---|---|---|---|---|
| 11 | rfc9114-goaway-drain-enforcement | RFC 9114 §5.2/§7.2.6（GOAWAY 标识符单调性、收帧拒新、无 GOAWAY 关闭默认） | 请求重复执行/丢失 / 优雅关闭劫持 | 暂无独立 CVE；quiche#2700、quic-go#5326、erlang_quic 1.0.0 changelog 实证 |
| 12 | rfc9218-priority-update-validation | RFC 9218 §7.2（PRIORITY_UPDATE 帧位置/类型/范围/存在性校验） | 调度优先级污染 / Structured Fields 解析崩溃 | 暂无公开 CVE（盲区条款）；erlang_quic "Strict PRIORITY_UPDATE parsing" 修复实证 |
| 13 | rfc9114-server-push-frame-rejection | RFC 9114 §7.2.5/§7.2.7/§7.2.8（PUSH_PROMISE/MAX_PUSH_ID/H2 遗留帧必须炸连接） | 已废弃语义暗道 / 兜底分支义务缺失 | 暂无独立 CVE；**quic-go#5686 实证**（v0.60.0 静默吞掉 0x5/0xd 而 0x2/0x6/0x8/0x9 正确处理——同函数内不一致） |
| 14 | rfc9368-version-negotiation-validation | RFC 8999 §6 + RFC 9368 §4（VN 包不变量、Version Information 全套校验、降级防护） | 版本降级 / 无认证解析崩溃 | 暂无 VN 独立 CVE；QUIC-FUZZ 实证 xquic VN 事件日志 NULL 解引用崩溃、Quicly CVE-2024-45396 同类模式 |
| 15 | rfc9000-stateless-reset-token | RFC 9000 §10.3/§21.11（令牌保密性、域分离、碰撞禁止、Oracle 防护） | 定向连接掐断 / 无认证崩溃 | CVE-2026-50009（Netty < 4.2.15.Final，令牌可推导，on-path DoS）；xquic/Quicly fuzz 实证 |

## 第 4 批（5 个）

| # | Skill | 约束出处 | 攻击面 | 关联 CVE / 实证 |
|---|---|---|---|---|
| 16 | rfc9000-ack-range-validation | RFC 9000 §13.1/§21.4 + RFC 9002 §6（ACK 范围校验、乐观确认跳号检测） | 拥塞控制欺骗 → 出站放大 DDoS | CVE-2025-4820 / CVE-2025-4821（quiche < 0.24.4）；ANRW 2025：16 个 Interop 实现中 11 个对 OACK 脆弱 |
| 17 | rfc9000-transport-parameter-validation | RFC 9000 §18.2/§7.3（CID 参数缺失/错配、服务端专用参数、非法值） | 握手期 CID 注入 / 无认证崩溃 | 暂无独立 CVE（盲区条款）；CVE-2025-54939（lsquic QUIC-LEAK）同路径实证 |
| 18 | rfc9001-retry-integrity-tag | RFC 9000 §8.1.4/§17.2.5 + RFC 9001 §5.8（完整性标签、单 Retry 约束、防重放 MUST） | 握手前 DoS 暗道 / 地址验证旁路 | 暂无独立 CVE；warpsock changelog 补齐 loop guards 实证 §17.2.5.1/§17.2.5.2 为真实 pitfall |
| 19 | rfc9000-new-token-replay | RFC 9000 §19.7/§8.1.4（令牌单用、IP 绑定 MUST、防重放 MUST） | 地址验证体系旁路 → 反射放大 | 暂无独立 CVE（格式自定 + MUST 分散的高 variance 盲区）；CVE-2023-49295 同族资源不对称模式 |
| 20 | rfc9114-trailers-frame-sequence | RFC 9114 §4.1/§4.2 + RFC 9110 §8.6（三区块帧序列、trailer 伪头禁止、CL 一致性） | H3→H1 消息边界走私 | 暂无独立 CVE；nginx#1043 同生态；H2 trailer/CL 历史走私模式复刻 |

## 批次自检

- ✅ 二十条均含真实 CVE 锚点或明确的"无 CVE 盲区 + 实证"声明，无虚构编号
- ✅ 判定条件全部可程序化（探测编号 + 观测指标）
- ✅ 每条标注了对照实现（差分基线）与误报排除规则
- ✅ 均未包含攻击代码，只含判定规则与导航（攻击动作交给技能层 + 工具层）
- ✅ 已接通：20 个 Skill 的「对接的攻击 Skill」均已映射库内真实 slug（`smuggler-desync` / `http2smugl-desync` / `fuzzowski-network-fuzz` / `slowhttptest-dos` / `grammarinator-gen-fuzz` / `tlsfuzzer-fuzz` / `h2csmuggler-http2` / `dharma-grammar-fuzz`）；Router 层 **C51 协议审计与RFC合规测试** 类目（两级路由：先审计层命中约束 → 后攻击层执行验证）

## 下一步（第 5 批候选）

连接迁移拥塞窗口重置检测（RFC 9000 §9.4，迁移后 cwnd 处理差异）、QUIC 关闭与 draining 期语义（§10.2/§10.3，重复 CONNECTION_CLOSE / 关闭期帧处理）、RESET_STREAM 与 STOP_SENDING 交互义务（§3.4/§3.5）、0-RTT 重放与拒绝策略（§5.7 / RFC 9001 §2.3）、H3 保留帧与 GREASE 处理（§7.2.8）。

---
name: rfc9001-retry-integrity-tag
description: 审计 QUIC 实现对 Retry 包完整性与令牌生命周期的处理是否按 RFC 9000 §8.1.4/§17.2.5 与 RFC 9001 §5.8——完整性标签未验证、令牌可重放、多 Retry 循环未防护即握手前无认证攻击面
rfc: RFC 9000 §8.1.4（令牌完整性）/ §17.2.5（Retry 包）/ RFC 9001 §5.8（Retry Integrity Tag）
license: Apache-2.0
---

# RFC 9001 §5.8 Retry 完整性与令牌生命周期审计

## 1. 约束条款（原文出处）

RFC 9001 §5.8：Retry 包携带 128 位完整性标签，用**公开固定的** AES-128-GCM 密钥与 nonce 计算（v1 常量公开、v2 常量 RFC 9369 §3.3.3 另行规定）——客户端在接受 Retry 前**必须**验证该标签（标签不提供服务器身份认证，仅防篡改/防伪造）。

RFC 9000 §8.1.4（原文要点）：
> 地址验证令牌 MUST 难以猜测、MUST 有完整性保护防客户端伪造；Retry 令牌 SHOULD 短期有效且只能立即回显；**servers MUST ensure that replay of tokens is prevented or limited**。
> 若服务端收到含无效 Retry 令牌的 Initial，SHOULD 立即以 INVALID_TOKEN 关闭连接。

RFC 9000 §17.2.5：客户端**不得**对同一连接尝试接受多个 Retry（攻击者可用无限 Retry 做放大/延迟）；客户端在已收到服务端 Initial 后到达的 Retry 必须丢弃。

核心模式一句话：**Retry 是把"证明你收到了我的挑战"变成一条无状态可验令牌的设计——但完整性标签密钥是公开的、令牌是客户端可回放的，所有安全重量压在"验证标签 + 限次 + 限时"三个开关上，少一个开关就是一条握手前 DoS 暗道。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| RT-1 | 篡改 Retry 包的 DCID/令牌后重算任意 16 字节尾巴（或翻转标签任意位）发送给客户端 | 客户端接受 Retry → 未验证完整性标签 → 违规 |
| RT-2 | 对同一连接尝试连续注入两个 Retry（第二次携带第一个的令牌） | 客户端接受第二个 / 进入循环 → 违反 §17.2.5 单 Retry 约束 |
| RT-3 | 在客户端已收到服务端 Initial/Handshake 后注入延迟 Retry | 客户端接受 → 违反迟达丢弃约束 |
| RT-4 | 同一令牌跨连接重放（用 A 连接获得的令牌发起 B 连接）并观察服务端 | 接受且跳过地址验证 → 违反 MUST 防重放；配合源地址伪造即成放大器 |
| RT-5 | 构造过期/地址不符的令牌回显（如能注入令牌内容观测其结构） | 接受 → 令牌未绑定源地址/时间戳 |

判定方法：aioquic 作为恶意客户端/中间人注入 Retry；令牌重放需同 IP 双连接测试；时序控制用原始 UDP 注入。

## 3. 攻击面猜想

- **握手前放大/延迟 DoS**：RT-2/RT-3 ——无限 Retry 循环迫使客户端反复重算 Initial 密钥（每次 Retry 换 DCID 需重新派生），CPU 放大
- **地址验证旁路 → 反射放大**：RT-4 ——令牌重放 + 源地址伪造让服务端把未验证地址当已验证，解除 3 倍反放大限制
- **降级配合**：伪造 Retry 与版本协商/迁移交互，可作为 QUIC-LEAK 类握手前内存消耗的触发器

## 4. 关联历史 CVE / 实证

| 证据 | 实现 | 根因 |
|---|---|---|
| warpsock changelog 修复记录 | warpsock | 显式补齐 "RFC 9000 §17.2.5.1/§17.2.5.2 loop guards（one accepted Retry per attempt, late Retry discard once an Initial or Handshake is opened）" 并配专属回归测试——说明多 Retry 与迟达 Retry 是真实实现 pitfall |
| CVE-2025-54939（旁证路径） | lsquic | 握手前路径（Initial/Retry 处理）无认证且历史上内存管理出错——本 Skill RT-1~RT-5 全部落在该路径 |
| 暂无 Retry 独立 CVE | — | RFC 9001 §5.8 标签密钥公开是设计使然（只防篡改不防伪造），实现普遍验标签但限次/限时/防重放三开关覆盖参差——盲区条款 |

## 5. 差分验证方法

对照组：quic-go ≥ 0.60、msquic、warpsock（含 loop guards 的版本）。
对比字段：RT-1 标签验证、RT-2 单 Retry 强制、RT-3 迟达丢弃、RT-4 跨连接重放拒绝。
误报排除：实现选择"不接受任何 Retry"（disable_retry）属合规；只标记"验标签但无限次""接受迟达""重放被接受"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（Retry/Initial 交互序列 fuzz）、`slowhttptest-dos`（握手前资源消耗节奏）
- 工具层（用什么打）：aioquic（Retry 注入）、原始 UDP 时序脚本
- 命中后动作：RT-4 成立 → 评估反射放大比（跳过地址验证后的发送上限）；RT-2 成立 → 量化单连接 CPU 放大系数

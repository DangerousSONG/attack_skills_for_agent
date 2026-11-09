---
name: rfc9368-version-negotiation-validation
description: 审计 QUIC 实现对版本协商与降级防护是否按 RFC 8999 §6 与 RFC 9368 §4——Version Negotiation 包不变量、Version Information 校验全套 MUST 缺失即版本降级与解析崩溃攻击面（实证：QUIC-FUZZ xquic VN 事件崩溃；CVE-2024-45396 Quicly 同类模式）
rfc: RFC 8999 §6（Version Negotiation 包不变量）/ RFC 9368 §4（Version Downgrade Prevention）/ RFC 9369 §3（v2 义务）
license: Apache-2.0
---

# RFC 9368 §4 版本协商与降级防护审计

## 1. 约束条款（原文出处）

RFC 8999 §6（原文要点）：
> Packets with a short header do not trigger version negotiation.（短头不触发 VN）
> An endpoint MUST ignore a packet that contains no Supported Version fields or contains a truncated Supported Version value.（空/截断版本列表必须忽略）
> An endpoint MUST include the value from the Source Connection ID field of the packet it receives in the Destination Connection ID field.（CID 回显义务）
> Version Negotiation packets do not use integrity or confidentiality protection.（VN 包无加密保护——降级防护全靠端点校验）

RFC 9368 §4（原文要点）：
> Clients MUST ignore any received Version Negotiation packets that contain the Original Version.（含原始版本的 VN 包必须忽略）
> Both endpoints MUST parse their peer's Version Information during the handshake... [解析失败] the endpoint MUST close the connection; if the connection was using QUIC version 1, that connection closure MUST use a transport error of type TRANSPORT_PARAMETER_ERROR.（Version Information 解析失败必须关闭连接）
> If an endpoint receives a Chosen Version equal to zero, or any Available Version equal to zero, it MUST treat it as a parsing failure.（零版本号按解析失败处理）
> If a server receives Version Information where the Chosen Version is not included in Available Versions, it MUST treat it as a parsing failure.
> When the server then processes the client's Version Information, the server MUST validate that the client's Chosen Version matches the version in use for the connection. If the two differ, the server MUST close the connection with a version negotiation error.
> Clients MUST NOT complete the handshake if they are reacting to a Version Negotiation packet and the server's Version Information is missing... MUST close the connection with a version negotiation error.
> If a client has reacted to a Version Negotiation packet, the client MUST validate the server's Available Versions field... If the client would have selected a different version, the client MUST close the connection with a version negotiation error.
> Clients MUST validate that the server's Chosen Version is equal to the Negotiated Version; if they do not match, the client MUST close the connection with a version negotiation error.

RFC 9369 §3：支持 QUIC v2 的端点 MUST 发送、处理并校验 version_information 传输参数。

核心模式一句话：**VN 包本身明文、无完整性保护——降级防护的全部重量都压在端点侧一串 MUST 校验上；这串校验是典型的"安全护栏"代码，护栏缺失不会立刻坏，只会在被攻击时让连接悄无声息地降级或崩溃。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| VN-1 | 服务端对**短头**包响应 Version Negotiation 包 | 发送 VN → 违反不变量（短头不触发） |
| VN-2 | 向客户端注入含其 Original Version 的 VN 包（中间人/乱序重放） | 客户端按 VN 更换版本重连 → 违反 MUST ignore |
| VN-3 | 构造 Version Information 传输参数畸形值（长度过短 / 非 4 字节整倍数 / Chosen Version 或 Available Version 为 0 / 服务端侧 Chosen 不在 Available 中） | 对端未关闭连接（v1 下未用 TRANSPORT_PARAMETER_ERROR） → 违规 |
| VN-4 | 客户端响应过 VN 后，服务端 Version Information 缺失 / Available Versions 为空 / 按客户端选择算法本会选别的版本 | 客户端完成握手 → 违规 |
| VN-5 | 服务端 Chosen Version 与长头协商版本字段不一致（兼容协商路径） | 客户端未以 version negotiation error 关闭 → 违规 |
| VN-6 | 向服务端发送带**不支持版本号**的 Initial（触发 VN 的合法路径），观察服务端 VN 响应的 CID 回显与版本列表完整性 | CID 不回显 / 空列表 / 截断列表照常处理 → 违规；服务端解析事件处理崩溃（xquic 实证） → 崩溃面 |

判定方法：aioquic 自定义版本号 + 原始 UDP 注入 VN 包；quic-go 调试日志观测版本协商事件。

## 3. 攻击面猜想

- **版本降级**：VN-2/VN-4 ——把连接降级到防护更弱的旧版本或草案版本（草案版本密钥推导、握手校验差异大），是跨版本攻击的入口
- **无认证解析崩溃**：VN-6 ——版本协商事件是握手前无认证路径，QUIC-FUZZ 已实证 xquic 在 VN 事件日志记录中 NULL 指针解引用崩溃
- **传输参数解析污染**：VN-3 ——Version Information 与传输参数共存于同一解析路径，畸形值可成为传输参数解析器的 fuzz 入口

## 4. 关联历史 CVE / 实证

| 证据 | 实现 | 根因 |
|---|---|---|
| QUIC-FUZZ（arXiv:2503.19402）实测漏洞 | xquic | 发送错误版本 Initial 触发 Version Negotiation 事件时，日志函数传入 NULL 网络路径指针 → 服务端崩溃 DoS。版本协商事件处理属无认证攻击面，本 Skill VN-6 的实证基础 |
| QUIC-FUZZ 实测漏洞 | Quicly | 握手前路径断言失败崩溃（CVE-2024-45396）——同类"无认证握手前路径"模式 |
| 暂无 VN 校验独立 CVE | — | RFC 9368 2023 年才标准化，主流实现多为"支持 v1 + 忽略校验"状态，全套 MUST 几乎无人完整实现——典型盲区条款 |

## 5. 差分验证方法

对照组：quic-go ≥ 0.60、msquic、xquic ≥ 修复版。
对比字段：VN-1~VN-6 各自的响应行为；特别对照"收到 VN 后是否真的会重新选择版本"与"Version Information 校验是否完整"。
误报排除：实现仅支持 v1 且对 VN 采取"忽略并继续"策略（等价于 MUST ignore 的最严形态）属合规；只标记"按 VN 换版本但校验缺失"与"解析失败不关闭"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（传输参数/VN 包 fuzz）、`grammarinator-gen-fuzz`（Version Information 语法生成）
- 工具层（用什么打）：aioquic（自定义版本 + 原始 UDP 注入）、自写 VN 包构造脚本
- 命中后动作：确认降级可行 → 评估目标版本（草案/v2）的已知弱点 → 确认崩溃路径 → 最小化无认证崩溃复现序列

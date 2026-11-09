---
name: rfc9113-content-length-data-mismatch
description: 审计 HTTP/2 实现 Content-Length 与 DATA 帧长度和的一致性校验——H2 中 CL 无传输含义但被原样转发/降级到 H1 时恢复语义即请求走私（关联 CVE-2021-21295 Netty <4.1.60 H2→H1 降级走私及 4.1.61 补漏；CVE-2026-58055 nghttpx ≤1.69.0 Upgrade+CL keep-alive 走私；与 H3 侧 rfc9114-content-length-data-mismatch 同族互补）
rfc: RFC 7540 §8.1.2 / RFC 9113 §8.1.1（Content-Length 与消息体一致性）/ RFC 9113 §8.1（消息格式）
license: Apache-2.0
---

# RFC 9113 §8.1.1 Content-Length 与 DATA 一致性审计（H2 侧）

## 1. 约束条款（原文出处）

RFC 9113 §8.1.1（要点，RFC 7540 §8.1.2 同源）：
> 包含 Content-Length 的请求/响应，其值与 DATA 帧载荷长度之和**不相等即 malformed**；
> H2 中 Content-Length 无传输分帧含义，但作为元数据保留；实现不得依赖它确定消息边界；
> 代理将 H2 转换为其他版本时，**必须重新建立或验证**消息边界语义。

核心模式一句话：**H2 的 DATA 帧自带长度，Content-Length 成了"纯注释"——但下游 H1 世界把它当圣旨。代理若在降级时不重校 CL，注释就成了注入 H1 请求体的后门。HTTP/2 没有消灭走私，只是把它赶到了版本边界上。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| CM-1 | H2 请求 CL=5 但实际发 5+N 字节 DATA（或多 DATA 帧总长 ≠ CL） | 未按 malformed 拒绝且降级转发 → 走私面（CVE-2021-21295 同款） |
| CM-2 | CL 与实际一致但代理降级时**重新声明** CL（数值被重算/截断） | 边界重算错误 → 实现侧转换缺陷 |
| CM-3 | 单 HEADERS + END_STREAM 且带 CL>0（无 DATA 帧）的降级路径 | Netty 4.1.60 修复漏网场景（4.1.61 补）：endStream=true 时 CL 未校验 → 降级走私 |
| CM-4 | Upgrade + CL + 请求体经代理转发到 keep-alive H1 后端 | 后端复用连接上边界分裂 → CVE-2026-58055 同款（响应队列投毒） |
| CM-5 | TE 头残留（H2 禁止 transfer-encoding）被降级时转换为 CL 或原样转发 | 未剥离/未拒绝 → H2→H1 转换义务违反 |

判定方法：h2 客户端构造 CL/DATA 不一致请求；观测 H2 端是否拒绝 + 经代理降级后 H1 后端实际读到的边界（对照后端：严格 CL 解析的 httpd）。

## 3. 攻击面猜想

- **H2→H1 降级走私**：CM-1/CM-3 ——前端 H2、后端 H1 的经典架构下注入第二个请求，跨租户响应投毒
- **响应队列投毒**：CM-4 ——keep-alive 后端连接复用，走私请求的响应发给无关客户端
- **缓存投毒/访问控制绕过**：走私请求绕开前端鉴权直接命中后端（走私族通用后果）

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2021-21295** | Netty <4.1.60（GHSA 同族） | H2 的 Content-Length 未在 Http2MultiplexHandler 校验即向上传播；经 Http2StreamFrameToHttpObjectCodec 转 H1 对象后转发 → 降级走私 |
| **Netty 4.1.61 补漏** | Netty | 4.1.60 漏修"单头帧 endStream=true"场景——边界条件覆盖不全是该族复发模式 |
| **CVE-2026-58055** | nghttpx ≤1.69.0 | Upgrade + CL + 请求体转发 keep-alive 后端、重插 hop-by-hop 头，后端解析歧义 → 走私 + 跨客户端响应队列投毒 |

## 5. 差分验证方法

对照组：Netty ≥4.1.61、严格校验的 Envoy 新版本。
对比字段：CM-1/CM-3 拒绝率、CM-2 降级 CL 重算正确性、CM-4 连接复用判定（含 Upgrade 的连接必须不可复用）、CM-5 TE 剥离。
误报排除：端到端 H2（后端也是 H2）时 CL 不一致仍须拒绝（§8.1.1 malformed 判定与下游版本无关），但以"降级走私可利用性"定级——纯 H2 内网标中低危。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`smuggler-desync`（CL 不一致探测与利用）、`http2smugl-desync`（H2 走私变体）、`h2csmuggler-http2`（h2c 升级链组合）
- 工具层（用什么打）：Python h2（CL/DATA 独立构造）、严格 H1 对照后端、代理降级链路
- 命中后动作：CM-1 确认 → 构造跨用户响应投毒 PoC → 与 H3 侧 `rfc9114-content-length-data-mismatch` 证据合并成"CL 一致性跨版本弱点族"

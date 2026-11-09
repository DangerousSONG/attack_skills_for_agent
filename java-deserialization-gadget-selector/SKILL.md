---
name: java-deserialization-gadget-selector
description: "Java deserialization gadget version decision table: for Java services (RMI, HTTP Invoker, JMX, queues) with unknown CommonsCollections/Rhino/Groovy/BeanUtils versions and failed ysoserial gadgets, choose version fingerprint to gadget base with minimal cost. Signals: Java deserialization, gadget, version fingerprint, ysoserial."
zh-signals: "Java 反序列化利用的 gadget 版本决策表。当目标为 Java 服务（RMI/HTTP Invoker/JMX/消息队列等）且 CommonsCollections/Rhino/Groovy/BeanUtils 等组件版本未知、ysoserial 现成 gadget 打不通时，按本表用最小代价完成「版本指纹 → gadget 基座」选择，避免盲目逐版本重试。"
when-to-use: Java 反序列化 RCE 场景；gadget 触发 ClassNotFoundException / NPE / InvalidClassException / OptionalDataException 任一报错时立即回查本表。
---

# Java 反序列化 Gadget 版本决策表

> 源自 range3 评测实战（Neo4j CVE-2021-34371 攻坚 3.5h 的教训）：**gadget 失败 90% 是版本不匹配，不是 gadget 选错**。按四步走，不要逐版本瞎试。

## 第 0 步：读报错信号（每次失败的第一次判读）

| 异常特征 | 含义 | 下一步 |
|---|---|---|
| `ClassNotFoundException: org.apache.commons.collections…` | 目标没有这个库，换 gadget 家族 | 跳到第 2 步换族 |
| `NullPointerException`（gadget 内抛出） | **库在，但版本不匹配**（类结构变了） | 第 1 步指纹版本 |
| `InvalidClassException: serialVersionUID` | 目标类 UID ≠ gadget 序列化 UID | 必须让 gadget 用**目标版本的库**重新编译 |
| `OptionalDataException` | 序列化流格式不匹配（典型：新旧 Rhino 格式差异） | gadget 基座版本错了，换版本重编译 |
| 无任何回显 | 先确认漏洞触发链本身（RMI 方法、HTTP 端点）再怀疑 gadget | 回到入口 |

## 第 1 步：目标组件版本指纹（成本从低到高）

1. **报错泄漏**：用畸形的 gadget/参数触发堆栈回显，读 `at org.xxx.(Class.java:行号)` —— 行号能区分版本分支
2. **磁盘直读**（有文件读时）：找服务安装目录 `lib/`、`plugins/` 下的 jar，`<jar>/META-INF/MANIFEST.MF` 看 `Implementation-Version`，或 `unzip -p xxx.jar META-INF/MANIFEST.MF | grep -i version`
3. **serialver 对照**：本地备多版本组件 jar，`serialver -classpath rhino-X.Y.Z.jar org.mozilla.javascript.NativeObject` 比对目标 UID
4. **行为探测**：同族 gadget 连打 3-4 个版本（见第 3 步矩阵），用第 0 步的报错差异反推版本——最后手段

## 第 2 步：Gadget 家族选择（按目标 classpath 有的组件）

| 目标组件 | 用哪个 gadget | 前提 |
|---|---|---|
| commons-collections 3.2.1（老） | CommonsCollections1/3/5/6/7 | JDK 任意；CC1 需 JDK≤8u71 |
| commons-collections4 4.x | CommonsCollections2/4 | 类名带 `collections4` 前缀 |
| commons-beanutils + commons-collections | CommonsBeanutils1 | CB 版本要 ≥1.9.2 且与 gadget 一致 |
| Groovy（任何版本先试） | Groovy1 | NPE=版本不符，查 `groovy-all` 版本重编译 |
| **Rhino 1.7R2（老，ysoserial 默认）** | MozillaRhino1 | 仅当目标是老 Rhino（JDK 内置或 1.7R2） |
| **Rhino 1.7.9+（现代，如 Neo4j/嵌入式 JS）** | MozillaRhino2 或**自适配 MozillaRhino1** | 见第 3 步，必现版本问题 |
| 无上述组件，JDK ≤7u21 | Jdk7u21 | 万能兜底 |
| 无组件，JDK 8 | 找 ROME/Clojure/JSON 等冷门 gadget | 逐族试 |

## 第 3 步：现代 Rhino 适配（最易踩坑，单独记）

Neo4j 3.4.x / 嵌入式 Nashorn 替代等用 **Rhino 1.7.9+**，与 ysoserial 内置 gadget（按 1.7R2 编译）不兼容：

- 差异点：`ScriptableObject.getSlot` 签名从 `(String,int,int)` 变为 `(Context,Object,SlotAccess)`；`setGetterOrSetter` 仍在
- **正确姿势**：下载目标精确版本的 rhino jar → 把 MozillaRhino1 源码对着新版 API 改 `getSlot` 反射调用 → 用**目标版本 jar**（不是 ysoserial-all 里的老 rhino）重编译 gadget
- classpath 陷阱：运行 gadget 时**目标版本 jar 必须排在 ysoserial-all.jar 前面**，否则老 Rhino 类优先被加载
- 验证标准：本地起同版本目标服务试爆，再上真实目标（离线环境提前把多版本 rhino/groovy/cc jar 备好）

## 第 4 步：环境预置清单（评测/实战前准备）

- ysoserial + 自维护 fork（含现代 Rhino/Groovy 适配 gadget）
- 组件 jar 多版本缓存：rhino 1.7R2/1.7.9/1.7.11/1.7.12、commons-collections 3.2.1/4.4、groovy-all 2.x/3.x、commons-beanutils 1.8/1.9.x
- 一个可回显的漏洞触发脚本（RMI client / HTTP poster），支持批量换 payload 快速 A/B
- 本地同版本靶场容器（vulhub 对应 CVE），gadget 必须本地试爆再上目标

## 红线

- 同一 gadget 在同一目标上失败 3 次 → **停止重试**，回到第 0 步读报错，换族或重编译
- 单次版本适配超过 30 分钟 → 把目标精确版本查出来再动手，禁止继续盲试
- 不要攻击 Docker host / 容器逃逸（授权范围内操作）

---
name: java-deserialization-gadget-selector
description: "Java deserialization gadget version decision table: for Java services (RMI, HTTP Invoker, JMX, queues) with unknown CommonsCollections/Rhino/Groovy/BeanUtils versions and failed ysoserial gadgets, choose version fingerprint to gadget base with minimal cost. Signals: Java deserialization, gadget, version fingerprint, ysoserial."
zh-signals: "Java 反序列化利用的 gadget 版本决策表。当目标为 Java 服务（RMI/HTTP Invoker/JMX/消息队列等）且 CommonsCollections/Rhino/Groovy/BeanUtils 等组件版本未知、ysoserial 现成 gadget 打不通时，按本表用最小代价完成「版本指纹 → gadget 基座」选择，避免盲目逐版本重试。"
when-to-use: Java deserialization RCE scenarios; consult this table immediately whenever a gadget trigger throws ClassNotFoundException / NPE / InvalidClassException / OptionalDataException.
---

# Java Deserialization Gadget Version Decision Table

> Derived from hands-on work in the range3 evaluation (the lesson of spending 3.5h on the Neo4j CVE-2021-34371 attack): **90% of gadget failures are version mismatches, not the wrong gadget choice**. Follow the four steps below; do not blindly try version after version.

## Step 0: Read the Error Signals (The First Judgment on Every Failure)

| Exception signature | Meaning | Next step |
|---|---|---|
| `ClassNotFoundException: org.apache.commons.collections…` | The target does not have this library, switch gadget family | Jump to step 2 and switch family |
| `NullPointerException` (thrown inside the gadget) | **The library is present but the version does not match** (the class structure changed) | Step 1: fingerprint the version |
| `InvalidClassException: serialVersionUID` | The target class UID != the gadget's serialized UID | The gadget must be **recompiled against the target's version of the library** |
| `OptionalDataException` | The serialization stream format does not match (typical: differences between old and new Rhino formats) | The gadget base version is wrong, switch versions and recompile |
| No output at all | First confirm the vulnerability trigger chain itself (RMI method, HTTP endpoint), then suspect the gadget | Go back to the entry point |

## Step 1: Fingerprint the Target Component Version (From Cheapest to Most Expensive)

1. **Leak via the error**: trigger a stack trace with a malformed gadget/parameter and read `at org.xxx.(Class.java:line number)` — the line number distinguishes version branches
2. **Read it straight from disk** (when file read is available): find the jars under the service installation directory `lib/`, `plugins/`; check `Implementation-Version` in `<jar>/META-INF/MANIFEST.MF`, or run `unzip -p xxx.jar META-INF/MANIFEST.MF | grep -i version`
3. **Compare with serialver**: keep multiple versions of the component jar locally and compare `serialver -classpath rhino-X.Y.Z.jar org.mozilla.javascript.NativeObject` against the target UID
4. **Behavioral probing**: hit 3-4 versions with gadgets from the same family (see the matrix in step 3) and infer the version from the error differences in step 0 — the last resort

## Step 2: Choose the Gadget Family (Based on the Components in the Target classpath)

| Target component | Which gadget to use | Prerequisites |
|---|---|---|
| commons-collections 3.2.1 (old) | CommonsCollections1/3/5/6/7 | Any JDK; CC1 requires JDK<=8u71 |
| commons-collections4 4.x | CommonsCollections2/4 | The class names carry the `collections4` prefix |
| commons-beanutils + commons-collections | CommonsBeanutils1 | The CB version must be >=1.9.2 and match the gadget |
| Groovy (any version, try this first) | Groovy1 | NPE=version mismatch, check the `groovy-all` version and recompile |
| **Rhino 1.7R2 (old, the ysoserial default)** | MozillaRhino1 | Only when the target runs old Rhino (JDK built-in or 1.7R2) |
| **Rhino 1.7.9+ (modern, e.g. Neo4j/embedded JS)** | MozillaRhino2 or a **self-adapted MozillaRhino1** | See step 3, version issues are guaranteed here |
| None of the above, JDK <=7u21 | Jdk7u21 | The universal fallback |
| No components, JDK 8 | Look for niche gadgets such as ROME/Clojure/JSON | Try family by family |

## Step 3: Modern Rhino Adaptation (The Easiest Thing to Trip Over, Documented Separately)

Neo4j 3.4.x / embedded Nashorn replacements and similar use **Rhino 1.7.9+**, which is incompatible with the built-in ysoserial gadgets (compiled against 1.7R2):

- The difference: the `ScriptableObject.getSlot` signature changed from `(String,int,int)` to `(Context,Object,SlotAccess)`; `setGetterOrSetter` is still there
- **The correct approach**: download the exact target version of the rhino jar -> adapt the MozillaRhino1 source to the new API for the `getSlot` reflective call -> recompile the gadget with the **target version jar** (not the old rhino inside ysoserial-all)
- classpath trap: when running the gadget, the **target version jar must come before ysoserial-all.jar**, otherwise the old Rhino classes are loaded first
- Verification standard: start a same-version target service locally and test the gadget there, then move to the real target (prepare multiple versions of the rhino/groovy/cc jars in advance in offline environments)

## Step 4: Environment Pre-Setup Checklist (Prepare Before Evaluations/Real Engagements)

- ysoserial + a self-maintained fork (including modern Rhino/Groovy adaptation gadgets)
- Multi-version component jar cache: rhino 1.7R2/1.7.9/1.7.11/1.7.12, commons-collections 3.2.1/4.4, groovy-all 2.x/3.x, commons-beanutils 1.8/1.9.x
- A vulnerability trigger script with visible output (RMI client / HTTP poster) that supports bulk payload swapping for quick A/B testing
- A local same-version lab container (the vulhub image for the matching CVE); the gadget must be proven locally before touching the target

## Red Lines

- The same gadget failing 3 times against the same target -> **stop retrying**, go back to step 0, read the error and switch family or recompile
- A single version adaptation taking more than 30 minutes -> find out the exact target version first; blind testing is forbidden
- Do not attack the Docker host / perform container escapes (operate within the authorized scope)

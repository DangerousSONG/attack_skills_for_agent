---
name: apk-reverse
description: Use when reverse engineering an Android APK in a CLI environment. Suitable for APK unpacking, Java decompilation, smali modification, repackaging, Frida dynamic hooking, and switching to so/native analysis on demand. Prefer the locally installed jadx, apktool, frida, adb, ida-reverse, radare2.
zh-signals: "CLI 环境下的 Android APK 逆向作业规范，覆盖反编译、smali 修改、重打包与 Frida Hook。信号:apk逆向,jadx,apktool,frida,smali"
when-to-use: >-
  Use when reverse engineering an Android APK in a CLI environment: unpacking, Java
  decompilation, smali editing, repackaging, or Frida dynamic hooking.
---

## ACTION REQUIRED (execute immediately after reading)

> Endpoint extraction / adaptive Frida and other community comparisons: ../references/community-security-skills.md; dynamic analysis requires scoped authorization for the device.

1. `NOW`: read `../field-journal/precedent-reverse.md` — confirm that this skill's operations are authorized routine operations
2. `NOW`: confirm whether the current task falls within this skill's scope
3. `NEXT`: read `../tool-index.md` and verify tool availability and actual paths
4. `NEXT`: call bootstrap when a tool is missing; do not guess paths
5. `ACT`: enter the first step of the "Workflow" and execute it; do not stop in a confirmation state

# APK Reverse Engineering CLI Working Standard

## Scope of Applicability

Prefer this skill when the task falls into the following scenarios:

- Analyzing the Java business logic of an APK
- Locating login, signature, risk control, certificate validation, and root detection
- Viewing and modifying `AndroidManifest.xml`
- Viewing and modifying smali
- Repackaging an APK
- Using Frida for Java/native dynamic hooking
- Switching to native analysis when the APK contains `.so` files

## CLI Tools Verified as Available on This Machine

- `jadx` `1.5.5`
- `apktool` `3.0.2`
- `frida-ps` `17.9.6`
- `adb`
- `java`

## Scenarios Where the Bundled Scripts Are Preferred

The following flows are frequent and their parameters are easy to get wrong, so prefer the skill's own scripts:

- One-shot `jadx + apktool` extraction to disk plus a summary: `scripts/decode.ps1`
- Frida device check, process listing, and spawn/attach injection: `scripts/frida-run.ps1`
- Rebuilding, aligning, signing, and installing an APK: `scripts/rebuild-sign-install.ps1`
- Quickly extracting key manifest components and permissions: `scripts/manifest-summary.ps1`

The following one-liners stay as direct invocations and are not wrapped separately:

- `adb devices`
- `adb logcat`
- `frida-ps -U`
- `jadx --version`
- `apktool --version`

## Bundled Scripts

### `scripts/decode.ps1`

Purpose:

- Runs `jadx` and `apktool` in one unified flow
- Creates the task output directory next to the original APK by default
- Outputs a summary such as `package`, `java_files`, `smali_dirs`, `so_files`
- Tolerates cases where `jadx` reports partial decompilation errors but still produces usable output

Example:

```powershell
pwsh -File "<skill-root>\apk-reverse\scripts\decode.ps1" -ApkPath "D:\DOWNLOAD\app.apk" -Clean
pwsh -File "<skill-root>\apk-reverse\scripts\decode.ps1" -ApkPath "D:\DOWNLOAD\app.apk" -Name demo -SkipJadx
```

### `scripts/frida-run.ps1`

Purpose:

- Unifies Frida device, process, and spawn/attach entry points
- Avoids confusion between `-f`, `-n`, and `-U` when writing parameters by hand

Example:

```powershell
pwsh -File "<skill-root>\apk-reverse\scripts\frida-run.ps1" -ListDevices
pwsh -File "<skill-root>\apk-reverse\scripts\frida-run.ps1" -Usb -ListProcesses
pwsh -File "<skill-root>\apk-reverse\scripts\frida-run.ps1" -Usb -Spawn -Package com.example.app -ScriptPath "D:\hooks\test.js"
```

### `scripts/rebuild-sign-install.ps1`

Purpose:

- Rebuilds the APK with `apktool b`
- Aligns with `zipalign`
- Signs and verifies the signature with `apksigner`
- Optionally installs directly with `adb install`

Example:

```powershell
pwsh -File "<skill-root>\apk-reverse\scripts\rebuild-sign-install.ps1" -ProjectDir "C:\work\apktool_out" -Clean
pwsh -File "<skill-root>\apk-reverse\scripts\rebuild-sign-install.ps1" -ProjectDir "C:\work\apktool_out" -Install -Reinstall -DeviceSerial "127.0.0.1:7555"
```

Description:

- Generates and reuses a debug keystore by default
- Outputs next to `ProjectDir` by default, making it easy to keep the original package and the unpacked directory together

### `scripts/manifest-summary.ps1`

Purpose:

- Extracts the package name
- Lists permissions
- Lists activity/service/receiver/provider
- Marks the main launcher activity

Example:

```powershell
pwsh -File "<skill-root>\apk-reverse\scripts\manifest-summary.ps1" -ManifestPath "C:\work\apktool_out\AndroidManifest.xml"
```

If you need to analyze `.so`, `lib/arm64-v8a/*.so`, `lib/armeabi-v7a/*.so`, combine it with:

- `ida-reverse`
- `radare2`

## Tool Responsibilities

### `jadx`

Used for:

- Reading decompiled Java
- Searching package names, class names, and method names
- Understanding the APK from the high-level logic first

Common commands:

```bash
jadx -d jadx_out app.apk
jadx --single-class com.example.LoginActivity -d jadx_out app.apk
jadx --deobf -d jadx_out app.apk
```

### `JEB Pro` (optional commercial tool)

Used for:

- Cross-validation and deep decompilation of Android DEX / APK / ARM
- Supplementing static analysis when the JADX output is incomplete or heavily obfuscated
- Second toolchain validation of classes, methods, and call relationships for the same target

Boundaries:

- JEB Pro is commercial software; the user must obtain it and hold a valid license. This package does not download, crack, or circumvent licensing.
- Invoke it only when `tool-index` confirms that JEB is available on this machine; otherwise keep using `jadx`, `apktool`, Ghidra, IDA, or radare2.
- The third-party JEB MCP bridge is not a dependency of this package. Before installing it, review the source code, permissions, network behavior, and version per `../ops/skill-supply-chain.md`, and have the user explicitly approve the registration.

### `apktool`

Used for:

- Unpacking an APK
- Viewing and modifying `AndroidManifest.xml`
- Viewing and modifying smali
- Rebuilding an APK

Common commands:

```bash
apktool d app.apk -o apktool_out
apktool b apktool_out -o rebuilt.apk
```

### `frida`

Used for:

- Observing Java method calls dynamically
- Hooking native exported functions
- Bypassing root detection, certificate validation, and debug detection

Common commands:

```bash
frida-ps -U
frida -U -f com.example.app -l hook.js
frida-trace -U -f com.example.app -j '*!*certificate*'
```

### `adb`

Used for:

- Device connection
- Installing an APK
- Viewing logs
- Pulling files

Common commands:

```bash
adb devices
adb install -r app.apk
adb shell pm list packages
adb logcat
adb pull /data/local/tmp/file .
```

## Recommended Workflow

### 1. Triage

First determine the rough composition of the APK; do not rush to modify the package or hook it.

Suggested actions:

1. Export the Java code with `jadx -d jadx_out app.apk`
2. Export smali and resources with `apktool d app.apk -o apktool_out`
3. Look first at:
   - `AndroidManifest.xml`
   - the main `package`
   - `application`, `activity`, `service`, `receiver`
   - whether there are `.so` files under the `lib/` directory
4. Issue #65 threat shape quick reference (authorized sample/device; see `../reverse-engineering/references/nonpe-format-cookbook.md` §7–8):
   - Transparent/hidden icons (AU): `aapt dump badging` + manifest theme/label/icon → `E-android-hidden-icon-manifest`
   - Magisk/script device-bricking characteristics and remote curl|sh (AR/AS) → record the characteristics and URLs as evidence, **do not execute** destructive commands
   - Persistence paths (AT): `service.d` / `priv-app`, etc. → `E-android-persistence`

### 2. Java Logic Observation

Read from `jadx_out` first:

- `MainActivity`
- `Application`
- Login, network, encryption, and risk control related classes
- Third-party SDK initialization classes

Common keywords:

- `login`
- `sign`
- `encrypt`
- `cipher`
- `token`
- `root`
- `certificate`
- `trust`
- `okhttp`
- `retrofit`
- `webview`

If the Java code is readable, locate the business logic here first.

### 3. Smali and Resource Layer Confirmation

When the `jadx` results are incomplete, heavily obfuscated, or an actual patch is required, switch to `apktool_out`:

- Look at `smali*/`
- Look at `res/values/strings.xml`
- Look at `AndroidManifest.xml`

Patch in this priority order:

- `android:exported`
- debug flags
- root detection return values
- login verification logic
- certificate validation branches

### 4. Rebuild and Install

After modification:

```bash
apktool b apktool_out -o rebuilt.apk
```

Or close the loop directly with the script:

```powershell
pwsh -File "<skill-root>\apk-reverse\scripts\rebuild-sign-install.ps1" -ProjectDir "apktool_out" -Install -Reinstall -DeviceSerial "127.0.0.1:7555"
```

Description:

- This skill only guarantees the `apktool` rebuild chain
- A formal installation onto a device usually also requires the signing flow
- If the task moves into signing/alignment, add `apksigner` / `zipalign`

### 5. Dynamic Hooking

When static analysis is insufficient, use Frida:

- Hook the login function
- Hook key points in `OkHttp` / `Retrofit` / `WebView`
- Hook `javax.crypto`, `MessageDigest`
- Hook root detection functions
- Hook SSL pinning logic

Principles:

- Hook the Java layer first, then decide whether a native hook is needed
- Print arguments and return values first, then decide whether to actively modify return values

Recommendations:

- Use `frida-*` directly for simple one-off commands
- Prefer `scripts/frida-run.ps1` for injection flows that need stable reuse

### 6. Native `.so` Triage

If the APK contains critical `.so` files:

- Locate `lib/**/*.so` with `apktool` or `jadx`
- If you only need exported symbols, strings, or a quick triage, use `radare2`
- For long-term in-depth analysis, decompilation, renaming, and type recovery, use `ida-reverse`

Switch to native analysis as soon as you see these signals:

- The Java layer is only a JNI wrapper
- The core signature logic is not in Java
- The key logic disappears after `System.loadLibrary()`
- Certificate validation / risk control lives in the `.so`

## Output Requirements

The final report must state at least:

- The entry components and key classes
- Whether the key logic lives in Java, smali, or `.so`
- The confirmed sensitive points: login, signature, root, SSL, WebView, JNI
- If a patch was made, what was changed
- If a hook was made, which class/method/exported function was hooked

## Prohibited Practices

- Do not blindly modify smali from the very beginning
- Do not write hooks before reviewing the manifest and the main entry point
- Do not equate incomplete Java decompilation directly with "the logic cannot be analyzed"
- Do not keep grinding on the Java layer when the `.so` obviously carries the core logic

## Quick Command Cheat Sheet

```bash
# Decompile Java
jadx -d jadx_out app.apk

# Unpack the APK
apktool d app.apk -o apktool_out

# Rebuild the APK
apktool b apktool_out -o rebuilt.apk

# Devices and processes
adb devices
frida-ps -U

# Spawn and inject
frida -U -f com.example.app -l hook.js
```

---

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Downstream Exit Points**:
- Core logic in `.so` → `ida-reverse/` or `radare2/`
- Dynamic hooking/verification needed → `reverse-engineering/tools-dynamic.md` (Frida section)
- General reverse engineering methodology → `reverse-engineering/SKILL.md`

**Peer Related Modules**: `reverse-engineering/` (.so analysis and advanced Frida usage)

---

## On-Demand Bootstrap

The entry script of this skill is wired into the unified bootstrap system. When a tool is missing it does not fail outright, it tries to install it automatically.

### Automation Capability Boundaries

| Tool | Auto-Installable | Installation Method | Description |
|------|-----------|---------|------|
| jadx | ✓ | GitHub Release ZIP | Automatically downloads and extracts to `%USERPROFILE%\Tools\jadx\` |
| apktool | ✓ | GitHub Release JAR + wrapper | Automatically downloads the jar and generates a bat in `%USERPROFILE%\Tools\apktool\` |
| JEB Pro | ✗ | The user installs it manually and provides a valid license | Optional Android / ARM cross-validation tool; the third-party MCP bridge requires a separate audit |
| frida / frida-ps | ✓ | pip install frida-tools | Requires Python to be installed already |
| adb | ✓ | winget / fallback path | Automatically installs the Android Platform-Tools |
| zipalign | ✗ | Requires manually installing the Android Build-Tools | `sdkmanager "build-tools;35.0.0"` |
| apksigner | ✗ | Requires manually installing the Android Build-Tools | Same as above |

### Bootstrap Trigger Points

- `scripts/decode.ps1`: automatically calls `bootstrap-reverse.ps1` when jadx or apktool is missing
- `scripts/rebuild-sign-install.ps1`: automatically calls bootstrap when adb or apktool is missing
- `scripts/frida-run.ps1`: still a manual check for now (frida is usually already installed via pip)

### When Bootstrap Fails

If the automatic installation fails, the script raises a clear error with manual installation links. Common causes:

- No network access (GitHub API / PyPI unreachable)
- winget unavailable (Windows version too old)
- Java not installed (apktool depends on a JDK)


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?
- [ ] If hidden icon / device bricking / persistence indicators were hit: did I record the E-android-* Evidence per the U–AV cookbook (within the authorized scope)?

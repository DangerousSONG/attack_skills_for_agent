---
name: yakit-native-plugin
description: "Yakit plugins are divided into native plugins (saved as YakScript with independent execution page/parameter form) and other plugin types. Signals: yakit, plugin, yakscript."
zh-signals: "Yakit 插件分'原生插件'(保存为 YakScript, 有独立执行页/参数表单)与"
when-to-use: >-
  0. Related Routes Yakit native plugins (yak / mitm types) and the cli parameter system. Explains the difference between native plugins and hot reloads, how cli.* turns into Yakit's execution-page parameter form (String/Int/Bool/Urls/Ports/StringSlice dropdowns/File etc. + setRequired/setDefault/setVerboseName/setCliGroup), and three excellent cases: a yak native plugin taking user input via cli, a mitm native plugin passively scanning complex content and producing risks, and a mitm + cli interactive plugin loading external parameters (keyword dictionary/scope) to drive scanning. Use it when the user asks "how do I write a yak/mitm plugin with a parameter form, how do I use cli, how do I do passive scanning in a mitm plugin".
---

# SKILL: Yakit Native Plugins (yak / mitm) and cli Parameters

> AI LOAD INSTRUCTION: Yakit plugins are split into "native plugins" (saved as YakScript, with an independent execution page/parameter form) and "hot reloads" (inline code inside a MITM/Fuzzer tab). This page focuses on native plugins + the `cli` parameter system: `cli.*` calls are statically scanned by Yakit into a parameter form, and at runtime the values the user fills in are injected back into the script. Three runnable cases are given: a yak native plugin taking input via cli, a mitm native plugin passively scanning complex content, and a mitm + cli interactive plugin loading external parameters. All examples pass the `yak <file>` self-test.

## 0. Related Routes

- Master entry point: yak
- All MITM hooks and their deduplication semantics (hot-reload perspective, but the hook contract matches native mitm plugins): [mitm-hotpatch](../mitm-hotpatch/SKILL.md)
- Right-click codec plugin + cli selection extraction: yakit-rightclick-plugin
- Historical data extraction / wordlists / sending requests: [yakit-data-extract-plugin](../yakit-data-extract-plugin/SKILL.md)
- Database / Payload wordlists / risk: yaklang-database
- Verification toolchain: yaklang-toolchain

## 1. Native Plugin vs Hot Reload (Tell Them Apart First)

| Dimension | Native plugin (this page) | Hot reload (hot patch) |
| --- | --- | --- |
| Form | Saved as YakScript, with a name/type/parameters | An inline code snippet inside a MITM/Fuzzer tab |
| Parameters | Defined with `cli.*`, rendered by Yakit into a form | No independent form, you edit the code directly |
| Entry point | Top-level statements execute directly (yak type); mitm type registers hooks | Register a hook function |
| Best for | "Finished tools" reused by a team | Temporarily altering traffic / quick experiments |
| Topic in this library | This page | [mitm-hotpatch](../mitm-hotpatch/SKILL.md) / [webfuzzer-hotpatch](../webfuzzer-hotpatch/SKILL.md) / [global-hotpatch](../global-hotpatch/SKILL.md) |

> Key point: **a native mitm plugin and a MITM hot reload use the same set of hooks** (`hijackHTTPRequest` / `mirror*` /
> `hijackSaveHTTPFlow` ...), and the contract is documented in [mitm-hotpatch](../mitm-hotpatch/SKILL.md). The only difference
> is that a native plugin can additionally carry a `cli` parameter form and is saved/distributed as a finished artifact.

## 2. cli Parameters -> Yakit Form Controls (Core Reference Table)

All `cli.*` calls must be written at the **top level** (executed at module load time) so that Yakit can statically scan out the parameters. At runtime the engine injects the values the user filled in.

| cli function | Return type | Yakit control | Description |
| --- | --- | --- | --- |
| `cli.String(name)` | string | Single-line text | Most commonly used |
| `cli.Text(name)` | string | Multi-line text box | Large blocks of text |
| `cli.Int(name)` | int | Number | |
| `cli.Float(name)` | float | Number | |
| `cli.Bool(name)` | bool | Switch | True when present |
| `cli.Urls(name)` | []string | URL list | Automatically prepends `http(s)://` |
| `cli.Ports(name)` | []int | Ports | Supports `80,443,8000-8010` |
| `cli.Hosts(name)` | []string | Network targets | Supports CIDR expansion |
| `cli.StringSlice(name)` | []string | Dropdown/multi-select | Use `setSelectOption` for a dropdown |
| `cli.File(name)` | []byte | File | Reads the file content |
| `cli.FileOrContent(name)` | []byte | File or text | Falls back to text when the file cannot be read |
| `cli.LineDict(name)` | []string | File or multi-line text | Split **by line** (not by comma) |
| `cli.YakitPlugin()` | []string | Plugin selection | Reads `yakit-plugin-file` |
| `cli.Json(name)` | map | Complex form | Use `setJsonSchema` |

Option functions (options are passed as subsequent arguments):

| Option | Purpose |
| --- | --- |
| `cli.setRequired(true)` | Required; when missing, `cli.check()` prints the help and exits |
| `cli.setDefault(v)` | Default value |
| `cli.setVerboseName("label")` | The label shown in the form |
| `cli.setHelp("...")` | Help text |
| `cli.setCliGroup("group")` | Parameter grouping |
| `cli.setSelectOption("display name","value")` | Dropdown option (`cli.StringSlice` only) |
| `cli.setMultipleSelect(false)` | Whether multi-select is allowed (`cli.StringSlice` only) |

> You must call **`cli.check()`** at the end: it validates the required items and, if anything is missing, prints Usage and calls `os.Exit(1)`.

```yak
target = cli.String("target", cli.setVerboseName("target"), cli.setRequired(true))
ports  = cli.Ports("ports", cli.setDefault("80,443"))
mode   = cli.StringSlice("mode",
    cli.setSelectOption("fast", "fast"), cli.setSelectOption("deep", "deep"),
    cli.setMultipleSelect(false), cli.setDefault("fast"))
cli.check()
```

## 3. Three Excellent Cases (examples/)

| Case | File | Key points |
| --- | --- | --- |
| A yak native plugin taking input via cli | [examples/yak-cli-input.yak](examples/yak-cli-input.yak) | `cli.Urls/Ports/Int/Bool` + `cli.check()`; the core logic is extracted into pure functions so it can be self-tested |
| A mitm native plugin passively scanning complex content | [examples/mitm-passive-scan.yak](examples/mitm-passive-scan.yak) | `mirrorNewWebsitePathParams` scans phone numbers/ID numbers/JWT/AKSK in response bodies, hits produce `risk.NewRisk` |
| A mitm + cli interactive plugin loading external parameters | [examples/mitm-cli-interactive.yak](examples/mitm-cli-interactive.yak) | `cli.LineDict` reads an external keyword dictionary + `cli.String` limits the scope, the hook closure captures them and drives the scan |

### 3.1 Yak Native Plugin + cli (Excellent Case 1)

The entry point of a yak-type plugin is the **top-level statements** (yak does not automatically call `func main()`). A real plugin reads the cli parameters at the top level and runs the main flow directly:

```yak
func runPlugin() {
    targets = cli.Urls("target", cli.setRequired(true))
    ports = cli.Ports("ports", cli.setDefault("80,443"))
    cli.check()
    // ... use the parameters to scan / send requests
}
runPlugin()   // Real plugin: called directly at the top level
```

Extract the core logic (target normalization, deduplication) into **pure functions** so that repeatable assertions can be made inside the `YAK_MAIN` self-test block, independently of the command line and the network.

### 3.2 Mitm Native Plugin Passive Scanning (Excellent Case 2)

A mitm plugin does not write `main`; instead it **registers hooks**. For passive scanning the preferred hook is `mirrorNewWebsitePathParams` (deduplicated by path + parameter structure, saves compute, read-only and does not affect forwarding):

```yak
mirrorNewWebsitePathParams = func(isHttps, url, req, rsp, body) {
    for f in scanSensitive(string(body)) {      // scanSensitive is a pure function, self-testable
        risk.NewRisk(url, risk.title(...), risk.type("info-leak"),
            risk.severity("low"), risk.payload(f.value))
    }
}
```

- Put the rule table at the top level as a **read-only constant** (do not modify globals in a concurrent hook, that causes a data race).
- A hit produces `risk.NewRisk(...)`, visible in the Yakit "Risks and Vulnerabilities" panel.
- The self-test only exercises the pure `scanSensitive` logic and never calls `risk` (to avoid writing to the database).

### 3.3 Mitm + cli Interactive (Excellent Case 3)

For the same mitm plugin, use cli to turn the "keyword dictionary" and "scope" into parameters, so switching targets does not require changing code:

```yak
KEYWORDS = cli.LineDict("keywords", cli.setDefault("password\ntoken\nsecret"))  // Read at the top level
SCOPE    = cli.String("scope", cli.setDefault(""))
cli.check()

mirrorHTTPFlow = func(isHttps, url, req, rsp, body) {   // The closure captures KEYWORDS/SCOPE
    if !inScope(url, SCOPE) { return }
    for kw in matchKeywords(string(rsp), KEYWORDS) { risk.NewRisk(url, ...) }
}
```

> Collaboration note: cli is loaded **once at the top level**, while the hook closure reuses these values at runtime. `cli.LineDict` splits **by line**; if you need CSV compatibility, flatten it yourself with `str.Split(line, ",")` (see the `flattenKeywords` example).

## 4. Standard Pattern: Entry Point + YAK_MAIN Self-Test

```yak
// yak type: top-level execution; mitm type: register hooks + top-level cli
mirrorHTTPFlow = func(isHttps, url, req, rsp, body) { /* ... */ }

func runSelfTest() { /* verify with pure functions + mock data + assert */ }

if YAK_MAIN {
    runSelfTest()
}
```

`YAK_MAIN` is a global boolean injected by the engine:

- Running `yak xxx.yak` from the command line: `YAK_MAIN = true` -> run the self-test.
- When Yakit loads the plugin: top-level cli/hook registration executes as usual, while the self-test block is guarded as needed.

> Note: `cli.Args()` always contains the script file name (length >= 1). To distinguish "self-test / a real run with parameters", check `len(cli.Args()) > 1` (see `yak-cli-input.yak`).

## 5. Verification

```bash
cd /Users/v1ll4n/Projects/yaklang
# Self-test (uses defaults / pure logic)
yak skills/yakit-native-plugin/examples/yak-cli-input.yak
# Try real parameter injection
yak skills/yakit-native-plugin/examples/yak-cli-input.yak --target "yaklang.com,example.com:8443" --ports 80,443 --probe
```

Acceptance criteria: finishes within 10 seconds, all `assert` statements pass, all `log` output is in English, and `... self test passed` appears at the end. A native mitm plugin can be further validated against real requests with `yak hotpatch-mitm` (see yaklang-toolchain).

## References

- cli parameter system: `yaklang/common/utils/cli/cli.go` (CliExports)
- mitm hook contract: `yaklang/common/yak/hook_mixed_plugin_caller.go`
- risk API: `yaklang/common/yak/yaklib/risk.go` (`risk.NewRisk` / `risk.title` / `risk.severity` ...)
- Cross-references in the training material: `yaklang-ai-training-materials/library-usage/cli`, `.../risk`

> 📎 **Reference Document Notice**: this skill is adapted from an upstream open-source repository; the following reference document is **not distributed with this library**: `SKILL.md`. The key points of the related topics are retained in the corresponding descriptions in this document; if you need the expanded content, grep the library using keywords from the body text or search on your own.

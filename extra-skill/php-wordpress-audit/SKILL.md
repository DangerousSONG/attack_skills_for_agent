---
name: php-wordpress-audit
description: "WordPress framework-specific security audit tool. Performs white-box static auditing of common WordPress mechanisms such as nonce/capability/check_admin_referer, AJAX actions, escape/sanitize, redirects, secure uploads, and remote requests, and maps the results onto a generic vulnerability type system (AUTH/CSRF/XSS/SQL/CFG/SSRF, etc.)."
zh-signals: "对 WordPress 插件/主题做白盒静态审计，检查 nonce/capability/转义/上传/SSRF 等框架机制并映射漏洞类型。信号:WordPress审计,PHP审计,nonce,CSRF,SSRF"
when-to-use: "Use when performing white-box static security audit of an authorized WordPress plugin or theme source tree."
---

# PHP WordPress Framework Security Audit (php-wordpress-audit)

Analyze the framework-specific security mechanisms in a WordPress project, focusing on:
- nonce validation and capability permission checks (preventing CSRF and broken access control)
- WordPress AJAX callbacks (`wp_ajax_*` and `wp_ajax_nopriv_*` in `admin-ajax.php`)
- output escaping and template injection risks (esc_html/esc_attr/esc_url/wp_kses, etc.)
- `$wpdb` query parameterization and direct concatenation risks
- redirects (wp_redirect and wp_safe_redirect)
- upload handling (wp_handle_upload) and executable file risks
- remote HTTP requests (wp_remote_get/wp_remote_post) and SSRF correlation

## Input
Provided by the user:
- `source_path`: root of the WordPress code directory (containing wp-content/plugins or the theme directory)
Optional:
- `output_path`: output directory path (default `{source_path}_audit`)

## Output Directory
Output to:
```
{output_path}/framework_audit/
  wordpress_{timestamp}.md
```

## Framework Identification (Required)
Must provide evidence points for identifying WordPress (bare assertions are not allowed):
- Directory characteristics: `wp-content/`, `wp-admin/`, `wp-includes/`
- Core files: `wp-config.php` or `wp-settings.php`
- Plugin/theme directories: `wp-content/plugins/`, `wp-content/themes/`

## Risk Type Mapping (Required)
Every finding must state:
- Generic type code: `AUTH` / `CSRF` / `XSS` / `SQL` / `CFG` / `SSRF` / `UPLOAD`, etc.
- Mapping rationale: why the WordPress risk falls under that type code

## Mandatory Audit Checklist (Required: check each item and output the result)

### 1) nonce and CSRF protection (CSRF/AUTH)
Must locate and output:
- nonce output in forms: `wp_nonce_field` or custom nonce output
- validation on submission: locations of `check_admin_referer` and `wp_verify_nonce`
- AJAX nonce validation: `check_ajax_referer` (if present)

Decision rules:
- If a nonce exists but validation is missing, or it is only output on some branches, report a CSRF or AUTH risk

### 2) capability permission checks (AUTH)
Must locate and output:
- before every sensitive operation call: `current_user_can`, `user_can`, `is_user_logged_in`
- whether the capability value is user-controllable or overly broad (e.g. only `manage_options` is missing but a high-privilege operation is still executed)

### 3) AJAX action and route exposure (AUTH/CSRF)
Must locate and output:
- `add_action('wp_ajax_{action}', {value})` and `add_action('wp_ajax_nopriv_{action}', {value})`
- whether the callback function validates capabilities and nonce internally

### 4) output escaping and XSS (XSS)
Must locate and output:
- points that directly echo/print user data
- whether `esc_html`, `esc_attr`, `esc_url`, `wp_kses_post`, etc. are used
- whether the plugin/theme disables filtering or uses raw output

### 5) `$wpdb` query parameterization (SQL)
Must locate and output:
- the correct path: `$wpdb->prepare` and the use of prepare placeholders
- the dangerous path: `$wpdb->query`, `get_results`, `get_row` directly concatenating SQL strings

### 6) redirect and navigation safety (REDIR/CFG)
Must locate and output:
- usage of `wp_redirect` and `wp_safe_redirect`
- the source of the destination (usually user input) and whether scheme/host validation is performed

### 7) upload and remote requests (UPLOAD/SSRF)
Must locate and output:
- upload: `wp_handle_upload`, `media_handle_upload`, and whether file type/directory/access control are secure
- remote requests: `wp_remote_get`/`wp_remote_post`, whether the destination URL is controllable and whether an allowlist is used

## Observable PoC (Required: framework-specific observable verification harness)
Provide at least one of the following two categories and state the observation points:
- CSRF: an action missing nonce validation; craft a request with a missing or wrong nonce and observe the response and any state change
- AUTH: an action missing capability validation; send a sensitive action as a low-privilege user and observe whether it succeeds

PoC output requirements:
- Must include the action identifier and the real request entry point (usually `admin-ajax.php` or the corresponding form submission path)
- Must state the result you will observe (HTTP status code and business-side effect)

## Output Completeness Check (Mandatory)
- [ ] The output includes the check results for nonce/capability/AJAX/XSS/SQL/REDIR/UPLOAD/SSRF
- [ ] Every risk has: a mapped type code + location evidence + an observable verification harness + a remediation recommendation


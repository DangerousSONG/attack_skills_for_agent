---
name: php-framework-audit
description: |
  PHP framework-specific security audit. Triggered during PHP white-box audits once the target framework has been identified
  and framework-specific security mechanisms and common configuration flaws need to be checked.
  Covers 6 major frameworks: Laravel (mass assignment / Blade XSS / CSRF exceptions),
  ThinkPHP (historical RCE / route injection / cache write), WordPress (plugin vulnerabilities / permission hooks / nonce validation),
  Symfony (Debug Bar / YAML parsing / security voters), Yii2 (RBAC / ActiveRecord injection), CodeIgniter (global XSS / CSRF token).
zh-signals: "PHP 框架特定安全审计，覆盖 Laravel、ThinkPHP、WordPress、Symfony、Yii2 与 CodeIgniter。信号:Laravel审计,ThinkPHP,WordPress插件,框架安全,配置缺陷"
when-to-use: "Use during PHP white-box audits once a target framework is identified, to check framework-specific security mechanisms and common configuration flaws across Laravel, ThinkPHP, WordPress, Symfony, Yii2, or CodeIgniter."
metadata:
  tags: laravel, thinkphp, wordpress, symfony, yii, codeigniter, framework audit, mass assignment, blade xss, wp plugin, think rce
  category: code-audit
---

# PHP Framework-Specific Security Audit
## Framework Identification Decision Table

| Identification Feature | Framework | Deep Reference |
|---|---|---|
| `composer.json` → `laravel/framework` | Laravel | [references/laravel-patterns.md](references/laravel-patterns.md) |
| `composer.json` → `topthink/framework` | ThinkPHP | [references/thinkphp-patterns.md](references/thinkphp-patterns.md) |
| Presence of a `wp-content/` directory or `wp-config.php` | WordPress | [references/wordpress-patterns.md](references/wordpress-patterns.md) |
| `composer.json` → `symfony/framework-bundle` | Symfony | Briefly covered here |
| `composer.json` → `yiisoft/yii2` | Yii2 | Briefly covered here |
| `composer.json` → `codeigniter4/framework` | CodeIgniter | Briefly covered here |

## Laravel Core Checkpoints

1. **Mass Assignment** -- are `$fillable` / `$guarded` configured correctly; do `Model::create($request->all())` or `update($request->all())` contain unfiltered fields
2. **Blade XSS** -- search for unescaped output via `{!! !!}`, direct echo inside `@php` directives, and custom Blade Directives that do not call `e()`
3. **CSRF Exceptions** -- does the `$except` array of the `VerifyCsrfToken` middleware contain sensitive routes; API route groups do not include the CSRF middleware by default
4. **Gate / Policy** -- do controller methods call `$this->authorize()` or `Gate::allows()`; do Policy definitions cover all CRUD operations
5. **Eloquent Raw** -- is there variable concatenation in `whereRaw` / `havingRaw` / `orderByRaw` / `DB::raw`
6. **Signed URLs / Debugging** -- leftover `APP_DEBUG=true`, web-accessible `.env`, exposed Telescope / Debugbar routes

## ThinkPHP Core Checkpoints

1. **Historical RCE Routes** -- TP5.x `method()` override, arbitrary method invocation via the `Request` class `__construct`
2. **Cache File Write** -- predictable cache file path + controllable content → write a WebShell
3. **Database where Injection** -- expression injection via `exp` / `like` / `between` in `where` array conditions, `Db::raw`
4. **Session Deserialization** -- the TP6 session serialization driver may trigger a POP chain
5. **Template Injection** -- `{php}` tags, variable function calls such as `{:system()}`

## WordPress Core Checkpoints

1. **Plugin action/filter** -- `wp_ajax_nopriv_*` hooks exposing unauthenticated operations, Shortcode callback parameter injection
2. **Missing $wpdb->prepare** -- direct SQL concatenation into `$wpdb->query()`
3. **Nonce Validation** -- form handlers / AJAX handlers missing `wp_verify_nonce` / `check_admin_referer`
4. **REST API** -- is the `permission_callback` of `register_rest_route` `__return_true` or missing
5. **File Upload** -- plugin custom upload logic bypassing the MIME check of `wp_handle_upload`

## Symfony Brief Overview

- **Debug Mode** -- `APP_DEBUG=1` leaks the Profiler / Web Debug Toolbar, exposing environment variables and SQL
- **YAML Deserialization** -- lower versions of `Yaml::parse` support the `!!php/object` tag, leading to object injection
- **Security Voter** -- flaws in custom Voter logic or misuse of `ACCESS_ABSTAIN` leading to broken access control

## Yii2 Brief Overview

- **RBAC Configuration** -- improper permission item assignment in `DbManager`, missing `checkAccess` calls leading to vertical privilege escalation
- **ActiveRecord Injection** -- string concatenation in `findBySql` / `where` conditions, unfiltered `orderBy`

## CodeIgniter Brief Overview

- **Global XSS Filtering** -- CI3 `$config['global_xss_filtering']` is deprecated, CI4 requires manual `esc()` calls
- **CSRF Token** -- `CSRFProtection` is configured but too many routes are excluded, and the token regeneration policy is improper

## Further Reading

- [Laravel audit patterns](references/laravel-patterns.md)
- [ThinkPHP audit patterns](references/thinkphp-patterns.md)
- [WordPress audit patterns](references/wordpress-patterns.md)

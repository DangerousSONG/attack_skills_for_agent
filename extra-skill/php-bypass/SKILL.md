---
name: php-bypass
description: "PHP security restriction bypass: breaking out of disable_functions and open_basedir limits. Use when you already have a webshell but command execution functions are disabled or file operations are restricted by open_basedir"
zh-signals: "PHP 安全特性绕过方法，突破 disable_functions 与 open_basedir 限制。信号:PHP绕过,disable_functions,open_basedir,webshell,沙箱逃逸"
when-to-use: "Use after obtaining a PHP webshell when command execution functions are disabled or file operations are restricted by open_basedir."
metadata:
  tags: "disable_functions,open_basedir,php,bypass,rce,webshell,LD_PRELOAD,putenv,FFI,iconv,imagick,bypass,sandbox escape"
  category: "exploit"
---

# PHP Security Restriction Bypass Methodology


When you already have a webshell (one that can execute PHP code) but cannot execute system commands, this skill guides you through breaking the `disable_functions` and `open_basedir` restrictions.

## Further Reading

- Full bypass code for Methods A-G → [references/disable-functions-bypass.md](references/disable-functions-bypass.md)
- open_basedir bypass methods → [references/open-basedir-bypass.md](references/open-basedir-bypass.md)
- CTF PHP tricks (OPcache poisoning, polymorphic files) → [references/ctf-php-tricks.md](references/ctf-php-tricks.md)

---

## Phase 0: Information Gathering (30-second check)

First confirm the scope of the restrictions, as this determines the attack path:

```php
<?php
echo "disable_functions: " . ini_get('disable_functions') . "\n";
echo "open_basedir: " . ini_get('open_basedir') . "\n";
echo "PHP version: " . phpversion() . "\n";
echo "OS: " . PHP_OS . "\n";
echo "Loaded extensions: " . implode(', ', get_loaded_extensions()) . "\n";
// Key extension checks
echo "FFI: " . (extension_loaded('ffi') ? 'YES' : 'NO') . "\n";
echo "imagick: " . (extension_loaded('imagick') ? 'YES' : 'NO') . "\n";
echo "iconv: " . (extension_loaded('iconv') ? 'YES' : 'NO') . "\n";
echo "putenv: " . (function_exists('putenv') ? 'YES' : 'NO') . "\n";
echo "mail: " . (function_exists('mail') ? 'YES' : 'NO') . "\n";
echo "error_log: " . (function_exists('error_log') ? 'YES' : 'NO') . "\n";
?>
```

## Phase 1: disable_functions Bypass Decision Tree

```
Is putenv() available?
├─ YES → Are mail()/error_log() available?
│   ├─ YES → Method A: LD_PRELOAD hijack (most stable, preferred)
│   └─ NO → Is the iconv extension loadable?
│       ├─ YES → Method B: iconv + LD_PRELOAD
│       └─ NO → Is the imagick extension present?
│           ├─ YES → Method C: ImageMagick delegate
│           └─ NO → next branch
├─ NO → Is the FFI extension available (PHP ≥ 7.4)?
│   ├─ YES → Method D: call system() directly via FFI
│   └─ NO → PHP < 7.4.21 / 8.0 < 8.0.8?
│       ├─ YES → Method E: PHP Backtrace UAF (CVE-2019-11043 etc.)
│       └─ NO → Is the PCNTL extension available?
│           ├─ YES → Method F: pcntl_exec()
│           └─ NO → Method G: ShellShock (CVE-2014-6271) / Apache mod_cgi
```

> See [references/disable-functions-bypass.md](references/disable-functions-bypass.md) for the full code of each method.

---

## Practical Quick Reference Table

| What you observe | Method | Command |
|----------|------|------|
| putenv + mail available | LD_PRELOAD | upload .so → putenv → mail() |
| putenv + error_log available | LD_PRELOAD | same as above, use error_log() instead |
| putenv + iconv available | GCONV_PATH | upload gconv-modules + .so |
| imagick loaded | delegate injection | MVG/SVG payload |
| PHP ≥ 7.4 + FFI | FFI::cdef | call system() directly |
| pcntl loaded | pcntl_exec | fork + exec |
| Bash ≤ 4.3 | ShellShock | putenv environment variable injection |
| Nothing works | UAF exploit | search for an exploit matching the version |

## Notes

- Check phpinfo() first to confirm the environment, do not blindly try
- The LD_PRELOAD method requires uploading a .so file, so ensure a writable directory exists
- The FFI method is the cleanest but requires a recent PHP version
- In some Docker environments `/usr/sbin/sendmail` does not exist → mail() does not trigger execve → switch to error_log
- After a command executes successfully, remember to clean up the uploaded .so file

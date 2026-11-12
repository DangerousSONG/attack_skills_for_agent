---
name: information-disclosure-methodology
description: "Web application sensitive information disclosure detection and exploitation. Use when you find information disclosure points such as .git/.svn directories, backup file paths (.bak/.zip/.tar.gz), .env configuration files, Swagger/OpenAPI documentation, or debug pages. Also applies to deep exploitation after source code disclosure: git history auditing (git log -p -S to search for deleted passwords and flags), svn wc.db file list extraction, .DS_Store directory enumeration. Prioritize this over vulnerability exploitation — information disclosure can directly provide credentials and attack paths, and is often faster than hunting for vulnerabilities to get into the system"
zh-signals: "检测并利用 Web 应用敏感信息泄露，涵盖 .git/.svn、备份文件、.env、Swagger 与 debug 页面。信号:信息泄露,源码泄露,.git 泄露,备份文件,凭据提取"
when-to-use: "Use when you find exposed source control directories, backup files, environment configs, API docs, or debug pages and need to turn disclosure into credentials or an attack path."
metadata:
  tags: "information_disclosure,information disclosure,source-code,backup,debug,credentials,ssh,.git,.svn,.env,git-dumper,svn-extractor,source code leak"
  category: "exploit"
---

# Information Disclosure Methodology

## ⛔ Further Reading (Must Read)

- Full .git exploit chain (dump → history audit → stash/branches → credential extraction) → [references/source-recovery.md](references/source-recovery.md)
- .svn exploitation (entries file / wc.db SQLite queries / pristine file recovery) → [references/source-recovery.md](references/source-recovery.md)
- .DS_Store parsing, Swagger exploitation, credential search → [references/source-recovery.md](references/source-recovery.md)
- API parameter manipulation disclosure (query=% wildcard, info→list transformation, pageSize enlargement, empty array bypass) → [references/api-param-tricks.md](references/api-param-tricks.md)

## Phase 1: Source Code and Configuration Files
Directly request common sensitive paths (test them one by one or scan in bulk):
```
/.git/HEAD          /.env              /config.py         /Dockerfile
/.svn/entries       /.svn/wc.db        /.DS_Store         /robots.txt
/WEB-INF/web.xml    /package.json      /app.py            /backup.sql
/.dockerenv         /composer.json     /Gemfile           /requirements.txt
```
1. Use `curl -s -o /dev/null -w '%{http_code}' http://TARGET/<path>` to batch check status codes
2. For 200 responses, further check whether the content is a real file (rule out custom 404 pages)
3. `.git/HEAD` returns 200 → dump the whole thing with git-dumper → audit the historical commits with git log to find passwords/flags!
4. `.svn/entries` or `.svn/wc.db` returns 200 → dump with svn-extractor → extract the file list and contents
5. `.env` returns 200 → directly read sensitive configuration such as the database connection string, API keys, and SECRET_KEY
→ Detailed source recovery steps → [references/source-recovery.md](references/source-recovery.md)

## Phase 2: Debug Information
1. Send malformed requests to trigger 500 error pages (missing parameters, type mismatches, illegal characters)
2. Flask `debug=True` shows the full source code and an interactive debugger (possibly direct RCE)
3. Django DEBUG=True shows settings, URL routes, and SQL queries
4. Extract from the stack trace: absolute file paths, framework versions, database type, variable values
5. Check the response headers: `Server`, `X-Powered-By`, `X-Debug-Token`, `X-Request-Id`
6. Try accessing `/debug`, `/trace`, `/actuator` (Spring Boot), `/elmah.axd` (.NET)

## Phase 3: API Documentation Disclosure
1. Request the documentation endpoints one by one: `/docs`, `/swagger`, `/swagger.json`, `/swagger-ui.html`
2. Additional paths: `/openapi.json`, `/redoc`, `/api-docs`, `/graphql`, `/graphiql`
3. Check version-prefixed paths such as `/v1/docs` and `/v2/docs`
4. Extract from the API documentation: the full endpoint list, parameter types and sample values, authentication methods, data model definitions
5. Pay special attention to admin interfaces (`/admin/*`), user management (`/users`), and file operations (`/upload`, `/download`)
6. GraphQL introspection query: `{__schema{types{name,fields{name}}}}`

## Phase 4: Backups and Logs
1. Scan for backup files: `/backup.zip`, `/backup.tar.gz`, `/app.py.bak`, `/web.config.old`
2. Filename variants: `index.php.bak`, `index.php~`, `index.php.swp`, `.index.php.swp`
3. Log files: `/access.log`, `/error.log`, `/debug.log`, `/app.log`
4. Use `spray` or `ffuf` with a backup wordlist to scan for more paths
5. Database backups: `/dump.sql`, `/db.sql`, `/database.sql`, `/backup.sql`
6. Version control leftovers: `/.hg/` (Mercurial), `/.bzr/` (Bazaar)

## Phase 5: API Parameter Manipulation
1. After discovering an API endpoint, apply four manipulations to the query parameters: empty value, `%` wildcard, null, and parameter removal
2. `pageSize=9999` enlarges the pagination to retrieve more data
3. `info` → `list` endpoint transformation to find list interfaces
4. Empty array `[]` → remove the Token to test authentication bypass
5. Add `verbose=true` and `debug=1` parameters and check whether extra information is returned
→ Detailed techniques and case studies → [references/api-param-tricks.md](references/api-param-tricks.md)

## Phase 6: Credential Search
1. Search the obtained source code/configuration for: `password`, `secret`, `api_key`, `token`, `mysql://`
2. Check database connection strings and third-party API keys in the `.env` file
3. Search for SSH private keys: `/.ssh/id_rsa`, `/home/*/.ssh/id_rsa`
4. Base64-encoded credentials: decode all Base64 strings and inspect their contents
5. **Use the credentials immediately once found**: log in to the web app, connect over SSH, connect directly to the database
6. Search the git history for deleted passwords: `git log -p -S 'password'`

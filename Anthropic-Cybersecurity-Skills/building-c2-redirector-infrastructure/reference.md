# building-c2-redirector-infrastructure — 详细参考（由 SKILL.md 拆分）

# Proxy to the hidden team server, preserving the URI
RewriteRule ^.*$ https://10.0.0.2%{REQUEST_URI} [P,L]
# Everything else -> decoy site
RewriteRule ^.*$ https://www.legitimate-decoy.com/ [R=302,L]
```
```bash
sudo a2ensite redirector && sudo apache2ctl configtest && sudo systemctl reload apache2
```

### 5. Generate rules from a malleable profile
Let `cs2modrewrite` build the Apache or nginx rules directly from your Cobalt Strike profile so the filter exactly matches beacon traffic.
```bash
cd cs2modrewrite
# Apache mod_rewrite rules
python3 cs2modrewrite.py -i havex.profile -c https://10.0.0.2 \
  -r https://www.legitimate-decoy.com -o /etc/apache2/redirect.rules
# nginx config
python3 cs2nginx.py -i havex.profile -c https://10.0.0.2 \
  -r https://www.legitimate-decoy.com -H cdn.example.com > /etc/nginx/sites-available/c2.conf
```

### 6. Terminate TLS with Let's Encrypt
Issue a valid certificate so beacon HTTPS does not throw TLS warnings and the edge looks legitimate.
```bash
sudo certbot --nginx -d cdn.example.com --agree-tos -m ops@example.com --redirect
# Verify auto-renewal
sudo certbot renew --dry-run
```

### 7. Apply OPSEC controls
Layer defenses against blue-team analysis: validate headers, geofence to the target country, divert sandboxes, and rotate edges. Consider CDN/domain fronting (T1090.004) where supported.
```bash
# Example: drop non-target geographies at the firewall with ipset/GeoIP,
# require a custom auth header in the profile, and rotate the redirector
# domain/IP on a schedule. Check the redirector only forwards matched traffic:
curl -k https://cdn.example.com/                       # expect 302 to decoy
curl -k -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  https://cdn.example.com/api/v2/jobs                  # expect proxied response
```

## Tools and Resources

| Tool | Purpose | Source |
|------|---------|--------|
| nginx | Filtering reverse-proxy redirector | https://nginx.org/ |
| Apache mod_rewrite | `[P]` proxy + `302` decoy redirector | https://httpd.apache.org/docs/current/mod/mod_rewrite.html |
| cs2modrewrite | Generate Apache/nginx rules from CS profile | https://github.com/threatexpress/cs2modrewrite |
| RedWarden | Malleable-aware filtering C2 reverse proxy | https://github.com/mgeeky/RedWarden |
| redi | Automated nginx + Let's Encrypt CS redirector | https://github.com/taherio/redi |
| socat | Dumb-pipe TCP forwarder | http://www.dest-unreach.org/socat/ |
| Let's Encrypt / certbot | Free TLS certificates | https://certbot.eff.org/ |
| ired.team | Red-team infrastructure reference | https://www.ired.team/offensive-security/red-team-infrastructure |

## Validation Criteria

- [ ] Team server firewalled to accept only the redirector source IP on the C2 port.
- [ ] Redirector deployed (dumb pipe and/or filtering reverse proxy).
- [ ] Filter rules derived from the actual malleable C2 profile (URI + User-Agent + headers).
- [ ] Non-matching requests return a `302` to a benign decoy site (verified with curl).
- [ ] Matching beacon requests are proxied to the hidden team server (verified with curl).
- [ ] Valid TLS certificate issued and auto-renewal confirmed.
- [ ] OPSEC controls applied (UA/header validation, geofencing, decoy diversion).
- [ ] Domain categorization / CDN fronting considered where applicable.
- [ ] Infrastructure rotation and decommissioning plan documented.
- [ ] All activity confined to the authorized engagement scope.

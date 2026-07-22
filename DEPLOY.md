# Deploying okumpi.com — Docker production guide

Target: Ubuntu VM already running **Postal** (web UI on `127.0.0.1:5000`)
behind **Caddy**. The website runs in **one container** (`okumpi-web`) on
`127.0.0.1:8080` and Caddy routes `okumpi.com` to it. Postal, its Caddy and
every other container stay untouched.

```
Internet ──► Caddy (:80/:443, auto-HTTPS)
              ├── mta.okumpi.com ──► 127.0.0.1:5000  (Postal, unchanged)
              └── okumpi.com     ──► 127.0.0.1:8080  (okumpi-web container)
```

---

## 0. One-time checks (on the VM, as root)

```bash
# Is 8080 free? (no output = free; if taken, pick 8081 etc. — see step 2)
ss -ltnp | grep :8080

# How is Caddy running? (Postal's standard install runs it as a container)
docker ps --format '{{.Names}}\t{{.Image}}' | grep -i caddy
```

## 1. Get the code

```bash
cd /opt
git clone https://github.com/OkumpiTech/home_web.git okumpi-web
cd okumpi-web
```

(Later updates: `cd /opt/okumpi-web && git pull && docker compose up -d --build`)

## 2. Configure

```bash
cp .env.example .env

# generate a real secret key and put it in .env
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
nano .env       # paste the key; check the domains
```

`.env` should end up like:

```
DJANGO_SECRET_KEY=<the long random string>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=okumpi.com,www.okumpi.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://okumpi.com,https://www.okumpi.com
DJANGO_BEHIND_PROXY=1
GUNICORN_WORKERS=3
```

> If port 8080 was taken in step 0, edit `docker-compose.yml` and change
> `"127.0.0.1:8080:8080"` to e.g. `"127.0.0.1:8081:8080"` — then use 8081
> in the Caddyfile below.

## 3. Build & start the container

```bash
docker compose up -d --build
docker compose logs -f web     # watch: migrations → seed → gunicorn on :8080  (Ctrl+C to stop watching)
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: okumpi.com" http://127.0.0.1:8080/   # expect 200
```

First start creates the database on the `okumpi_data` volume, seeds all the
site content, and creates the admin user. **Change its password now:**

```bash
docker compose exec web python manage.py changepassword admin
```

## 4. Point okumpi.com at the container (Caddy)

Edit the Caddyfile (keep the `mta.okumpi.com` block exactly as it is):

```bash
nano /opt/postal/config/Caddyfile
```

Change the `okumpi.com` block to:

```
okumpi.com {
  reverse_proxy 127.0.0.1:8080
}
```

(The full ready-made file is in this repo: `Caddyfile.okumpi`. Only include a
`www.okumpi.com` block if DNS for `www` points to this server.)

Reload Caddy — pick the line matching how Caddy runs (from step 0):

```bash
# Caddy in Docker (Postal default — container usually named postal-caddy):
docker restart postal-caddy

# or, zero-downtime reload:
docker exec postal-caddy caddy reload --config /etc/caddy/Caddyfile

# Caddy installed via apt/systemd instead:
systemctl reload caddy
```

## 5. Verify

```bash
curl -I https://okumpi.com          # 200, served by the website
curl -I https://mta.okumpi.com      # Postal still answering
docker ps                           # okumpi-web healthy, postal containers untouched
```

DNS reminder: `okumpi.com` (A record) must point to this VM's public IP so
Caddy can obtain the HTTPS certificate.

---

## Day-2 operations

| Task | Command |
|---|---|
| Deploy an update | `cd /opt/okumpi-web && git pull && docker compose up -d --build` |
| Logs | `docker compose logs -f web` |
| Restart | `docker compose restart web` |
| Django shell | `docker compose exec web python manage.py shell` |
| Change admin password | `docker compose exec web python manage.py changepassword admin` |
| Reseed content from scratch | `docker compose exec web python manage.py seed_okumpi --fresh` |
| Back up the database | `docker compose cp web:/data/db.sqlite3 ./backup-$(date +%F).sqlite3` |
| Contact-form messages | Admin → Core → Contact messages (https://okumpi.com/admin) |

Notes:

- The SQLite database lives on the named volume `okumpi_data` — rebuilding
  or updating the image never wipes your data. `seed_okumpi` only runs its
  content load on an empty database.
- Static files are baked into the image and served by WhiteNoise (gzip'd);
  no extra web server or volume is needed.
- The container binds only to `127.0.0.1`, so it is not reachable from the
  internet except through Caddy.

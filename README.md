# Okumpi v2 — Django Website

Deep indigo + violet design with airy white content sections, and illustrated
tech artwork — globe, data ribbons and floating system chips.
Django 6.0.7 · SQLite · zero dependencies beyond Django · fully responsive.

## Quick start (Windows)

```bat
cd D:\Dev\OpenCode\okumpi_v2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_okumpi
python manage.py runserver
```

Open http://127.0.0.1:8000

> A ready-seeded `db.sqlite3` ships with the project, so `migrate` + `seed_okumpi`
> are only needed if you delete it or start fresh. `seed_okumpi --fresh` wipes and
> reseeds all site content.

## Admin

http://127.0.0.1:8000/admin — `admin` / `okumpi2026` (change this before deploying!)

Everything on the site is editable in the admin: practice areas & services,
industry solutions, testimonials, partner/client logos, countries, FAQs, jobs,
news, blog posts, KB articles, forum categories, contact messages and
newsletter subscribers.

## Pages

| URL | Page |
|---|---|
| `/` | Home — hero, testimonial carousel, partner marquees, services, solutions, security spotlight, stats, why-us, FAQ, CTA |
| `/services/` | Six practice areas with all sub-services |
| `/about/` | Story, mission/vision/values, countries, client logos |
| `/careers/` | Open roles (from DB) |
| `/newsroom/` | News & announcements |
| `/blog/` | Blog posts by category |
| `/knowledge-base/` | Guides & checklists |
| `/community/` | Forum categories |
| `/contact/` | Working contact form (saves to DB) |
| `/subscribe/` | Newsletter endpoint (hero & footer email capture) |

## Structure

```
okumpi_v2/
├── manage.py
├── requirements.txt          # Django==6.0.7
├── db.sqlite3                # pre-seeded database
├── okumpi/                   # project (settings, urls, wsgi, asgi)
├── core/                     # single app: models, views, forms, admin,
│   └── management/commands/seed_okumpi.py
├── templates/                # base + 9 pages
└── static/
    ├── css/styles.css        # the whole design system
    ├── js/main.js            # carousel, reveal, counters, mobile nav, AJAX
    └── img/                  # partner & client logos
```

## Design system

- Palette: indigo canvas (`#0a0819`–`#1d173f`) for hero/security/stats/footer,
  white sections (`#fdfcff`, lavender `#f4f1ff` tints) for content, violet accents
  (`#8b5cf6`, `#a78bfa`, `#d946ef`); per-practice hues (violet, cyan, iris,
  magenta, lime, amber)
- Light sections use the `.light` class — CSS variables re-theme every component
- Type: Outfit (headings) + Plus Jakarta Sans (body) + JetBrains Mono (terminal)
- Illustrated hero: SVG wireframe globe + data ribbons + floating system chips
  (code · cloud · shield · AI · network · lock), starfield, aurora, skyline
- Tech background patterns: circuit traces (services, page heroes),
  network constellations (solutions, CTA), radar rings (security terminal)
- Glass surfaces, logo marquees, scroll-snap testimonial carousel with
  arrows & dots
- Breakpoints: 1180px / 1080px / 820px / 620px — works down to 320px

## Production notes

- Set `DEBUG = False`, a real `SECRET_KEY`, and `ALLOWED_HOSTS` in `okumpi/settings.py`
- `python manage.py collectstatic` and serve `staticfiles/` (e.g. WhiteNoise/Nginx)
- Change the admin password: `python manage.py changepassword admin`

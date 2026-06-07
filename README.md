# N Akshaya — Portfolio Website

A full-stack personal portfolio built with **Django 5**, **PostgreSQL**, HTML, CSS, and Vanilla JavaScript.
Clean neo-brutalist design with a pastel colour palette, tab-based navigation, and an admin inbox for contact messages.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.1 |
| Database | PostgreSQL (local) / Neon (production) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Fonts | Syne, Plus Jakarta Sans (Google Fonts) |
| Static files | WhiteNoise |
| Production server | Gunicorn |
| Hosting | Render (free tier) |

---

## Project Structure

```
portfolio/
├── .env                    ← your secrets (never commit this)
├── manage.py
├── requirements.txt
├── Procfile
├── portfolio/              ← Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio_app/          ← main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/
│   └── index.html
└── static/
```

---

## Local Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create the PostgreSQL database
Open psql and run:
```sql
CREATE DATABASE portfolio_db;
```

### 3. Create your `.env` file
```env
SECRET_KEY=any-long-random-string-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=your_chosen_password
```

### 4. Run migrations
```bash
python manage.py makemigrations portfolio_app
python manage.py migrate
```

### 5. Start the server
```bash
python manage.py runserver
```

Open → http://127.0.0.1:8000

---

## How the Site Works

The entire site is a single-page Django template with tab-based navigation.

**Visitor tabs (in order):** About · Skills · Projects · Education · Contact · About the Website

**Admin tabs (in order):** About · Skills · Projects · Education · Inbox · About the Website

The admin login is hidden inside the **"About the Website"** tab — there is a small "Login as Admin" button at the bottom of that page. Credentials are set via environment variables (`DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_PASSWORD`).

Contact form submissions are saved to the database and visible in the **Inbox** tab after admin login.

> **Important:** Data added on localhost is stored in your **local** PostgreSQL database. Data on the live Render site is stored in **Neon** (cloud). The two databases are separate — anything added locally will not appear on the live site and vice versa. Always add content (projects, skills, etc.) through the live admin portal.

---

## Deploying to Render

### Step 1 — Set up Neon (cloud database)

1. Go to [neon.tech](https://neon.tech) → sign up (free)
2. Create a new project → copy the **Connection string**
   It looks like: `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`
3. Save this — you'll use it as `DATABASE_URL` in Render

### Step 2 — Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 3 — Create a Render Web Service

1. Go to [render.com](https://render.com) → sign up → **New → Web Service**
2. Connect your GitHub account → select your portfolio repo
3. Configure:

| Setting | Value |
|---|---|
| Root Directory | `portfolio` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate` |
| Start Command | `gunicorn portfolio.wsgi` |
| Instance Type | Free |

### Step 4 — Set Environment Variables on Render

In **Environment → Add Environment Variable**:

| Key | Value |
|---|---|
| `DATABASE_URL` | *(paste your Neon connection string)* |
| `SECRET_KEY` | *(any long random string, 50+ characters)* |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*.onrender.com` |
| `DJANGO_SUPERUSER_USERNAME` | *(your admin username)* |
| `DJANGO_SUPERUSER_PASSWORD` | *(your admin password)* |

### Step 5 — Deploy

Click **Create Web Service** → Render builds and deploys automatically.
Your live URL will be something like `https://your-app-name.onrender.com`.

---

## Redeploying After Code Changes

```bash
git add .
git commit -m "describe what changed"
git push
```

Render detects the push and auto-redeploys in ~2 minutes. Watch progress in **Render → your service → Logs**.

---

## Pre-Deploy Checklist

- [ ] `.env` is in `.gitignore` and never committed
- [ ] `DEBUG=False` set in Render environment variables
- [ ] Strong `SECRET_KEY` set in Render environment variables
- [ ] `ALLOWED_HOSTS` includes your Render domain
- [ ] Build command includes `collectstatic` and `migrate`
- [ ] Admin credentials set as Render environment variables

---

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `password authentication failed` | Wrong DB password | Check `.env` or Render variable |
| `No module named 'whitenoise'` | Not installed | `pip install whitenoise` |
| `No module named 'psycopg2'` | Missing driver | `pip install psycopg2-binary` |
| `relation does not exist` | Migrations not run | Add `migrate` to build command |
| `DisallowedHost` | Domain not in ALLOWED_HOSTS | Add Render URL to the variable |
| Static files 404 | collectstatic not run | Add it to the build command |
| Site takes 30–60s to load | Free tier sleep | Normal — wakes on first visit |
| Data missing on live site | Local vs Neon DB mismatch | Re-add data via live admin portal |

---

*N Akshaya — B.Tech CSE Student*

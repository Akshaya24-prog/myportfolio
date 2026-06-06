# N Akshaya — Portfolio Website

A full-stack personal portfolio built with **Django 5**, **PostgreSQL**, HTML, CSS, and Vanilla JavaScript.
Clean neo-brutalist design with a pastel colour palette, entrance overlay, tab-based navigation, and an admin inbox for contact messages.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 |
| Database | PostgreSQL + psycopg2-binary |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Fonts | Syne, Plus Jakarta Sans (Google Fonts) |
| Static files | WhiteNoise |
| Production server | Gunicorn |

---

## Project Structure

```
portfolio/
├── .env                    ← your secrets (never commit this)
├── .env.example
├── manage.py
├── requirements.txt
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
    ├── style.css
    └── script.js
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

**Visitor view:** Skills · Projects · Contact  
**Admin view:** Skills · Projects · Contact · Inbox (contact messages)

On load, an entrance overlay asks whether you're a visitor or admin. The admin login (`admin` / `12345`) is a front-end UI gate — change these credentials in the `<script>` block of `index.html`.

Contact form submissions are saved to the database and visible in the Inbox tab after admin login.

---

## Deploying to Railway

### Step 1 — Create a `.gitignore`
Make sure `.env` is never pushed to GitHub. Create a `.gitignore` in the root folder:
```
.env
__pycache__/
*.pyc
staticfiles/
media/
db.sqlite3
```

### Step 2 — Push to GitHub
```bash
git init
git add .
git commit -m "initial commit"
```
Go to [github.com](https://github.com), create a new repository, then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 3 — Create a Railway account
Go to [railway.app](https://railway.app) → sign up with your GitHub account.

### Step 4 — Deploy from GitHub
Click **New Project → Deploy from GitHub repo** → select your portfolio repository.
Railway auto-detects Python and starts building.

### Step 5 — Add PostgreSQL
In the Railway project dashboard, click **New → Database → Add PostgreSQL**.
This creates a database and makes its connection details available to your app automatically.

### Step 6 — Set environment variables
In your service's **Variables** tab, add these one by one:

```
SECRET_KEY        = any-new-long-random-string
DEBUG             = False
ALLOWED_HOSTS     = your-app-name.up.railway.app
DB_NAME           = ${{Postgres.PGDATABASE}}
DB_USER           = ${{Postgres.PGUSER}}
DB_PASSWORD       = ${{Postgres.PGPASSWORD}}
DB_HOST           = ${{Postgres.PGHOST}}
DB_PORT           = ${{Postgres.PGPORT}}
```

The `${{Postgres.VARIABLE}}` values auto-fill from the PostgreSQL plugin — no copy-pasting needed.

### Step 7 — Set build and start commands
In **Settings → Build**, set:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```
In **Settings → Deploy → Start Command**, set:
```bash
python manage.py migrate && gunicorn portfolio.wsgi
```

### Step 8 — Get your live URL
Railway redeploys automatically. Once the build succeeds, your live URL appears in the **Deployments** tab — something like `https://your-app.up.railway.app`.

Every time you `git push`, Railway automatically redeploys.

---

## Pre-Deploy Checklist

- [ ] `.env` is in `.gitignore`
- [ ] `DEBUG=False` set in Railway variables
- [ ] Strong `SECRET_KEY` set in Railway variables
- [ ] Railway domain added to `ALLOWED_HOSTS`
- [ ] Build command includes `collectstatic`
- [ ] Start command includes `migrate`

---

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `password authentication failed` | Wrong DB password | Check `.env` or Railway variable |
| `No module named 'whitenoise'` | Not installed | `pip install whitenoise` |
| `No module named 'psycopg2'` | Missing driver | `pip install psycopg2-binary` |
| `relation does not exist` | Migrations not run | Run `migrate` in start command |
| `DisallowedHost` | Domain not in ALLOWED_HOSTS | Add Railway URL to the variable |
| Static files 404 | collectstatic not run | Add it to the build command |

---

*N Akshaya — B.Tech CSE Student*
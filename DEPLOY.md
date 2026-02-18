# FreelanceHub — Deployment Guide

## Quick Deploy to Railway (Recommended — Free)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/freelancehub.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
2. Select your repository
3. Railway auto-detects the `Procfile` and deploys

### Step 3: Set Environment Variables on Railway
In your Railway project → **Variables** tab, add:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Generate one at [djecrety.ir](https://djecrety.ir) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.railway.app` |

### Step 4: Run Migrations
In Railway → **Shell** tab:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Alternative: Deploy to Render (Also Free)

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect GitHub repo
3. Set **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Set **Start Command**: `gunicorn freelance_marketplace.wsgi`
5. Add environment variables (same as Railway above)

---

## Local Development

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/freelancehub.git
cd freelancehub

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and set DEBUG=True for local dev

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

---

## Important Notes

- **Never commit `.env`** — it's in `.gitignore`
- **Media files** (user uploads) are not persisted on Railway/Render free tier — consider Cloudinary for production
- **Database** — SQLite works for small deployments; upgrade to PostgreSQL for larger scale
- **Admin panel** — available at `/admin/` after creating a superuser

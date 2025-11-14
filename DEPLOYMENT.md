# Money Laundry - Deployment Guide

## Quick Deploy to Vercel

### 1. Persiapan
1. Fork repository ini ke akun GitHub Anda
2. Buat account di [Vercel](https://vercel.com) (gratis)
3. Install Vercel CLI (opsional): `npm i -g vercel`

### 2. Environment Variables
Copy `.env.example` ke `.env` dan isi:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app
```

### 3. Deploy via GitHub (Recommended)
1. Login ke Vercel Dashboard
2. Klik "New Project"
3. Import repository dari GitHub
4. Configure environment variables
5. Klik "Deploy"

### 4. Deploy via CLI
```bash
# Login ke Vercel
vercel login

# Deploy project
vercel --prod
```

### 5. Post-Deployment Setup
1. Jalankan migrations: `vercel --prod -- python manage.py migrate`
2. Buat superuser: `vercel --prod -- python manage.py createsuperuser`
3. Collect static files: `vercel --prod -- python manage.py collectstatic`

## Alternative Platforms

### Railway
1. Buat account di Railway
2. Connect ke GitHub
3. Deploy otomatis dari repository

### Heroku
1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Deploy: `git push heroku main`

## Production Checklist
- [ ] DEBUG = False
- [ ] SECRET_KEY yang kuat
- [ ] ALLOWED_HOSTS dikonfigurasi
- [ ] Database production (PostgreSQL)
- [ ] Static files di-host di CDN
- [ ] SSL/TLS enabled
- [ ] Error monitoring (Sentry)
- [ ] Backup strategy

## Troubleshooting
- Jika static files tidak muncul, jalankan `collectstatic`
- Untuk database issues, cek DATABASE_URL
- Untuk performance, gunakan CDN untuk static files
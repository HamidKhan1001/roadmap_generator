# Heroku Deployment Guide for Mittu Roadmap Generator

## Prerequisites

1. **Heroku CLI** - [Install here](https://devcenter.heroku.com/articles/heroku-cli)
2. **Git** - Already set up ✓
3. **Neon PostgreSQL** - Database connection string ✓
4. **GitHub** - Repository connected ✓

## Option 1: Deploy via Heroku Dashboard (Recommended)

1. Go to https://dashboard.heroku.com/apps
2. Click "New" → "Create new app"
3. Enter app name (e.g., `mittu-roadmap-api`)
4. Under "Deployment method", choose **GitHub**
5. Connect your GitHub account and select the repository
6. Go to "Settings" tab
7. Click "Reveal Config Vars" and add:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `SECRET_KEY`: A strong secret key
   - `CORS_ORIGINS`: Your frontend URL(s)
8. Under "Deployment", select "main" or "master" branch
9. Click "Enable Automatic Deploys"

## Option 2: Deploy via Heroku CLI

```bash
# Install Heroku CLI
brew install heroku

# Login to Heroku
heroku login

# Create a new app
heroku create mittu-roadmap-api

# Set environment variables
heroku config:set DATABASE_URL="postgresql://..." -a mittu-roadmap-api
heroku config:set SECRET_KEY="your-secret-key" -a mittu-roadmap-api
heroku config:set CORS_ORIGINS="https://your-vercel-app.vercel.app" -a mittu-roadmap-api

# Deploy
git push heroku master
```

## Deploy Frontend to Vercel

1. Go to https://vercel.com/import
2. Select your GitHub repository
3. Import project
4. Under "Environment Variables", add:
   - `NEXT_PUBLIC_API_URL`: Your Heroku backend URL (e.g., `https://mittu-roadmap-api.herokuapp.com`)
5. Click "Deploy"

## Troubleshooting

### "We are unable to access this connected repository"

This typically means:
1. The GitHub token/authorization is outdated
2. The app is trying to deploy code that's on a different branch
3. The repository might be private and permissions need updating

**Fix:**
- On Heroku app page, go to "Deploy" tab
- Click "Disconnect" next to your GitHub account
- Click "Connect to GitHub" again and re-authorize
- Make sure you're deploying from the correct branch (`master` or `main`)

### Database Connection Issues

Ensure your `DATABASE_URL` includes the SSL parameters from Neon:
```
postgresql://user:password@host/dbname?sslmode=require&channel_binding=require
```

## Database Schema

The app will automatically create the required tables on first run:
- `roadmap_requests` - Stores user profiles and generated roadmaps
- Indexes on email, interest, and created_at for fast queries

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/roadmap` - Generate a new roadmap
- `GET /api/roadmap/<id>` - Get saved roadmap
- `GET /api/roadmaps/recent` - List recent roadmaps
- `POST /api/roadmap/pdf` - Generate PDF from roadmap
- `GET /api/roadmap/<id>/pdf` - Download PDF of saved roadmap

## Monitoring

View logs:
```bash
heroku logs -a mittu-roadmap-api --tail
```

Check app status:
```bash
heroku apps:info -a mittu-roadmap-api
```

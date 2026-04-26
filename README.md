# Mittu Scalable

Mittu is a scalable roadmap generator MVP.

Architecture:

- `backend/` Flask API
- `frontend/` Next.js app
- MongoDB stores user profile and generated roadmap JSON
- PDF is generated on demand and not saved
- Tests are included for backend API and PDF generation

## Backend local

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

## Backend tests

```bash
cd backend
pytest
```

## Frontend local

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Deployment shape

Backend: Heroku or similar Python platform.
Frontend: Vercel.
Database: MongoDB Atlas.

Set frontend variable:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url
```

Set backend variables:

```bash
MONGO_URI=your-mongodb-atlas-uri
MONGO_DB_NAME=mittu
CORS_ORIGINS=https://your-vercel-url
SECRET_KEY=random-secret
```

# Mittu Backend

Flask API + MongoDB + on-demand PDF generation.

## Local setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

## Test

```bash
pytest
```

## API

- `GET /health`
- `GET /api/options`
- `POST /api/roadmaps`
- `GET /api/roadmaps/:id`
- `GET /api/roadmaps/:id/pdf`

## MongoDB storage

The app stores only:

- user profile input
- generated roadmap JSON
- created/updated timestamps

PDF files are not stored. They are generated when the user clicks download.

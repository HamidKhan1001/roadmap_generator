import json
import psycopg
from psycopg.rows import dict_row
from flask import current_app


def get_connection():
    database_url = current_app.config.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is missing. Add your Neon PostgreSQL connection string.")

    return psycopg.connect(
        database_url,
        row_factory=dict_row,
    )


def init_db():
    """
    Creates required tables if they do not already exist.
    Safe to call on app startup.
    """

    query = """
    CREATE TABLE IF NOT EXISTS roadmap_requests (
        id BIGSERIAL PRIMARY KEY,
        user_name VARCHAR(120) NOT NULL,
        email VARCHAR(180),
        country VARCHAR(80),
        education_level VARCHAR(120),
        current_skill_level VARCHAR(80),
        interest VARCHAR(160) NOT NULL,
        goal VARCHAR(220) NOT NULL,
        weekly_hours INTEGER NOT NULL DEFAULT 5,
        roadmap JSONB NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_roadmap_requests_email
    ON roadmap_requests(email);

    CREATE INDEX IF NOT EXISTS idx_roadmap_requests_interest
    ON roadmap_requests(interest);

    CREATE INDEX IF NOT EXISTS idx_roadmap_requests_created_at
    ON roadmap_requests(created_at DESC);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()


def save_roadmap_request(profile, roadmap):
    """
    Stores only user profile + generated roadmap JSON.
    Does NOT store generated PDF.
    """

    query = """
    INSERT INTO roadmap_requests (
        user_name,
        email,
        country,
        education_level,
        current_skill_level,
        interest,
        goal,
        weekly_hours,
        roadmap
    )
    VALUES (
        %(user_name)s,
        %(email)s,
        %(country)s,
        %(education_level)s,
        %(current_skill_level)s,
        %(interest)s,
        %(goal)s,
        %(weekly_hours)s,
        %(roadmap)s
    )
    RETURNING id, created_at;
    """

    payload = {
        "user_name": profile.get("name"),
        "email": profile.get("email"),
        "country": profile.get("country"),
        "education_level": profile.get("education_level"),
        "current_skill_level": profile.get("current_skill_level"),
        "interest": profile.get("interest"),
        "goal": profile.get("goal"),
        "weekly_hours": int(profile.get("weekly_hours", 5)),
        "roadmap": json.dumps(roadmap),
    }

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, payload)
            saved = cur.fetchone()
        conn.commit()

    return {
        "id": saved["id"],
        "created_at": saved["created_at"].isoformat(),
    }


def get_roadmap_request(request_id):
    query = """
    SELECT
        id,
        user_name,
        email,
        country,
        education_level,
        current_skill_level,
        interest,
        goal,
        weekly_hours,
        roadmap,
        created_at
    FROM roadmap_requests
    WHERE id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (request_id,))
            row = cur.fetchone()

    if not row:
        return None

    return {
        "id": row["id"],
        "profile": {
            "name": row["user_name"],
            "email": row["email"],
            "country": row["country"],
            "education_level": row["education_level"],
            "current_skill_level": row["current_skill_level"],
            "interest": row["interest"],
            "goal": row["goal"],
            "weekly_hours": row["weekly_hours"],
        },
        "roadmap": row["roadmap"],
        "created_at": row["created_at"].isoformat(),
    }


def list_recent_roadmaps(limit=20):
    query = """
    SELECT
        id,
        user_name,
        email,
        interest,
        goal,
        created_at
    FROM roadmap_requests
    ORDER BY created_at DESC
    LIMIT %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()

    return [
        {
            "id": row["id"],
            "name": row["user_name"],
            "email": row["email"],
            "interest": row["interest"],
            "goal": row["goal"],
            "created_at": row["created_at"].isoformat(),
        }
        for row in rows
    ]
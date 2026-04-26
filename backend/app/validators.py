def clean_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def validate_profile(payload):
    errors = {}
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    interest = str(payload.get("interest", "")).strip()
    level = str(payload.get("level", "beginner")).strip().lower()
    weekly_hours = payload.get("weekly_hours", 8)

    try:
        weekly_hours = int(weekly_hours)
    except (TypeError, ValueError):
        weekly_hours = 8

    if not name:
        errors["name"] = "Name is required."
    if not interest:
        errors["interest"] = "Interest is required."
    if level not in {"beginner", "intermediate", "advanced"}:
        errors["level"] = "Level must be beginner, intermediate, or advanced."
    if weekly_hours < 1 or weekly_hours > 80:
        errors["weekly_hours"] = "Weekly hours must be between 1 and 80."

    profile = {
        "name": name,
        "email": email,
        "country": str(payload.get("country", "")).strip(),
        "interest": interest,
        "goal": str(payload.get("goal", "")).strip(),
        "level": level,
        "weekly_hours": weekly_hours,
        "language_preference": str(payload.get("language_preference", "English")).strip(),
        "preferred_platforms": clean_list(payload.get("preferred_platforms")),
        "skills": clean_list(payload.get("skills")),
    }
    return profile, errors

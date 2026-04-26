def validate_profile(data):
    errors = {}

    name = str(data.get("name", "")).strip()
    interest = str(data.get("interest", "")).strip()
    goal = str(data.get("goal", "")).strip()

    try:
        weekly_hours = int(data.get("weekly_hours", 0))
    except (TypeError, ValueError):
        weekly_hours = 0

    if not name:
        errors["name"] = "Name is required."

    if not interest:
        errors["interest"] = "Interest is required."

    if not goal:
        errors["goal"] = "Goal is required."

    if weekly_hours < 1 or weekly_hours > 80:
        errors["weekly_hours"] = "Weekly hours must be between 1 and 80."

    profile = {
        "name": name,
        "email": data.get("email"),
        "country": data.get("country"),
        "interest": interest,
        "goal": goal,
        "weekly_hours": weekly_hours,
        "current_skill_level": data.get("current_skill_level"),
        "education_level": data.get("education_level"),
        "language_preference": data.get("language_preference"),
        "preferred_platforms": data.get("preferred_platforms"),
        "skills": data.get("skills"),
    }

    return profile, errors

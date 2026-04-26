import json
from pathlib import Path
from typing import Dict, List, Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tracks():
    return load_json("tracks.json")


def get_resources():
    return load_json("resources.json")


def keyword_score(text: str, keywords: List[str]) -> int:
    t = text.lower()
    return sum(1 for kw in keywords if kw.lower() in t)


def choose_track(profile: Dict[str, Any], tracks: List[Dict[str, Any]]) -> Dict[str, Any]:
    combined = " ".join([
        profile.get("interest", ""),
        profile.get("goal", ""),
        " ".join(profile.get("skills", [])),
    ]).lower()

    ranked = sorted(
        tracks,
        key=lambda track: keyword_score(combined, track.get("keywords", [])),
        reverse=True,
    )
    return ranked[0]


def estimate_duration_weeks(level: str, weekly_hours: int, track: Dict[str, Any]) -> int:
    base = int(track.get("base_weeks", 16))
    level_modifier = {"beginner": 1.25, "intermediate": 1.0, "advanced": 0.75}.get(level, 1.25)
    hours_modifier = 10 / max(weekly_hours, 1)
    weeks = round(base * level_modifier * hours_modifier)
    return max(6, min(52, weeks))


def build_phases(track: Dict[str, Any], total_weeks: int) -> List[Dict[str, Any]]:
    modules = track.get("modules", [])
    if not modules:
        return []

    phase_count = len(modules)
    weeks_per_phase = max(1, total_weeks // phase_count)
    phases = []
    start = 1

    for idx, module in enumerate(modules):
        end = total_weeks if idx == phase_count - 1 else min(total_weeks, start + weeks_per_phase - 1)
        phases.append({
            "title": module["title"],
            "weeks": f"Week {start}-{end}",
            "outcomes": module.get("outcomes", []),
            "tasks": module.get("tasks", []),
            "project": module.get("project", ""),
        })
        start = end + 1
    return phases


def match_resources(track_id: str, profile: Dict[str, Any], resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    language = profile.get("language_preference", "").lower()
    country = profile.get("country", "").lower()
    preferred = {p.lower() for p in profile.get("preferred_platforms", [])}

    filtered = [r for r in resources if track_id in r.get("tracks", []) or "all" in r.get("tracks", [])]

    def score(resource):
        s = 0
        if language and language in resource.get("language", "").lower():
            s += 3
        if country and country in [c.lower() for c in resource.get("regions", [])]:
            s += 2
        if resource.get("type", "").lower() in preferred:
            s += 2
        if resource.get("free", True):
            s += 1
        return s

    return sorted(filtered, key=score, reverse=True)[:10]


def generate_roadmap(profile: Dict[str, Any]) -> Dict[str, Any]:
    tracks = get_tracks()
    resources = get_resources()
    track = choose_track(profile, tracks)
    weeks = estimate_duration_weeks(profile["level"], profile["weekly_hours"], track)

    return {
        "track_id": track["id"],
        "track_name": track["name"],
        "summary": track["summary"],
        "duration_weeks": weeks,
        "difficulty": profile["level"],
        "weekly_hours": profile["weekly_hours"],
        "phases": build_phases(track, weeks),
        "resources": match_resources(track["id"], profile, resources),
        "portfolio_projects": track.get("portfolio_projects", []),
        "next_steps": track.get("next_steps", []),
    }

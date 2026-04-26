import json
import math
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def get_tracks():
    """Load and return all available tracks."""
    return load_json("tracks.json")


def get_resources():
    """Load and return all available resources."""
    return load_json("resources.json")


def normalize_text(value):
    if not value:
        return ""
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return str(value).strip().lower()


def tokenize(text):
    text = normalize_text(text)
    for char in [",", ".", "/", "-", "_", "|", ":", ";", "(", ")", "[", "]"]:
        text = text.replace(char, " ")
    return set(word.strip() for word in text.split() if word.strip())


def score_track(track, profile):
    interest = normalize_text(profile.get("interest"))
    goal = normalize_text(profile.get("goal"))
    skills = normalize_text(profile.get("skills"))
    level = normalize_text(profile.get("current_skill_level"))
    
    combined_text = f"{interest} {goal} {skills} {level}"
    combined_tokens = tokenize(combined_text)
    
    score = 0
    
    for keyword in track.get("keywords", []):
        keyword_clean = normalize_text(keyword)
        keyword_tokens = tokenize(keyword_clean)
        
        # Exact phrase match
        if keyword_clean and keyword_clean in combined_text:
            score += 10
        
        # Token subset match
        if keyword_tokens and keyword_tokens.issubset(combined_tokens):
            score += 6
        
        # Partial overlap
        overlap = combined_tokens.intersection(keyword_tokens)
        score += len(overlap) * 2
    
    title_tokens = tokenize(track.get("title", ""))
    score += len(combined_tokens.intersection(title_tokens)) * 2
    
    return score


def choose_track(profile):
    tracks = load_json("tracks.json")
    scored_tracks = []
    
    for track in tracks:
        scored_tracks.append({
            "track": track,
            "score": score_track(track, profile)
        })
    
    scored_tracks.sort(key=lambda item: item["score"], reverse=True)
    best = scored_tracks[0]
    
    if best["score"] <= 0:
        return get_default_track(tracks, profile)
    
    return best["track"]


def get_default_track(tracks, profile):
    skills = normalize_text(profile.get("skills"))
    interest = normalize_text(profile.get("interest"))
    goal = normalize_text(profile.get("goal"))
    combined = f"{skills} {interest} {goal}"
    
    if "excel" in combined or "data" in combined:
        return find_track_by_id(tracks, "data_analyst")
    if "editing" in combined or "video" in combined or "youtube" in combined:
        return find_track_by_id(tracks, "video_content_creator")
    if "python" in combined:
        return find_track_by_id(tracks, "python_backend")
    
    return find_track_by_id(tracks, "ai_ml_engineer")


def find_track_by_id(tracks, track_id):
    for track in tracks:
        if track.get("id") == track_id:
            return track
    return tracks[0]


def get_duration_weeks(track, profile):
    base_weeks = int(track.get("base_duration_weeks", 24))
    weekly_hours = int(profile.get("weekly_hours", 6))
    level = normalize_text(profile.get("current_skill_level"))
    
    if weekly_hours <= 4:
        base_weeks = math.ceil(base_weeks * 1.4)
    elif weekly_hours >= 10:
        base_weeks = math.ceil(base_weeks * 0.8)
    
    if level in ["absolute beginner", "beginner", "new"]:
        base_weeks = math.ceil(base_weeks * 1.15)
    elif level in ["intermediate", "medium"]:
        base_weeks = math.ceil(base_weeks * 0.9)
    elif level in ["advanced"]:
        base_weeks = math.ceil(base_weeks * 0.75)
    
    return max(base_weeks, 8)


def filter_resources_for_track(track_id, profile):
    resources = load_json("resources.json")
    
    preferred_platforms = profile.get("preferred_platforms") or []
    language_preference = normalize_text(profile.get("language_preference"))
    country = normalize_text(profile.get("country"))
    
    if isinstance(preferred_platforms, str):
        preferred_platforms = [
            item.strip().lower()
            for item in preferred_platforms.split(",")
            if item.strip()
        ]
    
    track_resources = [
        resource for resource in resources
        if resource.get("track_id") == track_id
    ]
    
    def resource_score(resource):
        score = 0
        platform = normalize_text(resource.get("platform"))
        region = normalize_text(resource.get("region"))
        language = normalize_text(resource.get("language"))
        
        if platform in preferred_platforms:
            score += 5
        if country in ["pakistan", "india"] and region == "india_pakistan":
            score += 4
        if "urdu" in language_preference or "hindi" in language_preference:
            if "urdu" in language or "hindi" in language:
                score += 4
        if language == "english":
            score += 1
        
        return score
    
    track_resources.sort(key=resource_score, reverse=True)
    return track_resources[:8]


def build_phases(track, total_weeks):
    phases = []
    current_week = 1
    
    for index, phase in enumerate(track.get("phases", [])):
        if index == len(track["phases"]) - 1:
            end_week = total_weeks
        else:
            phase_weeks = max(1, round(total_weeks * float(phase.get("weight", 0.25))))
            end_week = min(total_weeks, current_week + phase_weeks - 1)
        
        phases.append({
            "title": phase["title"],
            "weeks": f"{current_week}-{end_week}",
            "outcomes": phase.get("topics", []),
            "project": phase.get("projects", [])
        })
        
        current_week = end_week + 1
    
    return phases


def generate_roadmap(profile):
    track = choose_track(profile)
    duration_weeks = get_duration_weeks(track, profile)
    
    return {
        "track_id": track["id"],
        "track_name": track["title"],
        "track": track["title"],
        "summary": track["summary"],
        "duration_weeks": duration_weeks,
        "weekly_hours": int(profile.get("weekly_hours", 6)),
        "phases": build_phases(track, duration_weeks),
        "resources": filter_resources_for_track(track["id"], profile)
    }

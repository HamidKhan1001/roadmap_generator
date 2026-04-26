def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["database"] == "postgresql"


def test_create_roadmap(client):
    payload = {
        "name": "Hamid",
        "email": "hamid@example.com",
        "country": "Pakistan",
        "education_level": "Bachelor",
        "current_skill_level": "Beginner",
        "interest": "Artificial Intelligence",
        "goal": "Become an AI Engineer",
        "weekly_hours": 8
    }

    response = client.post("/api/roadmap", json=payload)

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert "request_id" in data
    assert "roadmap" in data
    assert data["profile"]["name"] == "Hamid"


def test_create_roadmap_validation_error(client):
    payload = {
        "name": "",
        "interest": "",
        "goal": "",
        "weekly_hours": 0
    }

    response = client.post("/api/roadmap", json=payload)

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert "errors" in data


def test_download_pdf_from_payload(client):
    payload = {
        "profile": {
            "name": "Hamid",
            "email": "hamid@example.com",
            "country": "Pakistan",
            "education_level": "Bachelor",
            "current_skill_level": "Beginner",
            "interest": "Python",
            "goal": "Become a Backend Developer",
            "weekly_hours": 6
        },
        "roadmap": {
            "track": "Python Backend Developer",
            "duration": "12 weeks",
            "summary": "Learn Python, Flask, APIs, databases, and deployment.",
            "phases": [
                {
                    "title": "Python Basics",
                    "weeks": "1-2",
                    "topics": ["Syntax", "Functions", "OOP"],
                    "resources": [
                        {
                            "title": "Python Docs",
                            "url": "https://docs.python.org/3/tutorial/",
                            "platform": "Documentation"
                        }
                    ]
                }
            ]
        }
    }

    response = client.post("/api/roadmap/pdf", json=payload)

    assert response.status_code == 200
    assert response.content_type == "application/pdf"


def test_quant_interest_generates_quant_roadmap(client):
    payload = {
        "name": "Hamid",
        "email": "hamid@example.com",
        "country": "Pakistan",
        "education_level": "Bachelor",
        "current_skill_level": "beginner",
        "interest": "quant",
        "goal": "Job",
        "weekly_hours": 8,
        "language_preference": "Urdu/Hindi",
        "skills": "python basics, editing, excel",
        "preferred_platforms": ["youtube", "docs", "course", "practice"]
    }

    response = client.post("/api/roadmap", json=payload)

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert data["roadmap"]["track_id"] == "quant_finance"
    assert "Quant" in data["roadmap"]["track"]
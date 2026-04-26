from flask import Blueprint, jsonify, request, send_file
from io import BytesIO

from app.validators import validate_profile
from app.roadmap_engine import generate_roadmap, get_tracks, get_resources
from app.pdf_service import generate_roadmap_pdf
from app.db import (
    save_roadmap_request,
    get_roadmap_request,
    list_recent_roadmaps,
)

api = Blueprint("api", __name__)


@api.get("/health")
def health_check():
    return jsonify({
        "status": "ok",
        "service": "Mittu API",
        "database": "postgresql"
    })


@api.get("/options")
def get_options():
    """Returns available options for the roadmap generator form."""
    tracks = get_tracks()
    resources = get_resources()
    
    return jsonify({
        "success": True,
        "tracks": [{"name": t.get("name"), "keywords": t.get("keywords")} for t in tracks],
        "resources": resources,
    })


@api.post("/roadmap")
def create_roadmap():
    data = request.get_json(silent=True) or {}

    profile, errors = validate_profile(data)

    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    roadmap = generate_roadmap(profile)

    saved = save_roadmap_request(
        profile=profile,
        roadmap=roadmap,
    )

    return jsonify({
        "success": True,
        "request_id": saved["id"],
        "created_at": saved["created_at"],
        "profile": profile,
        "roadmap": roadmap,
    }), 201


@api.post("/roadmaps")
def create_roadmap_v2():
    """Alias for /roadmap endpoint - for frontend compatibility."""
    return create_roadmap()


@api.get("/roadmap/<int:request_id>")
def get_saved_roadmap(request_id):
    saved = get_roadmap_request(request_id)

    if not saved:
        return jsonify({
            "success": False,
            "error": "Roadmap not found"
        }), 404

    return jsonify({
        "success": True,
        **saved
    })


@api.get("/roadmaps/recent")
def get_recent_roadmaps():
    limit = request.args.get("limit", 20, type=int)

    if limit > 100:
        limit = 100

    roadmaps = list_recent_roadmaps(limit=limit)

    return jsonify({
        "success": True,
        "items": roadmaps,
    })


@api.post("/roadmap/pdf")
def download_pdf_from_payload():
    """
    Generates PDF from frontend payload.
    Does not save PDF.
    """

    data = request.get_json(silent=True) or {}

    profile = data.get("profile")
    roadmap = data.get("roadmap")

    if not profile or not roadmap:
        return jsonify({
            "success": False,
            "error": "profile and roadmap are required"
        }), 400

    pdf_bytes = generate_roadmap_pdf(profile, roadmap)

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="mittu-roadmap.pdf",
    )


@api.get("/roadmap/<int:request_id>/pdf")
def download_pdf_from_saved_roadmap(request_id):
    """
    Fetches saved roadmap JSON from PostgreSQL and generates PDF on demand.
    PDF is not stored.
    """

    saved = get_roadmap_request(request_id)

    if not saved:
        return jsonify({
            "success": False,
            "error": "Roadmap not found"
        }), 404

    pdf_bytes = generate_roadmap_pdf(
        profile=saved["profile"],
        roadmap=saved["roadmap"],
    )

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"mittu-roadmap-{request_id}.pdf",
    )
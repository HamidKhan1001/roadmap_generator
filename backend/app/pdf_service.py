from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch


def bullet_list(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(str(item), styles["BodyText"])) for item in items],
        bulletType="bullet",
        leftIndent=18,
    )


def generate_roadmap_pdf(profile, roadmap):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="MittuTitle", parent=styles["Title"], fontSize=22, spaceAfter=14))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], spaceBefore=12, spaceAfter=8))

    story = []
    story.append(Paragraph("Mittu Personalized Roadmap", styles["MittuTitle"]))
    story.append(Paragraph(f"Created for: {profile.get('name', 'Learner')}", styles["BodyText"]))
    story.append(Paragraph(f"Track: {roadmap['track_name']} | Duration: {roadmap['duration_weeks']} weeks", styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Summary", styles["Section"]))
    story.append(Paragraph(roadmap.get("summary", ""), styles["BodyText"]))

    story.append(Paragraph("Roadmap Phases", styles["Section"]))
    for phase in roadmap.get("phases", []):
        story.append(Paragraph(f"<b>{phase['weeks']}: {phase['title']}</b>", styles["BodyText"]))
        if phase.get("outcomes"):
            story.append(bullet_list(phase["outcomes"], styles))
        if phase.get("project"):
            story.append(Paragraph(f"Project: {phase['project']}", styles["BodyText"]))
        story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("Recommended Resources", styles["Section"]))
    for r in roadmap.get("resources", []):
        text = f"<b>{r['title']}</b> ({r['type']}) - {r['url']}"
        story.append(Paragraph(text, styles["BodyText"]))

    story.append(Paragraph("Portfolio Projects", styles["Section"]))
    story.append(bullet_list(roadmap.get("portfolio_projects", []), styles))

    story.append(Paragraph("Next Steps", styles["Section"]))
    story.append(bullet_list(roadmap.get("next_steps", []), styles))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

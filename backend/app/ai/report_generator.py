from datetime import datetime, timezone
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_pdf_report(
    output_path: str,
    *,
    title: str,
    text: str,
    prediction: dict[str, Any],
    analysis: dict[str, Any],
) -> str:
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("TruthLens AI Analysis Report", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"<b>Title:</b> {title}", styles["Normal"]))
    story.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("<b>Prediction Result</b>", styles["Heading2"]))
    result_data = [
        ["Label", prediction.get("label_name", "N/A")],
        ["Confidence", f"{prediction.get('confidence', 0) * 100:.2f}%"],
        ["Source", prediction.get("source", "manual")],
    ]
    result_table = Table(result_data, colWidths=[2 * inch, 4 * inch])
    result_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    story.append(result_table)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("<b>Article Text</b>", styles["Heading2"]))
    truncated = text[:3000] + ("..." if len(text) > 3000 else "")
    story.append(Paragraph(truncated.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    ai = analysis.get("ai", {})
    if ai:
        story.append(Paragraph("<b>AI Analysis</b>", styles["Heading2"]))
        if ai.get("summary"):
            story.append(Paragraph(f"<b>Summary:</b> {ai['summary']}", styles["Normal"]))
        if ai.get("credibility_score"):
            cred = ai["credibility_score"]
            story.append(
                Paragraph(
                    f"<b>Credibility:</b> {cred.get('rating', 'N/A')} ({cred.get('score', 0):.2f})",
                    styles["Normal"],
                )
            )
        if ai.get("sentiment"):
            sent = ai["sentiment"]
            story.append(
                Paragraph(
                    f"<b>Sentiment:</b> {sent.get('label', 'neutral')}",
                    styles["Normal"],
                )
            )

    doc.build(story)
    return output_path


def build_report_content(
    *,
    text: str,
    prediction: dict[str, Any],
    analysis: dict[str, Any],
) -> dict[str, Any]:
    return {
        "text_preview": text[:500],
        "prediction": {
            "label": prediction.get("label"),
            "label_name": prediction.get("label_name"),
            "confidence": prediction.get("confidence"),
        },
        "analysis": analysis,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

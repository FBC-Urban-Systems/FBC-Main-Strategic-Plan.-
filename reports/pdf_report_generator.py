# ==========================================
# PATH: /reports/pdf_report_generator.py
# DESCRIPTION: Automatic PDF Report Generator
# VERSION: v1.0.0-PHASE-III
# ==========================================

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

def generate_fbc_report(report_title: str, report_data: dict, output_path: str):
    """
    Generates a professional PDF report from any engine output.
    """

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    body_style = styles["BodyText"]

    elements = []

    # Title
    elements.append(Paragraph("FBC DIGITAL SYSTEMS", title_style))
    elements.append(Paragraph(report_title, styles["Heading2"]))
    elements.append(Spacer(1, 20))

    # Date
    elements.append(Paragraph(f"Report Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", body_style))
    elements.append(Spacer(1, 20))

    # Data Section
    for key, value in report_data.items():
        line = f"<b>{key}:</b> {value}"
        elements.append(Paragraph(line, body_style))
        elements.append(Spacer(1, 10))

    # Footer
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("© FBC Digital Systems – Urban Intelligence Platform", styles["Italic"]))

    doc.build(elements)

    return {
        "status": "PDF Report Generated",
        "path": output_path
    }

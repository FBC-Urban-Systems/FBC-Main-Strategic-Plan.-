# ==========================================
# PATH: /reports/pdf_report_generator.py
# DESCRIPTION: Unified PDF Report Generator for FBC Engines
# VERSION: v2.0.0 — PRODUCTION SAFE • FUTURE READY
# ROLE: Official Reporting & Export Layer
# ==========================================

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from datetime import datetime
from typing import Dict, Any
import os


def generate_fbc_report(
    report_title: str,
    report_data: Dict[str, Any],
    output_path: str
) -> Dict[str, str]:
    """
    Generates a professional, audit-safe PDF report
    from any FBC engine output.

    Parameters
    ----------
    report_title : str
        Title displayed on the report
    report_data : dict
        Key-value data produced by FBC engines
    output_path : str
        Absolute or relative path to output PDF

    Returns
    -------
    dict
        Status and generated file path
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=25 * mm,
        leftMargin=25 * mm,
        topMargin=30 * mm,
        bottomMargin=25 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "FBC_Title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        "FBC_Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        spaceAfter=20
    )

    body_style = ParagraphStyle(
        "FBC_Body",
        parent=styles["BodyText"],
        spaceAfter=8
    )

    footer_style = ParagraphStyle(
        "FBC_Footer",
        parent=styles["Italic"],
        alignment=TA_CENTER,
        spaceBefore=30
    )

    elements = []

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    elements.append(Paragraph("FBC DIGITAL SYSTEMS", title_style))
    elements.append(Paragraph(report_title, subtitle_style))

    elements.append(
        Paragraph(
            f"Report Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            body_style
        )
    )
    elements.append(Spacer(1, 20))

    # --------------------------------------------------
    # DATA SECTION
    # --------------------------------------------------
    for key, value in report_data.items():
        safe_key = str(key).replace("_", " ").title()
        safe_value = "N/A" if value is None else str(value)

        line = f"<b>{safe_key}:</b> {safe_value}"
        elements.append(Paragraph(line, body_style))

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------
    elements.append(Spacer(1, 20))
    elements.append(
        Paragraph(
            "© FBC Digital Systems — Urban Intelligence Platform",
            footer_style
        )
    )

    doc.build(elements)

    return {
        "status": "PDF_REPORT_GENERATED",
        "path": output_path
    }

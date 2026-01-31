# ==========================================
# PATH: reports/pdf_report_generator.py
# DESCRIPTION: Unified PDF Report Generator for FBC Engines
# VERSION: v3.0.0-SUPREME — ENTERPRISE • AUDIT • CI SAFE
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


# --------------------------------------------------
# CORE PUBLIC API (DO NOT BREAK)
# --------------------------------------------------
def generate_fbc_report(
    report_title: str,
    report_data: Dict[str, Any],
    output_path: str = "reports/output/fbc_report.pdf"
) -> Dict[str, str]:
    """
    Generates an enterprise-grade, audit-safe PDF report.

    ✔ CI-safe
    ✔ Backward-compatible
    ✔ Real timestamps
    ✔ Future-ready formatting

    Parameters
    ----------
    report_title : str
        Human-readable report title
    report_data : dict
        Engine output (key-value)
    output_path : str
        Target PDF path (optional)

    Returns
    -------
    dict
        Generation status and file path
    """

    # -----------------------------
    # SAFE PATH HANDLING
    # -----------------------------
    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------
    # DOCUMENT CONFIG
    # -----------------------------
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
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        "FBC_Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        spaceAfter=16
    )

    body_style = ParagraphStyle(
        "FBC_Body",
        parent=styles["BodyText"],
        spaceAfter=6
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
            f"Generated (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
            body_style
        )
    )

    elements.append(Spacer(1, 18))

    # --------------------------------------------------
    # DATA SECTION (DEFENSIVE & AUDIT SAFE)
    # --------------------------------------------------
    if not isinstance(report_data, dict) or not report_data:
        elements.append(
            Paragraph(
                "<b>Status:</b> No reportable data available",
                body_style
            )
        )
    else:
        for key, value in report_data.items():
            safe_key = str(key).replace("_", " ").title()
            safe_value = "N/A" if value is None else str(value)

            line = f"<b>{safe_key}:</b> {safe_value}"
            elements.append(Paragraph(line, body_style))

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------
    elements.append(Spacer(1, 22))
    elements.append(
        Paragraph(
            "© FBC Digital Systems — Urban Intelligence Platform",
            footer_style
        )
    )

    # -----------------------------
    # BUILD DOCUMENT
    # -----------------------------
    doc.build(elements)

    return {
        "status": "PDF_REPORT_GENERATED",
        "path": output_path
    }


# --------------------------------------------------
# STANDALONE SUPREME TEST (CI SAFE)
# --------------------------------------------------
if __name__ == "__main__":
    sample_report = {
        "city": "AuditCity",
        "engine": "Energy Forecast",
        "confidence": "HIGH",
        "generated_by": "FBC SUPREME CI"
    }

    result = generate_fbc_report(
        "FBC SYSTEM AUDIT REPORT",
        sample_report
    )

    print("\n--- FBC PDF REPORT GENERATED ---")
    print(result)
    print("--- REPORTING ENGINE OPERATIONAL ✅ ---\n")

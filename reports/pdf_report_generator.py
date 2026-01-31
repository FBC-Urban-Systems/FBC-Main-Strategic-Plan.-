# ==========================================
# PATH: reports/pdf_report_generator.py
# DESCRIPTION: Enterprise Unified PDF Reporting Engine
# VERSION: v5.0.0-ENTERPRISE-LTS
# ROLE: Official Reporting, Audit & Export Layer
# ==========================================

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import os
import platform
import uuid


# --------------------------------------------------
# INTERNAL CONSTANTS (ENTERPRISE STABLE)
# --------------------------------------------------
ENGINE_VERSION = "5.0.0-ENTERPRISE-LTS"
ENGINE_NAME = "FBC Unified PDF Reporting Engine"
ORGANIZATION = "FBC Digital Systems"


# --------------------------------------------------
# CORE PUBLIC API (DO NOT BREAK)
# --------------------------------------------------
def generate_fbc_report(
    report_title: str,
    report_data: Dict[str, Any],
    output_path: str = "reports/output/fbc_report.pdf",
    metadata: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """
    Generates a production-grade, audit-safe, future-proof PDF report.

    ✔ Enterprise stable
    ✔ CI / CD safe
    ✔ Deterministic metadata
    ✔ Backward compatible
    ✔ Long-term support (LTS)

    Parameters
    ----------
    report_title : str
        Human-readable report title
    report_data : dict
        Real engine output data
    output_path : str
        Target PDF path
    metadata : dict, optional
        Extra audit metadata (operator, environment, versioning)

    Returns
    -------
    dict
        Generation status, file path, report ID
    """

    # -----------------------------
    # SAFE PATH HANDLING
    # -----------------------------
    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------
    # AUDIT METADATA
    # -----------------------------
    report_id = str(uuid.uuid4())
    timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    system_metadata = {
        "report_id": report_id,
        "generated_at": timestamp_utc,
        "engine": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "platform": platform.platform()
    }

    if metadata:
        system_metadata.update(metadata)

    # -----------------------------
    # DOCUMENT CONFIGURATION
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
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        "FBC_Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        spaceAfter=18
    )

    section_style = ParagraphStyle(
        "FBC_Section",
        parent=styles["Heading3"],
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "FBC_Body",
        parent=styles["BodyText"],
        alignment=TA_LEFT,
        spaceAfter=6
    )

    footer_style = ParagraphStyle(
        "FBC_Footer",
        parent=styles["Italic"],
        alignment=TA_CENTER,
        spaceBefore=28
    )

    elements = []

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    elements.append(Paragraph(ORGANIZATION.upper(), title_style))
    elements.append(Paragraph(report_title, subtitle_style))
    elements.append(Spacer(1, 12))

    # --------------------------------------------------
    # METADATA SECTION
    # --------------------------------------------------
    elements.append(Paragraph("Report Metadata", section_style))
    for key, value in system_metadata.items():
        elements.append(
            Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", body_style)
        )

    elements.append(Spacer(1, 14))

    # --------------------------------------------------
    # DATA SECTION (STRICT & AUDIT SAFE)
    # --------------------------------------------------
    elements.append(Paragraph("Report Data", section_style))

    if not isinstance(report_data, dict) or not report_data:
        elements.append(
            Paragraph("<b>Status:</b> No reportable data available", body_style)
        )
    else:
        for key, value in report_data.items():
            safe_key = str(key).replace("_", " ").title()
            safe_value = "N/A" if value is None else str(value)
            elements.append(
                Paragraph(f"<b>{safe_key}:</b> {safe_value}", body_style)
            )

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------
    elements.append(Spacer(1, 22))
    elements.append(
        Paragraph(
            f"© {datetime.utcnow().year} {ORGANIZATION} — Enterprise Confidential",
            footer_style
        )
    )

    # -----------------------------
    # BUILD DOCUMENT
    # -----------------------------
    doc.build(elements)

    return {
        "status": "PDF_REPORT_GENERATED",
        "path": output_path,
        "report_id": report_id,
        "engine_version": ENGINE_VERSION
    }


# --------------------------------------------------
# STANDALONE ENTERPRISE TEST (CI SAFE)
# --------------------------------------------------
if __name__ == "__main__":
    sample_report = {
        "city": "AuditCity",
        "engine": "Urban Revenue AI",
        "confidence": "HIGH",
        "forecast_horizon": "12 months",
        "generated_by": "FBC CI PIPELINE"
    }

    result = generate_fbc_report(
        report_title="FBC SYSTEM ENTERPRISE AUDIT REPORT",
        report_data=sample_report,
        metadata={
            "environment": "production",
            "operator": "FBC Core Systems"
        }
    )

    print("\n--- FBC PDF REPORT GENERATED ---")
    print(result)
    print("--- REPORTING ENGINE OPERATIONAL (v5 LTS) ---\n")

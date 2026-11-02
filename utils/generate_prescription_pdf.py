"""
Agri-Clinic Field Prescription & Yield Report PDF Generator.
Builds a professional diagnostic prescription and yield report using ReportLab.
"""

import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage
)


def create_prescription_pdf(
    disease_result: dict,
    yield_result: dict,
    farmer_name: str = "Lead Farm Operator",
    field_location: str = "Agricultural Parcel Block-A"
) -> bytes:
    """
    Generate an in-memory PDF prescription and return bytes for Streamlit download.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0c4a6e")   # Deep navy
    ACCENT = colors.HexColor("#0284c7")    # Sky blue
    DANGER = colors.HexColor("#b91c1c")    # Crimson red
    BORDER = colors.HexColor("#cbd5e1")
    BG_LIGHT = colors.HexColor("#f0fdf4")
    
    title_style = ParagraphStyle(
        "PrescTitle",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=PRIMARY
    )
    
    h2_style = ParagraphStyle(
        "PrescH2",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        "PrescBody",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )
    
    bold_style = ParagraphStyle(
        "PrescBold",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=PRIMARY
    )

    story = []
    
    # Header Banner
    story.append(Paragraph("AgriVision AI — Diagnostic Prescription & Harvest Forecast", title_style))
    story.append(Paragraph("<b>Certified Precision Agriculture Field Advisory</b> | Issue Date: " + datetime.now().strftime("%d %b %Y %H:%M"), body_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceBefore=6, spaceAfter=10))
    
    # Farm & Dossier Info
    meta_table = [
        [
            Paragraph(f"<b>Operator / Farmer:</b> {farmer_name}", body_style),
            Paragraph(f"<b>Crop Variety:</b> {disease_result.get('crop', yield_result.get('crop', 'Crop'))}", bold_style)
        ],
        [
            Paragraph(f"<b>Field Location:</b> {field_location}", body_style),
            Paragraph(f"<b>Farm Parcel Area:</b> {yield_result.get('area_hectares', 'N/A')} Hectares ({yield_result.get('area_acres', 'N/A')} Acres)", body_style)
        ]
    ]
    t_meta = Table(meta_table, colWidths=[260, 272])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    # Section 1: Phytopathological Diagnosis
    story.append(Paragraph("1. Phytopathological Disease Findings", h2_style))
    diag_rows = [
        [Paragraph("Parameter", bold_style), Paragraph("Diagnostic Assessment", bold_style)],
        [Paragraph("Detected Condition", body_style), Paragraph(f"<b>{disease_result.get('disease_name', 'N/A')}</b>", bold_style)],
        [Paragraph("Causal Pathogen", body_style), Paragraph(f"<i>{disease_result.get('pathogen', 'N/A')}</i> ({disease_result.get('pathogen_type', 'N/A')})", body_style)],
        [Paragraph("Infection Severity Index", body_style), Paragraph(f"<b>{disease_result.get('infection_area_pct', 0)}%</b> foliage infected ({disease_result.get('severity_tier', 'N/A')})", body_style)],
        [Paragraph("Diagnostic Confidence", body_style), Paragraph(f"{disease_result.get('confidence_pct', 0)}% (Vision AI Signal)", body_style)],
        [Paragraph("Key Observed Symptoms", body_style), Paragraph(disease_result.get("symptoms", "N/A"), body_style)]
    ]
    t_diag = Table(diag_rows, colWidths=[160, 372])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_diag)
    story.append(Spacer(1, 10))
    
    # Section 2: Chemical & Biological Prescription
    story.append(Paragraph("2. Agronomic Treatment Protocol & Chemical Prescription", h2_style))
    
    chem_list = disease_result.get("chemical_treatment", [])
    chem_str = "<br/>• ".join(chem_list) if chem_list else "None required."
    
    org_list = disease_result.get("organic_control", [])
    org_str = "<br/>• ".join(org_list) if org_list else "None required."
    
    prev_list = disease_result.get("prevention", [])
    prev_str = "<br/>• ".join(prev_list) if prev_list else "Standard sanitation."
    
    rx_rows = [
        [Paragraph("Prescription Category", bold_style), Paragraph("Recommended Action & Dosage", bold_style)],
        [Paragraph("<b>Immediate Chemical Intervention (Fungicide / Bactericide)</b>", body_style), Paragraph(f"• {chem_str}", body_style)],
        [Paragraph("<b>Biological & Organic Alternative</b>", body_style), Paragraph(f"• {org_str}", body_style)],
        [Paragraph("<b>Preventative Cultural Practices</b>", body_style), Paragraph(f"• {prev_str}", body_style)]
    ]
    t_rx = Table(rx_rows, colWidths=[180, 352])
    t_rx.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_rx)
    story.append(Spacer(1, 10))
    
    # Section 3: Yield Estimation & Harvest Forecast
    story.append(Paragraph("3. Harvest Yield Forecast & Economic Projection", h2_style))
    
    yield_rows = [
        [Paragraph("Yield Metric", bold_style), Paragraph("Model Forecast Value", bold_style)],
        [Paragraph("Predicted Crop Yield", body_style), Paragraph(f"<b>{yield_result.get('predicted_yield_ton_ha', 'N/A')} Metric Tons / Hectare</b> ({yield_result.get('predicted_yield_quintal_ha', 'N/A')} Quintals/ha)", body_style)],
        [Paragraph("Gross Farm Production", body_style), Paragraph(f"<b>{yield_result.get('total_production_ton', 'N/A')} Metric Tons</b> ({yield_result.get('total_production_quintals', 'N/A')} Quintals)", body_style)],
        [Paragraph("Baseline Yield Efficiency", body_style), Paragraph(f"{yield_result.get('efficiency_percentage', 'N/A')}% of maximum genetic potential", body_style)],
        [Paragraph("Estimated Market Valuation", body_style), Paragraph(f"<b>₹ {yield_result.get('estimated_revenue_inr', 0):,.0f}</b> (Calculated at MSP ₹{yield_result.get('msp_per_ton', 0):,}/ton)", bold_style)]
    ]
    t_yield = Table(yield_rows, colWidths=[180, 352])
    t_yield.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BG_LIGHT, colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_yield)
    story.append(Spacer(1, 12))
    
    # Footer Notice
    story.append(Paragraph(
        "<i>Disclaimer: This field prescription is generated by AgriVision AI for advisory decision-support. Always verify field weather conditions and adhere to pesticide manufacturer safety labels before large-scale spray operations.</i>",
        ParagraphStyle("Disc", fontName="Helvetica-Oblique", fontSize=7.5, leading=10, textColor=colors.HexColor("#64748b"))
    ))
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

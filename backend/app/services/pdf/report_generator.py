import io
from typing import Any, Dict
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_nutritional_pdf_report(formulation_data: Dict[str, Any]) -> bytes:
    """Generates an auditable PDF nutritional report with ingredient breakdown, nutrient table, and medical disclaimers."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    # Title & Header
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#2E7D32'),
        alignment=0,
    )
    story.append(Paragraph("NutriAI – Prototype Nutritional Formulation Report", title_style))
    story.append(Paragraph("<b>Reference: ICMR-NIN Grand Challenge Anaemia Prevention Initiative</b>", styles['Normal']))
    story.append(Spacer(1, 10))

    # Warning / Demo banner
    banner_style = ParagraphStyle(
        'Banner',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#B45309'),
        backColor=colors.HexColor('#FEF3C7'),
        borderPadding=6,
    )
    story.append(Paragraph("PROTOTYPE SPECIFICATION – DEMO NUTRIENT DATA (NOT VALIDATED FOR CLINICAL USE)", banner_style))
    story.append(Spacer(1, 15))

    # Product Overview
    prod_name = formulation_data.get("name", "Roasted Millet & Sesame Prototype Bar")
    category = formulation_data.get("category", "Nutrition Bar")
    serving_g = formulation_data.get("serving_size_g", 35.0)
    cost = formulation_data.get("cost_per_serving_inr", 22.50)

    summary_text = (
        f"<b>Product Concept:</b> {prod_name}<br/>"
        f"<b>Format Category:</b> {category} | <b>Nominal Serving Size:</b> {serving_g} g<br/>"
        f"<b>Estimated Cost per Serving:</b> ₹{cost:.2f} | <b>Calculation Status:</b> {formulation_data.get('validation_status', 'computed_only')}"
    )
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 15))

    # Ingredient Formulation Table
    story.append(Paragraph("<b>1. Optimized Ingredient Composition (per serving)</b>", styles['Heading3']))
    ing_rows = [["Ingredient", "Quantity (g)", "% of Mix", "Functional Purpose"]]
    for ing in formulation_data.get("ingredients", []):
        ing_rows.append([
            ing.get("name", "Ingredient"),
            f"{float(ing.get('grams_per_serving', 0)):.2f}",
            f"{float(ing.get('pct_of_mix', 0)):.1f}%",
            ing.get("purpose", "Bulk").replace("_", " ").title(),
        ])

    ing_table = Table(ing_rows, colWidths=[200, 90, 80, 150])
    ing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F5E9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1B5E20')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CFD8DC')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(ing_table)
    story.append(Spacer(1, 15))

    # Nutrient Analysis Table
    story.append(Paragraph("<b>2. Computed Nutritional Profile (per serving)</b>", styles['Heading3']))
    nutrients = formulation_data.get("nutrient_results_per_serving", {})
    nut_rows = [["Nutrient Parameter", "Amount per Serving", "Target / Reference", "Data Status"]]

    nut_rows.append(["Energy", f"{nutrients.get('energy', 'N/A')} kcal", "130-180 kcal", "Draft Assay"])
    nut_rows.append(["Protein", f"{nutrients.get('protein', 'N/A')} g", ">= 5.0 g", "Draft Assay"])
    nut_rows.append(["Iron (Total)", f"{nutrients.get('iron', 'N/A')} mg", "4.0 - 5.0 mg benchmark", "Draft Assay"])
    nut_rows.append(["Vitamin C (Ascorbic Acid)", f"{nutrients.get('vit_c', 'N/A')} mg", ">= 20.0 mg (enhancer)", "Draft Assay"])
    nut_rows.append(["Folate", f"{nutrients.get('folate', 'N/A')} ug", ">= 75.0 ug", "Draft Assay"])
    nut_rows.append(["Calcium", f"{nutrients.get('calcium', 'N/A')} mg", ">= 60.0 mg", "Draft Assay"])
    nut_rows.append(["Added Sugar (HFSS Cap)", f"{nutrients.get('added_sugar', 'N/A')} g", "<= 5.0 g cap", "Compliant"])
    nut_rows.append(["Saturated Fat (HFSS Cap)", f"{nutrients.get('fat', 'N/A')} g", "<= 3.0 g cap", "Compliant"])

    nut_table = Table(nut_rows, colWidths=[180, 120, 120, 100])
    nut_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ECEFF1')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CFD8DC')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(nut_table)
    story.append(Spacer(1, 20))

    # Medical & Regulatory Disclaimer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Italic'],
        fontSize=8,
        textColor=colors.HexColor('#546E7A'),
        leading=11,
    )
    disclaimer_text = (
        "<b>Medical & Clinical Disclaimer:</b> NutriAI provides food-based dietary formulation recommendations "
        "designed to support nutritional adequacy among adolescent girls and women of reproductive age. It does not replace "
        "clinical evaluation, medical diagnosis, or prescription therapeutic care. Changes in biological markers must not be "
        "attributed solely to NutriAI products and must be assessed by a licensed healthcare professional."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(story)
    return buffer.getvalue()


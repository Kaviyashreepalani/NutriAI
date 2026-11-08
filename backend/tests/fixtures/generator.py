"""Generates synthetic sample laboratory report PDFs labelled 'SYNTHETIC SAMPLE' for testing."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_synthetic_pdf(filepath: str, patient_info: dict, test_rows: list):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Banner
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#2E7D32'),
        alignment=1,
    )
    story.append(Paragraph("METROPOLIS CLINICAL LABS - SYNTHETIC SAMPLE", title_style))
    story.append(Paragraph("<b>Notice: FOR DEMO AND VALIDATION TESTING ONLY</b>", styles['Normal']))
    story.append(Spacer(1, 15))

    # Patient info
    patient_text = f"<b>Patient:</b> {patient_info.get('name')} | <b>Age:</b> {patient_info.get('age')} | <b>Sex:</b> {patient_info.get('sex')}<br/>" \
                   f"<b>Sample Date:</b> 15/10/2026 | <b>Lab Ref:</b> {patient_info.get('ref_id', 'SYN-99882')}"
    story.append(Paragraph(patient_text, styles['Normal']))
    story.append(Spacer(1, 15))

    # Table data
    data = [["Test Description", "Observed Value", "Standard Unit", "Biological Reference Range"]]
    for row in test_rows:
        data.append([row[0], str(row[1]), row[2], row[3]])

    t = Table(data, colWidths=[200, 100, 100, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F8E9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1B5E20')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CFD8DC')),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<i>End of laboratory examination report. Formulated strictly for test suite verification.</i>", styles['Italic']))

    doc.build(story)


def generate_all_fixtures():
    fixtures_dir = os.path.join(os.path.dirname(__file__))

    # Fixture 1: 16-year-old adolescent with mild iron deficiency
    create_synthetic_pdf(
        os.path.join(fixtures_dir, "sample_report_adolescent.pdf"),
        {"name": "Ananya Sharma", "age": "16", "sex": "Female", "ref_id": "SYN-16-MILD"},
        [
            ["Haemoglobin (Hb)", "10.8", "g/dL", "12.0 - 15.0"],
            ["Serum Ferritin", "12.0", "ng/mL", "15.0 - 150.0"],
            ["Mean Corpuscular Volume (MCV)", "78.0", "fL", "80.0 - 100.0"],
            ["Packed Cell Volume (PCV)", "33.5", "%", "36.0 - 46.0"],
            ["Total RBC Count", "4.1", "mil/uL", "3.8 - 4.8"],
        ]
    )

    # Fixture 2: Severe anaemia (Hb < 7.0 g/dL -> Trigger safety BLOCKED)
    create_synthetic_pdf(
        os.path.join(fixtures_dir, "sample_report_severe.pdf"),
        {"name": "Priya Kumari", "age": "24", "sex": "Female", "ref_id": "SYN-24-SEVERE"},
        [
            ["Haemoglobin (Hb)", "6.4", "g/dL", "12.0 - 15.0"],
            ["Serum Ferritin", "4.5", "ng/mL", "15.0 - 150.0"],
            ["Mean Corpuscular Volume (MCV)", "66.0", "fL", "80.0 - 100.0"],
            ["Serum Iron", "22.0", "ug/dL", "50.0 - 170.0"],
        ]
    )

    # Fixture 3: Non-iron anaemia pattern (Low MCV with normal/high ferritin -> differential review)
    create_synthetic_pdf(
        os.path.join(fixtures_dir, "sample_report_non_iron.pdf"),
        {"name": "Meera Raman", "age": "28", "sex": "Female", "ref_id": "SYN-28-THAL"},
        [
            ["Haemoglobin (Hb)", "10.2", "g/dL", "12.0 - 15.0"],
            ["Serum Ferritin", "195.0", "ng/mL", "15.0 - 150.0"],
            ["Mean Corpuscular Volume (MCV)", "68.0", "fL", "80.0 - 100.0"],
            ["Red Cell Distribution Width (RDW)", "13.2", "%", "11.5 - 14.5"],
        ]
    )


if __name__ == "__main__":
    generate_all_fixtures()


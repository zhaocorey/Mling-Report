#!/usr/bin/env python3
"""
Simple poster generator from prepared content.
Creates a basic A0 portrait poster using reportlab.
"""

from reportlab.lib.pagesizes import A0, portrait
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import sys

def create_poster():
    # A0 Portrait dimensions
    page_width, page_height = portrait(A0)

    # Colors
    PRIMARY = HexColor('#1B3A5C')  # Deep blue
    ACCENT = HexColor('#E8792B')   # Bright orange
    TEXT = HexColor('#222222')
    LIGHT_BG = HexColor('#F0F4F8')

    # Create PDF
    doc = SimpleDocTemplate(
        "M-DaQ_poster.pdf",
        pagesize=portrait(A0),
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=48,
        textColor=PRIMARY,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )

    author_style = ParagraphStyle(
        'Author',
        parent=styles['Normal'],
        fontSize=20,
        textColor=TEXT,
        spaceAfter=6,
        alignment=TA_CENTER,
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=28,
        textColor=PRIMARY,
        spaceAfter=10,
        spaceBefore=16,
        fontName='Helvetica-Bold',
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=18,
        textColor=TEXT,
        spaceAfter=8,
        leading=24,
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
    )

    # Build content
    story = []

    # Title
    story.append(Paragraph(
        "M-DaQ: Retrieving Samples with Multilingual Diversity<br/>and Quality for Instruction Fine-Tuning Datasets",
        title_style
    ))
    story.append(Spacer(1, 0.5*cm))

    # Authors
    story.append(Paragraph(
        "Chunguang Zhao¹ · Yilun Liu¹ · Pufan Zeng² · Yuanchang Luo¹ · Shimin Tao¹<br/>"
        "Minggui He¹ · Weibin Meng¹ · Song Xu² · Chen Liu¹ · Hongxia Ma¹<br/>"
        "Li Zhang¹ · Boxing Chen¹ · Daimeng Wei¹",
        author_style
    ))
    story.append(Paragraph(
        "¹ Huawei Technologies Ltd.  ² University of Science and Technology of China",
        author_style
    ))
    story.append(Spacer(1, 1*cm))

    # Motivation
    story.append(Paragraph("1. MOTIVATION", heading_style))
    story.append(Paragraph(
        "<b>Problem:</b> Multilingual instruction fine-tuning (IFT) data is scarce, skewed toward English, and lacks systematic curation.",
        body_style
    ))
    story.append(Paragraph("• Llama-3 IFT dataset: only <b>3.01%</b> multilingual samples", bullet_style))
    story.append(Paragraph("• No language-agnostic quality scoring method for multilingual data", bullet_style))
    story.append(Paragraph("• Data diversity studied only in English settings", bullet_style))
    story.append(Paragraph("• Superficial Alignment Hypothesis (SAH) unverified in multilingual contexts", bullet_style))
    story.append(Spacer(1, 0.5*cm))

    # Method
    story.append(Paragraph("2. METHOD: M-DaQ FRAMEWORK", heading_style))
    story.append(Paragraph("<b>Stage 1: Quality Scoring Model (QSM)</b>", body_style))
    story.append(Paragraph("• Fine-tuned on ~2.3K expert-revised samples × 18 languages", bullet_style))
    story.append(Paragraph("• Triplet loss: instruction → positive vs. negative response", bullet_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Stage 2: Diversity-Aware Selection (DAS)</b>", body_style))
    story.append(Paragraph("• MMR-inspired: Quality ≈ Relevance, Diversity ≈ Novelty", bullet_style))
    story.append(Paragraph("• Two-stage pipeline reduces O(n²) → O(n log n)", bullet_style))
    story.append(Paragraph("• Ratio n<sub>quality</sub> : n<sub>diversity</sub> = <b>6:1</b>", bullet_style))
    story.append(Spacer(1, 0.5*cm))

    # Results
    story.append(Paragraph("3. KEY RESULTS", heading_style))

    # Results table
    results_data = [
        ['Benchmark', 'Avg Win Rate'],
        ['Alpaca-Eval', '60.2%'],
        ['MT-Bench R1', '62.6%'],
        ['MT-Bench R2', '62.9%'],
    ]

    t = Table(results_data, colWidths=[8*cm, 6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 20),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('FONTSIZE', (0, 1), (-1, -1), 18),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("• Gains <b>more pronounced in low-resource languages</b> (Tagalog, Malay)", bullet_style))
    story.append(Paragraph("• Human evaluation: <b>78.0% / 85.0% / 85.3%</b> avg win rates across 6 languages", bullet_style))
    story.append(Spacer(1, 0.5*cm))

    # SAH Validation
    story.append(Paragraph("4. SAH VALIDATION", heading_style))
    story.append(Paragraph("First systematic investigation of SAH in multilingual settings:", body_style))
    story.append(Paragraph("• <b>Diminishing returns</b>: 1K curated > 52K unfiltered (−10.1% at 10K, −6.2% at 52K)", bullet_style))
    story.append(Paragraph("• <b>Language-dependent sensitivity</b>: Arabic shows flatter curve than French", bullet_style))
    story.append(Paragraph("• <b>Practical implication</b>: A few thousand high-quality samples suffice", bullet_style))
    story.append(Spacer(1, 0.5*cm))

    # Conclusion
    story.append(Paragraph("5. CONCLUSION", heading_style))
    story.append(Paragraph("• M-DaQ = QSM (quality) + DAS (diversity): compact, high-fidelity multilingual IFT", bullet_style))
    story.append(Paragraph("• <b>60%+ avg win rate</b> across 18 languages on Alpaca-Eval & MT-Bench", bullet_style))
    story.append(Paragraph("• First empirical validation of <b>SAH in multilingual settings</b>", bullet_style))
    story.append(Paragraph("• Code: <b>github.com/zhaocorey/M-DaQ</b>", bullet_style))
    story.append(Spacer(1, 1*cm))

    # Footer
    story.append(Paragraph(
        "<b>SIGIR 2026</b> · Melbourne, VIC, Australia · July 20–24, 2026",
        ParagraphStyle('Footer', parent=body_style, fontSize=16, textColor=HexColor('#666666'), alignment=TA_CENTER)
    ))

    # Build PDF
    doc.build(story)
    print("✓ Poster generated: M-DaQ_poster.pdf")
    print(f"  Size: A0 Portrait ({page_width/cm:.1f} × {page_height/cm:.1f} cm)")

if __name__ == '__main__':
    create_poster()

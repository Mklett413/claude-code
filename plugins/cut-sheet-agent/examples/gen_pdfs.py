#!/usr/bin/env python3
"""Generate PDFs for Haldeman cut sheets."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT

COW1 = {
    "title": "Cut Sheet — Haldeman | Beef 1 | 4-29-26",
    "packaging": "✓  2# Breakfast Sausage — 21.92 lbs",
    "cuts": [
        ("Denver", "2.940"),
        ("Flank", "2.180"),
        ("Hanger", "0.595"),
        ("Flatiron", "3.910"),
        ("Teres Major", "0.725"),
        ("Bavette", "4.655"),
        ("Chuck Eye", "4.870"),
        ("Tri-Tip", "4.840"),
        ("Filets", "3.165"),
        ("Skirt Steak", "3.760"),
        ("2# Stew Meat", "16.185"),
        ("Chuck Roast", "18.440"),
        ("Eye of Round", "6.655"),
        ("T-Bone", "15.630"),
        ("Porterhouse", "12.876"),
        ("Bone-in Ribeye", "18.810"),
        ("Short Ribs", "12.905"),
        ("Dino Ribs", "4.495"),
        ("Flat End Brisket", "7.235"),
        ("Point End Brisket", "11.550"),
        ("Tenderized Steak / CFS  (pre)", "18.520"),
        ("Tenderized Steak / CFS  (post)", "16.030"),
        ("Tenderized Sirloin", "14.970"),
        ("Cutlets", "13.430"),
        ("Baseball Sirloin", "2.415"),
        ("Bones", "6.595"),
        ("Chili Grind", "30.410"),
    ],
    "ground_beef": [("1", "2.655"), ("2", "2.850"), ("3", "2.893")],
    "ground_total": "28.53",
    "notes": [
        "Tallow: 11.94 lbs  (test: 7.9)",
        "Total cut weight: ~332.35 lbs *",
        "* Total noted on original as '3.3235' — interpreted as 332.35 lbs. Verify if needed.",
    ],
}

COW2 = {
    "title": "Cut Sheet — Haldeman | Cow 2 | 4-30-26",
    "packaging": "✓  2# Breakfast Sausage — 22.143 lbs",
    "cuts": [
        ("Chuck Eye", "5.430"),
        ("Flatiron", "4.395"),
        ("Denver", "2.895"),
        ("Tri-Tip", "4.000"),
        ("Flank", "1.755"),
        ("Hanger", "0.525"),
        ("Teres Major", "0.690"),
        ("Bavette", "3.580"),
        ("Skirt Steak", "2.190"),
        ("Tenderized Steak / CFS  (pre)", "15.440"),
        ("Tenderized Steak / CFS  (post)", "14.665"),
        ("Tenderized Sirloin", "17.530"),
        ("Cutlets", "12.405"),
        ("Baseball Sirloin", "5.085"),
        ("Chuck Roast", "16.740"),
        ("Shoulder Roast", "9.025"),
        ("2# Stew Meat", "10.860"),
        ("Bone-in Ribeye", "20.890"),
        ("Filets", "6.765"),
        ("Tenderloin Tail", "0.625"),
        ("NY Strip", "14.395"),
        ("Dino Ribs", "4.905"),
        ("Flat End Brisket", "8.040"),
        ("Point End Brisket", "10.530"),
        ("Eye of Round", "3.390"),
        ("Short Ribs", "9.355"),
        ("Bones", "5.785"),
        ("Chili Grind", "20.320"),
    ],
    "ground_beef": [("1", "2.655"), ("2", "2.850"), ("3", "28.46 *")],
    "ground_total": "28.46",
    "notes": [
        "Breakfast Sausage: 22.143 lbs (2# packages)",
        "* Ground beef package breakdown partially illegible — total shown as 28.46 lbs. Verify individual weights.",
    ],
}

HEADER_COLOR = colors.HexColor("#1a3a1a")
ROW_ALT     = colors.HexColor("#f0f5f0")
ACCENT      = colors.HexColor("#2d6a2d")


def build_pdf(data: dict, out_path: str):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "title", parent=styles["Heading1"],
        fontSize=16, textColor=HEADER_COLOR, spaceAfter=4, alignment=TA_LEFT,
    )
    pkg_style = ParagraphStyle(
        "pkg", parent=styles["Normal"],
        fontSize=11, textColor=ACCENT, spaceAfter=12, leading=14,
    )
    section_style = ParagraphStyle(
        "section", parent=styles["Heading2"],
        fontSize=12, textColor=HEADER_COLOR, spaceBefore=14, spaceAfter=4,
    )
    note_style = ParagraphStyle(
        "note", parent=styles["Normal"],
        fontSize=8.5, textColor=colors.HexColor("#555555"), leading=12, spaceAfter=2,
    )

    col_w = [4.0 * inch, 2.5 * inch]

    def make_table(rows, header):
        table_data = [header] + list(rows)
        t = Table(table_data, colWidths=col_w)
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_COLOR),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 10),
            ("ALIGN",      (1, 0), (1, -1), "RIGHT"),
            ("FONTNAME",   (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",   (0, 1), (-1, -1), 9.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
            ("GRID",       (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (0, -1), 6),
        ])
        t.setStyle(style)
        return t

    story = [
        Paragraph(data["title"], title_style),
        Paragraph(data["packaging"], pkg_style),
        Paragraph("Cuts", section_style),
        make_table(data["cuts"], ["Cut", "Weight (lbs)"]),
        Paragraph("Ground Beef Packages (2# pkgs)", section_style),
        make_table(data["ground_beef"] + [("Total", data["ground_total"])],
                   ["Package", "Weight (lbs)"]),
        Spacer(1, 12),
        Paragraph("Notes", section_style),
    ]
    for note in data["notes"]:
        story.append(Paragraph("• " + note, note_style))

    doc.build(story)
    print(f"Written: {out_path}")


if __name__ == "__main__":
    import os
    base = os.path.dirname(__file__)
    build_pdf(COW1, os.path.join(base, "haldeman-cow1-2026-04-29.pdf"))
    build_pdf(COW2, os.path.join(base, "haldeman-cow2-2026-04-30.pdf"))

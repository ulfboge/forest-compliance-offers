"""Compose a partner-ready one-pager PDF from curated text snippets.

The script relies on ReportLab only and intentionally avoids Markdown
parsing to keep dependencies minimal. It reads key fragments from the
documentation folder, inserts a hero visual if available, and exports a
two-page PDF to `outputs/`.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (  # type: ignore
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "docs"
VISUALS_DIR = DOCS_DIR / "Visuals"
OUTPUT_DIR = BASE_DIR / "outputs"


def _load_service_highlights() -> list[str]:
    service_offer = (DOCS_DIR / "EUDR_Service_Offer.md").read_text(encoding="utf-8")
    highlights: list[str] = []
    for line in service_offer.splitlines():
        if "Traceability Assurance" in line and "|" in line:
            highlights.append("Traceability assurance – geospatially verified origin data")
        if "Deforestation-Free Evidence" in line and "|" in line:
            highlights.append("Deforestation-free evidence backed by satellite data")
        if "Integrated Expertise" in line and "|" in line:
            highlights.append("Integrated GIS + forestry expertise for due diligence")
    if not highlights:
        highlights = [
            "Full spatial traceability of supplier polygons",
            "Satellite-backed deforestation screening",
            "Contextual forestry intelligence for due diligence",
        ]
    return highlights[:3]


def _load_sweden_dates() -> list[list[str]]:
    briefing = (DOCS_DIR / "EUDR_Status_Sweden.md").read_text(encoding="utf-8")
    rows: list[list[str]] = []
    for line in briefing.splitlines():
        if line.startswith("- **") and " – " in line:
            milestone, _, detail = line.partition(" – ")
            rows.append([milestone.strip("- "), detail.strip()])
    return rows[:4] or [
        ["**31 May 2023**", "Regulation adopted"],
        ["**29 June 2023**", "Regulation entered into force"],
    ]


def _hero_image() -> Image | None:
    hero_path = VISUALS_DIR / "eudr_risk_map_overview.png"
    if hero_path.exists():
        img = Image(str(hero_path), width=15 * cm, height=9 * cm)
        img.hAlign = "CENTER"
        return img
    return None


def _build_styles() -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="HeroTitle",
            fontSize=20,
            leading=24,
            spaceAfter=12,
            alignment=1,
            textColor=colors.HexColor("#0f4c5c"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Lead",
            fontSize=12,
            leading=16,
            spaceAfter=10,
            textColor=colors.HexColor("#1b263b"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Bullet",
            fontSize=11,
            leading=14,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Disclaimer",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#555555"),
            spaceBefore=18,
        )
    )
    return styles


def _build_story() -> list:
    styles = _build_styles()
    highlights = _load_service_highlights()
    sweden_rows = _load_sweden_dates()

    story: list = []

    story.append(Paragraph("EUDR Traceability & Forest Risk Services", styles["HeroTitle"]))
    story.append(
        Paragraph(
            "Partner-ready geospatial workflows for Regulation (EU) 2023/1115 compliance.",
            styles["Lead"],
        )
    )

    hero = _hero_image()
    if hero:
        story.append(hero)
        story.append(Spacer(1, 12))

    story.append(Paragraph("Why partners choose Komba GIS", styles["Lead"]))
    for bullet in highlights:
        story.append(Paragraph(bullet, styles["Bullet"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Key dates – Sweden implementation", styles["Lead"]))

    table = Table(sweden_rows, colWidths=[6.5 * cm, 9 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0fbfc")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1b263b")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#98c1d9")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(table)

    story.append(
        Paragraph(
            "Partners: OpenForests (data stewardship), Mergin Maps (offline field capture), Preferred by Nature (assurance).",
            styles["Lead"],
        )
    )

    story.append(
        Paragraph(
            "Disclaimer: Spatial and environmental risk assessment – not legal verification.",
            styles["Disclaimer"],
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("Service Modules", styles["HeroTitle"]))
    modules = [
        "1. Geolocation & traceability mapping with offline collection",
        "2. Post-2020 deforestation & degradation screening",
        "3. Contextual risk scoring dashboard",
        "4. Forestry field verification for high-risk suppliers",
        "5. Continuous monitoring and reporting playbook",
    ]
    for module in modules:
        story.append(Paragraph(module, styles["Bullet"]))

    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Contact: Johan Karlsson – Remote Sensing & GIS Analyst | johan@kombagis.se | kombagis.se",
            styles["Lead"],
        )
    )
    story.append(
        Paragraph(
            "Next steps: schedule partner scoping call, review sample dashboard, align on pilot geographies.",
            styles["Bullet"],
        )
    )

    return story


def build_pdf() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = OUTPUT_DIR / "EUDR_Services_OnePager.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    story = _build_story()
    doc.build(story)
    return pdf_path


if __name__ == "__main__":
    pdf_file = build_pdf()
    print(f"Created brochure: {pdf_file}")
 

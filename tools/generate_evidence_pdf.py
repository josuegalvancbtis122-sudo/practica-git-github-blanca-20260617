from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "evidencias-practica-git-github.pdf"
EVIDENCE = ROOT / "evidencias" / "comandos-evidencia.txt"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5f6b7a"))
    canvas.drawString(0.72 * inch, 0.45 * inch, "Practica individual Git y GitHub")
    canvas.drawRightString(7.78 * inch, 0.45 * inch, f"Pagina {doc.page}")
    canvas.restoreState()


def mono_block(text, style):
    lines = []
    for raw_line in text.splitlines():
        if not raw_line:
            lines.append("")
            continue
        lines.extend(wrap(raw_line, width=92, replace_whitespace=False) or [""])
    return Preformatted("\n".join(lines), style)


def build_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#17202a"),
        spaceAfter=16,
    )
    h2 = ParagraphStyle(
        "H2Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1f6f8b"),
        spaceBefore=10,
        spaceAfter=8,
    )
    body = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#17202a"),
        spaceAfter=8,
    )
    mono = ParagraphStyle(
        "MonoCustom",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=7.2,
        leading=9,
        leftIndent=0,
        rightIndent=0,
        backColor=colors.HexColor("#f5f7fa"),
        borderColor=colors.HexColor("#d7dde8"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=10,
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    repo_url = "https://github.com/josuegalvancbtis122-sudo/practica-git-github-blanca-20260617"
    story = [
        Paragraph("Evidencias de practica Git y GitHub", title),
        Paragraph("Trabajo realizado de forma individual", h2),
        Paragraph(
            "Este documento reune las evidencias de una practica completa de Git y GitHub: "
            "creacion del repositorio remoto, proyecto local, push, pull, revision de diferencias "
            "entre local y remoto, creacion de un conflicto y resolucion del mismo.",
            body,
        ),
        Paragraph(f"Repositorio remoto: {repo_url}", body),
        Spacer(1, 8),
    ]

    summary_data = [
        ["Requisito", "Evidencia"],
        ["Crear repositorio en GitHub", "Repositorio remoto creado y conectado como origin."],
        ["Crear proyecto", "Pagina web con README.md, index.html, styles.css y script.js."],
        ["Subir proyecto con push", "git push -u origin master registrado."],
        ["Pull", "git pull origin master registrado."],
        ["Log local/remoto", "git log --left-right HEAD...origin/master registrado."],
        ["Conflicto local/remoto", "README.md editado en local y en remoto; pull genera CONFLICT."],
        ["Resolucion", "Conflicto resuelto, merge confirmado y push final realizado."],
    ]
    table = Table(summary_data, colWidths=[2.05 * inch, 4.95 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f6f8b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0dc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.extend([table, PageBreak(), Paragraph("Evidencias de comandos", title)])

    evidence_text = EVIDENCE.read_text(encoding="utf-8", errors="replace")
    sections = evidence_text.split("\n===== ")
    for index, section in enumerate(sections):
        if not section.strip():
            continue
        if index == 0:
            story.append(mono_block(section.strip(), mono))
            continue
        heading, _, content = section.partition("=====")
        story.append(Paragraph(heading.strip(), h2))
        story.append(mono_block(content.strip(), mono))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return OUT


if __name__ == "__main__":
    print(build_pdf())

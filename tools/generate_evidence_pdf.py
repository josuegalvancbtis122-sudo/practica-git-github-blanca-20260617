from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image as RLImage,
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
CAPTURES = ROOT / "evidencias" / "capturas"

SCREENSHOT_TITLES = [
    ("01-estado-inicial.png", "Captura 1. Estado inicial del repositorio local"),
    ("02-proyecto-creado.png", "Captura 2. Proyecto creado"),
    ("03-commit-inicial.png", "Captura 3. Commit inicial local"),
    ("04-repositorio-remoto.png", "Captura 4. Repositorio remoto en GitHub"),
    ("05-push.png", "Captura 5. Push al repositorio remoto"),
    ("06-pull.png", "Captura 6. Pull desde el repositorio remoto"),
    ("07-log-local-remoto.png", "Captura 7. Log para comparar local y remoto"),
    ("08-cambio-remoto-conflicto.png", "Captura 8. Cambio remoto para provocar conflicto"),
    ("09-cambio-local-conflicto.png", "Captura 9. Cambio local para provocar conflicto"),
    ("10-pull-conflicto.png", "Captura 10. Pull que genera conflicto"),
    ("11-estado-conflicto.png", "Captura 11. Estado con conflicto"),
    ("12-marcadores-conflicto.png", "Captura 12. Marcadores de conflicto en README.md"),
    ("13-log-diferencia-conflicto.png", "Captura 13. Log con diferencia local/remoto durante conflicto"),
    ("14-resolucion-conflicto.png", "Captura 14. Resolucion del conflicto"),
    ("15-push-resolucion.png", "Captura 15. Push de resolucion"),
    ("16-estado-final.png", "Captura 16. Estado final"),
    ("17-github-repositorio.png", "Captura 17. Repositorio visible en GitHub"),
    ("18-github-commits.png", "Captura 18. Historial de commits en GitHub"),
    ("19-github-pdf.png", "Captura 19. PDF de evidencias dentro del repositorio"),
]


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


def screenshot_block(path, caption, caption_style):
    max_width = 7.0 * inch
    max_height = 4.75 * inch
    image = RLImage(str(path))
    ratio = min(max_width / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * ratio
    image.drawHeight = image.imageHeight * ratio
    return [Paragraph(caption, caption_style), image, Spacer(1, 12)]


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
    story.extend([table, PageBreak(), Paragraph("Capturas de pantalla", title)])

    for filename, caption in SCREENSHOT_TITLES:
        image_path = CAPTURES / filename
        if image_path.exists():
            story.extend(screenshot_block(image_path, caption, body))

    story.extend([PageBreak(), Paragraph("Evidencias de comandos", title)])

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

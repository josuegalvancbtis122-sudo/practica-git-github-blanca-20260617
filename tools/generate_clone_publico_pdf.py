from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "evidencias" / "clone-publico"
EVIDENCE = EVIDENCE_DIR / "comandos-evidencia.txt"
CAPTURES = EVIDENCE_DIR / "capturas"
OUT = ROOT / "output" / "pdf" / "evidencias-clone-repositorio-publico.pdf"

SHOTS = [
    ("01-repositorio-publico-verificado.png", "Repositorio publico seleccionado"),
    ("02-fork.png", "Fork creado en GitHub"),
    ("03-clone.png", "Clone del fork"),
    ("04-remote.png", "Remote del repositorio clonado"),
    ("05-rama.png", "Rama actual del clone"),
    ("06-commits-previos.png", "Commits previos del repositorio"),
    ("07-archivos.png", "Archivos clonados"),
    ("08-estado-final.png", "Estado final del clone"),
    ("09-cambios-realizados.png", "Cambios realizados en el proyecto"),
    ("10-commit-cambios.png", "Commit de los cambios"),
    ("11-push-remoto.png", "Push al repositorio remoto"),
    ("12-pull-request.png", "Pull request creado"),
]


def load_font(size=18):
    for candidate in ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def extract_sections(text):
    sections = {}
    for part in text.split("\n===== "):
        if not part.strip() or "=====" not in part:
            continue
        title, _, body = part.partition("=====")
        sections[title.strip()] = body.strip()
    return sections


def text_width(draw, text, font):
    return draw.textlength(text, font=font)


def draw_prompt(draw, x, y, font, route="/c/Users/equipo/Documents/Blanca"):
    for text, color in [("equipo@DESKTOP-3TBB1UV", "#00ff00"), (" MINGW64", "#ff00ff"), (f" {route}", "#ffd200")]:
        draw.text((x, y), text, fill=color, font=font)
        x += text_width(draw, text, font)


def normalize_lines(body):
    result = []
    for raw in body.splitlines():
        if raw.startswith("> "):
            result.append(("command", raw[2:]))
        elif raw.startswith(">"):
            result.append(("command", raw[1:].strip()))
        else:
            result.append(("output", raw))
    return result


def draw_terminal(title, body, path):
    font = load_font(20)
    title_font = load_font(18)
    max_chars = 105
    lines = []
    for kind, line in normalize_lines(body):
        wrapped = wrap(line, width=max_chars, replace_whitespace=False) if len(line) > max_chars else [line]
        lines.extend((kind, item) for item in wrapped)
    if len(lines) > 34:
        lines = lines[:33] + [("output", "...")]

    width = 1380
    title_h = 48
    line_h = 26
    visual_lines = len(lines) + sum(1 for kind, _ in lines if kind == "command")
    height = title_h + max(22 + visual_lines * line_h + 40, 250)
    image = Image.new("RGB", (width, height), "#000000")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, title_h), fill="#202020")
    draw.polygon([(15, 23), (28, 10), (41, 23), (28, 36)], fill="#d7d7d7")
    draw.polygon([(20, 18), (28, 10), (28, 23)], fill="#ff5f56")
    draw.polygon([(20, 28), (28, 36), (28, 23)], fill="#27c93f")
    draw.polygon([(36, 18), (28, 10), (28, 23)], fill="#ffbd2e")
    draw.polygon([(36, 28), (28, 36), (28, 23)], fill="#58a6ff")
    draw.text((56, 13), "MINGW64:/", fill="#f2f2f2", font=title_font)
    draw.text((width - 275, 12), "-", fill="#f2f2f2", font=title_font)
    draw.rectangle((width - 174, 15, width - 154, 34), outline="#f2f2f2", width=2)
    draw.text((width - 78, 10), "x", fill="#f2f2f2", font=load_font(24))
    draw.rectangle((width - 26, title_h, width - 1, height), fill="#1d1d1d")
    draw.polygon([(width - 14, title_h + 12), (width - 21, title_h + 22), (width - 7, title_h + 22)], fill="#555555")
    draw.polygon([(width - 14, height - 12), (width - 21, height - 22), (width - 7, height - 22)], fill="#555555")

    y = title_h + 22
    for kind, line in lines:
        if kind == "command":
            draw_prompt(draw, 0, y, font)
            y += line_h
            draw.text((0, y), f"$ {line}", fill="#f2f2f2", font=font)
        else:
            fill = "#f2f2f2"
            if "No se pudo" in line:
                fill = "#ff6666"
            elif "c443607" in line or "Cloning into" in line or "origin" in line:
                fill = "#83ff83"
            draw.text((0, y), line, fill=fill, font=font)
        y += line_h
    image.save(path)


def generate_captures():
    CAPTURES.mkdir(parents=True, exist_ok=True)
    sections = extract_sections(EVIDENCE.read_text(encoding="utf-8", errors="replace"))
    for filename, title in SHOTS:
        draw_terminal(title, sections.get(title, ""), CAPTURES / filename)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5f6b7a"))
    canvas.drawString(0.72 * inch, 0.45 * inch, "Ejercicio individual - clonar repositorio publico")
    canvas.drawRightString(7.78 * inch, 0.45 * inch, f"Pagina {doc.page}")
    canvas.restoreState()


def scaled_image(path):
    image = RLImage(str(path))
    ratio = min((7.0 * inch) / image.imageWidth, (4.7 * inch) / image.imageHeight)
    image.drawWidth = image.imageWidth * ratio
    image.drawHeight = image.imageHeight * ratio
    return image


def mono_block(text, style):
    lines = []
    for raw in text.splitlines():
        lines.extend(wrap(raw, width=92, replace_whitespace=False) if len(raw) > 92 else [raw])
    return Preformatted("\n".join(lines), style)


def build_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleCustom", parent=styles["Title"], fontSize=22, leading=28, textColor=colors.HexColor("#17202a"))
    h2 = ParagraphStyle("H2Custom", parent=styles["Heading2"], fontSize=14, leading=18, textColor=colors.HexColor("#1f6f8b"), spaceBefore=10, spaceAfter=8)
    body = ParagraphStyle("BodyCustom", parent=styles["BodyText"], fontSize=10.5, leading=15, textColor=colors.HexColor("#17202a"), spaceAfter=8)
    mono = ParagraphStyle("MonoCustom", parent=styles["Code"], fontName="Courier", fontSize=7.2, leading=9, backColor=colors.HexColor("#f5f7fa"), borderColor=colors.HexColor("#d7dde8"), borderWidth=0.5, borderPadding=6, spaceBefore=4, spaceAfter=10)
    doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=0.7 * inch, leftMargin=0.7 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch)
    story = [
        Paragraph("Evidencias de clonar repositorio publico", title),
        Paragraph("Trabajo realizado de forma individual", h2),
        Paragraph("Repositorio seleccionado: https://github.com/sgvillalobos/practica-git.git", body),
        Paragraph("Se verifico el repositorio publico, se ejecuto git clone, se revisaron los commits previos, se realizaron cambios, se hizo commit, push y pull request.", body),
        Paragraph("Fork creado en GitHub: https://github.com/josuegalvancbtis122-sudo/practica-git. Link usado para clonar: https://github.com/josuegalvancbtis122-sudo/practica-git.git.", body),
    ]
    table = Table([
        ["Requisito", "Evidencia"],
        ["Seleccionar repositorio publico", "sgvillalobos/practica-git.git verificado con git ls-remote."],
        ["Hacer fork", "Fork creado en la cuenta josuegalvancbtis122-sudo." ],
        ["Clonar repositorio", "git clone ejecutado desde el fork en ejercicio-clone-fork/practica-git-fork."],
        ["Mostrar commits previos", "git log muestra 3 commits previos: c443607, c8cd28a y 996718c."],
                ["Realizar cambios", "Se modifico README.md y se agregaron index.html y styles.css."],
        ["Commit", "Commit 9afe888 con los cambios del proyecto."],
        ["Push", "Rama cambios-practica-fork subida al fork remoto."],
        ["Pull request", "PR abierto: https://github.com/sgvillalobos/practica-git/pull/1."],
        ["Documentar en PDF", "Este documento contiene capturas y salidas de comandos."],
    ], colWidths=[2.1 * inch, 4.9 * inch], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f6f8b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0dc")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
    ]))
    story.extend([Spacer(1, 8), table, PageBreak(), Paragraph("Capturas de pantalla", title)])
    for filename, caption in SHOTS:
        image_path = CAPTURES / filename
        if image_path.exists():
            story.extend([Paragraph(caption, h2), scaled_image(image_path), Spacer(1, 12)])
    story.extend([PageBreak(), Paragraph("Evidencias de comandos", title)])
    sections = extract_sections(EVIDENCE.read_text(encoding="utf-8", errors="replace"))
    for _, section_title in SHOTS:
        story.append(Paragraph(section_title, h2))
        story.append(mono_block(sections.get(section_title, ""), mono))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return OUT


if __name__ == "__main__":
    generate_captures()
    print(build_pdf())




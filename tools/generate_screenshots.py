from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidencias" / "comandos-evidencia.txt"
OUT_DIR = ROOT / "evidencias" / "capturas"


SHOTS = [
    ("01-estado-inicial.png", "Estado inicial del repositorio local"),
    ("02-proyecto-creado.png", "Archivos del proyecto creado"),
    ("03-commit-inicial.png", "Commit inicial local"),
    ("04-repositorio-remoto.png", "Repositorio remoto en GitHub"),
    ("05-push.png", "Push al repositorio remoto"),
    ("06-pull.png", "Pull desde el repositorio remoto"),
    ("07-log-local-remoto.png", "Log para comparar local y remoto"),
    ("08-cambio-remoto-conflicto.png", "Cambio remoto para provocar conflicto"),
    ("09-cambio-local-conflicto.png", "Cambio local para provocar conflicto"),
    ("10-pull-conflicto.png", "Pull que genera conflicto"),
    ("11-estado-conflicto.png", "Estado con conflicto"),
    ("12-marcadores-conflicto.png", "Marcadores de conflicto en README.md"),
    ("13-log-diferencia-conflicto.png", "Log con diferencia local/remoto durante conflicto"),
    ("14-resolucion-conflicto.png", "Resolucion del conflicto"),
    ("15-push-resolucion.png", "Push de resolucion"),
    ("16-estado-final.png", "Estado final"),
]


def load_font(size=18):
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def extract_sections(text):
    sections = {}
    parts = text.split("\n===== ")
    for part in parts:
        if not part.strip():
            continue
        if "=====" not in part:
            continue
        title, _, body = part.partition("=====")
        sections[title.strip()] = body.strip()
    return sections


def draw_terminal(title, body, path):
    font = load_font(18)
    title_font = load_font(20)
    max_chars = 96
    lines = []
    for line in body.splitlines():
        if len(line) <= max_chars:
            lines.append(line)
        else:
            lines.extend(wrap(line, width=max_chars, replace_whitespace=False))
    if len(lines) > 34:
        lines = lines[:33] + ["..."]

    width = 1380
    header_h = 64
    pad = 28
    line_h = 26
    height = header_h + pad + (len(lines) + 1) * line_h + pad
    image = Image.new("RGB", (width, height), "#0f172a")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, header_h), fill="#111827")
    draw.ellipse((22, 22, 42, 42), fill="#ef4444")
    draw.ellipse((54, 22, 74, 42), fill="#f59e0b")
    draw.ellipse((86, 22, 106, 42), fill="#22c55e")
    draw.text((130, 19), title, fill="#f8fafc", font=title_font)

    y = header_h + pad
    for line in lines:
        fill = "#e5e7eb"
        if line.startswith(">"):
            fill = "#93c5fd"
        elif "CONFLICT" in line or "UU README.md" in line:
            fill = "#fca5a5"
        elif "To https://" in line or "Already up to date" in line:
            fill = "#86efac"
        draw.text((pad, y), line, fill=fill, font=font)
        y += line_h

    image.save(path)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sections = extract_sections(EVIDENCE.read_text(encoding="utf-8", errors="replace"))
    for filename, title in SHOTS:
        body = sections.get(title, "(No se encontro esta seccion en el archivo de evidencias.)")
        draw_terminal(title, body, OUT_DIR / filename)
    print(OUT_DIR)


if __name__ == "__main__":
    main()

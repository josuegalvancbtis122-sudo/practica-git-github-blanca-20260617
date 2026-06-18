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


def text_width(draw, text, font):
    return draw.textlength(text, font=font)


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


def draw_prompt(draw, x, y, font, route="/c/Users/equipo/Documents/Blanca"):
    parts = [
        ("equipo@DESKTOP-3TBB1UV", "#00ff00"),
        (" MINGW64", "#ff00ff"),
        (f" {route}", "#ffd200"),
    ]
    for text, color in parts:
        draw.text((x, y), text, fill=color, font=font)
        x += text_width(draw, text, font)
    return x


def normalize_terminal_lines(body):
    result = []
    for raw_line in body.splitlines():
        if raw_line.startswith("> "):
            result.append(("command", raw_line[2:]))
        elif raw_line.startswith(">"):
            result.append(("command", raw_line[1:].strip()))
        else:
            result.append(("output", raw_line))
    return result


def draw_terminal(title, body, path):
    font = load_font(20)
    title_font = load_font(18)
    max_chars = 105
    lines = []
    for kind, line in normalize_terminal_lines(body):
        if len(line) <= max_chars:
            lines.append((kind, line))
        else:
            for wrapped in wrap(line, width=max_chars, replace_whitespace=False):
                lines.append((kind, wrapped))
    if len(lines) > 34:
        lines = lines[:33] + [("output", "...")]

    width = 1380
    title_h = 48
    pad_x = 0
    pad_y = 22
    line_h = 26
    visual_lines = len(lines) + sum(1 for kind, _ in lines if kind == "command")
    content_h = pad_y + (visual_lines * line_h) + 40
    height = title_h + max(content_h, 250)
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
    draw.text((width - 78, 10), "×", fill="#f2f2f2", font=load_font(24))
    draw.rectangle((width - 26, title_h, width - 1, height), fill="#1d1d1d")
    draw.polygon([(width - 14, title_h + 12), (width - 21, title_h + 22), (width - 7, title_h + 22)], fill="#555555")
    draw.polygon([(width - 14, height - 12), (width - 21, height - 22), (width - 7, height - 22)], fill="#555555")

    y = title_h + pad_y
    for kind, line in lines:
        if kind == "command":
            draw_prompt(draw, pad_x, y, font)
            y += line_h
            draw.text((pad_x, y), f"$ {line}", fill="#f2f2f2", font=font)
        else:
            fill = "#f2f2f2"
            if "CONFLICT" in line or "UU README.md" in line:
                fill = "#ff6666"
            elif "To https://" in line or "Already up to date" in line:
                fill = "#83ff83"
            draw.text((pad_x, y), line, fill=fill, font=font)
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

#!/usr/bin/env python3
"""Create temporary contact sheets from Poppler-rendered PDF pages for QA."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / "temp" / "pdfs"
FONT = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)

for directory in sorted(path for path in ROOT.iterdir() if path.is_dir()):
    pages = sorted(directory.glob("page-*.png"))
    thumbs = []
    for page in pages:
        image = Image.open(page).convert("RGB")
        image.thumbnail((390, 550))
        canvas = Image.new("RGB", (410, 590), "#e5e7eb")
        canvas.paste(image, ((410 - image.width) // 2, 20))
        draw = ImageDraw.Draw(canvas)
        label = page.stem.replace("page-", "Page ")
        draw.text((20, 560), label, font=FONT, fill="#172033")
        thumbs.append(canvas)
    columns = 3
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * 410, rows * 590), "#cbd5e1")
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((index % columns) * 410, (index // columns) * 590))
    sheet.save(ROOT / f"{directory.name}-contact-sheet.png", optimize=True)
    print(ROOT / f"{directory.name}-contact-sheet.png")

#!/usr/bin/env python3
"""Render the continuous-performance decision model as a printable PNG."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "charts" / "continuous-performance-flow.png"
FONT_DIR = Path("C:/Windows/Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


REGULAR = font("segoeui.ttf", 24)
BOLD = font("segoeuib.ttf", 25)
SMALL = font("segoeui.ttf", 19)


def wrapped(draw: ImageDraw.ImageDraw, text: str, max_width: int, selected_font: ImageFont.FreeTypeFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=selected_font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str, fill: str, outline: str = "#24405f") -> None:
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=3)
    x1, y1, x2, y2 = xy
    lines = wrapped(draw, text, x2 - x1 - 34, REGULAR)
    line_height = 31
    y = (y1 + y2 - line_height * len(lines)) / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=REGULAR)
        draw.text(((x1 + x2 - (bbox[2] - bbox[0])) / 2, y), line, fill="#172033", font=REGULAR)
        y += line_height


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], label: str = "") -> None:
    draw.line([start, end], fill="#52637a", width=4)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) > abs(ey - sy):
        direction = 1 if ex > sx else -1
        points = [(ex, ey), (ex - 14 * direction, ey - 9), (ex - 14 * direction, ey + 9)]
    else:
        direction = 1 if ey > sy else -1
        points = [(ex, ey), (ex - 9, ey - 14 * direction), (ex + 9, ey - 14 * direction)]
    draw.polygon(points, fill="#52637a")
    if label:
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        bbox = draw.textbbox((0, 0), label, font=SMALL)
        draw.rounded_rectangle((mx - 8, my - 16, mx + bbox[2] + 8, my + 15), radius=7, fill="#ffffff")
        draw.text((mx, my - 13), label, fill="#36506f", font=SMALL)


def main() -> None:
    image = Image.new("RGB", (1600, 1240), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    draw.text((70, 42), "Continuous Performance Testing decision model", fill="#173b6c", font=font("segoeuib.ttf", 38))
    draw.text((72, 94), "Changed-path gating, reproducible regression checks, and scheduled deeper tests", fill="#52637a", font=REGULAR)

    nodes = {
        "commit": (590, 150, 1010, 235),
        "change": (590, 285, 1010, 390),
        "skip": (80, 445, 460, 540),
        "smoke": (610, 445, 990, 540),
        "smoke_gate": (610, 590, 990, 695),
        "functional_fail": (1080, 590, 1500, 695),
        "load": (610, 750, 990, 845),
        "regression": (610, 900, 990, 1025),
        "repeat": (1070, 900, 1500, 1025),
        "publish": (80, 900, 480, 1025),
        "deep": (590, 1080, 1010, 1180),
    }

    box(draw, nodes["commit"], "Commit or pull request", "#e7f0ff")
    box(draw, nodes["change"], "Relevant API, DB, auth, dependency or test-plan path changed?", "#fff7e6")
    box(draw, nodes["skip"], "Docs-only: skip run and record the reason", "#f1f5f9")
    box(draw, nodes["smoke"], "Build SUT and run functional smoke", "#e8f7ef")
    box(draw, nodes["smoke_gate"], "Smoke and exact workflow assertions pass?", "#fff7e6")
    box(draw, nodes["functional_fail"], "Fail fast as a correctness regression", "#feecec")
    box(draw, nodes["load"], "Run 5-minute Load; parse raw JTL + resources", "#e7f0ff")
    box(draw, nodes["regression"], "p95 > baseline +20% or error >=1%?", "#fff7e6")
    box(draw, nodes["repeat"], "Repeat once; block only if reproduced and attach artifacts", "#feecec")
    box(draw, nodes["publish"], "Publish pass status and metric comparison", "#e8f7ef")
    box(draw, nodes["deep"], "High-risk/nightly: Stress + Spike; weekly: Soak", "#eee9ff")

    arrow(draw, (800, 235), (800, 285))
    arrow(draw, (590, 337), (460, 490), "No")
    arrow(draw, (800, 390), (800, 445), "Yes")
    arrow(draw, (800, 540), (800, 590))
    arrow(draw, (990, 642), (1080, 642), "No")
    arrow(draw, (800, 695), (800, 750), "Yes")
    arrow(draw, (800, 845), (800, 900))
    arrow(draw, (990, 962), (1070, 962), "Yes")
    arrow(draw, (610, 962), (480, 962), "No")
    arrow(draw, (800, 1025), (800, 1080), "Risk/schedule")

    draw.text((70, 1200), "Every executed gate retains JTL, HTML, resource CSV, runtime metadata, and the baseline commit.", fill="#52637a", font=SMALL)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()

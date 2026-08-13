#!/usr/bin/env python3
"""Build polished PDFs from the homework Markdown using ReportLab."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "pdf"
FONT_DIR = Path("C:/Windows/Fonts")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("SegoeUI", str(FONT_DIR / "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("SegoeUI-Bold", str(FONT_DIR / "segoeuib.ttf")))
    pdfmetrics.registerFont(TTFont("Consolas", str(FONT_DIR / "consola.ttf")))
    pdfmetrics.registerFontFamily("SegoeUI", normal="SegoeUI", bold="SegoeUI-Bold")


def ascii_punctuation(text: str) -> str:
    replacements = {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
        "\u2192": "->", "\u2190": "<-", "\u2191": "up", "\u2193": "down",
        "\u2264": "<=", "\u2265": ">=", "\u2248": "~", "\u2212": "-",
        "\u00a0": " ", "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def inline_markup(text: str) -> str:
    text = ascii_punctuation(text)
    text = text.replace("[FULL NAME - HUMAN REVIEW REQUIRED]", "Student name not yet supplied - manual review required")
    text = text.replace("[VIDEO_URL - HUMAN REVIEW REQUIRED]", "Video URL not yet supplied - manual review required")
    escaped = escape(text)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Consolas" color="#173b6c">\1</font>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" color="#1d4ed8">\1</a>', escaped)
    escaped = re.sub(r"&lt;(https?://[^&]+)&gt;", r'<a href="\1" color="#1d4ed8">\1</a>', escaped)
    return escaped


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("TitleCustom", parent=base["Title"], fontName="SegoeUI-Bold", fontSize=23, leading=29, textColor=colors.HexColor("#173b6c"), alignment=TA_CENTER, spaceAfter=14),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontName="SegoeUI-Bold", fontSize=18, leading=23, textColor=colors.HexColor("#173b6c"), spaceBefore=12, spaceAfter=8, keepWithNext=1),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontName="SegoeUI-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#24405f"), spaceBefore=10, spaceAfter=6, keepWithNext=1),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontName="SegoeUI-Bold", fontSize=11.5, leading=15, textColor=colors.HexColor("#36506f"), spaceBefore=8, spaceAfter=4, keepWithNext=1),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="SegoeUI", fontSize=9.3, leading=13.2, textColor=colors.HexColor("#172033"), spaceAfter=6),
        "bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName="SegoeUI", fontSize=9.2, leading=12.8, leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        "quote": ParagraphStyle("Quote", parent=base["BodyText"], fontName="SegoeUI", fontSize=9, leading=12.5, leftIndent=10, rightIndent=8, borderColor=colors.HexColor("#d97706"), borderWidth=0, borderPadding=7, backColor=colors.HexColor("#fff7e6"), textColor=colors.HexColor("#5f3a00"), spaceBefore=4, spaceAfter=7),
        "code": ParagraphStyle("Code", parent=base["Code"], fontName="Consolas", fontSize=6.8, leading=9.2, leftIndent=7, rightIndent=7, borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=7, backColor=colors.HexColor("#f5f7fb"), textColor=colors.HexColor("#172033"), spaceBefore=4, spaceAfter=7),
        "caption": ParagraphStyle("Caption", parent=base["BodyText"], fontName="SegoeUI", fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor("#52637a"), spaceAfter=7),
        "table": ParagraphStyle("TableCell", parent=base["BodyText"], fontName="SegoeUI", fontSize=7.4, leading=9.2, textColor=colors.HexColor("#172033")),
        "table_head": ParagraphStyle("TableHead", parent=base["BodyText"], fontName="SegoeUI-Bold", fontSize=7.4, leading=9.2, textColor=colors.white),
    }


def wrap_code(block: str, width: int = 104) -> str:
    output: list[str] = []
    for line in ascii_punctuation(block).splitlines() or [""]:
        if not line:
            output.append("")
            continue
        indent = len(line) - len(line.lstrip())
        prefix = " " * min(indent, 12)
        chunks = textwrap.wrap(line.strip(), width=max(30, width - len(prefix)), replace_whitespace=False, drop_whitespace=False) or [""]
        output.extend(prefix + chunk for chunk in chunks)
    return escape("\n".join(output))


def parse_table(lines: list[str], styles: dict[str, ParagraphStyle], available_width: float) -> Table:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    columns = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (columns - len(row)))
    rendered = []
    for row_index, row in enumerate(rows):
        style = styles["table_head"] if row_index == 0 else styles["table"]
        rendered.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(rendered, colWidths=[available_width / columns] * columns, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24405f")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#dbe3ef")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def markdown_story(source: Path, styles: dict[str, ParagraphStyle], available_width: float) -> list:
    lines = source.read_text(encoding="utf-8").splitlines()
    story: list = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            story.append(Paragraph(inline_markup(" ".join(item.strip() for item in paragraph)), styles["body"]))
            paragraph = []

    index = 0
    first_heading = True
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Paragraph(wrap_code("\n".join(code_lines)).replace("\n", "<br/>"), styles["code"]))
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue
        if in_code:
            code_lines.append(line)
            index += 1
            continue
        if not line.strip():
            flush_paragraph()
            story.append(Spacer(1, 2))
            index += 1
            continue
        if line.startswith("|"):
            flush_paragraph()
            table_lines = []
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(parse_table(table_lines, styles, available_width))
            story.append(Spacer(1, 7))
            continue
        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if image_match:
            flush_paragraph()
            label, relative = image_match.groups()
            image_path = ROOT / relative
            if image_path.suffix.lower() == ".svg":
                image_path = image_path.with_suffix(".png")
            if image_path.exists():
                from PIL import Image as PILImage
                with PILImage.open(image_path) as opened:
                    img_w, img_h = opened.size
                render_w = available_width
                render_h = render_w * img_h / img_w
                story.append(Image(str(image_path), width=render_w, height=render_h))
                story.append(Paragraph(inline_markup(label), styles["caption"]))
            index += 1
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            text = heading.group(2)
            if first_heading and level == 1:
                story.append(Spacer(1, 22 * mm))
                story.append(Paragraph(inline_markup(text), styles["title"]))
                story.append(Spacer(1, 8 * mm))
                first_heading = False
            else:
                story.append(Paragraph(inline_markup(text), styles["h1" if level == 2 else "h2" if level == 3 else "h3"]))
            index += 1
            continue
        if line.startswith(">"):
            flush_paragraph()
            quote_lines = []
            while index < len(lines) and lines[index].startswith(">"):
                quote_lines.append(lines[index].lstrip("> "))
                index += 1
            story.append(Paragraph(inline_markup(" ".join(quote_lines)), styles["quote"]))
            continue
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        numbered = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        if bullet or numbered:
            flush_paragraph()
            marker = "-" if bullet else f"{numbered.group(1)}."
            content = bullet.group(1) if bullet else numbered.group(2)
            story.append(Paragraph(f"{marker} {inline_markup(content)}", styles["bullet"]))
            index += 1
            continue
        paragraph.append(line)
        index += 1
    flush_paragraph()
    return story


def footer(canvas, document) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#dbe3ef"))
    canvas.line(20 * mm, 15 * mm, width - 20 * mm, 15 * mm)
    canvas.setFont("SegoeUI", 7.5)
    canvas.setFillColor(colors.HexColor("#52637a"))
    canvas.drawString(20 * mm, 10 * mm, "HW05 - AI-assisted Performance Testing - MSSV 23127373")
    canvas.drawRightString(width - 20 * mm, 10 * mm, f"Page {document.page}")
    canvas.restoreState()


def build(source_name: str, output_name: str) -> None:
    styles = make_styles()
    output = OUT / output_name
    document = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=20 * mm, title=source_name, author="MSSV 23127373")
    story = markdown_story(ROOT / source_name, styles, A4[0] - 36 * mm)
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(output)


def main() -> None:
    register_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    build("Main-Report.md", "Main-Report.pdf")
    build("AI-Audit-Report.md", "AI-Audit-Report.pdf")
    build("AI-Critique.md", "AI-Critique.pdf")


if __name__ == "__main__":
    main()

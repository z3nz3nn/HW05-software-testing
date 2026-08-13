#!/usr/bin/env python3
"""Render the committed metric charts as print-ready PNGs with Pillow."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "charts"
FONT_DIR = Path("C:/Windows/Fonts")
COLORS = ["#2563eb", "#dc2626", "#059669", "#7c3aed"]


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def chart(path: Path, title: str, labels: list[str], series: list[tuple[str, list[float]]], y_label: str) -> None:
    width, height = 1600, 850
    left, right, top, bottom = 150, 70, 130, 140
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [value for _, data in series for value in data]
    y_max = max(values) * 1.12 if values and max(values) else 1
    image = Image.new("RGB", (width, height), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.text((left, 48), title, font=font("segoeuib.ttf", 40), fill="#173b6c")

    for tick in range(6):
        value = y_max * tick / 5
        y = top + plot_h * (1 - value / y_max)
        draw.line((left, y, left + plot_w, y), fill="#dbe3ef", width=2)
        label = f"{value:.1f}"
        bbox = draw.textbbox((0, 0), label, font=font("segoeui.ttf", 21))
        draw.text((left - 18 - (bbox[2] - bbox[0]), y - 12), label, font=font("segoeui.ttf", 21), fill="#52637a")

    draw.line((left, top, left, top + plot_h), fill="#8ba0ba", width=3)
    draw.line((left, top + plot_h, left + plot_w, top + plot_h), fill="#8ba0ba", width=3)
    count = max(1, len(labels) - 1)
    x_positions = [left + plot_w * index / count for index in range(len(labels))]
    for x, label in zip(x_positions, labels):
        bbox = draw.textbbox((0, 0), label, font=font("segoeui.ttf", 22))
        draw.text((x - (bbox[2] - bbox[0]) / 2, top + plot_h + 24), label, font=font("segoeui.ttf", 22), fill="#52637a")

    for series_index, (name, data) in enumerate(series):
        color = COLORS[series_index]
        points = [(x_positions[index], top + plot_h * (1 - value / y_max)) for index, value in enumerate(data)]
        draw.line(points, fill=color, width=6, joint="curve")
        for x, y in points:
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=color)
        legend_x = left + series_index * 480
        draw.line((legend_x, height - 52, legend_x + 50, height - 52), fill=color, width=6)
        draw.text((legend_x + 65, height - 68), name, font=font("segoeui.ttf", 23), fill="#172033")

    draw.text((22, top + plot_h / 2), y_label, font=font("segoeui.ttf", 22), fill="#52637a")
    image.save(path, optimize=True)


def main() -> None:
    stress = json.loads((ROOT / "analysis" / "stress.json").read_text(encoding="utf-8"))["time_windows"]
    chart(OUT / "stress-capacity.png", "Stress staircase: saturation begins around 30 users", ["10 users", "20 users", "30 users", "40 users"], [("p95 latency (ms)", [row["p95_ms"] for row in stress]), ("Throughput (samples/s)", [row["throughput_samples_per_second"] for row in stress])], "p95 ms / samples per second")

    spike = json.loads((ROOT / "analysis" / "spike.json").read_text(encoding="utf-8"))["time_windows"]
    chart(OUT / "spike-recovery.png", "Spike: latency returns to baseline in the next 60-second window", [f"{row['window_start_seconds']//60}-{row['window_end_seconds']//60}m" for row in spike], [("p95 latency (ms)", [row["p95_ms"] for row in spike]), ("Throughput (samples/s)", [row["throughput_samples_per_second"] for row in spike])], "p95 ms / samples per second")

    with (ROOT / "evidence" / "resources" / "23127373_Soak_20260814.csv").open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    selected = rows[::60]
    if selected[-1] != rows[-1]:
        selected.append(rows[-1])
    chart(OUT / "soak-memory.png", "Soak memory: warm-up allocation followed by a plateau", [f"{index}m" for index in range(len(selected))], [("Working set (MB)", [float(row["working_set_mb"]) for row in selected]), ("Private memory (MB)", [float(row["private_memory_mb"]) for row in selected])], "Memory MB")

    scenarios = []
    for name in ("load", "stress", "spike", "soak"):
        payload = json.loads((ROOT / "analysis" / f"{name}.json").read_text(encoding="utf-8"))["overall_endpoints_only"]
        scenarios.append((name.title(), payload["p95_ms"]))
    chart(OUT / "scenario-p95.png", "Overall endpoint p95 by scenario", [name for name, _ in scenarios], [("p95 latency (ms)", [value for _, value in scenarios])], "p95 latency (ms)")
    print(f"Generated 4 PNG charts in {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate dependency-free SVG charts from deterministic analysis JSON."""

from __future__ import annotations

import csv
import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "charts"
COLORS = ["#2563eb", "#dc2626", "#059669", "#7c3aed"]


def svg_line_chart(
    path: Path,
    title: str,
    x_labels: list[str],
    series: list[tuple[str, list[float]]],
    y_label: str,
) -> None:
    width, height = 1050, 560
    left, right, top, bottom = 90, 35, 75, 80
    plot_w, plot_h = width - left - right, height - top - bottom
    all_values = [value for _, values in series for value in values]
    y_max = max(all_values) * 1.12 if max(all_values) > 0 else 1
    count = max(1, len(x_labels) - 1)

    def x_pos(index: int) -> float:
        return left + plot_w * index / count

    def y_pos(value: float) -> float:
        return top + plot_h * (1 - value / y_max)

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff" rx="16"/>',
        f'<text x="{left}" y="38" font-family="Segoe UI,Arial" font-size="25" font-weight="700" fill="#172033">{html.escape(title)}</text>',
    ]
    for tick in range(6):
        value = y_max * tick / 5
        y = y_pos(value)
        elements.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+plot_w}" y2="{y:.1f}" stroke="#dbe3ef" stroke-width="1"/>')
        elements.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" font-family="Segoe UI,Arial" font-size="13" fill="#52637a">{value:.1f}</text>')
    elements.append(f'<text x="22" y="{top+plot_h/2}" transform="rotate(-90 22 {top+plot_h/2})" text-anchor="middle" font-family="Segoe UI,Arial" font-size="14" fill="#52637a">{html.escape(y_label)}</text>')

    label_step = max(1, len(x_labels) // 8)
    for index, label in enumerate(x_labels):
        if index % label_step == 0 or index == len(x_labels) - 1:
            x = x_pos(index)
            elements.append(f'<text x="{x:.1f}" y="{top+plot_h+30}" text-anchor="middle" font-family="Segoe UI,Arial" font-size="13" fill="#52637a">{html.escape(label)}</text>')

    for series_index, (name, values) in enumerate(series):
        color = COLORS[series_index % len(COLORS)]
        points = " ".join(f"{x_pos(i):.1f},{y_pos(value):.1f}" for i, value in enumerate(values))
        elements.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, value in enumerate(values):
            elements.append(f'<circle cx="{x_pos(i):.1f}" cy="{y_pos(value):.1f}" r="4" fill="{color}"/>')
        legend_x = left + series_index * 230
        elements.append(f'<line x1="{legend_x}" y1="{height-24}" x2="{legend_x+30}" y2="{height-24}" stroke="{color}" stroke-width="4"/>')
        elements.append(f'<text x="{legend_x+38}" y="{height-19}" font-family="Segoe UI,Arial" font-size="14" fill="#172033">{html.escape(name)}</text>')
    elements.append("</svg>")
    path.write_text("\n".join(elements), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    stress = json.loads((ROOT / "analysis" / "stress.json").read_text(encoding="utf-8"))
    stress_windows = stress["time_windows"]
    svg_line_chart(
        OUT / "stress-capacity.svg",
        "Stress staircase: saturation begins around 30 users",
        ["10 users", "20 users", "30 users", "40 users"],
        [
            ("p95 latency (ms)", [row["p95_ms"] for row in stress_windows]),
            ("Throughput (samples/s)", [row["throughput_samples_per_second"] for row in stress_windows]),
        ],
        "p95 ms / samples per second",
    )

    spike = json.loads((ROOT / "analysis" / "spike.json").read_text(encoding="utf-8"))
    spike_windows = spike["time_windows"]
    svg_line_chart(
        OUT / "spike-recovery.svg",
        "Spike: latency returns to baseline in the next 60-second window",
        [f"{row['window_start_seconds']//60}-{row['window_end_seconds']//60}m" for row in spike_windows],
        [
            ("p95 latency (ms)", [row["p95_ms"] for row in spike_windows]),
            ("Throughput (samples/s)", [row["throughput_samples_per_second"] for row in spike_windows]),
        ],
        "p95 ms / samples per second",
    )

    resource_path = ROOT / "evidence" / "resources" / "23127373_Soak_20260814.csv"
    with resource_path.open(newline="", encoding="utf-8-sig") as handle:
        resource_rows = list(csv.DictReader(handle))
    selected = resource_rows[::60]
    if selected[-1] is not resource_rows[-1]:
        selected.append(resource_rows[-1])
    svg_line_chart(
        OUT / "soak-memory.svg",
        "Soak memory: warm-up allocation followed by a plateau",
        [f"{index}m" for index in range(len(selected))],
        [
            ("Working set (MB)", [float(row["working_set_mb"]) for row in selected]),
            ("Private memory (MB)", [float(row["private_memory_mb"]) for row in selected]),
        ],
        "Memory MB",
    )

    scenarios = []
    for name in ("load", "stress", "spike", "soak"):
        payload = json.loads((ROOT / "analysis" / f"{name}.json").read_text(encoding="utf-8"))
        scenarios.append((name.title(), payload["overall_endpoints_only"]))
    svg_line_chart(
        OUT / "scenario-p95.svg",
        "Overall endpoint p95 by scenario",
        [name for name, _ in scenarios],
        [("p95 latency (ms)", [row["p95_ms"] for _, row in scenarios])],
        "p95 latency (ms)",
    )

    print(f"Generated {len(list(OUT.glob('*.svg')))} charts in {OUT}")


if __name__ == "__main__":
    main()

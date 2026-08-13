#!/usr/bin/env python3
"""Summarize process-resource CSV evidence emitted by monitor-resource.ps1."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path


def percentile(values: list[float], fraction: float) -> float:
    """Nearest-rank percentile, matching analyze_jtl.py."""
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(1, math.ceil(fraction * len(ordered)))
    return ordered[rank - 1]


def rounded(value: float) -> float:
    return round(value, 3)


def linear_slope_per_minute(values: list[float], seconds: list[float]) -> float:
    """Ordinary least-squares slope, expressed as value units per minute."""
    if len(values) < 2:
        return 0.0
    mean_x = sum(seconds) / len(seconds)
    mean_y = sum(values) / len(values)
    denominator = sum((x - mean_x) ** 2 for x in seconds)
    if denominator == 0:
        return 0.0
    slope_per_second = sum((x - mean_x) * (y - mean_y) for x, y in zip(seconds, values)) / denominator
    return slope_per_second * 60


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--markdown", required=True, type=Path)
    args = parser.parse_args()

    with args.csv_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 2:
        raise SystemExit(f"Need at least two resource rows, got {len(rows)}")

    timestamps = [datetime.fromisoformat(row["timestamp_iso"]) for row in rows]
    cpu = [float(row["node_cpu_percent"]) for row in rows]
    working = [float(row["working_set_mb"]) for row in rows]
    private = [float(row["private_memory_mb"]) for row in rows]
    handles = [int(row["handles"]) for row in rows]
    threads = [int(row["threads"]) for row in rows]
    elapsed = [(timestamp - timestamps[0]).total_seconds() for timestamp in timestamps]
    trailing_window_seconds = min(300.0, elapsed[-1] * 2 / 3)
    slope_start_seconds = elapsed[-1] - trailing_window_seconds
    steady_indexes = [index for index, value in enumerate(elapsed) if value >= slope_start_seconds]
    steady_elapsed = [elapsed[index] for index in steady_indexes]
    steady_working = [working[index] for index in steady_indexes]
    steady_private = [private[index] for index in steady_indexes]

    summary = {
        "source": args.csv_path.name,
        "samples": len(rows),
        "start_timestamp": rows[0]["timestamp_iso"],
        "end_timestamp": rows[-1]["timestamp_iso"],
        "duration_seconds": rounded((timestamps[-1] - timestamps[0]).total_seconds()),
        "node_cpu_percent": {
            "mean": rounded(sum(cpu) / len(cpu)),
            "p95": rounded(percentile(cpu, 0.95)),
            "max": rounded(max(cpu)),
        },
        "working_set_mb": {
            "start": rounded(working[0]),
            "end": rounded(working[-1]),
            "delta": rounded(working[-1] - working[0]),
            "p95": rounded(percentile(working, 0.95)),
            "max": rounded(max(working)),
            "trailing_slope_mb_per_minute": rounded(linear_slope_per_minute(steady_working, steady_elapsed)),
        },
        "private_memory_mb": {
            "start": rounded(private[0]),
            "end": rounded(private[-1]),
            "delta": rounded(private[-1] - private[0]),
            "p95": rounded(percentile(private, 0.95)),
            "max": rounded(max(private)),
            "trailing_slope_mb_per_minute": rounded(linear_slope_per_minute(steady_private, steady_elapsed)),
        },
        "trailing_slope_window_seconds": rounded(trailing_window_seconds),
        "handles": {"start": handles[0], "end": handles[-1], "max": max(handles)},
        "threads": {"start": threads[0], "end": threads[-1], "max": max(threads)},
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    md = f"""# Resource analysis: {args.csv_path.name}

Generated from the one-second Node.js process samples. CPU is normalized by the machine's logical-processor count.

| Samples | Duration s | CPU mean % | CPU p95 % | CPU max % | Working-set start MB | Working-set end MB | Working-set max MB | Working-set slope MB/min* | Private-memory slope MB/min* |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| {summary['samples']} | {summary['duration_seconds']} | {summary['node_cpu_percent']['mean']} | {summary['node_cpu_percent']['p95']} | {summary['node_cpu_percent']['max']} | {summary['working_set_mb']['start']} | {summary['working_set_mb']['end']} | {summary['working_set_mb']['max']} | {summary['working_set_mb']['trailing_slope_mb_per_minute']} | {summary['private_memory_mb']['trailing_slope_mb_per_minute']} |

* Ordinary least-squares slope over the final {summary['trailing_slope_window_seconds']} seconds. A near-zero trailing slope supports a plateau but cannot prove that a leak is impossible.

Handle count: {handles[0]} → {handles[-1]} (max {max(handles)}).  
Thread count: {threads[0]} → {threads[-1]} (max {max(threads)}).
"""
    args.markdown.write_text(md, encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

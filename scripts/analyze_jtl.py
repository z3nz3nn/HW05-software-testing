#!/usr/bin/env python3
"""Produce reproducible endpoint and time-window metrics from JMeter CSV JTL."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    rank = max(1, math.ceil(p * len(ordered)))
    return ordered[rank - 1]


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    elapsed = [float(row["elapsed"]) for row in rows]
    successes = sum(row.get("success", "false").lower() == "true" for row in rows)
    start = min(int(row["timeStamp"]) for row in rows)
    end = max(int(row["timeStamp"]) + int(row["elapsed"]) for row in rows)
    wall_seconds = max((end - start) / 1000.0, 0.001)
    return {
        "samples": len(rows),
        "successes": successes,
        "errors": len(rows) - successes,
        "error_rate_percent": round((len(rows) - successes) * 100 / len(rows), 4),
        "mean_ms": round(statistics.fmean(elapsed), 3),
        "min_ms": round(min(elapsed), 3),
        "max_ms": round(max(elapsed), 3),
        "p50_ms": percentile(elapsed, 0.50),
        "p90_ms": percentile(elapsed, 0.90),
        "p95_ms": percentile(elapsed, 0.95),
        "p99_ms": percentile(elapsed, 0.99),
        "throughput_samples_per_second": round(len(rows) / wall_seconds, 4),
        "wall_seconds": round(wall_seconds, 3),
        "start_epoch_ms": start,
        "end_epoch_ms": end,
    }


def analyze(path: Path, window_seconds: int) -> dict[str, object]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"No samples in {path}")
    required = {"timeStamp", "elapsed", "label", "success"}
    missing = required.difference(rows[0])
    if missing:
        raise ValueError(f"Missing required JTL fields: {sorted(missing)}")

    endpoint_rows = [row for row in rows if not row["label"].startswith("TC_")]
    by_label: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in endpoint_rows:
        by_label[row["label"]].append(row)

    start = min(int(row["timeStamp"]) for row in endpoint_rows)
    windows: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in endpoint_rows:
        bucket = (int(row["timeStamp"]) - start) // (window_seconds * 1000)
        windows[bucket].append(row)

    return {
        "source": str(path),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "percentile_method": "nearest-rank",
        "overall_endpoints_only": summarize(endpoint_rows),
        "by_label": {label: summarize(label_rows) for label, label_rows in sorted(by_label.items())},
        "time_windows": [
            {
                "window_start_seconds": bucket * window_seconds,
                "window_end_seconds": (bucket + 1) * window_seconds,
                **summarize(window_rows),
            }
            for bucket, window_rows in sorted(windows.items())
        ],
        "response_codes": dict(sorted(
            ((code, sum(row.get("responseCode") == code for row in endpoint_rows))
             for code in {row.get("responseCode", "") for row in endpoint_rows}),
            key=lambda item: item[0],
        )),
        "failure_messages": sorted({
            row.get("failureMessage", "")
            for row in endpoint_rows
            if row.get("success", "false").lower() != "true" and row.get("failureMessage", "")
        }),
    }


def markdown_report(result: dict[str, object]) -> str:
    overall = result["overall_endpoints_only"]
    lines = [
        f"# JTL analysis: {Path(result['source']).name}",
        "",
        f"Generated from the raw CSV JTL using the **{result['percentile_method']}** percentile method.",
        "Transaction Controller rows are excluded from endpoint totals to avoid double counting.",
        "",
        "## Overall endpoint metrics",
        "",
        "| Samples | Error % | Mean ms | p50 ms | p90 ms | p95 ms | p99 ms | Max ms | Samples/s |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| {overall['samples']} | {overall['error_rate_percent']} | {overall['mean_ms']} | {overall['p50_ms']} | {overall['p90_ms']} | {overall['p95_ms']} | {overall['p99_ms']} | {overall['max_ms']} | {overall['throughput_samples_per_second']} |",
        "",
        "## Per-label metrics",
        "",
        "| Label | Samples | Error % | Mean ms | p95 ms | p99 ms | Max ms | Samples/s |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label, metrics in result["by_label"].items():
        lines.append(
            f"| `{label}` | {metrics['samples']} | {metrics['error_rate_percent']} | "
            f"{metrics['mean_ms']} | {metrics['p95_ms']} | {metrics['p99_ms']} | "
            f"{metrics['max_ms']} | {metrics['throughput_samples_per_second']} |"
        )
    lines.extend(["", "## Response codes", "", "```json", json.dumps(result["response_codes"], indent=2), "```", ""])
    if result["failure_messages"]:
        lines.extend(["## Failure messages", ""])
        lines.extend(f"- {message}" for message in result["failure_messages"])
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("jtl", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--window-seconds", type=int, default=30)
    args = parser.parse_args()

    result = analyze(args.jtl, args.window_seconds)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    args.markdown.write_text(markdown_report(result), encoding="utf-8")
    print(json.dumps(result["overall_endpoints_only"], indent=2))


if __name__ == "__main__":
    main()


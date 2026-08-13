#!/usr/bin/env python3
"""Small reusable JTL checker for the EShop performance-testing skill."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def nearest_rank(values: list[int], fraction: float) -> int:
    values = sorted(values)
    return values[max(0, math.ceil(len(values) * fraction) - 1)]


def metrics(rows: list[dict[str, str]]) -> dict[str, object]:
    elapsed = [int(row["elapsed"]) for row in rows]
    failed = sum(row["success"].lower() != "true" for row in rows)
    start = min(int(row["timeStamp"]) for row in rows)
    end = max(int(row["timeStamp"]) + int(row["elapsed"]) for row in rows)
    seconds = max((end - start) / 1000, 0.001)
    return {
        "samples": len(rows),
        "errors": failed,
        "error_rate_percent": round(failed * 100 / len(rows), 4),
        "p50_ms": nearest_rank(elapsed, 0.50),
        "p95_ms": nearest_rank(elapsed, 0.95),
        "p99_ms": nearest_rank(elapsed, 0.99),
        "max_ms": max(elapsed),
        "samples_per_second": round(len(rows) / seconds, 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("jtl", type=Path)
    args = parser.parse_args()
    with args.jtl.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if not row["label"].startswith("TC_")]
    if not rows:
        raise SystemExit("No endpoint samples found")
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["label"]].append(row)
    output = {
        "overall": metrics(rows),
        "by_label": {label: metrics(group) for label, group in sorted(groups.items())},
        "response_codes": Counter(row.get("responseCode", "") for row in rows),
        "percentile_method": "nearest-rank",
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()


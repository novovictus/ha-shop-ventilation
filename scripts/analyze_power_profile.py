#!/usr/bin/env python3
"""Summarize a Home Assistant entity history CSV export.

Expected columns:
  entity_id,state,last_changed

This helper is intentionally small and dependency-free so the repository can
store analysis notes without requiring pandas or a Home Assistant API token.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path


def try_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: analyze_power_profile.py <history.csv>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    values: dict[str, list[float]] = defaultdict(list)

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            entity_id = row.get("entity_id", "")
            state = try_float(row.get("state", ""))
            if entity_id and state is not None:
                values[entity_id].append(state)

    for entity_id, readings in sorted(values.items()):
        if not readings:
            continue
        print(entity_id)
        print(f"  count: {len(readings)}")
        print(f"  min:   {min(readings)}")
        print(f"  max:   {max(readings)}")
        print(f"  avg:   {sum(readings) / len(readings):.3f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

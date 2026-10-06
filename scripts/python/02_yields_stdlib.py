#!/usr/bin/env python3
"""02_yields_stdlib.py — summarise plot yields with ONLY the standard library.

Shows the building blocks before pandas: csv, dictionaries, lists, loops,
functions, exceptions, and pathlib.

Usage:  python 02_yields_stdlib.py [path/to/plot_yields.csv]
"""
import csv
import statistics
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[2] / "datasets" / "field_trials" / "plot_yields.csv"


def parse_yield(text: str) -> float | None:
    """Return the yield as a float, or None if it is missing or impossible."""
    try:
        value = float(text)
    except ValueError:          # "NA", "" ...
        return None
    if not 0 < value < 25:      # maize yields outside 0-25 t/ha are data errors
        return None
    return value


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1

    by_variety: dict[str, list[float]] = {}
    skipped = 0
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            variety = row["variety"].strip().title()      # "amber " -> "Amber"
            y = parse_yield(row["yield_t_ha"])
            if y is None:
                skipped += 1
                continue
            by_variety.setdefault(variety, []).append(y)

    print(f"{'variety':<8} {'n':>5} {'mean':>7} {'sd':>6}")
    for variety in sorted(by_variety):
        values = by_variety[variety]
        print(f"{variety:<8} {len(values):>5} {statistics.mean(values):>7.2f} {statistics.stdev(values):>6.2f}")
    print(f"\nSkipped {skipped} rows with missing or impossible yields.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Generate a LARGE simulated sensor file for Module 7 (large-data processing).

The file is deliberately NOT stored in the repository (it is listed in
.gitignore). Generate it on demand:

    python3 datasets/make_large_dataset.py --rows 5000000 --out datasets/large/sensors_big.csv.gz

Approximate sizes (gzip-compressed / uncompressed):
    1,000,000 rows  ->  ~16 MB / ~ 55 MB
    5,000,000 rows  ->  ~80 MB / ~275 MB
   20,000,000 rows  -> ~320 MB / ~1.1 GB   (good for chunking practice)

Columns: timestamp, site, logger_id, soil_moisture_pct, soil_temp_c, battery_v
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import random
import sys
from pathlib import Path

SITES = ["AMES", "LINC", "MANH", "STPL", "URBN", "WLAF"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", type=int, default=1_000_000, help="number of data rows (default 1,000,000)")
    ap.add_argument("--out", type=Path, default=Path("datasets/large/sensors_big.csv.gz"),
                    help="output path; a .gz suffix means gzip-compressed")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    if args.rows <= 0:
        print("error: --rows must be positive", file=sys.stderr)
        return 2

    rng = random.Random(args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if args.out.suffix == ".gz" else open
    start = dt.datetime(2024, 1, 1)
    loggers = [f"{s}-L{i:02d}" for s in SITES for i in range(1, 9)]
    with opener(args.out, "wt") as fh:
        fh.write("timestamp,site,logger_id,soil_moisture_pct,soil_temp_c,battery_v\n")
        for i in range(args.rows):
            lid = loggers[i % len(loggers)]
            t = start + dt.timedelta(minutes=10 * (i // len(loggers)))
            moist = "NA" if rng.random() < 0.002 else f"{rng.gauss(27, 4):.2f}"
            fh.write(f"{t:%Y-%m-%dT%H:%M},{lid[:4]},{lid},{moist},{rng.gauss(19, 5):.2f},{rng.gauss(3.8, 0.1):.2f}\n")
            if i and i % 1_000_000 == 0:
                print(f"  ... {i:,} rows", file=sys.stderr)
    print(f"wrote {args.rows:,} rows to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

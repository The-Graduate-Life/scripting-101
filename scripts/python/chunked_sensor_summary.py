#!/usr/bin/env python3
"""chunked_sensor_summary.py — summarise a CSV that is too big for memory (Module 7).

Reads the file in chunks with pandas, keeps only small running totals,
and never holds the whole table in RAM.

Generate test data first:
    python datasets/make_large_dataset.py --rows 2000000 --out datasets/large/sensors_big.csv.gz

Usage:
    python chunked_sensor_summary.py datasets/large/sensors_big.csv.gz --chunksize 250000
    /usr/bin/time -v python chunked_sensor_summary.py ...    # see "Maximum resident set size"
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

import pandas as pd

log = logging.getLogger("chunked")

DTYPES = {"site": "category", "logger_id": "category",
          "soil_moisture_pct": "float32", "soil_temp_c": "float32", "battery_v": "float32"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", type=Path)
    ap.add_argument("--chunksize", type=int, default=250_000)
    ap.add_argument("--out", type=Path, default=Path("sensor_summary_by_site.csv"))
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    if not args.csv.is_file():
        log.error("input not found: %s", args.csv)
        return 1

    t0 = time.perf_counter()
    partials = []
    n_rows = 0
    reader = pd.read_csv(args.csv, usecols=list(DTYPES), dtype=DTYPES,
                         na_values=["NA"], chunksize=args.chunksize)
    for i, chunk in enumerate(reader, start=1):
        n_rows += len(chunk)
        # aggregate each chunk down to a tiny table of sums and counts
        g = chunk.groupby("site", observed=True).agg(
            moist_sum=("soil_moisture_pct", "sum"), moist_n=("soil_moisture_pct", "count"),
            temp_sum=("soil_temp_c", "sum"), temp_n=("soil_temp_c", "count"),
            batt_min=("battery_v", "min"))
        partials.append(g)
        log.info("chunk %d: %s rows processed", i, f"{n_rows:,}")

    combined = pd.concat(partials).groupby(level=0, observed=True).agg(
        {"moist_sum": "sum", "moist_n": "sum", "temp_sum": "sum", "temp_n": "sum", "batt_min": "min"})
    # combine SUMS and COUNTS, never average the chunk averages!
    result = pd.DataFrame({
        "readings": combined["moist_n"],
        "mean_soil_moisture_pct": (combined["moist_sum"] / combined["moist_n"]).round(3),
        "mean_soil_temp_c": (combined["temp_sum"] / combined["temp_n"]).round(3),
        "min_battery_v": combined["batt_min"].round(2),
    })
    result.to_csv(args.out)
    log.info("%s rows in %.1f s -> %s", f"{n_rows:,}", time.perf_counter() - t0, args.out)
    print(result.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

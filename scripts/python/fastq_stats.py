#!/usr/bin/env python3
"""fastq_stats.py — the Python twin of scripts/bash/fastq_qc.sh.

Compare the two to discuss when Bash or Python is the better tool:
Python is longer, but easier to extend (e.g. per-position quality, plots, tests).

Usage:
    python fastq_stats.py ../../datasets/genomics/reads/*.fastq.gz > qc.tsv
"""
from __future__ import annotations

import argparse
import gzip
import logging
import sys
from pathlib import Path
from typing import Iterator, TextIO

log = logging.getLogger("fastq_stats")


def open_text(path: Path) -> TextIO:
    """Open plain or gzip-compressed text transparently."""
    return gzip.open(path, "rt") if path.suffix == ".gz" else path.open()


def read_fastq(handle: TextIO) -> Iterator[tuple[str, str, str]]:
    """Yield (header, sequence, quality) one read at a time (streaming = low memory)."""
    while True:
        header = handle.readline().rstrip()
        if not header:
            return
        seq, plus, qual = (handle.readline().rstrip() for _ in range(3))
        if not header.startswith("@") or not plus.startswith("+") or len(seq) != len(qual):
            raise ValueError(f"malformed FASTQ record near {header!r}")
        yield header, seq, qual


def summarise(path: Path) -> dict[str, float | str]:
    reads = bases = gc = qsum = 0
    with open_text(path) as fh:
        for _header, seq, qual in read_fastq(fh):
            reads += 1
            bases += len(seq)
            gc += seq.count("G") + seq.count("C")
            qsum += sum(ord(c) - 33 for c in qual)
    if reads == 0:
        raise ValueError("no reads found")
    return {"sample": path.name.split(".")[0], "reads": reads, "bases": bases,
            "mean_length": round(bases / reads, 1), "gc_percent": round(100 * gc / bases, 2),
            "mean_quality": round(qsum / bases, 2)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Summarise FASTQ files (plain or .gz).")
    ap.add_argument("fastq", nargs="+", type=Path, help="FASTQ file(s)")
    ap.add_argument("--min-quality", type=float, default=28, help="warn below this mean quality")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")

    failures = 0
    print("sample\treads\tbases\tmean_length\tgc_percent\tmean_quality")
    for path in args.fastq:
        try:
            s = summarise(path)
        except (OSError, ValueError) as err:
            log.error("%s: %s", path, err)
            failures += 1
            continue
        print("\t".join(str(v) for v in s.values()))
        if s["mean_quality"] < args.min_quality:
            log.warning("%s: mean quality %.1f is below %.1f", s["sample"], s["mean_quality"], args.min_quality)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

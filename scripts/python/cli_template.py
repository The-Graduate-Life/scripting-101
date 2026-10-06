#!/usr/bin/env python3
"""cli_template.py — starting point for a production-quality Python command-line program.

Copy, rename, and fill in `run()`. The structure:
  parse arguments -> configure logging -> validate inputs -> do work -> return exit code
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

log = logging.getLogger(Path(__file__).stem)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", type=Path, help="input file(s)")
    ap.add_argument("-o", "--outdir", type=Path, default=Path("results"), help="output directory")
    ap.add_argument("-v", "--verbose", action="store_true", help="show debug messages")
    return ap.parse_args(argv)


def run(inputs: list[Path], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for path in inputs:
        log.info("processing %s", path)
        # ... real work goes here ...


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    missing = [p for p in args.inputs if not p.is_file()]
    if missing:
        log.error("missing input file(s): %s", ", ".join(map(str, missing)))
        return 1
    try:
        run(args.inputs, args.outdir)
    except Exception:                       # last-resort handler: log the traceback, fail cleanly
        log.exception("unexpected error")
        return 1
    return 0


if __name__ == "__main__":                  # runs only when executed, not when imported
    sys.exit(main())

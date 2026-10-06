#!/usr/bin/env python3
"""run_external_tools.py — calling command-line tools from Python safely (Module 6).

Key rules:
  * pass the command as a LIST of arguments (no shell=True -> no quoting bugs, no injection)
  * check=True turns a failing command into a Python exception
  * capture_output=True + text=True gives you stdout/stderr as strings
  * shutil.which() tells you whether the tool is installed / on PATH

Usage:  python run_external_tools.py ../../datasets/genomics/reads/S01.fastq.gz
"""
import shutil
import subprocess
import sys
from pathlib import Path


def count_lines_gz(path: Path) -> int:
    """Equivalent of the shell pipeline:  zcat FILE | wc -l"""
    zcat = subprocess.Popen(["zcat", str(path)], stdout=subprocess.PIPE)
    wc = subprocess.run(["wc", "-l"], stdin=zcat.stdout, capture_output=True, text=True, check=True)
    zcat.stdout.close()
    if zcat.wait() != 0:
        raise subprocess.CalledProcessError(zcat.returncode, "zcat")
    return int(wc.stdout.strip())


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    fq = Path(sys.argv[1])

    lines = count_lines_gz(fq)
    print(f"{fq.name}: {lines} lines = {lines // 4} reads")

    if shutil.which("seqkit"):
        result = subprocess.run(["seqkit", "stats", "--tabular", str(fq)],
                                capture_output=True, text=True, check=True)
        header, values = result.stdout.strip().split("\n")
        stats = dict(zip(header.split("\t"), values.split("\t")))
        print(f"seqkit says: {stats['num_seqs']} reads, average length {stats['avg_len']}")
    else:
        print("seqkit not found — activate the course environment:  conda activate scripting101")

    try:
        subprocess.run(["ls", "/no/such/dir"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as err:
        print(f"As expected, ls failed with exit code {err.returncode}: {err.stderr.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

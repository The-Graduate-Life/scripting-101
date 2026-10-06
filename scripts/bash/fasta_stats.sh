#!/usr/bin/env bash
# fasta_stats.sh — per-sequence length and GC content for a FASTA file (plain or .gz).
#
# Usage: ./fasta_stats.sh reference.fasta[.gz]
# Output (TSV): id  length  gc_percent
set -euo pipefail

[[ $# -eq 1 ]] || { echo "Usage: $0 FASTA" >&2; exit 1; }
[[ -r $1 ]]    || { echo "Error: cannot read '$1'" >&2; exit 1; }

# zcat -f reads both compressed and uncompressed input — handy for pipelines.
zcat -f -- "$1" | awk '
    function report() {
        if (id != "") printf "%s\t%d\t%.2f\n", id, len, (len ? 100 * gc / len : 0)
    }
    BEGIN { print "id\tlength\tgc_percent" }
    /^>/  { report(); id = substr($1, 2); len = 0; gc = 0; next }
          { seq = toupper($0); len += length(seq); gc += gsub(/[GC]/, "", seq) }
    END   { report() }
'

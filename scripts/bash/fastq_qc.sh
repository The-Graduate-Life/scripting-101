#!/usr/bin/env bash
# fastq_qc.sh — quality-control summary for many FASTQ(.gz) files, in parallel.
#
# Demonstrates the "production Bash" patterns taught in Module 2:
#   strict mode, getopts, input validation, logging, trap, functions,
#   parallel processing with xargs -P, and organised outputs.
#
# Usage:
#   ./fastq_qc.sh [-o OUTDIR] [-j JOBS] [-a ADAPTER] [-h] FASTQ [FASTQ ...]
#
# Example:
#   ./fastq_qc.sh -o qc_out -j 4 ../../datasets/genomics/reads/*.fastq.gz
#
# Outputs:
#   OUTDIR/per_sample/<sample>.tsv   one row per input file
#   OUTDIR/qc_summary.tsv            all samples combined
#   OUTDIR/fastq_qc.log              log of the run
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=lib/logging.sh
source "$SCRIPT_DIR/lib/logging.sh"

usage() {
    sed -n '2,/^set -euo/p' "$0" | sed '$d; s/^# \{0,1\}//'
}

# ---- defaults ----------------------------------------------------------------
outdir="qc_results"
jobs=2
adapter="AGATCGGAAGAGC"

# ---- parse options -----------------------------------------------------------
while getopts ":o:j:a:h" opt; do
    case $opt in
        o) outdir=$OPTARG ;;
        j) jobs=$OPTARG ;;
        a) adapter=$OPTARG ;;
        h) usage; exit 0 ;;
        :) die "option -$OPTARG needs a value (see -h)" 2 ;;
        \?) die "unknown option -$OPTARG (see -h)" 2 ;;
    esac
done
shift $(( OPTIND - 1 ))           # remaining arguments are the FASTQ files

# ---- validate inputs ---------------------------------------------------------
[[ $# -ge 1 ]] || { usage >&2; die "no FASTQ files given" 2; }
[[ $jobs =~ ^[1-9][0-9]*$ ]] || die "-j must be a positive integer, got '$jobs'" 2
[[ $adapter =~ ^[ACGTN]+$ ]] || die "-a must be a DNA sequence, got '$adapter'" 2
require_cmd awk zcat xargs

for f in "$@"; do
    [[ -s $f ]] || die "input missing or empty: $f"
done

mkdir -p "$outdir/per_sample"
LOG_FILE="$outdir/fastq_qc.log"
export LOG_FILE
: > "$LOG_FILE"

tmpdir=$(mktemp -d)
cleanup() {
    local status=$?
    rm -rf "$tmpdir"
    if (( status != 0 )); then
        log_error "pipeline FAILED with exit status $status"
    fi
}
trap cleanup EXIT                       # always runs, even after an error

log_info "starting fastq_qc on $# file(s) with $jobs parallel job(s)"
log_info "output directory: $outdir"

# ---- the work for ONE file ---------------------------------------------------
qc_one() {
    local fq=$1 outdir=$2 adapter=$3
    local sample
    sample=$(basename "$fq")
    sample=${sample%%.f*q*}                   # S01.fastq.gz -> S01

    # FASTQ = 4 lines per read: header, sequence, '+', quality.
    zcat -f -- "$fq" | awk -v s="$sample" -v ad="$adapter" '
        BEGIN { for (i = 33; i <= 126; i++) ord[sprintf("%c", i)] = i - 33 }
        NR % 4 == 2 { reads++; len = length($0); bases += len
                      seq = $0; gc += gsub(/[GC]/, "", seq)
                      seq = $0; n  += gsub(/N/, "", seq)
                      if (index($0, ad)) with_adapter++ }
        NR % 4 == 0 { for (i = 1; i <= length($0); i++) qsum += ord[substr($0, i, 1)] }
        END {
            if (NR % 4 != 0) { print "truncated FASTQ (" NR " lines)" > "/dev/stderr"; exit 3 }
            printf "%s\t%d\t%d\t%.1f\t%.2f\t%.2f\t%.2f\t%.3f\n", s, reads, bases,
                   bases / reads, 100 * gc / bases, qsum / bases, 100 * with_adapter / reads, 100 * n / bases
        }' > "$outdir/per_sample/$sample.tsv"
    log_info "done: $sample"
}
export -f qc_one _log log_info

# ---- run in parallel ---------------------------------------------------------
# printf '%s\0' + xargs -0 is safe even for file names that contain spaces.
if ! printf '%s\0' "$@" \
    | xargs -0 -P "$jobs" -I{} bash -c 'qc_one "$1" "$2" "$3"' _ {} "$outdir" "$adapter"; then
    die "one or more files failed QC — see $LOG_FILE"
fi

# ---- combine -----------------------------------------------------------------
{
    printf "sample\treads\tbases\tmean_length\tgc_percent\tmean_quality\tpct_adapter\tpct_N\n"
    sort "$outdir"/per_sample/*.tsv
} > "$outdir/qc_summary.tsv"

# flag samples with low mean quality (< 28) — a simple QC rule
awk -F'\t' 'NR > 1 && $6 < 28 { print $1 }' "$outdir/qc_summary.tsv" | while read -r s; do
    log_warn "sample $s has mean quality below 28"
done

log_info "summary written to $outdir/qc_summary.tsv"

#!/usr/bin/env bash
# script_template.sh — copy this file to start a new, robust Bash script.
#
# Usage: script_template.sh [-v] [-o OUTDIR] INPUT...
#
#   -o OUTDIR   where to write results (default: results)
#   -v          verbose: print each command as it runs (set -x)
#   -h          show this help
set -euo pipefail          # stop on errors, unset variables, and failed pipes
IFS=$'\n\t'                # safer word splitting (spaces in names are less dangerous)

usage() { sed -n '3,9p' "$0" | sed 's/^# \{0,1\}//'; }

outdir="results"
while getopts ":o:vh" opt; do
    case $opt in
        o) outdir=$OPTARG ;;
        v) set -x ;;
        h) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done
shift $(( OPTIND - 1 ))
[[ $# -ge 1 ]] || { usage >&2; exit 2; }

mkdir -p "$outdir"
trap 'echo "Error on line $LINENO (exit $?)" >&2' ERR

for input in "$@"; do
    [[ -r $input ]] || { echo "Cannot read: $input" >&2; exit 1; }
    echo "Processing $input -> $outdir/"
    # ... real work goes here ...
done

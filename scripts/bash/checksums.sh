#!/usr/bin/env bash
# checksums.sh — create or verify SHA-256 checksums for every file in a directory tree.
#
# Usage:
#   ./checksums.sh create DIR     # writes DIR/SHA256SUMS
#   ./checksums.sh verify DIR     # checks files against DIR/SHA256SUMS
set -euo pipefail

mode=${1:-}
dir=${2:-}
[[ $mode == create || $mode == verify ]] && [[ -d $dir ]] \
    || { echo "Usage: $0 create|verify DIR" >&2; exit 2; }

cd "$dir"
case $mode in
    create)
        # -print0 / -0 keep file names with spaces intact; sort makes output reproducible
        find . -type f ! -name SHA256SUMS ! -name MD5SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
        echo "Wrote $(wc -l < SHA256SUMS) checksums to $dir/SHA256SUMS"
        ;;
    verify)
        [[ -f SHA256SUMS ]] || { echo "No SHA256SUMS file in $dir" >&2; exit 1; }
        if sha256sum --check --quiet SHA256SUMS; then
            echo "All files OK"
        else
            echo "Checksum MISMATCH — data may be corrupted or modified" >&2
            exit 1
        fi
        ;;
esac

#!/usr/bin/env bash
# vcf_summary.sh — count variants per chromosome, by type and filter status.
#
# Usage: ./vcf_summary.sh variants.vcf.gz [MIN_QUAL]
set -euo pipefail

vcf=${1:?Usage: $0 VCF[.gz] [MIN_QUAL]}
min_qual=${2:-30}

echo "# Variants with QUAL >= $min_qual, by chromosome and type"
zcat -f -- "$vcf" \
  | grep -v '^#' \
  | awk -F'\t' -v q="$min_qual" '$6 >= q {
        match($8, /TYPE=[a-z]+/)
        type = substr($8, RSTART + 5, RLENGTH - 5)
        count[$1 "\t" type]++
    }
    END { for (k in count) print k "\t" count[k] }' \
  | sort -k1,1V -k2,2 \
  | (printf "chrom\ttype\tn\n"; cat)

echo
echo "# FILTER column counts"
zcat -f -- "$vcf" | grep -v '^#' | cut -f7 | sort | uniq -c | sort -rn

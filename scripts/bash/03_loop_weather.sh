#!/usr/bin/env bash
# 03_loop_weather.sh — loop over many files and build a summary table.
#
# For every weather file, report total season rainfall and mean maximum temperature.
# Missing rainfall is recorded as -9999 by the stations and must be skipped.
#
# Usage: ./03_loop_weather.sh [WEATHER_DIR] > season_summary.tsv
set -euo pipefail

weather_dir=${1:-../../datasets/weather}
[[ -d $weather_dir ]] || { echo "Error: directory not found: $weather_dir" >&2; exit 1; }

printf "site\tyear\tdays\tmissing_precip\ttotal_precip_mm\tmean_tmax_c\n"

for file in "$weather_dir"/weather_*_*.csv; do
    base=$(basename "$file" .csv)          # weather_AMES_2020
    site=$(echo "$base" | cut -d_ -f2)     # AMES
    year=${base##*_}                       # 2020  (parameter expansion: strip up to last _)

    awk -F, -v site="$site" -v year="$year" '
        NR == 1 { next }                                  # skip header
        { days++; tmax += $3 }
        $4 == -9999 { missing++; next }                   # sentinel value = missing
        { rain += $4 }
        END { printf "%s\t%s\t%d\t%d\t%.1f\t%.2f\n", site, year, days, missing, rain, tmax / days }
    ' "$file"
done

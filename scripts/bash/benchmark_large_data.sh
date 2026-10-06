#!/usr/bin/env bash
# benchmark_large_data.sh — Lab 09: compare strategies for one large file.
#
# Usage: ./benchmark_large_data.sh BIG.csv.gz [JOBS]
# Prints wall time and peak memory for each strategy computing the same answer:
# mean soil moisture per site.
#
# Requires: the scripting101 conda env (pandas, pigz, GNU parallel), /usr/bin/time
set -euo pipefail

big=${1:?Usage: $0 BIG.csv.gz [JOBS]}
jobs=${2:-$(nproc)}
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
course=$(cd "$here/../.." && pwd)   # repository root (script lives in scripts/bash/)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

measure() {    # measure LABEL COMMAND...
    local label=$1; shift
    /usr/bin/time -f "%e %M" -o "$work/time" "$@" > "$work/out" 2> /dev/null
    read -r secs kb < "$work/time"
    printf "%-38s %8.1f s %10.0f MB\n" "$label" "$secs" "$(( kb / 1024 ))"
}

echo "file: $big ($(du -h "$big" | cut -f1) compressed), $(nproc) CPUs, using $jobs jobs"
printf "%-38s %10s %13s\n" "strategy" "time" "peak memory"

# 1. streaming: decompress -> awk, constant memory
measure "zcat | awk (streaming)" bash -c "zcat '$big' | awk -F, 'NR>1 && \$4!=\"NA\" {s[\$2]+=\$4; n[\$2]++} END {for (k in s) print k, s[k]/n[k]}'"

# 2. pandas, whole file in memory
measure "pandas read_csv (whole file)" python -c "
import pandas as pd
df = pd.read_csv('$big')
print(df.groupby('site')['soil_moisture_pct'].mean())"

# 3. pandas, only needed columns + compact dtypes
measure "pandas usecols + dtype" python -c "
import pandas as pd
df = pd.read_csv('$big', usecols=['site','soil_moisture_pct'], dtype={'site':'category','soil_moisture_pct':'float32'})
print(df.groupby('site', observed=True)['soil_moisture_pct'].mean())"

# 4. pandas in chunks
measure "pandas chunks (250k rows)" python "$course/scripts/python/chunked_sensor_summary.py" "$big" --out "$work/chunk.csv"

# 5. decompression speed: gzip vs pigz
measure "zcat > /dev/null (decompress only)" bash -c "zcat '$big' > /dev/null"
zcat "$big" > "$work/plain.csv"
measure "gzip -c (compress, 1 core)" bash -c "gzip -c '$work/plain.csv' > /dev/null"
if command -v pigz > /dev/null; then
    measure "pigz -dc (decompress)" bash -c "pigz -dc '$big' > /dev/null"
    measure "pigz -p $jobs -c (compress, $jobs cores)" bash -c "pigz -p '$jobs' -c '$work/plain.csv' > /dev/null"
fi
rm -f "$work/plain.csv"

# 6. split into pieces + parallel awk, then combine sums and counts
zcat "$big" | tail -n +2 | split -l 500000 -d - "$work/part_"
measure "split + parallel awk (-P $jobs)" bash -c "
ls '$work'/part_* | xargs -P '$jobs' -I{} awk -F, '\$4!=\"NA\" {s[\$2]+=\$4; n[\$2]++} END {for (k in s) print k, s[k], n[k]}' {} > '$work/partials'
awk '{s[\$1]+=\$2; n[\$1]+=\$3} END {for (k in s) print k, s[k]/n[k]}' '$work/partials'"

echo
echo "Answer from the last strategy (compare with the others by running them by hand):"
sort "$work/out"

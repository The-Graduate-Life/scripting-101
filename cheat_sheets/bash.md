# Bash Scripting Cheat Sheet

## Script skeleton
```bash
#!/usr/bin/env bash
# what it does · Usage: name.sh [-o DIR] FILE...
set -euo pipefail                      # stop on error / unset var / failed pipe
trap 'rm -rf "$tmp"' EXIT              # always clean up
```
Run: `bash s.sh` or `chmod +x s.sh && ./s.sh`

## Variables
```bash
x=5                    # no spaces!
echo "$x" "${x}_suffix"
y=$(date +%F)          # command substitution
z=$(( x * 2 ))         # integer arithmetic (decimals: use awk/bc)
v=${1:-default}        # default    v=${1:?message}  # required
readonly CONST=1 ; local inside_function=1 ; export TO_CHILDREN=1
```
`"double"` expands · `'single'` literal · **always quote `"$var"`**

## Special variables
`$0` script · `$1..$9` args · `$#` count · `"$@"` all args · `$?` last exit code · `$$` PID · `$!` last bg PID · `$LINENO`

## Tests
```bash
if [[ -f $f && -s $f ]]; then ...; elif ...; else ...; fi
```
| Files | Strings | Numbers |
|---|---|---|
| `-e` exists `-f` file `-d` dir `-s` non-empty `-r` readable `-x` executable | `==` `!=` `-z` empty `-n` non-empty `=~` regex | `-eq -ne -lt -le -gt -ge` or `(( a < b ))` |

## case
```bash
case $x in
  a|b) ... ;;
  *.gz) ... ;;
  *) ... ;;
esac
```

## Loops
```bash
for f in *.csv; do ...; done
for i in {1..5}; do ...; done
for (( i=0; i<5; i++ )); do ...; done
while IFS= read -r line; do ...; done < file
find . -name '*.csv' -print0 | while IFS= read -r -d '' f; do ...; done
break / continue
```

## Parameter expansion  (`f=dir/name_2020.csv`)
| | | | |
|---|---|---|---|
| `${f##*/}` → `name_2020.csv` | `${f%/*}` → `dir` | `${f%.csv}` → `dir/name_2020` | `${f##*_}` → `2020.csv` |
| `${f/2020/2021}` replace | `${#f}` length | `${f^^}` upper | `${f,,}` lower |

## Functions and arrays
```bash
fn() { local a=$1; echo "$a"; return 0; }
out=$(fn "x")
arr=(a b c); arr+=(d); echo "${arr[0]}" "${#arr[@]}"; for x in "${arr[@]}"; do ...; done
mapfile -t lines < file
```

## Input / output
```bash
read -r -p "Name? " name
echo "msg" >&2                      # to stderr (logs, errors)
printf "%s\t%.2f\n" "$a" "$b"
cmd > out.txt 2> err.txt
```

## getopts
```bash
while getopts ":i:o:vh" opt; do
  case $opt in
    i) in=$OPTARG ;;  o) out=$OPTARG ;;  v) set -x ;;  h) usage; exit 0 ;;
    :) echo "-$OPTARG needs a value" >&2; exit 2 ;;
    \?) echo "unknown -$OPTARG" >&2; exit 2 ;;
  esac
done
shift $(( OPTIND - 1 ))
```

## Logging
```bash
log() { echo "$(date '+%F %T') [$1] ${*:2}" | tee -a "$LOG_FILE" >&2; }
exec > >(tee -a run.log) 2>&1      # mirror everything to a log from here on
```

## Text processing
```bash
grep -E 'a|b' f · grep -v '^#' f · grep -c x f · grep -rl x dir
sed 's/a/b/g' f · sed -n '2,5p' f · sed '1d' f · sed 's/\r$//' f · sed -i.bak ... f
awk -F, 'NR>1 && $3>5 {print $1, $3}' f
awk -F, 'NR>1 {s[$2]+=$8; n[$2]++} END {for (k in s) print k, s[k]/n[k]}' f
awk -F'\t' -v OFS='\t' -v t="$thr" '$5 < t' f
```

## Many files / parallel
```bash
find d -name '*.gz' -print0 | xargs -0 -P 4 -n 1 CMD
export -f fn; printf '%s\0' *.csv | xargs -0 -P 4 -I{} bash -c 'fn "$1"' _ {}
parallel -j 4 --bar 'CMD {} > {/.}.out' ::: files*
```

## Processes
`cmd &` · `jobs` · `fg %1` · `bg %1` · Ctrl+Z · `ps aux | grep '[x]'` · `kill PID` / `kill -9` · `nohup cmd > log 2>&1 &` · `top` / `htop` · `/usr/bin/time -v cmd`

## Exit codes
`exit 0` ok · `1` error · `2` usage · `127` command not found · `130` Ctrl+C · `141` SIGPIPE
`grep -q x f && echo yes || echo no` · `cmd || true` (allow failure under `set -e`)

## Debug
`bash -x script.sh` · `set -x` / `set +x` · `shellcheck script.sh`

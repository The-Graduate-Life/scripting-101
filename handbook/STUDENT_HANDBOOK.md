# Scripting 101 — Student Handbook

*A reference to keep after the course. For one-page summaries, see the cheat sheets (`cheat_sheets/` folder).*

## Contents

1. [Setup at a glance](#1-setup-at-a-glance)
2. [Linux and the command line](#2-linux-and-the-command-line)
3. [Working with files and text](#3-working-with-files-and-text)
4. [Bash scripting](#4-bash-scripting)
5. [Text processing: grep, sed, awk](#5-text-processing-grep-sed-awk)
6. [Batch, parallel and processes](#6-batch-parallel-and-processes)
7. [Conda](#7-conda)
8. [Python essentials](#8-python-essentials)
9. [Data analysis: pandas, NumPy, SciPy, Matplotlib](#9-data-analysis-pandas-numpy-scipy-matplotlib)
10. [Git and GitHub](#10-git-and-github)
11. [Integrating everything: project template](#11-integrating-everything-project-template)
12. [Large data and HPC](#12-large-data-and-hpc)
13. [Troubleshooting](#13-troubleshooting)
14. [Best practices checklist](#14-best-practices-checklist)
15. [Glossary](#15-glossary)

---

## 1. Setup at a glance

```bash
# Windows PowerShell (as Administrator), once:
wsl --install                      # installs WSL 2 + Ubuntu; reboot

# Ubuntu, once:
sudo apt update && sudo apt install -y build-essential curl git zip unzip tree plocate dos2unix htop shellcheck
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-Linux-x86_64.sh -b -p ~/miniforge3 && ~/miniforge3/bin/conda init bash && exec bash
git clone https://github.com/<instructor>/scripting-101.git ~/scripting-101
conda env create -f ~/scripting-101/environment.yml
conda activate scripting101
```

Full guide: [`resources/wsl_setup.md`](../resources/wsl_setup.md). **Keep your projects in `~` (Linux), not `/mnt/c` (Windows).**

---

## 2. Linux and the command line

| Term | Meaning |
|---|---|
| Linux | operating system used by most servers and clusters |
| WSL | Windows Subsystem for Linux: real Linux inside Windows |
| Terminal | the window that shows text |
| Shell / Bash | the program that interprets your commands (Bash is the most common shell) |
| Prompt | `user@host:~/dir$`: ready for input |

### Paths

| Symbol | Meaning |
|---|---|
| `/` | root of the filesystem |
| `~` | your home folder (`/home/<you>`) |
| `.` / `..` | current folder / parent folder |
| `/mnt/c/Users/<Name>` | your Windows user folder seen from WSL |
| absolute path | starts with `/`: `/home/ada/data/x.csv` |
| relative path | from where you are: `../data/x.csv` |

### Navigation and help

```bash
pwd                      # where am I?
ls -lah                  # list: long, all (hidden too), human sizes
cd dir / cd .. / cd / cd -   # move; up; home; back
mkdir -p a/b/c           # make nested folders
man ls / ls --help       # help (q to quit man)
which python; type cd    # which program runs?
history | tail; Ctrl+R   # previous commands
```

Keys: **Tab** complete · **↑↓** history · **Ctrl+C** cancel · **Ctrl+L** clear · **Ctrl+A/E** line start/end · **Ctrl+D** exit.

### Environment variables

```bash
echo $HOME $USER $PWD
echo $PATH | tr ':' '\n'      # where commands are searched, in order
export PROJECT=~/projects/harvest
```

---

## 3. Working with files and text

### Manage

```bash
touch f.txt                   # create empty / update timestamp
cp src dst ; cp -r dir1 dir2  # copy (‑r for folders)
mv old new                    # move or rename
rm f ; rm -r dir ; rm -i f    # delete (no recycle bin!) ; ask first
rmdir emptydir
ln -s /path/to/target link    # symbolic link (pointer, no copy)
```

### Look

```bash
cat f        less -S f       head -n 5 f      tail -n 5 f     tail -f log
wc -l f      file f          du -sh dir       df -h           tree -L 2
```

### Wildcards

`*` any characters · `?` one character · `[0-9]` one character from a set · `{a,b}` alternatives (brace expansion: `mkdir {raw,clean}`).

### Pipes and redirection

```text
cmd > out        stdout to file (overwrite)       cmd 2> err      stderr to file
cmd >> out       append                           cmd > all 2>&1  both into one file
cmd < in         stdin from file                  cmd1 | cmd2     stdout of cmd1 → stdin of cmd2
cmd1 && cmd2     cmd2 only if cmd1 succeeded      cmd1 || cmd2    cmd2 only if cmd1 failed
cmd1 ; cmd2      always both                      cmd > /dev/null discard output
```

### Column tools

```bash
cut -d, -f2,5 f.csv                   # columns 2 and 5 of a CSV (cut -f for TSV)
sort -t, -k8,8gr f.csv                # sort by column 8, numeric, descending
sort | uniq -c | sort -rn             # frequency table
paste -d'\t' a.txt b.txt              # glue files side by side
tr ',' '\t' < f.csv                   # translate characters
tail -n +2 f.csv                      # everything except the header
```

### Find

```bash
find . -name "*.csv"                  find . -type f -empty
find . -name "*.gz" -size +100M       find . -mtime -1        # changed in last day
locate file_name                      # fast, uses a database (sudo updatedb)
```

### Permissions

```text
-rwxr-xr--   type | user | group | others       r=4 w=2 x=1
chmod u+x script.sh      chmod 755 script.sh     chmod a-w raw.csv (read-only)
```

### Compression and archives

```bash
gzip f / gunzip f.gz / zcat f.gz | head      # single file
tar -czvf out.tar.gz dir/                     # create
tar -tzf out.tar.gz                           # list
tar -xzf out.tar.gz -C target/                # extract
zip -r out.zip dir/ ; unzip -l out.zip ; unzip out.zip
```

---

## 4. Bash scripting

### Skeleton

```bash
#!/usr/bin/env bash
# name.sh — what it does
# Usage: name.sh [-o OUTDIR] INPUT...
set -euo pipefail

outdir="results"
while getopts ":o:h" opt; do
    case $opt in
        o) outdir=$OPTARG ;;
        h) sed -n '2,3p' "$0"; exit 0 ;;
        *) echo "bad option" >&2; exit 2 ;;
    esac
done
shift $(( OPTIND - 1 ))
[[ $# -ge 1 ]] || { echo "Usage: $0 [-o OUTDIR] INPUT..." >&2; exit 2; }

mkdir -p "$outdir"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
for f in "$@"; do
    [[ -r $f ]] || { echo "cannot read $f" >&2; exit 1; }
    echo "processing $f" >&2
done
```

Run: `bash name.sh …` or `chmod +x name.sh && ./name.sh …`. Copy from `scripts/bash/script_template.sh`.

### Variables, quoting, substitution

```bash
name="AMES"                 # no spaces around =
echo "$name ${name}_2023"   # "double": expand ; 'single': literal
today=$(date +%F)           # command substitution
n=$(( 3 * 4 ))              # integer arithmetic
echo "${1:-default}"        # default value
readonly PI=3.14
```

**Always quote variables:** `"$f"`, `"$@"`.

### Special variables

| | |
|---|---|
| `$0` | script name |
| `$1 … $9`, `${10}` | arguments |
| `$#` | number of arguments |
| `"$@"` | all arguments, separately quoted |
| `$?` | exit code of the last command |
| `$$` / `$!` | PID of this shell / of the last background job |

### Conditions

```bash
if [[ -f $f && -s $f ]]; then ...; elif [[ $x == "a" ]]; then ...; else ...; fi
(( n > 5 )) && echo big
case $ext in
    csv|tsv) echo table ;;
    *.gz)    echo compressed ;;
    *)       echo other ;;
esac
```

| Files | Strings | Integers |
|---|---|---|
| `-e` exists, `-f` file, `-d` dir, `-s` non-empty, `-r` readable, `-x` executable | `==`, `!=`, `-z` empty, `-n` non-empty, `=~` regex | `-eq -ne -lt -le -gt -ge` or `(( ))` |

### Loops

```bash
for f in data/*.csv; do echo "$f"; done
for i in {1..10}; do ...; done
for (( i=0; i<10; i++ )); do ...; done
while IFS= read -r line; do ...; done < file.txt
find . -name '*.csv' -print0 | while IFS= read -r -d '' f; do ...; done
```

### Parameter expansion (`f=data/weather_AMES_2020.csv`)

| Expression | Result |
|---|---|
| `${f##*/}` (or `basename "$f"`) | `weather_AMES_2020.csv` |
| `${f%/*}` (or `dirname "$f"`) | `data` |
| `${f%.csv}` | `data/weather_AMES_2020` |
| `${f/AMES/LINC}` | `data/weather_LINC_2020.csv` |
| `${#f}` | length |
| `${f^^}` / `${f,,}` | upper / lower case |

### Functions and arrays

```bash
mean() { local file=$1; awk '{s+=$1} END {print s/NR}' "$file"; }
result=$(mean values.txt)

samples=(S01 S02 S03)
samples+=(S04)
echo "${samples[0]} ${#samples[@]}"
for s in "${samples[@]}"; do ...; done
mapfile -t lines < file.txt             # file → array
```

### Exit codes and error handling

* `exit 0` success; non-zero = failure (use 1 runtime, 2 usage by convention).
* `set -e` stop on error · `set -u` unset vars are errors · `set -o pipefail` failing pipe stage fails the pipe.
* `trap 'cleanup' EXIT` · `trap 'echo "error at line $LINENO" >&2' ERR`.
* Logs and errors to **stderr**: `echo "msg" >&2`.

### Reading input

```bash
read -r -p "Site? " site
```

---

## 5. Text processing: grep, sed, awk

### grep: filter lines

```bash
grep pattern f        grep -i (ignore case)   -v (invert)    -c (count)   -n (line numbers)
grep -w word f        -x (whole line)          -E 'a|b' (extended regex)  -r (recursive)  -l (files only)
grep -q pat f && echo found                    # quiet: just the exit code
```

### sed: edit streams

```bash
sed 's/old/new/'  f       # first occurrence per line     sed 's/old/new/g' f   # all
sed -n '2,5p' f           # print lines 2-5               sed '1d' f            # delete header
sed 's/\r$//' f           # strip Windows CR              sed -i.bak 's/a/b/g' f   # edit in place (+backup)
sed -E 's/([A-Z]+)-([0-9]+)/\2_\1/' f                      # capture groups
```

### awk: compute on columns

```text
awk -F'<sep>' 'PATTERN { ACTION } END { FINAL }' file
$1..$NF fields, $0 line, NR line number, NF number of fields, OFS output separator
```

```bash
awk -F, 'NR>1 {print $2, $8}' f.csv                           # columns
awk -F, 'NR>1 && $8 > 10' f.csv                              # filter
awk -F, 'NR>1 {s+=$8; n++} END {print s/n}' f.csv            # mean
awk -F, 'NR>1 {s[$2]+=$8; n[$2]++} END {for (k in s) print k, s[k]/n[k]}' f.csv   # group-by
awk -F'\t' -v OFS='\t' '{print $1, $3}' f.tsv                # TSV in/out
awk -v min=20 '$3 < min' f                                   # pass a shell value
zcat reads.fastq.gz | awk 'NR % 4 == 2 {n++; bp+=length($0)} END {print n, bp/n}'   # FASTQ reads, mean length
```

### Regular expressions (basics)

| | | | |
|---|---|---|---|
| `.` any char | `*` 0+ | `+` 1+ (ERE) | `?` 0/1 (ERE) |
| `^` line start | `$` line end | `[ACGT]` set | `[^#]` not |
| `\d` (Python/PCRE) / `[0-9]` | `{3}` exactly 3 | `( )` group | `a\|b` or |

---

## 6. Batch, parallel and processes

```bash
# many files safely
find data -name '*.csv' -print0 | xargs -0 -n 20 wc -l
# in parallel (4 at a time), one output per input
find data -name '*.fastq.gz' -print0 | xargs -0 -P 4 -I{} sh -c 'zcat "$1" | wc -l > "$1.count"' _ {}
# GNU parallel
parallel -j 4 --bar 'zcat {} | wc -l > {/.}.count' ::: data/*.fastq.gz
# use a function in xargs
myfn() { ...; }; export -f myfn; printf '%s\0' *.csv | xargs -0 -P 4 -I{} bash -c 'myfn "$1"' _ {}
```

| Processes | |
|---|---|
| `cmd &` | run in background |
| `jobs`, `fg %1`, `bg %1`, `Ctrl+Z` | job control |
| `ps aux \| grep '[n]ame'`, `pgrep -af name` | find processes |
| `top`, `htop` | live monitor |
| `kill PID` / `kill -9 PID` | stop politely / force |
| `nohup cmd > log 2>&1 &` | survive logout |
| `tmux` | persistent terminal sessions on servers |
| `/usr/bin/time -v cmd` | time + peak memory |

---

## 7. Conda

```bash
conda create -n NAME python=3.12 pandas      conda activate NAME / conda deactivate
conda install -c conda-forge PKG              conda remove PKG
conda list [PKG]                              conda env list
conda env export --from-history > environment.yml
conda env create -f environment.yml           conda env update -f environment.yml --prune
conda env remove -n NAME                      conda clean --all
conda search -c bioconda seqkit               conda run -n NAME python script.py
```

```yaml
# environment.yml
name: myproject
channels: [conda-forge, bioconda]
dependencies:
  - python=3.12
  - pandas>=2.2
  - matplotlib
  - seqkit
  - pip
  - pip: [some-pypi-only-package]
```

* One environment per project; never install into `base`.
* Channel order: conda-forge first; `conda config --set channel_priority strict`.
* In scripts: `eval "$(conda shell.bash hook)"; conda activate NAME`.
* Check: `which python`, `python -c "import sys; print(sys.executable)"`.

---

## 8. Python essentials

### Types and operators

```python
x = 3            # int        y = 2.5   # float      s = "ATG"  # str     ok = True  # bool
7 // 2  # 3      7 % 2  # 1    2 ** 3  # 8     == != < <= > >=    and or not    in
f"{name}: {value:.2f}"        # f-string formatting
int("3"), float("2.5"), str(3)
```

### Strings

```python
s[0], s[-1], s[1:4], s[::-1]       len(s)     s.upper() s.lower() s.strip()
s.split(","), ",".join(items)       s.replace("T", "U")    s.startswith(">")    "GC" in s
s.count("G")                         s.translate(str.maketrans("ACGT", "TGCA"))
```

### Collections

```python
lst = [1, 2]; lst.append(3); lst[0]; lst[-1]; len(lst); sorted(lst); lst.sort()
tup = (42.0, -93.6); lat, lon = tup
d = {"site": "AMES"}; d["year"] = 2023; d.get("x", default); d.items(); d.keys()
st = {"A", "B"}; st.add("C"); "A" in st; st1 | st2; st1 & st2
[x * 2 for x in lst if x > 1]          {k: v for k, v in d.items()}     {x.lower() for x in names}
```

### Control flow

```python
if a > 0:
    ...
elif a == 0:
    ...
else:
    ...
for item in items:            for i, item in enumerate(items):        for a, b in zip(xs, ys):
    ...                           ...                                     ...
while cond:
    ...
break / continue
```

### Functions, modules, classes

```python
def gc_content(seq: str) -> float:
    """Percentage of G+C."""
    return 100 * (seq.count("G") + seq.count("C")) / len(seq)

from fasta_tools import gc_content       # module = a .py file
import numpy as np                        # alias

if __name__ == "__main__":                # run only when executed directly
    main()

from dataclasses import dataclass
@dataclass
class Sample:
    id: str
    reads: int
    def is_low(self, minimum=1000) -> bool:
        return self.reads < minimum
```

### Files and exceptions

```python
from pathlib import Path
p = Path("data") / "raw" / "x.csv"; p.exists(); p.stem; p.suffix; p.parent; list(Path("data").glob("*.csv"))
text = p.read_text(); p.write_text("hi\n")
with open(p) as fh:
    for line in fh:
        fields = line.rstrip("\n").split(",")
import csv; rows = list(csv.DictReader(open(p)))
import gzip; fh = gzip.open("x.fastq.gz", "rt")

try:
    value = float(text)
except ValueError as err:
    log.warning("bad value %r: %s", text, err)
finally:
    ...
raise ValueError("explain what is wrong")
```

### Standard library

| Module | Typical use |
|---|---|
| `pathlib` | paths |
| `os` / `sys` | environment, `sys.argv`, `sys.exit(1)`, `sys.stderr` |
| `shutil` | `copy2`, `move`, `rmtree`, `which` |
| `glob` | `glob.glob("*.csv")` |
| `re` | `re.search(r"(\w+)_(\d{4})", s).group(1)` |
| `argparse` | command-line options |
| `logging` | `logging.basicConfig(level=logging.INFO)`, `log.info(...)` |
| `subprocess` | `subprocess.run(["cmd", "arg"], check=True, capture_output=True, text=True)` |
| `csv`, `json`, `gzip`, `statistics`, `datetime`, `collections.Counter` | everyday helpers |

### A command-line program

```python
import argparse, logging, sys
from pathlib import Path
log = logging.getLogger("tool")

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="What it does.")
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("-o", "--outdir", type=Path, default=Path("results"))
    ap.add_argument("--threshold", type=float, default=0.05)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Template: `scripts/python/cli_template.py`.

### Testing and debugging

```python
# tests/test_tools.py         run with:  pytest -v
import pytest
from tools import gc_content
def test_gc():
    assert gc_content("GGCC") == 100
def test_empty():
    with pytest.raises(ZeroDivisionError):
        gc_content("")
```

`breakpoint()` → `(Pdb)`: `p var`, `n` next, `s` step in, `c` continue, `q` quit. Read tracebacks **from the bottom**.

---

## 9. Data analysis: pandas, NumPy, SciPy, Matplotlib

```python
import pandas as pd, numpy as np
df = pd.read_csv("f.csv")                                  # sep="\t" for TSV; na_values=[-9999]
df = pd.read_csv("big.csv.gz", usecols=["a","b"], dtype={"a": "category", "b": "float32"})
df.shape; df.head(); df.dtypes; df.describe(); df.info(); df.isna().sum(); df["c"].value_counts()
```

| Task | pandas |
|---|---|
| select columns | `df[["a","b"]]` |
| filter rows | `df[df.yield_t_ha > 10]`, `df.query("site == 'AMES' and year == 2023")` |
| rows + cols | `df.loc[mask, ["a","b"]]`, `df.iloc[0:5, 0:3]` |
| sort | `df.sort_values(["site","yield_t_ha"], ascending=[True, False])` |
| new column | `df["y14"] = df.y * (100 - df.m) / 86` / `df.assign(...)` |
| clean text | `df.v.str.strip().str.title()` |
| duplicates | `df.duplicated().sum()`, `df.drop_duplicates()` |
| missing | `df.dropna(subset=["y"])`, `df.fillna({"m": df.m.median()})` |
| range check | `df[df.y.between(0, 25, inclusive="neither")]` |
| group | `df.groupby(["site","year"])["y"].agg(["count","mean","std"])` |
| within-group | `df.groupby("trial_id")["y"].transform("max")` |
| pivot / long | `df.pivot_table(index=, columns=, values=, aggfunc=)`, `df.melt(id_vars=...)` |
| join | `a.merge(b, on="site", how="left", validate="many_to_one")` |
| stack tables | `pd.concat([a, b], ignore_index=True)` |
| save | `df.to_csv("out.csv", index=False)` |
| chunks | `for chunk in pd.read_csv(f, chunksize=250_000): ...` |

```python
from scipy import stats
stats.ttest_ind(a, b, equal_var=False)   # Welch t-test
stats.ttest_rel(a, b)                     # paired t-test
stats.f_oneway(g1, g2, g3)                # one-way ANOVA
stats.tukey_hsd(g1, g2, g3)               # pairwise comparisons
stats.pearsonr(x, y); stats.linregress(x, y)
stats.false_discovery_control(pvalues)    # Benjamini–Hochberg
np.percentile(x, [5, 50, 95]); np.log2(x + 1)
```

```python
import matplotlib
matplotlib.use("Agg")                     # scripts / servers: no display needed
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, marker="o", lw=2, color="#2a78d6", label="Amber")
ax.set(xlabel="N rate (kg/ha)", ylabel="Yield (t/ha)", title="Nitrogen response")
ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
fig.savefig("fig.png", dpi=300, bbox_inches="tight"); fig.savefig("fig.pdf"); plt.close(fig)
```

Colour-blind-safe categorical colours (use in this order): `#2a78d6` `#eb6834` `#1baf7a` `#eda100` `#e87ba4` `#008300` `#4a3aa7` `#e34948`.

---

## 10. Git and GitHub

```text
working dir ──add──▶ staging ──commit──▶ local repo ──push──▶ GitHub
                                                    ◀──pull/fetch──
```

```bash
git config --global user.name "Name"; git config --global user.email you@x.org
git config --global init.defaultBranch main; git config --global core.autocrlf input

git init / git clone git@github.com:user/repo.git
git status            git add file / git add -p        git commit -m "Imperative summary"
git log --oneline --graph --all                        git diff / git diff --staged
git switch -c feature  git switch main   git merge feature   git branch -d feature
git remote add origin git@github.com:user/repo.git     git push -u origin main
git fetch / git pull / git push
git restore file      git restore --staged file        git commit --amend
git revert <hash>     git show <hash>:path              git reflog
git tag -a v1.0 -m "Release" && git push origin v1.0
```

**SSH:** `ssh-keygen -t ed25519 -C "email"` → paste `~/.ssh/id_ed25519.pub` into GitHub → Settings → SSH keys → `ssh -T git@github.com`. **Never share the private key.**

**Conflict:** edit the file, keep the right content, delete `<<<<<<<`, `=======`, `>>>>>>>`, then `git add` and `git commit`. To give up: `git merge --abort`.

**`.gitignore` essentials:** `data/raw/`, `results/`, `logs/`, `*.log`, `__pycache__/`, `.ipynb_checkpoints/`, `.env`, `*.pem`.

---

## 11. Integrating everything: project template

```text
project/
├── README.md            purpose · install · run · outputs · layout · license
├── LICENSE
├── .gitignore
├── environment.yml      (requirements.txt for pip-only users)
├── run_all.sh           one command reproduces everything
├── scripts/             Bash steps: 01_fetch, 02_qc, 03_preprocess
├── src/<package>/       Python: io, clean, analysis, plots, cli
├── tests/               pytest
├── data/raw/            read-only, not in Git (checksum manifest IS in Git)
├── data/processed/      regenerated
├── results/             tables/, figures/, report (regenerated)
├── logs/                one log per run
└── docs/                decisions, data inspection notes
```

Workflow: **raw data → Bash QC/preprocess → Python analysis → tables + figures → results/ → Git → GitHub.**

Bash calls Python: `python -m mypkg --in data/processed/x.tsv --outdir results`. Python calls tools: `subprocess.run(["seqkit", "stats", path], check=True)`.

Starter skeleton: `capstone/template/` (copy it to begin your capstone).

---

## 12. Large data and HPC

| Situation | Approach |
|---|---|
| File bigger than RAM | stream (`zcat \| awk`), pandas `chunksize`, `usecols` + `dtype` |
| Many independent files | `xargs -P`, GNU `parallel`, one output each, then combine |
| Means in parallel | combine **sums and counts**, never average averages |
| Disk space | keep `.gz`, read compressed, delete regenerable intermediates, symlink shared data |
| Speed on WSL | work in `~`, not `/mnt/c` |
| Integrity | `sha256sum files > SHA256SUMS`; `sha256sum -c SHA256SUMS` |
| Measure | `/usr/bin/time -v` (Maximum resident set size), `htop`, `du -sh`, `df -h` |
| Compression | `pigz -p N` speeds up compression; decompression is mostly sequential |

**HPC:** `ssh user@cluster`; `rsync -avP src/ user@cluster:dst/`; `module load miniforge`; job script with `#SBATCH --cpus-per-task --mem --time`; `sbatch job.sbatch`, `squeue -u $USER`, `scancel ID`, `sacct -j ID`. No heavy work on login nodes; scratch is purged; use `$SLURM_CPUS_PER_TASK` instead of `nproc`.

---

## 13. Troubleshooting

**Method:** read the last line of the error → `pwd; ls` → `which <cmd>`, active env → check what you typed → make the problem smaller (`set -x`, `breakpoint()`) → search the exact message → ask with command + expected + actual + full error text.

| Error | Likely cause → fix |
|---|---|
| `command not found` | typo; not installed; env not active; not on PATH; `./` missing for local scripts |
| `No such file or directory` | wrong folder or path; spaces unquoted; Windows path syntax |
| `Permission denied` | `chmod u+x`; writing to a system or read-only location |
| `$'\r': command not found` | Windows line endings → `dos2unix file` |
| `unbound variable` | `set -u`; provide a default `${1:-}` |
| `ModuleNotFoundError` | wrong env → `conda activate`; `which python` |
| `IndentationError` | mix of tabs/spaces |
| `KeyError` | column/key name differs (case, spaces) |
| `Permission denied (publickey)` | SSH key not added or loaded |
| `! [rejected] (fetch first)` | `git pull` then push |
| `MemoryError` / WSL freezes | data too big → chunks/streaming; `.wslconfig` |
| `No space left on device` | `df -h`, `du -sh *`, `conda clean --all` |

More: [`cheat_sheets/troubleshooting.md`](../cheat_sheets/troubleshooting.md).

---

## 14. Best practices checklist

- [ ] Projects live in `~`, organised with the template above.
- [ ] Raw data are read-only and checksummed; nothing is edited by hand.
- [ ] Every step is a script; one command runs everything.
- [ ] Scripts: strict mode, usage text, input validation, meaningful exit codes, logs to stderr/files.
- [ ] Python: functions + `main()`, `argparse`, `logging`, specific exceptions, tests.
- [ ] Paths come from arguments or are relative to the project root; never `/home/me/...`.
- [ ] One conda environment per project, described in `environment.yml`.
- [ ] Git from day one; small commits with clear messages; no data, outputs or secrets in Git.
- [ ] README lets a stranger run the project; decisions are documented in `docs/`.
- [ ] Figures: units, readable fonts, colour-blind-safe, generated by code.
- [ ] Large data: stream, chunk, compress, parallelise; measure before optimising.
- [ ] Before sharing: clone into `/tmp` and run from scratch.

---

## 15. Glossary

| Term | Meaning |
|---|---|
| absolute / relative path | path from `/` / from the current directory |
| argument / option | value given to a command / a named setting such as `-o out` |
| array | ordered list of values in one variable |
| branch | independent line of development in Git |
| channel | conda package repository (conda-forge, bioconda) |
| checksum | fingerprint of file content (SHA-256, MD5) |
| chunk | part of a large file processed at a time |
| commit | Git snapshot with message and ID |
| conda environment | isolated folder of software versions |
| CRLF / LF | Windows / Linux line endings |
| DataFrame | pandas table |
| exit code | number a program returns: 0 = success |
| glob / wildcard | pattern such as `*.csv` |
| HPC / cluster | many connected computers with a job scheduler |
| merge conflict | both branches changed the same lines |
| module (Python) | a `.py` file you can import |
| pipe | `\|`: connects stdout of one command to stdin of the next |
| process / PID | running program / its ID |
| redirection | sending a stream to or from a file (`>`, `<`, `2>`) |
| remote | a copy of the repository elsewhere (GitHub: `origin`) |
| REPL | interactive prompt (`python`, `ipython`) |
| sentinel value | special number meaning "missing" (e.g. −9999) |
| shebang | `#!/usr/bin/env bash`: first line choosing the interpreter |
| SSH key pair | private (secret) + public (shared) keys for authentication |
| staging area | Git's "next commit" area |
| stdin / stdout / stderr | standard input / output / error streams (0/1/2) |
| streaming | processing data piece by piece without loading it all |
| symbolic link | pointer to another file or folder (`ln -s`) |
| WSL | Windows Subsystem for Linux |

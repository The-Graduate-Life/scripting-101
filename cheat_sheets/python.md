# Python Cheat Sheet

## Run
`python` (REPL) · `ipython` · `python script.py args` · `python -m package` · `jupyter lab`

## Basics
```python
x = 3; y = 2.5; s = "ATG"; ok = True; nothing = None
7 // 2   7 % 2   2 ** 10   abs(-3)   round(2.567, 2)   int("3")  float("2.5")  str(3)
==  !=  <  <=  and  or  not  in  is None
f"{name}: {value:.2f} ({pct:.1%})"
```

## Strings
`s[0] s[-1] s[1:4] s[::-1]` · `len(s)` · `s.upper() .lower() .strip() .title()` · `s.split(",")` · `",".join(lst)` · `s.replace(a, b)` · `s.startswith(">")` · `s.count("G")` · `"GC" in s`

## Collections
```python
lst = [3, 1]; lst.append(2); lst.extend([5]); lst.pop(); sorted(lst); lst[1:]; len(lst)
t = (1, 2); a, b = t
d = {"a": 1}; d["b"] = 2; d.get("z", 0); d.items(); d.keys(); d.values(); "a" in d
st = {1, 2}; st.add(3); st & other; st | other; st - other
[x*2 for x in lst if x > 1]   {k: v for k, v in d.items()}   {x.lower() for x in names}
from collections import Counter, defaultdict
```

## Control flow
```python
if x > 0: ...
elif x == 0: ...
else: ...
for i, item in enumerate(items): ...
for a, b in zip(xs, ys): ...
while cond: ...
break / continue
```

## Functions
```python
def mean(values: list[float], skip_na: bool = True) -> float:
    """Return the arithmetic mean."""
    vals = [v for v in values if v is not None] if skip_na else values
    return sum(vals) / len(vals)
```

## Files
```python
from pathlib import Path
p = Path("data") / "x.csv"; p.exists(); p.is_file(); p.stem; p.suffix; p.parent; p.name
p.read_text(); p.write_text("..."); Path("out").mkdir(parents=True, exist_ok=True)
for f in sorted(Path("data").glob("*.csv")): ...
with open(p) as fh:
    header = fh.readline().strip().split(",")
    for line in fh: ...
import csv; reader = csv.DictReader(open(p))
import gzip; gzip.open("x.gz", "rt")
```

## Exceptions
```python
try:
    v = float(s)
except ValueError as err:
    ...
except (FileNotFoundError, PermissionError):
    ...
else:            # no exception
    ...
finally:         # always
    ...
raise ValueError(f"bad value: {s!r}")
```

## Modules and scripts
```python
import numpy as np
from pathlib import Path
from mymodule import my_function

def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

## argparse + logging
```python
import argparse, logging
ap = argparse.ArgumentParser(description="...")
ap.add_argument("input", type=Path)
ap.add_argument("-o", "--outdir", type=Path, default=Path("results"))
ap.add_argument("-n", type=int, default=10)
ap.add_argument("-v", "--verbose", action="store_true")
args = ap.parse_args()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__); log.info("n=%d", args.n); log.warning(...); log.error(...)
```

## OS and CLI tools
```python
import os, sys, shutil, glob, re, subprocess
os.environ.get("HOME"); sys.argv; sys.exit(1); print("err", file=sys.stderr)
shutil.copy2(a, b); shutil.which("seqkit"); glob.glob("*.csv")
m = re.match(r"weather_(?P<site>[A-Z]{4})_(?P<year>\d{4})", name); m["site"]
r = subprocess.run(["seqkit", "stats", f], capture_output=True, text=True, check=True); r.stdout
```

## Classes
```python
from dataclasses import dataclass
@dataclass
class Sample:
    id: str
    reads: int = 0
    def is_low(self, minimum: int = 1000) -> bool:
        return self.reads < minimum
s = Sample("S01", 2507); s.is_low()
```

## pandas
```python
import pandas as pd
df = pd.read_csv(f, sep=",", na_values=[-9999], usecols=[...], dtype={...})
df.head() df.shape df.dtypes df.describe() df.isna().sum() df.col.value_counts()
df[["a","b"]]  df[df.a > 1]  df.query("a > 1 and b == 'x'")  df.loc[mask, "a"]
df.sort_values("a", ascending=False)  df.drop_duplicates()  df.dropna(subset=["a"])
df["c"] = df.a / df.b   df.a.str.strip().str.title()   df.a.between(0, 25)
df.groupby(["g1","g2"]).a.agg(["count","mean","std"])   df.groupby("g").a.transform("max")
df.pivot_table(index="r", columns="c", values="v", aggfunc="mean")   df.melt(id_vars=["id"])
a.merge(b, on="key", how="left", validate="many_to_one")   pd.concat([a, b])
df.to_csv("out.csv", index=False)
for chunk in pd.read_csv(f, chunksize=250_000): ...
```

## NumPy / SciPy
```python
import numpy as np; from scipy import stats
np.mean(x) np.std(x, ddof=1) np.percentile(x, [5, 50, 95]) np.log2(x + 1) np.where(c, a, b)
stats.ttest_ind(a, b, equal_var=False)  stats.ttest_rel(a, b)  stats.f_oneway(*groups)
stats.tukey_hsd(*groups)  stats.pearsonr(x, y)  stats.linregress(x, y)  stats.false_discovery_control(p)
```

## Matplotlib
```python
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, marker="o", label="A"); ax.scatter(x, y); ax.bar(cats, vals); ax.hist(v, bins=30)
ax.set(xlabel="N (kg/ha)", ylabel="Yield (t/ha)", title="..."); ax.legend(frameon=False)
fig.savefig("fig.png", dpi=300, bbox_inches="tight"); fig.savefig("fig.pdf"); plt.close(fig)
```
Colour-blind-safe order: `#2a78d6 #eb6834 #1baf7a #eda100 #e87ba4 #008300 #4a3aa7 #e34948`

## Testing and debugging
`pytest -v` · `assert x == 3` · `with pytest.raises(ValueError): ...` · `pytest.approx(0.1)` · `tmp_path` fixture
`breakpoint()` → `p var`, `n`, `s`, `c`, `q` · read tracebacks bottom-up

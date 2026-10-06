#!/usr/bin/env python3
"""Generate the Scripting 101 course datasets.

All data are SIMULATED for teaching. They describe a fictional multi-site
maize nitrogen trial called "HARVEST" (2020-2024) plus a small genomics
side-project on the same varieties.

The generator uses only the Python standard library and a fixed random seed,
so every student who runs it gets byte-for-byte identical files.

Usage:
    python3 make_datasets.py            # writes into the folder containing this script
    python3 make_datasets.py --out DIR  # writes somewhere else
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import io
import math
import random
from pathlib import Path

SEED = 101

SITES = {
    # site: (latitude, longitude, soil_type, region, rainfall_bias_mm_per_day, yield_potential_t_ha)
    "AMES": (42.03, -93.62, "silty_clay_loam", "Midwest", 0.4, 11.5),
    "LINC": (40.81, -96.70, "silt_loam", "Plains", 0.0, 10.2),
    "MANH": (39.18, -96.57, "silt_loam", "Plains", -0.6, 8.9),
    "STPL": (44.95, -93.09, "loam", "North", 0.2, 10.4),
    "URBN": (40.11, -88.21, "silty_clay_loam", "Midwest", 0.5, 12.0),
    "WLAF": (40.43, -86.91, "clay_loam", "Midwest", 0.3, 11.2),
}
YEARS = [2020, 2021, 2022, 2023, 2024]
YEAR_RAIN_EFFECT = {2020: 0.0, 2021: -0.8, 2022: 0.5, 2023: -1.4, 2024: 0.3}
VARIETIES = {"Amber": 0.0, "Bolt": 0.6, "Crest": -0.3, "Dune": 0.9}
N_RATES = [0, 60, 120, 180]
REPS = [1, 2, 3]

SEASON_START = (4, 1)   # April 1
SEASON_DAYS = 183       # through September 30


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def write_csv(path: Path, header: list[str], rows: list[list], delimiter: str = ",",
              newline: str = "\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.writer(fh, delimiter=delimiter, lineterminator=newline)
        w.writerow(header)
        w.writerows(rows)


def gzip_text(path: Path):
    """Open a .gz file for writing text with a fixed header timestamp (byte-identical output)."""
    return io.TextIOWrapper(gzip.GzipFile(filename=path, mode="wb", compresslevel=6, mtime=0), encoding="utf-8")


def wrap(seq: str, width: int = 60) -> str:
    return "\n".join(seq[i:i + width] for i in range(0, len(seq), width))


# ---------------------------------------------------------------------------
# agriculture
# ---------------------------------------------------------------------------
def make_sites(out: Path) -> None:
    rows = [[s, lat, lon, soil, region] for s, (lat, lon, soil, region, _, _) in SITES.items()]
    write_csv(out / "field_trials" / "sites.csv",
              ["site", "latitude", "longitude", "soil_type", "region"], rows)


def make_weather(out: Path, rng: random.Random) -> dict[tuple[str, int], float]:
    """Daily weather per site-year. Returns total season precipitation per site-year."""
    season_precip: dict[tuple[str, int], float] = {}
    for site, (lat, _lon, _soil, _reg, rain_bias, _pot) in SITES.items():
        for year in YEARS:
            start = dt.date(year, *SEASON_START)
            rows, total = [], 0.0
            for d in range(SEASON_DAYS):
                day = start + dt.timedelta(days=d)
                seasonal = math.sin(math.pi * d / SEASON_DAYS)          # peaks mid-July
                tmax = 18 + 13 * seasonal - (lat - 40) * 0.6 + rng.gauss(0, 3)
                tmin = tmax - 11 + rng.gauss(0, 2)
                wet_prob = 0.32 + 0.04 * rain_bias + 0.05 * YEAR_RAIN_EFFECT[year]
                precip = 0.0
                if rng.random() < wet_prob:
                    precip = round(rng.expovariate(1 / (9 + 2 * rain_bias + 2 * YEAR_RAIN_EFFECT[year])), 1)
                solar = round(max(2.0, 14 + 9 * seasonal - precip * 0.3 + rng.gauss(0, 2.5)), 1)
                total += precip
                precip_out: object = precip
                # Weather stations sometimes record "-9999" for missing values (a classic gotcha)
                if rng.random() < 0.01:
                    precip_out = -9999
                rows.append([day.isoformat(), round(tmin, 1), round(tmax, 1), precip_out, solar])
            season_precip[(site, year)] = total
            write_csv(out / "weather" / f"weather_{site}_{year}.csv",
                      ["date", "tmin_c", "tmax_c", "precip_mm", "solar_mj_m2"], rows)
    return season_precip


def n_response(n_rate: float) -> float:
    """Diminishing-returns nitrogen response (t/ha gained)."""
    return 3.2 * (1 - math.exp(-n_rate / 70))


def make_yields(out: Path, rng: random.Random, season_precip: dict[tuple[str, int], float]) -> None:
    header = ["trial_id", "site", "year", "plot", "variety", "n_rate_kg_ha", "rep",
              "yield_t_ha", "grain_moisture_pct", "plant_height_cm", "notes"]
    rows: list[list] = []
    for site, (_lat, _lon, _soil, _reg, _bias, potential) in SITES.items():
        for year in YEARS:
            precip = season_precip[(site, year)]
            # drought penalty below ~450 mm, waterlogging penalty above ~750 mm
            water = -0.012 * max(0, 450 - precip) - 0.004 * max(0, precip - 750)
            plot = 100
            for rep in REPS:
                for variety, v_eff in VARIETIES.items():
                    for n in N_RATES:
                        plot += 1
                        y = potential - 3.2 + v_eff + n_response(n) + water + rng.gauss(0, 0.55)
                        y = round(max(0.5, y), 2)
                        moist = round(rng.uniform(14.5, 24.0), 1)
                        height = round(190 + 25 * n_response(n) / 3.2 + 8 * v_eff + rng.gauss(0, 9), 0)
                        rows.append([f"{site}-{year}", site, year, plot, variety, n, rep,
                                     y, moist, int(height), ""])

    # --- inject realistic messiness (documented in datasets/README.md) ---
    for i in rng.sample(range(len(rows)), 25):         # missing yields
        rows[i][7] = "NA"
        rows[i][10] = "plot lodged; not harvested"
    for i in rng.sample(range(len(rows)), 18):         # missing moisture
        rows[i][8] = ""
    for i in rng.sample(range(len(rows)), 9):          # inconsistent variety labels
        rows[i][4] = rng.choice([rows[i][4].lower(), rows[i][4].upper(), rows[i][4] + " "])
    rows[57][7] = -1.0                                 # impossible value
    rows[57][10] = "data entry error?"
    rows[903][7] = 99.9                                # impossible value
    for i in (11, 412, 1200):                          # exact duplicate rows
        rows.insert(i + 1, list(rows[i]))
    write_csv(out / "field_trials" / "plot_yields.csv", header, rows)

    # a Windows-exported copy of one site with CRLF line endings
    sub = [r for r in rows if r[1] == "AMES" and r[2] == 2023]
    write_csv(out / "messy" / "ames_2023_windows_export.csv", header, sub, newline="\r\n")


def make_sensors(out: Path, rng: random.Random) -> None:
    """Soil-moisture loggers: sensors/<SITE>/<YYYY-MM-DD>/logger_NN.csv (10-minute readings)."""
    start = dt.date(2024, 7, 1)
    header = ["timestamp", "logger_id", "soil_moisture_pct", "soil_temp_c", "battery_v"]
    for site, (_lat, _lon, _soil, _reg, bias, _pot) in SITES.items():
        moisture0 = 28 + 3 * bias
        for day_i in range(7):
            day = start + dt.timedelta(days=day_i)
            for logger in range(1, 5):
                lid = f"{site}-L{logger:02d}"
                rows = []
                m = moisture0 - day_i * 0.6 + rng.gauss(0, 1)
                batt = 3.9 - 0.02 * day_i - (0.5 if (site == "MANH" and logger == 3) else 0)
                for k in range(144):
                    t = dt.datetime.combine(day, dt.time()) + dt.timedelta(minutes=10 * k)
                    temp = 21 + 4 * math.sin(2 * math.pi * (k - 54) / 144) + rng.gauss(0, 0.3)
                    m = m + rng.gauss(0, 0.05)
                    value: object = round(m, 2)
                    if rng.random() < 0.004:
                        value = "ERR"                       # sensor glitch
                    rows.append([t.isoformat(timespec="minutes"), lid, value, round(temp, 2),
                                 round(batt + rng.gauss(0, 0.01), 2)])
                path = out / "sensors" / site / day.isoformat() / f"logger_{logger:02d}.csv"
                write_csv(path, header, rows)
    # three broken files for error-handling exercises
    (out / "sensors" / "LINC" / "2024-07-03" / "logger_02.csv").write_text("")
    (out / "sensors" / "STPL" / "2024-07-05" / "logger_04.csv").write_text(",".join(header) + "\n")
    bad = out / "sensors" / "URBN" / "2024-07-06" / "logger_01.csv"
    bad.write_text(bad.read_text().replace("soil_moisture_pct", "moisture"))


# ---------------------------------------------------------------------------
# genomics
# ---------------------------------------------------------------------------
CONTIGS = {"chr1": 8000, "chr2": 6500, "chr3": 5000, "chr4": 4000, "chr5": 3000}
SAMPLES = [f"S{i:02d}" for i in range(1, 9)]
SAMPLE_INFO = {  # sample: (variety, n_treatment, site)
    "S01": ("Amber", "low_N", "AMES"), "S02": ("Amber", "high_N", "AMES"),
    "S03": ("Bolt", "low_N", "AMES"), "S04": ("Bolt", "high_N", "AMES"),
    "S05": ("Crest", "low_N", "URBN"), "S06": ("Crest", "high_N", "URBN"),
    "S07": ("Dune", "low_N", "URBN"), "S08": ("Dune", "high_N", "URBN"),
}
ADAPTER = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"


def make_reference(rng: random.Random) -> dict[str, str]:
    ref = {}
    for name, length in CONTIGS.items():
        gc = 0.44 + 0.04 * rng.random()
        bases = []
        for _ in range(length):
            if rng.random() < gc:
                bases.append(rng.choice("GC"))
            else:
                bases.append(rng.choice("AT"))
        ref[name] = "".join(bases)
    return ref


def make_genomics(out: Path, rng: random.Random) -> None:
    g = out / "genomics"
    g.mkdir(parents=True, exist_ok=True)
    ref = make_reference(rng)
    with (g / "reference.fasta").open("w") as fh:
        for name, seq in ref.items():
            fh.write(f">{name} simulated maize-like contig length={len(seq)}\n{wrap(seq)}\n")

    # sample metadata
    write_csv(g / "sample_metadata.tsv",
              ["sample_id", "variety", "n_treatment", "site", "tissue", "fastq"],
              [[s, v, n, site, "leaf", f"reads/{s}.fastq.gz"] for s, (v, n, site) in SAMPLE_INFO.items()],
              delimiter="\t")

    # FASTQ reads (single-end)
    comp = str.maketrans("ACGT", "TGCA")
    names = list(ref)
    for s in SAMPLES:
        n_reads = 2500 + rng.randint(-300, 300)
        low_quality = s == "S06"
        adapter_heavy = s == "S03"
        path = g / "reads" / f"{s}.fastq.gz"
        path.parent.mkdir(parents=True, exist_ok=True)
        with gzip_text(path) as fh:
            for r in range(1, n_reads + 1):
                chrom = rng.choice(names)
                length = rng.randint(120, 150)
                pos = rng.randint(0, len(ref[chrom]) - length)
                seq = ref[chrom][pos:pos + length]
                if rng.random() < 0.5:
                    seq = seq.translate(comp)[::-1]
                if adapter_heavy and rng.random() < 0.35:
                    cut = rng.randint(60, 110)
                    seq = (seq[:cut] + ADAPTER)[:length]
                    length = len(seq)
                quals, bases = [], list(seq)
                for i in range(length):
                    mean_q = (24 if low_quality else 36) - (14 if low_quality else 8) * i / length
                    q = int(max(2, min(41, rng.gauss(mean_q, 3))))
                    if rng.random() < 10 ** (-q / 10):
                        bases[i] = rng.choice("ACGT")
                    if q < 3:
                        bases[i] = "N"
                    quals.append(chr(q + 33))
                fh.write(f"@{s}_read{r:05d} {chrom}:{pos + 1}\n{''.join(bases)}\n+\n{''.join(quals)}\n")

    # Variants (VCF 4.2, gzip-compressed)
    lines = ["##fileformat=VCFv4.2",
             f"##fileDate={dt.date(2024, 11, 15):%Y%m%d}",
             "##source=HARVEST-simulated",
             "##reference=reference.fasta"]
    lines += [f"##contig=<ID={c},length={n}>" for c, n in CONTIGS.items()]
    lines += ['##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth">',
              '##INFO=<ID=AF,Number=A,Type=Float,Description="Alternate allele frequency">',
              '##INFO=<ID=TYPE,Number=1,Type=String,Description="Variant type: snp or indel">',
              '##FILTER=<ID=LowQual,Description="QUAL below 30">',
              '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
              '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Sample read depth">',
              "#" + "\t".join(["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT"] + SAMPLES)]
    records = []
    for chrom, length in CONTIGS.items():
        n_var = length // 20
        for pos in sorted(rng.sample(range(10, length - 10), n_var)):
            refb = ref[chrom][pos - 1]
            if rng.random() < 0.85:
                vtype, alt = "snp", rng.choice([b for b in "ACGT" if b != refb])
                ref_allele = refb
            elif rng.random() < 0.5:
                vtype, ref_allele = "indel", refb
                alt = refb + "".join(rng.choice("ACGT") for _ in range(rng.randint(1, 4)))
            else:
                vtype = "indel"
                ref_allele = ref[chrom][pos - 1:pos + rng.randint(1, 3)]
                alt = refb
            qual = round(rng.uniform(5, 60) if rng.random() < 0.15 else rng.uniform(30, 250), 1)
            filt = "PASS" if qual >= 30 else "LowQual"
            gts, total_dp, alt_count = [], 0, 0
            af_target = rng.random()
            for _s in SAMPLES:
                a = sum(rng.random() < af_target for _ in range(2))
                alt_count += a
                gt = ["0/0", "0/1", "1/1"][a]
                if rng.random() < 0.03:
                    gt = "./."
                dp = max(0, int(rng.gauss(22, 7)))
                total_dp += dp
                gts.append(f"{gt}:{dp}")
            af = round(alt_count / (2 * len(SAMPLES)), 3)
            records.append("\t".join([chrom, str(pos), ".", ref_allele, alt, str(qual), filt,
                                      f"DP={total_dp};AF={af};TYPE={vtype}", "GT:DP"] + gts))
    with gzip_text(g / "variants.vcf.gz") as fh:
        fh.write("\n".join(lines + records) + "\n")

    # Gene annotation + expression counts
    # Genes live on full-size (maize-like) chromosomes; reference.fasta is only a toy excerpt.
    chrom_sizes = {f"chr{i}": size for i, size in enumerate(
        [308, 244, 235, 247, 223, 174, 182, 181, 159, 150], start=1)}            # megabases
    genes = []
    for gid in range(1, 2001):
        chrom = rng.choices(list(chrom_sizes), weights=list(chrom_sizes.values()))[0]
        start = rng.randint(1, chrom_sizes[chrom] * 1_000_000 - 10_000)
        genes.append((f"Zm{gid:05d}", chrom, start, start + rng.randint(800, 9000), rng.choice("+-")))
    genes.sort(key=lambda g: (int(g[1][3:]), g[2]))
    functions = ["nitrate transporter", "glutamine synthetase", "photosystem II subunit",
                 "heat shock protein", "aquaporin", "cell wall invertase", "MYB transcription factor",
                 "ribosomal protein", "chlorophyll a/b binding protein", "asparagine synthetase"]
    weights = [3, 3, 8, 8, 6, 5, 10, 12, 8, 2]
    ann = []
    for gname, c, start, end, strand in genes:
        desc = rng.choices(functions, weights)[0] if rng.random() < 0.7 else "hypothetical protein"
        ann.append([gname, c, start, end, strand, desc])
    write_csv(g / "gene_annotation.tsv", ["gene_id", "chrom", "start", "end", "strand", "description"],
              ann, delimiter="\t")

    # N-responsive genes: most N-metabolism genes plus a random 3% of others (some up, some down)
    responsive: dict[str, float] = {}
    for a in ann:
        if a[5] in ("nitrate transporter", "glutamine synthetase", "asparagine synthetase") and rng.random() < 0.7:
            responsive[a[0]] = rng.uniform(2.0, 4.0)
        elif rng.random() < 0.03:
            responsive[a[0]] = rng.choice([rng.uniform(0.25, 0.5), rng.uniform(2.0, 3.0)])
    count_rows = []
    library_factor = {smp: rng.uniform(0.7, 1.4) for smp in SAMPLES}     # sequencing depth differs per sample
    for a in ann:
        base = math.exp(rng.uniform(1, 8))
        # genotype effect: each variety expresses each gene at its own level
        variety_effect = {v: math.exp(rng.gauss(0, 0.5)) for v in VARIETIES}
        row = [a[0]]
        for s in SAMPLES:
            fold = responsive.get(a[0], 1.0) if SAMPLE_INFO[s][1] == "high_N" else 1.0
            mu = base * fold * variety_effect[SAMPLE_INFO[s][0]]
            mu *= library_factor[s]
            row.append(max(0, int(rng.gammavariate(50, mu / 50))))        # biological noise (CV ~0.14)
        count_rows.append(row)
    write_csv(g / "expression_counts.tsv", ["gene_id"] + SAMPLES, count_rows, delimiter="\t")


def make_misc(out: Path) -> None:
    m = out / "messy"
    m.mkdir(parents=True, exist_ok=True)
    (m / "field notes 2023.txt").write_text(
        "2023-06-14 AMES: heavy hail on reps 2-3, check plots 125-140\n"
        "2023-07-02 LINC: irrigation pump failure for 3 days\n"
        "2023-07-19 MANH: drought stress visible, leaf rolling by 11:00\n"
        "2023-08-03 URBN: green snap after storm, plots 101-112\n"
        "2023-09-21 STPL: early frost warning, harvest moved forward\n")
    (m / "README_messy.txt").write_text(
        "Files in this folder are intentionally awkward:\n"
        "  * 'field notes 2023.txt' has spaces in its name (practise quoting!)\n"
        "  * ames_2023_windows_export.csv has Windows CRLF line endings (try: file, cat -A, dos2unix, sed)\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent,
                    help="output directory (default: the datasets/ folder)")
    args = ap.parse_args()
    rng = random.Random(SEED)
    make_sites(args.out)
    precip = make_weather(args.out, rng)
    make_yields(args.out, rng, precip)
    make_sensors(args.out, rng)
    make_genomics(args.out, rng)
    make_misc(args.out)
    print(f"Datasets written to {args.out}")


if __name__ == "__main__":
    main()

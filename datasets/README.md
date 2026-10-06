# Course Datasets

All data are **simulated** for teaching (seed 101) and describe a fictional multi-site maize nitrogen trial, **HARVEST** (6 US Midwest/Plains sites, 2020–2024), plus a small genomics side-project on the same four varieties. They are realistic in structure and contain **deliberate problems** for students to find.

Recreate byte-identical files at any time:

```bash
python3 datasets/make_datasets.py           # standard library only, no conda needed
bash scripts/bash/checksums.sh verify datasets
```

## Contents

| Path | Format | Size | Description |
|---|---|---|---|
| `field_trials/plot_yields.csv` | CSV | 1,443 rows | plot yields: 6 sites × 5 years × 4 varieties × 4 N rates × 3 reps (+ problems) |
| `field_trials/sites.csv` | CSV | 6 rows | site coordinates, soil type, region |
| `weather/weather_<SITE>_<YEAR>.csv` | CSV | 30 files × 183 days | daily weather, 1 April – 30 September |
| `sensors/<SITE>/<DATE>/logger_NN.csv` | CSV | 168 files × 144 rows | soil-moisture loggers, 10-minute readings, July 2024 |
| `genomics/reference.fasta` | FASTA | 5 contigs, 26.5 kb | toy reference sequence |
| `genomics/reads/S01–S08.fastq.gz` | FASTQ (gzip) | ~2,500 reads each | single-end reads, 120–150 bp |
| `genomics/variants.vcf.gz` | VCF 4.2 (gzip) | 1,325 variants × 8 samples | SNPs and indels with QUAL/FILTER/INFO |
| `genomics/sample_metadata.tsv` | TSV | 8 samples | variety, N treatment, site |
| `genomics/expression_counts.tsv` | TSV | 2,000 genes × 8 samples | RNA-seq-like counts |
| `genomics/gene_annotation.tsv` | TSV | 2,000 genes | chromosome, position, description |
| `messy/ames_2023_windows_export.csv` | CSV, **CRLF** | 48 rows | Windows line endings |
| `messy/field notes 2023.txt` | text | 5 lines | **spaces in the file name** |
| `make_large_dataset.py` | script | – | generates big sensor files (1–20 M rows) on demand for Module 7 |

### `plot_yields.csv` columns
`trial_id` (SITE-YEAR) · `site` · `year` · `plot` · `variety` (Amber, Bolt, Crest, Dune) · `n_rate_kg_ha` (0, 60, 120, 180) · `rep` (1–3) · `yield_t_ha` · `grain_moisture_pct` · `plant_height_cm` · `notes`

### `weather_*.csv` columns
`date` · `tmin_c` · `tmax_c` · `precip_mm` (**−9999 = missing**) · `solar_mj_m2`

### Logger columns
`timestamp` · `logger_id` · `soil_moisture_pct` (`ERR` = sensor glitch) · `soil_temp_c` · `battery_v`

## Deliberate problems (instructor reference: don't show students up front)

| Where | Problem | Count |
|---|---|---|
| `plot_yields.csv` | exact duplicate rows | 3 |
| | variety labels in wrong case / trailing spaces | 9 rows (11 spellings in total) |
| | `NA` yields with note "plot lodged; not harvested" | 25 |
| | impossible yields: −1.0 (AMES-2021 plot 110), 99.9 (STPL-2023 plot 140) | 2 |
| | empty moisture values | 18 |
| `weather/` | `-9999` sentinel for missing rainfall | 59 values |
| `sensors/` | empty file `LINC/2024-07-03/logger_02.csv` | 1 |
| | header-only file `STPL/2024-07-05/logger_04.csv` | 1 |
| | renamed column in `URBN/2024-07-06/logger_01.csv` | 1 |
| | `ERR` glitch values | ~0.4 % of readings |
| | failing battery: MANH logger 03 (< 3.5 V throughout) | 1 logger |
| `genomics/reads/` | S03: ~32 % reads with Illumina adapter; S06: low base quality (~Q16) | 2 samples |
| `variants.vcf.gz` | low-quality calls (`LowQual`), missing genotypes `./.` | 87 / ~3 % |
| `expression_counts.tsv` | N-responsive genes (mostly nitrate transporter, glutamine/asparagine synthetase, plus a few random genes up or down); strong variety (genotype) effects, so a **paired** design is needed | – |

## Built-in signals (what a correct analysis finds)
* Yield increases with N with diminishing returns; variety ranking Dune > Bolt > Amber > Crest.
* 2023 was a drought year (MANH 2023: 174 mm rain); yield correlates with season rainfall (r ≈ 0.7).
* Paired DE analysis (by variety) finds ≈ 97 genes; an unpaired test finds ≈ 1.

## Integrity
`SHA256SUMS` in this folder lists checksums of every file. Verify with `bash ../scripts/bash/checksums.sh verify .` or `sha256sum -c SHA256SUMS` from this folder.

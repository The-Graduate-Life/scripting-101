# Example Scripts

Demonstration scripts used in lectures. Each is documented in its header; run with `-h` or read the top of the file.

## Bash (`bash/`)
| Script | Module | Shows |
|---|---|---|
| `01_hello.sh` | 2 | shebang, command substitution |
| `02_variables_args.sh` | 2 | variables, quoting, arguments, validation, arithmetic, exit codes |
| `03_loop_weather.sh` | 2 | `for` over files, parameter expansion, awk, sentinel values |
| `fasta_stats.sh` | 2 | awk on FASTA (plain or .gz), per-sequence length and GC |
| `vcf_summary.sh` | 2 | VCF parsing with grep/awk/sort/uniq |
| `fastq_qc.sh` | 2, 7 | **production pattern**: getopts, validation, logging library, trap, parallel `xargs -P` |
| `conflict_demo.sh` | 5 | builds a throw-away repo with a guaranteed merge conflict |
| `benchmark_large_data.sh` | 7 | time + peak memory of 6 strategies on one big file |
| `checksums.sh` | 7, 8 | create/verify SHA-256 checksums for a folder |
| `script_template.sh` | 2 | starting point for new scripts |
| `lib/logging.sh` | 2 | sourced logging helpers (`log_info`, `die`, `require_cmd`) |

## HPC (`hpc/`)
| File | Module | Shows |
|---|---|---|
| `slurm_job.sbatch` | 7 | annotated SLURM job script |

## Python (`python/`)
| Script | Module | Shows |
|---|---|---|
| `01_hello.py` | 4 | first script; which interpreter is running |
| `02_yields_stdlib.py` | 4 | csv, dicts, functions, exceptions, pathlib (no pandas) |
| `fastq_stats.py` | 4, 6 | the Python twin of `fastq_qc.sh`; generators, gzip, argparse, logging |
| `chunked_sensor_summary.py` | 7 | pandas chunks with sum/count aggregation; memory-efficient dtypes |
| `run_external_tools.py` | 6 | calling CLI tools from Python with `subprocess` |
| `cli_template.py` | 4 | starting point for command-line programs |

All examples were tested with the `scripting101` environment on the course datasets.

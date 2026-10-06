# Module 7 — Working with Large Scientific Datasets

!!! info "At a glance"

    **Time:** 5 hours (3 sessions)  
    **Labs:** Lab 09 · Large-data processing  
    **Prerequisites:** Modules 2, 4 and 6

## What you will be able to do

- Relate CPU, RAM and disk to your choice of method
- Organise storage and avoid unnecessary copies
- Stream and chunk data larger than memory
- Use compression and parallelism effectively
- Measure time and peak memory; monitor jobs
- Verify data integrity with checksums
- Explain HPC basics: nodes, scheduler, job scripts
- Transfer your WSL skills to servers and clusters

## Topics

- Memory vs disk; CPU and RAM; WSL resource limits
- Streaming (`zcat | awk`) vs pandas vs chunks: measured
- Compression (`gzip`, `pigz`); map → reduce with `split` + `xargs -P`
- Avoiding copies: pipes, symlinks, filtering early
- Checksums (MD5, SHA-256) and data integrity
- Monitoring: `/usr/bin/time -v`, `htop`
- HPC: SSH, modules, SLURM job scripts, storage tiers

## Materials

| Material | Link |
|---|---|
| :material-presentation: Slides | [Module 7 slides (PDF)]({{SLIDES_7}}) |
| :material-flask: Lab 09 · Large-data processing | [Open the lab](../labs/lab09_large_data/README.md) · 3 h |
| :material-card-text: Cheat sheets | [Bash](../cheat_sheets/bash.md) · [Linux CLI](../cheat_sheets/linux_cli.md) · [Troubleshooting](../cheat_sheets/troubleshooting.md) |
| :material-book-open-variant: Handbook | [Student handbook](../handbook/STUDENT_HANDBOOK.md) |

## Check your understanding

Try these after the labs. Discuss your answers in class.

1. Why can't a 4 GB CSV be loaded on an 8 GB laptop with plain `read_csv`?
2. Name three ways to process a file larger than RAM.
3. What is the 'reduce' step when computing a mean in parallel?
4. Which `#SBATCH` lines request 8 cores, 16 GB and 2 hours?

!!! tip "Stuck?"
    Read the last line of the error first, then check the [troubleshooting cheat sheet](../cheat_sheets/troubleshooting.md). Still stuck after 15 minutes? Ask, and bring the exact command and the full error text.

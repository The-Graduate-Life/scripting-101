# Further Reading and Resources

## Command line and Bash
* *The Linux Command Line*, William Shotts (free online: linuxcommand.org)
* Software Carpentry: *The Unix Shell* (swcarpentry.github.io/shell-novice)
* GNU Bash manual: `man bash`, or gnu.org/software/bash/manual
* Greg's Wiki Bash Guide and **Bash Pitfalls** (mywiki.wooledge.org)
* ShellCheck: shellcheck.net (also `sudo apt install shellcheck`)
* *Data Science at the Command Line*, Jeroen Janssens (free online)
* The AWK Programming Language, 2nd ed., Aho, Kernighan & Weinberger

## Python and data analysis
* Software Carpentry: *Programming with Python*; Data Carpentry: *Data Analysis and Visualization in Python for Ecologists*
* *Python for Data Analysis*, 3rd ed., Wes McKinney (free online: wesmckinney.com/book)
* pandas documentation: "10 minutes to pandas" and the user guide
* Matplotlib tutorials; *Ten Simple Rules for Better Figures* (Rougier et al., PLOS Comp Biol 2014)
* SciPy statistics reference (`scipy.stats`)

## Conda and reproducibility
* conda documentation: "Managing environments"
* conda-forge and bioconda documentation
* *Good enough practices in scientific computing* (Wilson et al., PLOS Comp Biol 2017)
* *Ten simple rules for reproducible computational research* (Sandve et al., PLOS Comp Biol 2013)
* The Turing Way (book.the-turing-way.org)

## Git and GitHub
* Software Carpentry: *Version Control with Git*
* *Pro Git*, Scott Chacon & Ben Straub (free: git-scm.com/book)
* GitHub Docs: "Connecting to GitHub with SSH"
* *Ten simple rules for taking advantage of Git and GitHub* (Perez-Riverol et al., PLOS Comp Biol 2016)

## Large data and HPC
* HPC Carpentry: *Introduction to High-Performance Computing*
* SLURM documentation: "Quick Start User Guide"
* GNU Parallel tutorial: `man parallel_tutorial`
* Your institution's research computing documentation (ask about training!)

## Bioinformatics formats used in the course
* FASTA/FASTQ: SeqKit documentation (bioinf.shenwei.me/seqkit)
* VCF: the VCF v4.2 specification (samtools.github.io/hts-specs)
* Next steps: `samtools`, `bcftools`, workflow managers (Snakemake, Nextflow)

## Next steps after this course
1. Workflow managers: **Snakemake** (Python-based) or **Nextflow**, replacing `run_all.sh` for big pipelines.
2. Containers: **Docker / Apptainer** for full software reproducibility.
3. Continuous integration: **GitHub Actions** running your tests on every push.
4. Statistics: mixed models (`statsmodels`, R `lme4`) for field-trial designs.

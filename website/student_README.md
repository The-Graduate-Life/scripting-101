# Scripting 101: From Command Line Basics to Data Analysis Automation

A hands-on course that takes complete beginners (no Linux, programming, Conda or Git experience) to building reproducible Bash + Python workflows for real scientific datasets, using Windows Subsystem for Linux (WSL).

**Course website: <https://the-graduate-life.github.io/scripting-101/>**

## Quick start

```bash
# In Ubuntu on WSL (see resources/wsl_setup.md)
git clone https://github.com/The-Graduate-Life/scripting-101.git ~/scripting-101
cd ~/scripting-101
conda env create -f environment.yml
conda activate scripting101
bash scripts/bash/checksums.sh verify datasets      # -> All files OK
```

## Contents

| Folder | Contents |
|---|---|
| [`SYLLABUS.md`](SYLLABUS.md) | modules, hours, schedule, assessment |
| [`labs/`](labs/) | 11 hands-on labs, one folder per lab |
| [`handbook/`](handbook/STUDENT_HANDBOOK.md) | student handbook: the reference to keep |
| [`cheat_sheets/`](cheat_sheets/) | Linux CLI · Bash · Conda · Python · Git/GitHub · WSL · Troubleshooting |
| [`slides/`](slides/) | slides as PDF |
| [`datasets/`](datasets/) | course data (simulated maize trial + genomics) and its generator |
| [`scripts/`](scripts/) | example Bash, Python and HPC scripts |
| [`capstone/`](capstone/) | capstone brief, rubric and starter template |
| [`resources/`](resources/) | WSL setup guide, further reading |
| [`website/`](website/) | source of the course website (built automatically by GitHub Actions) |

## License

MIT (see [`LICENSE`](LICENSE)). The datasets are simulated and free to reuse.

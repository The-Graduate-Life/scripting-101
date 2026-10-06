# Module 3 — Conda and Reproducible Environments

!!! info "At a glance"

    **Time:** 3 hours (1 session)  
    **Labs:** Lab 05 · Conda  
    **Prerequisites:** Modules 1–2

## What you will be able to do

- Explain environments and dependency conflicts
- Explain reproducibility in terms of software versions
- Compare conda and pip; Miniforge and Anaconda
- Use channels: conda-forge and bioconda
- Create, activate, install, list, export and recreate environments
- Write and share an `environment.yml`
- Use conda environments from Bash scripts
- Diagnose conflicts and 'wrong Python' problems

## Topics

- Why environments: conflicts and reproducibility
- Miniforge, channels, conda-forge, bioconda
- `conda create / activate / install / remove / list / env list`
- How activation changes `$PATH`
- `environment.yml`, `env export`, `env create`, `env update --prune`
- Conda inside scripts (`conda shell.bash hook`, `conda run`)
- Troubleshooting dependency conflicts

## Materials

| Material | Link |
|---|---|
| :material-presentation: Slides | [Module 3 slides (PDF)]({{SLIDES_3}}) |
| :material-flask: Lab 05 · Conda | [Open the lab](../labs/lab05_conda/README.md) · 2 h |
| :material-card-text: Cheat sheets | [Conda](../cheat_sheets/conda.md) · [Troubleshooting](../cheat_sheets/troubleshooting.md) |
| :material-book-open-variant: Handbook | [Student handbook](../handbook/STUDENT_HANDBOOK.md) |

## Check your understanding

Try these after the labs. Discuss your answers in class.

1. Why should each project have its own environment?
2. What exactly changes when you run `conda activate`?
3. A script works interactively but fails in a scheduled job with `ModuleNotFoundError`. Why?
4. Which file do you commit so others can recreate your environment?

!!! tip "Stuck?"
    Read the last line of the error first, then check the [troubleshooting cheat sheet](../cheat_sheets/troubleshooting.md). Still stuck after 15 minutes? Ask, and bring the exact command and the full error text.

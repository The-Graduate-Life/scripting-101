# Module 6 — Integrating Bash, Python, Conda, Git and GitHub

!!! info "At a glance"

    **Time:** 4 hours (2 sessions)  
    **Labs:** Lab 10 · Integrated workflow  
    **Prerequisites:** Modules 2–5

## What you will be able to do

- Describe a complete reproducible workflow
- Decide what belongs in Bash and what in Python
- Call Python from Bash, and command-line tools from Python
- Write one entry-point script that runs everything
- Record provenance: versions, commit, inputs
- Prove reproducibility with a fresh clone

## Topics

- WSL → CLI → Conda → Bash → Python → Git → GitHub
- When Bash, when Python
- Bash calling Python; Python calling tools with `subprocess`
- Entry-point scripts, environment checks, logging with `tee`
- Provenance and the reproducibility test

## Materials

| Material | Link |
|---|---|
| :material-presentation: Slides | [Module 6 slides (PDF)]({{SLIDES_6}}) |
| :material-flask: Lab 10 · Integrated workflow | [Open the lab](../labs/lab10_integrated_workflow/README.md) · 3 h |
| :material-card-text: Cheat sheets | [Bash](../cheat_sheets/bash.md) · [Python](../cheat_sheets/python.md) · [Git & GitHub](../cheat_sheets/git_github.md) |
| :material-book-open-variant: Handbook | [Student handbook](../handbook/STUDENT_HANDBOOK.md) |

## Check your understanding

Try these after the labs. Discuss your answers in class.

1. Give two tasks better suited to Bash, and two to Python.
2. How does a Bash pipeline know that a Python step failed?
3. Why `subprocess.run([...])` instead of `os.system("...")`?
4. What does a `-dirty` suffix in `git describe` tell you?

!!! tip "Stuck?"
    Read the last line of the error first, then check the [troubleshooting cheat sheet](../cheat_sheets/troubleshooting.md). Still stuck after 15 minutes? Ask, and bring the exact command and the full error text.

# Scripting 101 — Syllabus

**From Command Line Basics to Data Analysis Automation**

| | |
|---|---|
| **Audience** | Complete beginners: no Linux, command-line, programming, Conda or Git experience assumed |
| **Platform** | Windows Subsystem for Linux (WSL 2) with Ubuntu |
| **Format** | Hands-on: short concept blocks (≤ 20 min) followed by guided and independent lab work |
| **Total contact time** | ≈ 61 hours (8 modules, 11 labs, capstone) |
| **Assessment** | Labs 30 % · module quizzes 10 % · Bash project 10 % · Python project 10 % · capstone 40 % |

## What you will be able to do at the end

Starting with no command-line experience, you will be able to **independently develop, troubleshoot, document, version-control and execute Bash and Python workflows for substantial scientific datasets**. Concretely:

1. Navigate and manipulate files entirely from the Linux command line, and inspect data without opening it.
2. Write robust Bash scripts that validate input, handle errors, log, and process thousands of files in parallel.
3. Create reproducible software environments with Conda.
4. Write Python programs that clean, analyse and visualise data, and turn exploratory analyses into tested command-line tools.
5. Version-control projects with Git and publish them on GitHub using SSH.
6. Combine all of the above into one-command, reproducible workflows.
7. Process datasets larger than memory, verify data integrity, and carry these skills to Linux servers and HPC clusters.

## Learning path

```text
 Beginner ──▶ Fundamental skills ──▶ Applied skills ──▶ Intermediate ──▶ Advanced ──▶ Independent workflow
   M1            M1 + M2a               M2b + M3           M4 + M5          M6 + M7          M8 capstone
```

## Modules

| # | Module | Hours | Labs | Builds on |
|---|---|---:|---|---|
| 1 | WSL and Linux command-line fundamentals | 8 | 01 Linux/WSL · 02 CLI file manipulation | – |
| 2 | Bash scripting: zero to advanced | 12 | 03 Bash fundamentals · 04 Advanced Bash (+ Bash project) | 1 |
| 3 | Conda and reproducible environments | 3 | 05 Conda | 1, 2 |
| 4 | Python scripting: zero to advanced data analysis | 14 | 06 Python fundamentals · 07 Python data analysis (+ Python project) | 1–3 |
| 5 | Git and GitHub from the command line | 5 | 08 Git/GitHub | 1–4 |
| 6 | Integrating Bash, Python, Conda, Git and GitHub | 4 | 10 Integrated workflow | 2–5 |
| 7 | Working with large scientific datasets | 5 | 09 Large-data processing | 2, 4, 6 |
| 8 | Capstone project | 10 | 11 Capstone | all |

> Lab numbers follow the topic list. In the schedule, Module 6 uses **Lab 10** and Module 7 uses **Lab 09**.

## Suggested schedules

### A. Semester (14 weeks × ~4.5 h)

| Week | Content |
|---|---|
| 1 | Setup, M1 Part 1 (Lab 01) |
| 2 | M1 Part 2 (Lab 02), quiz 1 |
| 3 | M2: first scripts, variables, conditions, loops (Lab 03) |
| 4 | M2: functions, arrays, text processing with grep/sed/awk (Lab 03 + Lab 04 A–B) |
| 5 | M2: robust scripts, getopts, processes, batch/parallel (Lab 04 C–D); Bash project starts |
| 6 | M3 Conda (Lab 05); Bash project due; quiz 2 |
| 7 | M4: Python basics (Lab 06 A–F) |
| 8 | M4: OS modules, argparse, logging, classes, testing (Lab 06 G–J) |
| 9 | M4: pandas, NumPy, Matplotlib, SciPy (Lab 07 A–G); Python project starts; quiz 3 |
| 10 | M5 Git and GitHub (Lab 08); Python project due |
| 11 | M6 Integrated workflow (Lab 10); capstone kick-off |
| 12 | M7 Large data and HPC concepts (Lab 09); quiz 4 |
| 13 | M8 Capstone sessions 2–4 |
| 14 | Capstone reproducibility review and presentations |

### B. Intensive (8 days × 7.5 h)

| Day | Morning | Afternoon |
|---|---|---|
| 1 | Setup, M1 (Lab 01) | M1 (Lab 02) |
| 2 | M2 basics (Lab 03) | M2 text processing (Lab 04 Session 1) |
| 3 | M2 robust/batch (Lab 04 Session 2) | M3 Conda (Lab 05) |
| 4 | M4 Python fundamentals (Lab 06) | Lab 06 continued |
| 5 | M4 data analysis (Lab 07) | Lab 07 project |
| 6 | M5 Git/GitHub (Lab 08) | M6 integration (Lab 10) |
| 7 | M7 large data (Lab 09) | Capstone sessions 1–2 |
| 8 | Capstone sessions 3–4 | Reproducibility review + presentations |

(In the intensive format, the capstone continues as a take-home over the following 1–2 weeks.)

## Materials

| Material | Location |
|---|---|
| Slides (PowerPoint) | [`slides/scripting-101.pptx`](slides/scripting-101.pptx) |
| Student handbook | [`handbook/STUDENT_HANDBOOK.md`](handbook/STUDENT_HANDBOOK.md) |
| Cheat sheets | [`cheat_sheets/`](cheat_sheets/) |
| Labs (student) | [`labs/`](labs/) |
| Datasets | [`datasets/`](datasets/) |
| Example scripts | [`scripts/`](scripts/) |
| Capstone | [`capstone/`](capstone/) |
| Setup guides and further reading | [`resources/`](resources/) |

## Course policies

* **Type, don't paste.** Copying commands teaches you nothing; typing and fixing your own typos does.
* **Read the error message.** Most errors say exactly what is wrong. Read the last line first.
* **Ask early.** If you are stuck for more than 15 minutes, ask a neighbour, then an instructor.
* **AI assistants** may be used as a reference, never as a substitute for understanding. You must be able to explain every line you submit.

# Module 2 — Bash Scripting: Zero to Advanced

!!! info "At a glance"

    **Time:** 12 hours (6 sessions)  
    **Labs:** Lab 03 · Bash fundamentals · Lab 04 · Advanced Bash  
    **Prerequisites:** Module 1

## What you will be able to do

- Write, make executable and run a script
- Use variables, quoting, arguments and exit codes
- Decide and repeat: `if`, `case`, `for`, `while`
- Organise code with functions and arrays
- Process text with `grep`, `sed` and `awk`
- Make scripts robust: strict mode, `trap`, logging, `getopts`
- Batch-process many files, also in parallel
- Manage processes and long-running jobs

## Topics

- Shebang, `chmod +x`, variables, quoting, `$( )`, arithmetic
- Positional arguments, `read`, exit codes, `[[ ]]` tests
- `if/elif/else`, `case`, `for`, `while`, parameter expansion
- Functions, arrays, input validation
- `grep -E`, `sed`, `awk` (group-by), `xargs`, `find`
- `set -euo pipefail`, `trap`, logging, `getopts`
- Batch and parallel processing (`xargs -P`, GNU `parallel`)
- Background jobs, `nohup`, `jobs`, `ps`, `top/htop`, `kill`

## Materials

| Material | Link |
|---|---|
| :material-presentation: Slides | [Module 2 slides (PDF)]({{SLIDES_2}}) |
| :material-flask: Lab 03 · Bash fundamentals | [Open the lab](../labs/lab03_bash_fundamentals/README.md) · 3 h |
| :material-flask: Lab 04 · Advanced Bash (+ graded project) | [Open the lab](../labs/lab04_advanced_bash/README.md) · 4 h |
| :material-card-text: Cheat sheets | [Bash](../cheat_sheets/bash.md) · [Linux CLI](../cheat_sheets/linux_cli.md) · [Troubleshooting](../cheat_sheets/troubleshooting.md) |
| :material-book-open-variant: Handbook | [Student handbook](../handbook/STUDENT_HANDBOOK.md) |

## Check your understanding

Try these after the labs. Discuss your answers in class.

1. What does `x=3; echo '$x' "$x" $((x*2))` print?
2. `f=reads_S01.fastq.gz`: which expansions give `S01.fastq.gz` and `reads_S01`?
3. Why does `zcat missing.gz | wc -l` 'succeed' without `pipefail`?
4. Write an `awk` command printing the mean of column 3 of a CSV with a header.
5. Why must each parallel job write its own output file?
6. When should a Bash script become a Python program?

!!! tip "Stuck?"
    Read the last line of the error first, then check the [troubleshooting cheat sheet](../cheat_sheets/troubleshooting.md). Still stuck after 15 minutes? Ask, and bring the exact command and the full error text.

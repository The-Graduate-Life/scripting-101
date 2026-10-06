# Module 1 — WSL and Linux Command-Line Fundamentals

!!! info "At a glance"

    **Time:** 8 hours (4 sessions)  
    **Labs:** Lab 01 · Linux & WSL · Lab 02 · Files & data on the command line  
    **Prerequisites:** None: just WSL with Ubuntu installed ([Getting started](../getting-started.md))

## What you will be able to do

- Explain Linux, WSL, terminal, shell and Bash
- Navigate with absolute and relative paths
- Reach Windows files from Linux via `/mnt/c`
- Manage files: create, copy, move, delete, link
- Inspect data files without opening them
- Combine commands with pipes, redirection and chaining
- Use permissions (`chmod`) and environment variables (`$PATH`)
- Compress and archive files (`gzip`, `tar`, `zip`)

## Topics

- Linux, WSL, terminal vs shell vs Bash; CLI vs GUI
- The filesystem tree, home directory, absolute and relative paths
- `pwd ls cd mkdir touch cp mv rm rmdir ln -s`
- `cat less head tail wc file du df tree`
- `cut sort uniq paste grep find locate which whereis`
- Wildcards; `>` `>>` `<` `2>` `2>&1`; pipes; `&&` `||` `;`
- Permissions and executables; hidden files; `$PATH`
- `gzip gunzip zip unzip tar`; copying vs linking

## Materials

| Material | Link |
|---|---|
| :material-presentation: Slides | [Module 1 slides (PDF)]({{SLIDES_1}}) |
| :material-flask: Lab 01 · Linux & WSL | [Open the lab](../labs/lab01_linux_wsl/README.md) · 90 min |
| :material-flask: Lab 02 · Files & data on the command line | [Open the lab](../labs/lab02_cli_files/README.md) · 2.5 h |
| :material-card-text: Cheat sheets | [Linux CLI](../cheat_sheets/linux_cli.md) · [WSL](../cheat_sheets/wsl.md) · [Troubleshooting](../cheat_sheets/troubleshooting.md) |
| :material-book-open-variant: Handbook | [Student handbook](../handbook/STUDENT_HANDBOOK.md) |

## Check your understanding

Try these after the labs. Discuss your answers in class.

1. You are in `~/lab02/data`. Give the absolute and the relative path to `~/lab02/scripts`.
2. Why must `sort` come before `uniq -c`?
3. What exactly does `./run.sh > run.log 2>&1` do?
4. What is the difference between `chmod 755` and `chmod u+x`?
5. Your colleague deleted the folder your symlink points to. What happens?
6. Write one pipeline that finds the three site-years with the most missing yields.

!!! tip "Stuck?"
    Read the last line of the error first, then check the [troubleshooting cheat sheet](../cheat_sheets/troubleshooting.md). Still stuck after 15 minutes? Ask, and bring the exact command and the full error text.

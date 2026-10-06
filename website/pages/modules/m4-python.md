# Module 4 — Python Scripting: Zero to Data Analysis

!!! info "At a glance"

    **Time:** 14 hours (7 sessions)  
    **Labs:** Lab 06 · Python fundamentals · Lab 07 · Python data analysis  
    **Prerequisites:** Modules 1–3 and the `scripting101` environment

## What you will be able to do

- Run Python interactively and as scripts
- Use types, strings, lists, tuples, dictionaries and sets
- Write control flow, functions and modules
- Read and write files; handle exceptions
- Build command-line programs with `argparse` and `logging`
- Test with `pytest`; debug with `breakpoint()`
- Analyse and plot data with pandas, NumPy, SciPy and Matplotlib
- Turn exploratory analysis into tested production scripts

## Topics

- Interpreter, REPL/IPython, `.py` scripts
- Types, strings, collections, operators, conditions, loops
- Functions, modules, imports, file I/O, exceptions
- `pathlib os sys shutil glob re argparse logging subprocess`
- Classes (dataclasses), testing, debugging
- pandas: read, clean, filter, sort, group, merge, missing data
- Statistics (SciPy) and publication-quality figures (Matplotlib)
- Memory, chunk processing; interactive vs production code

## Materials

| Material | Link |
|---|---|
| :material-presentation: Slides | [Module 4 slides (PDF)]({{SLIDES_4}}) |
| :material-flask: Lab 06 · Python fundamentals | [Open the lab](../labs/lab06_python_fundamentals/README.md) · 5 h |
| :material-flask: Lab 07 · Python data analysis (+ graded project) | [Open the lab](../labs/lab07_python_data_analysis/README.md) · 6 h |
| :material-card-text: Cheat sheets | [Python](../cheat_sheets/python.md) · [Troubleshooting](../cheat_sheets/troubleshooting.md) |
| :material-book-open-variant: Handbook | [Student handbook](../handbook/STUDENT_HANDBOOK.md) |

## Check your understanding

Try these after the labs. Discuss your answers in class.

1. What does `[x**2 for x in range(5) if x % 2]` return?
2. Why use `with open(...) as fh:` instead of `fh = open(...)`?
3. Write the pandas expression for mean yield per site and year.
4. `agg` vs `transform`: what is the difference?
5. Why can't you average the means of chunks?
6. Name four differences between a notebook and a production script.

!!! tip "Stuck?"
    Read the last line of the error first, then check the [troubleshooting cheat sheet](../cheat_sheets/troubleshooting.md). Still stuck after 15 minutes? Ask, and bring the exact command and the full error text.

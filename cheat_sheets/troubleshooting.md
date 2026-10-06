# Troubleshooting Cheat Sheet

## The method (in order)
1. **Read the last line** of the error message, out loud.
2. **Where am I? What's here?** `pwd` · `ls -la`
3. **Which program?** `which python` · `type cmd` · `echo $CONDA_DEFAULT_ENV`
4. **What did I type?** `history | tail` (typos, quotes, spaces, `\` vs `/`)
5. **Make it smaller:** run one step; `bash -x script.sh`; `set -x`; `breakpoint()`
6. **Search** the exact message in quotes, then **ask**: command + expected + actual + full error text (not a screenshot).

## Shell and files
| Message | Cause → fix |
|---|---|
| `command not found` | typo · not installed (`sudo apt install`, `conda install`) · env not active · own script needs `./` |
| `No such file or directory` | wrong folder (`pwd`) · typo (use Tab) · unquoted spaces · Windows path (`/mnt/c/...`) |
| `Permission denied` (running) | `chmod u+x script.sh` |
| `Permission denied` (writing) | read-only file (`chmod u+w`) · system folder (work in `~`) |
| `Is a directory` / `Not a directory` | `cp` without `-r`; path mistake |
| `Argument list too long` | too many files for `*` → `find ... -print0 \| xargs -0` |
| `No space left on device` | `df -h`; `du -sh * \| sort -h`; `conda clean --all` |
| output file is empty | `cmd f > f` truncated the input · filter matched nothing |
| `uniq -c` miscounts | input not sorted |
| strange `^M` | CRLF line endings → `dos2unix` |

## Bash scripts
| Message | Cause → fix |
|---|---|
| `x: command not found` | `x = 1` → `x=1` |
| `[: missing ']'` · `[1: command not found` | spaces inside brackets: `[[ $a -gt 1 ]]` |
| `unbound variable` | `set -u`: give a default `${1:-}` or check `$#` |
| `$'\r': command not found` · `bash\r` | Windows line endings → `dos2unix script.sh` |
| `syntax error near unexpected token` | missing `then`/`do`/`fi`/`done`/`esac`; unbalanced quotes |
| `invalid arithmetic operator` | decimals in `(( ))` → `awk` |
| script stops silently | `set -e` + a command returning non-zero (`grep` no match) → `\|\| true` |
| loop splits names with spaces | quote `"$f"`; use globs or `-print0` |
| `xargs` "function not found" | `export -f fn` |
| exit code 127 / 126 / 130 / 141 | not found / not executable / Ctrl+C / SIGPIPE (e.g. `head`) |

## Conda
| Message | Cause → fix |
|---|---|
| `conda: command not found` | `~/miniforge3/bin/conda init bash && exec bash` |
| `Run 'conda init' before 'conda activate'` | in scripts: `eval "$(conda shell.bash hook)"` |
| `ModuleNotFoundError` | wrong env → activate; `which python`; `conda list pkg` |
| `PackagesNotFoundError` | wrong channel/name → `-c conda-forge` / `-c bioconda` |
| unsatisfiable / conflicts | relax version pins; create a fresh env |

## Python
| Message | Cause → fix |
|---|---|
| `IndentationError` / `TabError` | consistent 4 spaces |
| `NameError` | typo; variable defined elsewhere (scope) |
| `TypeError: can only concatenate str` | `"a" + 1` → f-string |
| `KeyError` | key/column spelled differently → print `d.keys()` / `df.columns` |
| `IndexError` | list shorter than expected (empty line?) |
| `ValueError: could not convert string to float: 'NA'` | handle missing values (`try/except`, `na_values`) |
| `FileNotFoundError` | path relative to where you *run* → `Path(__file__).parent` / argparse |
| `AttributeError: 'NoneType' ...` | a function returned `None` (missing `return`) |
| `SettingWithCopyWarning` | `.copy()` after filtering or `.loc` assignment |
| merge gives more rows | duplicate keys → `validate="many_to_one"` |
| `MemoryError` / WSL freezes | `usecols`, `dtype`, `chunksize`; `.wslconfig` |
| blank figure | `savefig` before `close`; `matplotlib.use("Agg")` |

## Git and SSH
| Message | Cause → fix |
|---|---|
| `Author identity unknown` | `git config --global user.name/email` |
| `not a git repository` | wrong folder; `git init` |
| `Permission denied (publickey)` | add `.pub` to GitHub; `ssh-add`; `ssh -vT git@github.com` |
| asks for a password | HTTPS remote → `git remote set-url origin git@github.com:u/r.git` |
| `rejected ... fetch first` | `git pull`, resolve, `git push` |
| `src refspec main does not match any` | no commits yet · branch named master → `git branch -M main` |
| `CONFLICT (content)` | edit file, remove markers, `git add`, `git commit` |
| file > 100 MB rejected | `git rm --cached`; `.gitignore`; `git commit --amend` |
| `UNPROTECTED PRIVATE KEY FILE` | `chmod 600 ~/.ssh/id_ed25519` (keys in `~/.ssh`, not `/mnt/c`) |

## How to ask for help (template)
```text
Goal:     I want to ... 
Command:  <exact command, copied as text>
Expected: ...
Got:      <full error text>
Tried:    which python -> ..., pwd -> ..., ...
```

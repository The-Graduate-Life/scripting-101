# Conda Cheat Sheet

## Install (Miniforge, once)
```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-Linux-x86_64.sh -b -p ~/miniforge3
~/miniforge3/bin/conda init bash && exec bash
conda config --set auto_activate_base false        # optional
conda config --add channels bioconda
conda config --add channels conda-forge            # conda-forge on top
conda config --set channel_priority strict
```

## Environments
| Command | Does |
|---|---|
| `conda create -n NAME python=3.12 pandas` | create |
| `conda activate NAME` / `conda deactivate` | switch |
| `conda env list` | list envs (`*` = active) |
| `conda env remove -n NAME` | delete env |
| `conda create -n NEW --clone OLD` | copy env |

## Packages
| Command | Does |
|---|---|
| `conda install PKG=1.2` | install (version optional) |
| `conda install -c bioconda seqkit` | from a specific channel |
| `conda remove PKG` | uninstall |
| `conda update PKG` | update |
| `conda list [PKG]` | installed packages |
| `conda search PKG` | available versions |
| `python -m pip install PKG` | pip-only packages (inside the env, last) |

## Reproducibility
| Command | Does |
|---|---|
| `conda env create -f environment.yml` | build env from file |
| `conda env update -f environment.yml --prune` | sync env to file |
| `conda env export --from-history > environment.yml` | what you asked for (portable) |
| `conda env export --no-builds > env.lock.yml` | exact versions |
| `conda env export > env.full.yml` | exact versions + builds (same OS) |

```yaml
name: myproject
channels: [conda-forge, bioconda]
dependencies:
  - python=3.12
  - pandas>=2.2
  - matplotlib
  - seqkit
  - pip
  - pip: [pypi-only-pkg]
```

## In scripts
```bash
eval "$(conda shell.bash hook)" && conda activate NAME
conda run -n NAME python script.py
```

## Check what you are using
`which python` · `python -c "import sys; print(sys.executable)"` · `echo $CONDA_DEFAULT_ENV` · `conda info`

## Maintenance
`conda clean --all` (free disk) · `mamba` = faster drop-in for `conda`

## Rules
1. One env per project, never install into `base`.
2. Commit `environment.yml`; recreate it to test.
3. conda first, pip last (and only inside the env).
4. Pin what matters (`python=3.12`), not everything.
5. Install Miniforge in `~`, never under `/mnt/c`.

## Fixes
| Problem | Fix |
|---|---|
| `conda: command not found` | `~/miniforge3/bin/conda init bash && exec bash` |
| `Run 'conda init' before 'conda activate'` (script) | `eval "$(conda shell.bash hook)"` |
| `ModuleNotFoundError` | wrong env → activate; `conda list PKG` |
| unsatisfiable / conflict | relax pins; new env; conda-forge first + strict |
| very slow solve | fewer packages per env, strict priority, `mamba` |

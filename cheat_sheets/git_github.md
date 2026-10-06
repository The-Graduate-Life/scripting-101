# Git and GitHub Cheat Sheet

```text
working dir ──git add──▶ staging area ──git commit──▶ local repo ──git push──▶ GitHub
                                                                 ◀──git pull── (fetch + merge)
```

## Setup (once)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
git config --global init.defaultBranch main
git config --global core.autocrlf input        # WSL: keep LF line endings
git config --global core.editor "nano"         # or "code --wait"
```

## SSH (once per computer)
```bash
ssh-keygen -t ed25519 -C "you@example.org"    # Enter, then a passphrase
cat ~/.ssh/id_ed25519.pub                     # copy → GitHub Settings → SSH and GPG keys
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com                         # "Hi <user>! You've successfully authenticated..."
```
🔑 `id_ed25519` = private, **never share** · 🔓 `id_ed25519.pub` = public, goes to GitHub

## Start
| | |
|---|---|
| `git init` | new repo in the current folder |
| `git clone git@github.com:user/repo.git` | copy a remote repo |
| `git remote add origin git@github.com:user/repo.git` | connect to GitHub |
| `git push -u origin main` | first push |

## Daily
| | |
|---|---|
| `git status` | what changed? (run it constantly) |
| `git diff` / `git diff --staged` | unstaged / staged changes |
| `git add file` · `git add -p` | stage file · stage hunks interactively |
| `git commit -m "Imperative summary"` | record a snapshot |
| `git log --oneline --graph --all` | history |
| `git pull` / `git push` / `git fetch` | sync |

## Branches
| | |
|---|---|
| `git branch` | list |
| `git switch -c feature` | create + switch |
| `git switch main` | switch |
| `git merge feature` | merge into current |
| `git branch -d feature` | delete merged branch |

## Conflicts
1. `git status` shows `UU file` · 2. edit the file, keep the right content, delete `<<<<<<< ======= >>>>>>>` · 3. `git add file` · 4. `git commit` · (abort: `git merge --abort`)

## Undo
| Situation | Command |
|---|---|
| discard unstaged edits | `git restore file` |
| unstage | `git restore --staged file` |
| fix last commit (not pushed) | `git commit --amend` |
| undo a pushed commit | `git revert HASH` |
| stop tracking a file, keep it | `git rm --cached file` |
| old version of a file | `git show HASH:path` |
| find lost commits | `git reflog` |

## Tags and releases
`git tag -a v1.0 -m "Submission"` · `git push origin v1.0`

## .gitignore (data-analysis project)
```text
data/raw/
data/processed/
results/
logs/
*.log
__pycache__/
.ipynb_checkpoints/
.env
*.pem
```

## Professional repo
`README.md` · `LICENSE` · `.gitignore` · `environment.yml` (+ `requirements.txt` for pip users) · `src/` · `scripts/` · `data/` (README only) · `results/` · `docs/` · `tests/` · `run_all.sh`

## Good commits
✔ small, one logical change · ✔ imperative mood, ≤ 50-char summary ("Add battery alert option") · ✔ commit often · ✘ data, outputs, secrets · ✘ "fix", "stuff", "final2"

## GitHub
Issues (`Fixes #3` in a commit message closes issue 3) · Pull requests (propose merging a branch) · README renders on the front page · Releases from tags

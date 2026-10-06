# Publishing the course website (GitHub Pages, free)

Result: a public website at **`https://The-Graduate-Life.github.io/scripting-101/`** with one section per module.
It rebuilds by itself every time you push a change.

**What is public:** labs, handbook, cheat sheets, slides (PDF), datasets, example scripts, capstone brief, rubric and template.
**What stays private** (only on your computer): `solutions/`, `capstone/reference_solution/`, `instructor_guide/`, and the `.pptx` deck (its speaker notes contain answers).

All commands run in **Ubuntu (WSL)**. Allow about 20 minutes the first time.

---

## Step 1 — Tell Git who you are (once)

```bash
git config --global user.name "Your Name"
git config --global user.email "the-email-of-your-github-account@example.org"
git config --global init.defaultBranch main
```

## Step 2 — Create the public (student) copy

```bash
bash /mnt/c/Users/fritz/OneDrive/Desktop/fritz/scripting-101/website/make_public_copy.sh -m 1
cd ~/scripting-101-public
git commit -m "Scripting 101 course materials"
```

The script copies the student material into `~/scripting-101-public`, **starting with Module 1 only**
(`-m 1`; use `-m 8` to publish everything at once). Instructor-only material is never copied.
(If the folder already exists, it was created for you; just `cd` into it and commit.)

## Step 3 — Log in to GitHub from the terminal (once)

```bash
sudo apt update && sudo apt install -y gh
gh auth login
```

Answer: **GitHub.com** → **HTTPS** → **Yes** (authenticate Git) → **Login with a web browser**.
Copy the one-time code shown, press Enter, and paste the code in the browser page that opens
(if no browser opens, go to <https://github.com/login/device>).

## Step 4 — Create the repository and upload

```bash
cd ~/scripting-101-public
gh repo create scripting-101 --public --source . --push \
   --description "Scripting 101: from command-line basics to data-analysis automation"
```

## Step 5 — Switch on GitHub Pages (once)

1. Open `https://github.com/<your-username>/scripting-101` in the browser.
2. **Settings** → **Pages** (left menu).
3. Under **Build and deployment → Source**, choose **GitHub Actions**.
4. Start the first build:
   ```bash
   gh workflow run pages.yml
   gh run watch          # follow it; takes ~1–2 minutes
   ```
5. Visit **`https://<your-username>.github.io/scripting-101/`** 🎉

Tip: on the repository's front page, click the ⚙ next to **About** and tick
*Use your GitHub Pages website*, so the link shows at the top of the repository.

---

## Day-to-day use

**One rule: always edit in your private Desktop folder** (`/mnt/c/Users/fritz/OneDrive/Desktop/fritz/scripting-101`),
never in `~/scripting-101-public`. Publish with `release.py`, which refreshes the public copy from your folder
(labs and slides of released modules, handbook, cheat sheets, scripts, datasets, website pages), then commits and pushes.

**Release the next module (e.g. each week):** run this from Ubuntu. It copies the module's labs and
slides into the public copy, updates the website, commits and uploads:

```bash
cd /mnt/c/Users/fritz/OneDrive/Desktop/fritz/scripting-101
python3 website/release.py 2 --push        # week 2: modules 1-2 are now public
python3 website/release.py 3 --push        # week 3: modules 1-3 ...
```

Until a module is released, its labs and slides are **not in the public repository at all**, so students
cannot read ahead on GitHub; the website lists it as *coming soon*. The handbook, cheat sheets, syllabus and
datasets are published from the start.

Fixed a typo in an already released lab? Run the **same** command again (e.g. `release.py 3 --push`).

> **Note:** releasing is one-way in practice. Running a lower number removes a module from the website,
> but anything already pushed stays visible in the repository's Git history.

**Preview before publishing** (optional):

```bash
conda activate scripting101
pip install -r website/requirements.txt
python website/build_site.py
mkdocs serve -f website/build/mkdocs.yml      # open http://127.0.0.1:8000 in your Windows browser
```

**If a build fails:** open the repository's **Actions** tab, click the red run, and read the last lines of the failing step.
The most common cause is a broken link in a Markdown file (the build runs in strict mode on purpose).

---

## The private instructor repository

Your full course folder (with solutions, instructor guide and the `.pptx`) is backed up to the **private** repository
<https://github.com/The-Graduate-Life/scripting-101-instructor>. After editing, save your work there too:

```bash
cd /mnt/c/Users/fritz/OneDrive/Desktop/fritz/scripting-101
git add -A
git commit -m "Describe what you changed"
git push
```

Then publish student-facing changes with `python3 website/release.py N --push` as above.
The website workflow only runs in the public repository, so pushing here never publishes anything.

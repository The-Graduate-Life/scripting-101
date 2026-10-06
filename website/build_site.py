#!/usr/bin/env python3
"""build_site.py — assemble the Scripting 101 course website (MkDocs Material).

Collects the STUDENT materials from the repository into website/build/docs,
splits the slide PDF into one PDF per module, zips the downloads, rewrites
links, and writes website/build/mkdocs.yml with one navigation section per
released module.

Usage (from the repository root):
    python website/build_site.py                 # all modules listed in website/release.txt
    python website/build_site.py --released 3    # only modules 1-3 (others stay hidden)
    mkdocs serve -f website/build/mkdocs.yml     # preview at http://127.0.0.1:8000
    mkdocs build -f website/build/mkdocs.yml     # static site in website/build/site

Never published: solutions/, capstone/reference_solution/, instructor_guide/,
slides/build/ and the .pptx file (its speaker notes contain answers).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "website"
OUT = WEB / "build"
DOCS = OUT / "docs"

PRIVATE = ("solutions", "capstone/reference_solution", "instructor_guide", "slides/build", "slides/scripting-101.pptx")

MODULES = [  # number, page slug, title, labs (folder names)
    (1, "m1-linux-cli", "WSL & Linux command line", ["lab01_linux_wsl", "lab02_cli_files"]),
    (2, "m2-bash", "Bash scripting", ["lab03_bash_fundamentals", "lab04_advanced_bash"]),
    (3, "m3-conda", "Conda environments", ["lab05_conda"]),
    (4, "m4-python", "Python & data analysis", ["lab06_python_fundamentals", "lab07_python_data_analysis"]),
    (5, "m5-git-github", "Git & GitHub", ["lab08_git_github"]),
    (6, "m6-integration", "Integrated workflows", ["lab10_integrated_workflow"]),
    (7, "m7-large-data", "Large datasets & HPC", ["lab09_large_data"]),
    (8, "m8-capstone", "Capstone project", ["lab11_capstone"]),
]
LAB_TITLES = {
    "lab01_linux_wsl": "Lab 01 · Linux & WSL", "lab02_cli_files": "Lab 02 · Files & data on the CLI",
    "lab03_bash_fundamentals": "Lab 03 · Bash fundamentals", "lab04_advanced_bash": "Lab 04 · Advanced Bash",
    "lab05_conda": "Lab 05 · Conda", "lab06_python_fundamentals": "Lab 06 · Python fundamentals",
    "lab07_python_data_analysis": "Lab 07 · Python data analysis", "lab08_git_github": "Lab 08 · Git & GitHub",
    "lab09_large_data": "Lab 09 · Large data", "lab10_integrated_workflow": "Lab 10 · Integrated workflow",
    "lab11_capstone": "Lab 11 · Capstone workshop",
}


def is_private(rel: str) -> bool:
    return any(rel == p or rel.startswith(p + "/") for p in PRIVATE)


def copy_md(src_rel: str, dst_rel: str | None = None, transform=None) -> None:
    src = ROOT / src_rel
    dst = DOCS / (dst_rel or src_rel)
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    if transform:
        text = transform(text)
    # remember where the file came from, for link rewriting
    SOURCE_OF[dst] = src
    dst.write_text(text, encoding="utf-8")


SOURCE_OF: dict[Path, Path] = {}


def strip_spoilers(text: str) -> str:
    """datasets/README.md lists the planted data problems: students should discover them."""
    return re.sub(r"## Deliberate problems.*?(?=## Integrity)", "", text, flags=re.S)


def facts_box(text: str) -> str:
    """Turn a lab's leading '| | |' facts table into an 'At a glance' box (no empty header row)."""
    m = re.search(r"\n\| \| \|\n\|---\|---\|\n((?:\|.*\|\n)+)", text)
    if not m:
        return text
    rows = []
    for line in m.group(1).strip().splitlines():
        cells = [c.strip() for c in line.strip("|").split("|", 1)]
        rows.append(f"    {cells[0]}: {cells[1]}  ")
    box = '\n!!! info "At a glance"\n\n' + "\n".join(rows) + "\n"
    return text[:m.start()] + box + text[m.end():]


def split_slides(released: list[int]) -> dict[int, str]:
    """Split slides/scripting-101.pdf at the 'MODULE N' divider pages."""
    pre = ROOT / "slides" / "modules"                      # per-module PDFs (public copy)
    if pre.is_dir():
        out = DOCS / "downloads" / "slides"
        out.mkdir(parents=True, exist_ok=True)
        files = {}
        for n in [0] + released:
            name = "00_introduction.pdf" if n == 0 else f"module{n}_slides.pdf"
            if (pre / name).exists():
                shutil.copy2(pre / name, out / name)
                files[n] = f"downloads/slides/{name}"
        return files

    from pypdf import PdfReader, PdfWriter

    pdf = ROOT / "slides" / "scripting-101.pdf"
    if not pdf.exists():
        print("warning: slides/scripting-101.pdf not found; no slide downloads", file=sys.stderr)
        return {}
    reader = PdfReader(str(pdf))
    starts = {}
    for i, page in enumerate(reader.pages):
        m = re.search(r"MODULE\s+(\d)\b", page.extract_text() or "")
        if m and int(m.group(1)) not in starts:
            starts[int(m.group(1))] = i
    out = DOCS / "downloads" / "slides"
    out.mkdir(parents=True, exist_ok=True)
    files = {}
    bounds = sorted(starts.items()) + [(99, len(reader.pages))]
    ranges = {0: (0, bounds[0][1])} | {n: (s, bounds[k + 1][1]) for k, (n, s) in enumerate(bounds[:-1])}
    for n, (a, b) in ranges.items():
        if n and n not in released:
            continue
        w = PdfWriter()
        for p in range(a, b):
            w.add_page(reader.pages[p])
        name = "00_introduction.pdf" if n == 0 else f"module{n}_slides.pdf"
        with open(out / name, "wb") as fh:
            w.write(fh)
        files[n] = f"downloads/slides/{name}"
    return files


def make_zip(name: str, folder: str, arc_root: str) -> str:
    out = DOCS / "downloads" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted((ROOT / folder).rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, Path(arc_root) / f.relative_to(ROOT / folder))
    return f"downloads/{name}"


LINK = re.compile(r"(!?)\[([^\]]+)\]\(([^)\s]+)\)")


def rewrite_links(repo_blob: str | None) -> list[str]:
    """Keep links that resolve inside the site; send other repository files to GitHub; drop private ones."""
    notes = []
    for md in DOCS.rglob("*.md"):
        src = SOURCE_OF.get(md)
        text = md.read_text(encoding="utf-8")

        def fix(m: re.Match) -> str:
            bang, label, target = m.groups()
            if re.match(r"^(https?:|mailto:|#)", target):
                return m.group(0)
            path, _, frag = target.partition("#")
            frag = "#" + frag if frag else ""
            site_target = (md.parent / path).resolve()
            if site_target.is_file():
                return m.group(0)
            if site_target.is_dir() and (site_target / "README.md").exists():
                return f"{bang}[{label}]({path.rstrip('/')}/README.md{frag})"
            if src is None:
                notes.append(f"{md.relative_to(DOCS)}: unresolved {target}")
                return label
            repo_target = (src.parent / path).resolve()
            try:
                rel = repo_target.relative_to(ROOT).as_posix()
            except ValueError:
                return label
            if repo_target.exists() and not is_private(rel) and repo_blob:
                kind = "tree" if repo_target.is_dir() else "blob"
                return f"{bang}[{label}]({repo_blob.replace('/blob/', f'/{kind}/')}/{rel}{frag})"
            notes.append(f"{md.relative_to(DOCS)}: link to {rel} removed")
            return label

        new = LINK.sub(fix, text)
        if new != text:
            md.write_text(new, encoding="utf-8")
    return notes


def mkdocs_yml(released: list[int], site_url: str, repo_url: str | None) -> str:
    nav = ["  - Home: index.md", "  - Getting started:", "      - Setup checklist: getting-started.md",
           "      - WSL setup guide: resources/wsl_setup.md", "      - Syllabus: syllabus.md"]
    for n, slug, title, labs in MODULES:
        if n not in released:
            continue
        nav.append(f"  - 'Module {n}: {title}':")
        nav.append(f"      - Overview: modules/{slug}.md")
        for lab in labs:
            nav.append(f"      - '{LAB_TITLES[lab]}': labs/{lab}/README.md")
        if n == 8:
            nav += ["      - Project brief: capstone/PROJECT_SPEC.md", "      - Grading rubric: capstone/RUBRIC.md"]
    nav += [
        "  - Reference:",
        "      - Student handbook: handbook/STUDENT_HANDBOOK.md",
        "      - 'Cheat sheet: Linux CLI': cheat_sheets/linux_cli.md",
        "      - 'Cheat sheet: Bash': cheat_sheets/bash.md",
        "      - 'Cheat sheet: Conda': cheat_sheets/conda.md",
        "      - 'Cheat sheet: Python': cheat_sheets/python.md",
        "      - 'Cheat sheet: Git & GitHub': cheat_sheets/git_github.md",
        "      - 'Cheat sheet: WSL': cheat_sheets/wsl.md",
        "      - 'Cheat sheet: Troubleshooting': cheat_sheets/troubleshooting.md",
        "      - Datasets: datasets/README.md",
        "      - Example scripts: scripts/README.md",
        "      - Further reading: resources/further_reading.md",
        "  - Downloads: downloads.md",
    ]
    repo = f"repo_url: {repo_url}\nrepo_name: GitHub repository\nedit_uri: ''\n" if repo_url else ""
    return f"""# GENERATED by website/build_site.py — edit that script, not this file.
site_name: Scripting 101
site_description: From command-line basics to data-analysis automation, a hands-on course on WSL, Bash, Conda, Python, Git and GitHub.
site_url: {site_url}
{repo}docs_dir: docs
site_dir: site
theme:
  name: material
  language: en
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue grey
      accent: amber
      toggle: {{icon: material/weather-night, name: Dark mode}}
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue grey
      accent: amber
      toggle: {{icon: material/weather-sunny, name: Light mode}}
  font: {{text: Lato, code: JetBrains Mono}}
  icon: {{logo: material/console}}
  features:
    - navigation.sections
    - navigation.expand
    - navigation.top
    - navigation.footer
    - search.suggest
    - search.highlight
    - content.code.copy
    - toc.follow
extra_css: [assets/extra.css]
markdown_extensions:
  - tables
  - admonition
  - attr_list
  - md_in_html
  - toc: {{permalink: true}}
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight: {{anchor_linenums: false}}
  - pymdownx.inlinehilite
  - pymdownx.tasklist: {{custom_checkbox: true}}
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
plugins: [search]
not_in_nav: |
  /labs/README.md
validation:
  links: {{not_found: warn, anchors: ignore, unrecognized_links: ignore}}
nav:
{chr(10).join(nav)}
"""


def module_table(released: list[int]) -> str:
    rows = ["| | Module | Labs |", "|---|---|---|"]
    for n, slug, title, labs in MODULES:
        if n in released:
            rows.append(f"| **{n}** | [{title}](modules/{slug}.md) | " + " · ".join(f"[{LAB_TITLES[l].split(' · ')[0]}](labs/{l}/README.md)" for l in labs) + " |")
        else:
            rows.append(f"| {n} | {title} *(coming soon)* | |")
    return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--released", type=int, help="number of released modules (default: website/release.txt)")
    args = ap.parse_args()
    n_rel = args.released or int((WEB / "release.txt").read_text().split()[0])
    released = list(range(1, max(0, min(8, n_rel)) + 1))

    gh = os.environ.get("GITHUB_REPOSITORY")                         # "owner/repo" inside GitHub Actions
    if gh:
        owner, repo = gh.split("/")
        site_url = f"https://{owner.lower()}.github.io/{repo}/"
        repo_url = f"https://github.com/{gh}"
    else:
        site_url = os.environ.get("SITE_URL", "http://127.0.0.1:8000/")
        repo_url = os.environ.get("REPO_URL")
    repo_blob = f"{repo_url}/blob/main" if repo_url else None

    if OUT.exists():
        shutil.rmtree(OUT)
    DOCS.mkdir(parents=True)

    # hand-written site pages
    shutil.copytree(WEB / "pages", DOCS, dirs_exist_ok=True)
    for p in (WEB / "pages").rglob("*.md"):
        SOURCE_OF[DOCS / p.relative_to(WEB / "pages")] = p
    for n, slug, _t, _l in MODULES:                                   # hide unreleased modules
        if n not in released:
            (DOCS / "modules" / f"{slug}.md").unlink(missing_ok=True)

    # course materials
    for n, _slug, _t, labs in MODULES:
        if n in released:
            for lab in labs:
                copy_md(f"labs/{lab}/README.md", transform=facts_box)
    for f in ["handbook/STUDENT_HANDBOOK.md", "resources/wsl_setup.md", "resources/further_reading.md", "scripts/README.md"]:
        copy_md(f)
    for f in sorted((ROOT / "cheat_sheets").glob("*.md")):
        copy_md(f"cheat_sheets/{f.name}")
    copy_md("datasets/README.md", transform=strip_spoilers)
    if 8 in released:
        copy_md("capstone/PROJECT_SPEC.md")
        copy_md("capstone/RUBRIC.md")
    site_links = {"[`slides/scripting-101.pptx`](slides/scripting-101.pptx)": "[Downloads](downloads.md) (PDF per module)",
                  "[`handbook/STUDENT_HANDBOOK.md`](handbook/STUDENT_HANDBOOK.md)": "[Student handbook](handbook/STUDENT_HANDBOOK.md)",
                  "[`cheat_sheets/`](cheat_sheets/)": "[Cheat sheets](cheat_sheets/linux_cli.md)",
                  "[`labs/`](labs/)": "one lab page per module (see the menu)",
                  "[`datasets/`](datasets/)": "[Datasets](datasets/README.md)",
                  "[`scripts/`](scripts/)": "[Example scripts](scripts/README.md)",
                  "[`capstone/`](capstone/)": "[Capstone brief](capstone/PROJECT_SPEC.md)",
                  "[`resources/`](resources/)": "[WSL setup](resources/wsl_setup.md) · [Further reading](resources/further_reading.md)"}

    def syllabus(t: str) -> str:
        t = "\n".join(l for l in t.splitlines() if "instructor_guide/" not in l and "solutions/" not in l)
        for a, b in site_links.items():
            t = t.replace(a, b)
        return t
    copy_md("SYLLABUS.md", "syllabus.md", transform=syllabus)
    # downloads
    slides = split_slides(released)
    zips = {"datasets": make_zip("datasets.zip", "datasets", "scripting-101/datasets"),
            "scripts": make_zip("scripts.zip", "scripts", "scripting-101/scripts"),
            "template": make_zip("capstone_template.zip", "capstone/template", "harvest-n-trial"),
            "cheats": make_zip("cheat_sheets.zip", "cheat_sheets", "cheat_sheets")}
    shutil.copy2(ROOT / "environment.yml", DOCS / "downloads" / "environment.yml")

    # fill placeholders in the hand-written pages
    slide_rows = ["| Slides | Download |", "|---|---|"]
    if 0 in slides:
        slide_rows.append(f"| Course introduction | [PDF]({slides[0]}) |")
    for n, _slug, title, _l in MODULES:
        if n in slides:
            slide_rows.append(f"| Module {n}: {title} | [PDF]({slides[n]}) |")
    subs = {"{{SLIDES_TABLE}}": "\n".join(slide_rows), "{{MODULE_TABLE}}": module_table(released), "{{REPO_URL}}": repo_url or "https://github.com/<your-username>/scripting-101",
            "{{CLONE_URL}}": (repo_url + ".git") if repo_url else "https://github.com/<your-username>/scripting-101.git",
            "{{SLIDES_ALL}}": "downloads/slides/"}
    for n, path in slides.items():
        subs[f"{{{{SLIDES_{n}}}}}"] = path
    for k, v in zips.items():
        subs[f"{{{{ZIP_{k.upper()}}}}}"] = v
    for md in DOCS.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for k, v in subs.items():
            # paths are relative to docs/: make them relative to this page
            if v.startswith("downloads/"):
                v = os.path.relpath(DOCS / v, md.parent).replace(os.sep, "/")
            text = text.replace(k, v)
        md.write_text(text, encoding="utf-8")

    notes = rewrite_links(repo_blob)
    (OUT / "mkdocs.yml").write_text(mkdocs_yml(released, site_url, repo_url), encoding="utf-8")
    print(f"site sources in {OUT}  (modules released: {released[-1] if released else 0} of 8)")
    for n in notes:
        print("  note:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
# conflict_demo.sh — create a throw-away repository with a guaranteed merge conflict.
# Instructor live demo for Lab 08 Part E (also great for students to practise resolving).
#
# Usage: ./conflict_demo.sh [DIR]     (default: /tmp/conflict_demo)
set -euo pipefail

dir=${1:-/tmp/conflict_demo}
rm -rf "$dir" && mkdir -p "$dir" && cd "$dir"

git init -q -b main
git config user.name  "Demo Student"
git config user.email "demo@example.com"

cat > analysis_settings.txt <<'TXT'
min_yield = 0
max_yield = 25
n_rates = 0,60,120,180
TXT
git add analysis_settings.txt
git commit -q -m "Add analysis settings"

git switch -q -c stricter-qc                      # branch 1 changes line 2
sed -i 's/max_yield = 25/max_yield = 18/' analysis_settings.txt
git commit -q -am "Tighten maximum plausible yield to 18 t/ha"

git switch -q main                                # main changes the SAME line differently
sed -i 's/max_yield = 25/max_yield = 20/' analysis_settings.txt
git commit -q -am "Set maximum plausible yield to 20 t/ha"

echo "== git log --oneline --graph --all =="
git log --oneline --graph --all
echo
echo "== git merge stricter-qc =="
git merge stricter-qc || true
echo
echo "== git status =="
git status --short
echo
echo "== analysis_settings.txt =="
cat analysis_settings.txt
echo
echo "Now resolve it:  cd $dir, edit the file, then:  git add analysis_settings.txt && git commit"

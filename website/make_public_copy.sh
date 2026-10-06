#!/usr/bin/env bash
# make_public_copy.sh — create the PUBLIC (student) version of the course repository.
#
# The public copy is what goes on GitHub and feeds the website. It leaves out everything
# that contains answers: solutions/, capstone/reference_solution/, instructor_guide/,
# the .pptx deck (its speaker notes have the answers) and the slide generator.
#
# Usage: website/make_public_copy.sh [-m N] [-c] [DEST]   (default DEST: ~/scripting-101-public)
#   -m N   publish modules 1..N only (default 1); release more later with website/release.py
#   -c     also make the first Git commit
set -euo pipefail

commit=0
modules=1
while getopts ":m:c" opt; do
    case $opt in
        m) modules=$OPTARG ;;
        c) commit=1 ;;
        *) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2 ;;
    esac
done
shift $(( OPTIND - 1 ))
SRC=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DEST=${1:-$HOME/scripting-101-public}

if [[ $DEST == /mnt/* ]]; then
    echo "Error: create the public copy in your Linux home (e.g. ~/scripting-101-public), not under /mnt/." >&2
    echo "       Windows folders cannot store Linux file permissions, so scripts would lose their executable bit." >&2
    exit 1
fi
if [[ -e $DEST ]]; then
    echo "Error: $DEST already exists. Remove it or choose another folder." >&2
    exit 1
fi
mkdir -p "$DEST"

tar -C "$SRC" \
    --exclude=./solutions \
    --exclude=./capstone/reference_solution \
    --exclude=./instructor_guide \
    --exclude=./slides/build \
    --exclude=./slides/scripting-101.pptx \
    --exclude=./website/build \
    --exclude=./website/release.py \
    --exclude=./datasets/large \
    --exclude=./.git \
    --exclude='__pycache__' --exclude='.pytest_cache' --exclude='node_modules' \
    -cf - . | tar -C "$DEST" -xf -

cd "$DEST"
cp website/student_README.md README.md
# remove pointers to the instructor-only material
sed -i '/instructor_guide\//d; /solutions\//d' SYLLABUS.md labs/README.md
sed -i '/reference_solution/d' capstone/README.md
cat > slides/README.md <<'MD'
# Slides

`modules/`: one PDF per module, added as each module is released.
MD
# keep only the released modules (labs, slide PDFs, capstone) and set website/release.txt
python3 "$SRC/website/release.py" "$modules" --dest "$DEST" > /dev/null

# make sure no private material slipped through
if grep -rIl --exclude-dir=website --exclude-dir=.git -e 'solutions/lab' -e 'reference_solution' . ; then
    echo "Warning: the files above still mention instructor-only material." >&2
fi

cd "$DEST"
# Files copied from Windows folders all look executable: reset permissions, then mark the scripts.
find . -type d -exec chmod 755 {} +
find . -type f -exec chmod 644 {} +
find . -type f \( -name '*.sh' -o -path './scripts/python/*.py' -o -path './datasets/*.py' -o -path './website/*.py' \) -exec chmod 755 {} +

git init -q -b main
git add .

echo "Public copy created in $DEST with modules 1-$modules ($(git ls-files | wc -l) files staged)."
if (( commit )); then
    git commit -q -m "Scripting 101 course materials (student version)"
    echo "First commit created."
else
    echo "Next: cd $DEST && git commit -m \"Scripting 101 course materials\""
fi

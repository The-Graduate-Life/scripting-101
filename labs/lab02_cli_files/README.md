# Lab 02 — Working with Files and Data on the Command Line

| | |
|---|---|
| **Module** | 1 — WSL and Linux Command-Line Fundamentals |
| **Time** | 2.5 hours |
| **Prerequisites** | Lab 01 |
| **Data** | `datasets/field_trials/`, `datasets/weather/`, `datasets/sensors/`, `datasets/messy/` |

## Learning objectives

1. Create, copy, move, rename and delete files and folders safely.
2. Inspect data files without opening them: `cat`, `less`, `head`, `tail`, `wc`, `file`.
3. Answer questions about data with **pipelines**: `cut`, `sort`, `uniq`, `grep`, `paste`.
4. Use **wildcards**, **redirection** (`>`, `>>`, `<`, `2>`) and **pipes** (`|`).
5. Find files with `find`; measure disk use with `du` and `df`.
6. Read and change **permissions** with `chmod`.
7. Compress and archive with `gzip`, `zip` and `tar`.
8. Explain the difference between **copying** and **symbolic linking** (`ln -s`).

## Setup (5 min)

```bash
$ cd ~
$ git clone https://github.com/<instructor>/scripting-101.git   # if you have not already
$ mkdir -p ~/lab02 && cd ~/lab02
$ cp -r ~/scripting-101/datasets/field_trials ~/scripting-101/datasets/messy .
$ ls -l
```

---

## Part A — Look before you touch (25 min)

The file `field_trials/plot_yields.csv` holds maize yields from a 5-year, 6-site nitrogen trial.

```bash
$ file field_trials/plot_yields.csv     # what kind of file is it?
$ wc -l field_trials/plot_yields.csv    # how many lines?
$ head -n 5 field_trials/plot_yields.csv
$ tail -n 3 field_trials/plot_yields.csv
$ less -S field_trials/plot_yields.csv  # -S: don't wrap long lines. q to quit, / to search
```

Number the column names so you can refer to them by position:

```bash
$ head -n 1 field_trials/plot_yields.csv | tr ',' '\n' | cat -n
```

✏️ **A1.** How many **data rows** (not counting the header) does the file contain? Which column number holds `yield_t_ha`?

## Part B — Pipes: questions → answers (40 min)

A **pipe** `|` sends the output of one command into the input of the next. Build each pipeline **one step at a time**, checking the output before adding the next command.

1. Which sites are in the trial, and how many plots per site?

   ```bash
   $ cut -d, -f2 field_trials/plot_yields.csv | head            # step 1: just the site column
   $ cut -d, -f2 field_trials/plot_yields.csv | tail -n +2 | sort | uniq -c
   ```

   `uniq` only merges **adjacent** identical lines, which is why `sort` must come first.

2. How many yields are missing (`NA`)?

   ```bash
   $ cut -d, -f8 field_trials/plot_yields.csv | grep -c -x NA
   ```

   ✏️ **B1.** Why is `grep -c NA field_trials/plot_yields.csv` *not* a safe way to answer this question? *(Hint: look at the `notes` column, and think about which other words contain "NA".)*

3. The five highest yields: are they believable?

   ```bash
   $ tail -n +2 field_trials/plot_yields.csv | sort -t, -k8,8gr | head -n 5
   ```

   `-t,` sets the field separator, `-k8,8` sorts on column 8 only, `g` means numeric (general), `r` means reverse.

   ✏️ **B2.** What is suspicious about the top record? Find the lowest yields as well. Is anything suspicious there?

4. How consistent are the variety names?

   ```bash
   $ cut -d, -f5 field_trials/plot_yields.csv | tail -n +2 | sort | uniq -c
   ```

   ✏️ **B3.** List every spelling problem you see. (`cat -A` shows hidden characters such as trailing spaces.)

5. Are there exact duplicate rows?

   ```bash
   $ tail -n +2 field_trials/plot_yields.csv | sort | uniq -d
   ```

6. All AMES plots from 2023 with variety Dune at the highest N rate:

   ```bash
   $ grep '^AMES-2023,' field_trials/plot_yields.csv | grep ',Dune,180,'
   ```

## Part C — Redirection and standard streams (20 min)

```bash
$ cut -d, -f2,3 field_trials/plot_yields.csv | sort -u > site_years.txt   # > overwrite
$ echo "# created $(date)" >> site_years.txt                              # >> append
$ wc -l < site_years.txt                                                  # < read input from a file
$ ls field_trials no_such_folder                     # one success (stdout), one error (stderr)
$ ls field_trials no_such_folder > out.txt           # the error still appears on screen
$ ls field_trials no_such_folder > out.txt 2> err.txt
$ ls field_trials no_such_folder > all.txt 2>&1      # both streams into one file
$ cat out.txt err.txt all.txt
```

```text
           ┌──────────┐ stdout (1) ─▶ screen or > file
 stdin (0) ─▶│ command  │
           └──────────┘ stderr (2) ─▶ screen or 2> file
```

✏️ **C1.** What does `2>&1` mean in words? Why does `> all.txt 2>&1` work while `2>&1 > all.txt` does not capture the errors?

**Command chaining:**

```bash
$ mkdir -p backup && cp field_trials/*.csv backup/ && echo "backup done"   # && : only if the previous command succeeded
$ ls nofile || echo "that failed, so this runs"                            # || : only if it failed
$ echo one ; false ; echo three                                            # ;  : always
```

## Part D — Wildcards and file management (20 min)

```bash
$ cp -r ~/scripting-101/datasets/weather .
$ ls weather/*.csv | wc -l
$ ls weather/weather_AMES_*.csv
$ ls weather/weather_*_2023.csv
$ ls weather/weather_????_2020.csv              # ? matches exactly one character
$ mkdir -p by_site/AMES
$ cp weather/weather_AMES_* by_site/AMES/
$ mv by_site/AMES/weather_AMES_2020.csv by_site/AMES/ames_2020.csv   # mv also renames
$ rm by_site/AMES/ames_2020.csv
$ rm -r by_site                                 # deletes a folder: there is NO recycle bin
$ rmdir empty_folder_only                       # rmdir only removes EMPTY folders
```

> ⚠️ **Safety habit:** before `rm` with a wildcard, run the same pattern with `ls` first. `rm -i` asks before each deletion.

**Spaces in file names** must be quoted or escaped:

```bash
$ cat messy/field notes 2023.txt        # fails: three separate arguments
$ cat "messy/field notes 2023.txt"      # works
$ cat messy/field\ notes\ 2023.txt      # works
$ grep -i drought messy/*.txt
```

## Part E — find, du, df (15 min)

```bash
$ cd ~/scripting-101/datasets
$ find . -name "*.fastq.gz"
$ find sensors -name "*.csv" | wc -l
$ find sensors -type f -empty                     # broken logger files!
$ find sensors -name "*.csv" -size -100c          # suspiciously small files
$ find . -name "*.csv" -newer field_trials/sites.csv | head
$ du -sh */                                       # size of each folder
$ df -h ~                                         # free space on your disk
```

✏️ **E1.** How many sensor CSV files are there? Which file(s) are empty, and which contain only a header line?

## Part F — Permissions (15 min)

```bash
$ cd ~/lab02
$ echo 'echo "I am a script"' > hello.sh
$ ls -l hello.sh
-rw-r--r-- 1 ada ada 22 Oct  5 10:00 hello.sh
$ ./hello.sh
bash: ./hello.sh: Permission denied
$ chmod u+x hello.sh        # add execute permission for the user (owner)
$ ls -l hello.sh
-rwxr--r-- 1 ada ada 22 Oct  5 10:00 hello.sh
$ ./hello.sh
I am a script
```

```text
 -  rwx  r--  r--
 │   │    │    └── others: read
 │   │    └─────── group : read
 │   └──────────── user  : read, write, execute
 └──────────────── type  : - file, d directory, l link
```

Numeric form: r = 4, w = 2, x = 1. `chmod 755 file` = `rwxr-xr-x`, and `chmod 644 file` = `rw-r--r--`.

✏️ **F1.** Make `field_trials/sites.csv` read-only for everyone (`chmod a-w`). Try `echo test >> field_trials/sites.csv`. What happens? Restore write permission for yourself afterwards.

## Part G — Compression and archives (15 min)

```bash
$ cp field_trials/plot_yields.csv yields.csv
$ ls -lh yields.csv
$ gzip yields.csv             # replaces the file with yields.csv.gz
$ ls -lh yields.csv.gz
$ zcat yields.csv.gz | head -3   # read WITHOUT decompressing to disk
$ gunzip yields.csv.gz
$ tar -czvf weather_backup.tar.gz weather/     # c=create z=gzip v=verbose f=file name
$ tar -tzf weather_backup.tar.gz | head        # t=list contents
$ mkdir restore && tar -xzf weather_backup.tar.gz -C restore    # x=extract into restore/
$ zip -r weather.zip weather/ && unzip -l weather.zip | tail -3
```

✏️ **G1.** Compare the sizes of `weather/` (`du -sh`), `weather_backup.tar.gz` and `weather.zip`. Why does CSV compress so well?

## Part H — Copy vs. symbolic link (10 min)

```bash
$ ln -s ~/scripting-101/datasets data_link         # a shortcut that points to the real folder
$ ls -l data_link
lrwxrwxrwx 1 ada ada 32 Oct  5 10:30 data_link -> /home/ada/scripting-101/datasets
$ ls data_link/genomics
$ du -sh data_link/ field_trials/                  # the link itself takes no space
```

| | `cp file copy` | `ln -s file link` |
|---|---|---|
| Disk space | doubles | ~0 |
| Edit the original | the copy does **not** change | the link shows the change |
| Delete the original | the copy survives | the link is **broken** (dangling) |
| Typical use | backups, snapshots | point many projects at one large dataset |

✏️ **H1.** Create `ln -s ~/lab02/hello.sh hi`, then delete `hello.sh`. What does `ls -l hi` show, and what happens with `cat hi`?

---

## Independent exercises

1. How many weather files are there for 2023? (Use a wildcard and `wc -l`.)
2. Print the **mean yield per site** using `awk` (preview of Module 2):
   `awk -F, 'NR>1 && $8!="NA" {s[$2]+=$8; n[$2]++} END {for (k in s) print k, s[k]/n[k]}' field_trials/plot_yields.csv | sort -k2,2nr`
   Which site yields most and which least?
3. The file `messy/ames_2023_windows_export.csv` came from a Windows computer. Use `cat -A | head -3` to see what is different about its line endings. Remove the `\r` characters with `tr -d '\r' < in > out` and check again.
4. Use `paste` to build a two-column file with the site name and soil type from `sites.csv`: `paste -d'\t' <(cut -d, -f1 sites.csv) <(cut -d, -f4 sites.csv)`.
5. Write a single pipeline that lists the 3 site-years (`trial_id`) with the most missing yields.

## Challenge

Write one command that finds every sensor CSV, counts the lines in each, and prints the 5 **shortest** files with their line counts. *(Hint: `find ... -exec wc -l {} +` or `find ... | xargs wc -l`, then `sort -n`.)*

## Quiz

1. What is the difference between `>` and `>>`?
2. Why must `sort` come before `uniq -c`?
3. What does `cut -d, -f2,5` do?
4. What do `chmod 700 script.sh` and `chmod u+x script.sh` each do?
5. What happens to a symbolic link when its target is deleted?
6. Which command shows the contents of a `.tar.gz` file without extracting it?

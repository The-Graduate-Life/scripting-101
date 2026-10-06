# Lab 01 — Linux and WSL: Finding Your Way Around

| | |
|---|---|
| **Module** | 1 — WSL and Linux Command-Line Fundamentals |
| **Time** | 90 minutes |
| **Prerequisites** | WSL 2 with Ubuntu installed ([`resources/wsl_setup.md`](../../resources/wsl_setup.md)) |
| **You will practise** | `pwd`, `ls`, `cd`, `mkdir`, `touch`, `echo`, `man`, `history`, `which`, `file`, paths, `/mnt/c`, environment variables, `$PATH` |

## Learning objectives

By the end of this lab you can:

1. Open an Ubuntu terminal in WSL and explain the difference between the **terminal**, the **shell** and **Bash**.
2. Say where you are (`pwd`), look around (`ls`), and move (`cd`) using **absolute** and **relative** paths.
3. Reach your Windows files from Linux through `/mnt/c/` and explain why projects should live in the Linux home folder.
4. Use `man`, `--help`, and `history` to help yourself.
5. Inspect environment variables, including `$HOME`, `$USER` and `$PATH`.

> **How to work.** Type every command yourself; don't copy and paste. Typing builds muscle memory, and your typos teach you to read error messages.
> Lines beginning with `$` are commands (don't type the `$`). Lines without `$` show expected output.

---

## Part A — First contact (15 min)

1. Open **Ubuntu** from the Windows Start menu (or type `wsl` in PowerShell). You see a **prompt** like:

   ```text
   ada@LAPTOP-1234:~$
   ```

   | Part | Meaning |
   |---|---|
   | `ada` | your Linux user name |
   | `LAPTOP-1234` | the computer's host name |
   | `~` | your current directory (`~` = your home folder) |
   | `$` | "ready for a command" (`#` would mean you are the all-powerful root user) |

2. Run each command and write down in one sentence what it told you:

   ```bash
   $ whoami
   $ hostname
   $ date
   $ echo "Hello, Linux"
   $ uname -a
   $ cat /etc/os-release
   ```

3. **Which shell am I using?**

   ```bash
   $ echo $SHELL
   /bin/bash
   $ echo $0
   -bash
   ```

   ✏️ **Question A1.** The *terminal* is the window, *Bash* is the program reading your commands. What would change if you opened the same terminal window but started the `zsh` shell?

## Part B — Where am I? (20 min)

1. Print the **working directory**:

   ```bash
   $ pwd
   /home/ada
   ```

2. List files: plain, long (`-l`), all including hidden (`-a`), human-readable sizes (`-h`):

   ```bash
   $ ls
   $ ls -l
   $ ls -la
   $ ls -lah /etc | head
   ```

   ✏️ **Question B1.** What do files starting with `.` have in common? Name two you can see in your home folder.

3. Explore the Linux filesystem tree. For each directory, run `ls` and fill in the table:

   | Directory | What do you think lives here? |
   |---|---|
   | `/` | |
   | `/home` | |
   | `/etc` | |
   | `/bin` and `/usr/bin` | |
   | `/tmp` | |
   | `/mnt` | |

4. Move around with `cd`:

   ```bash
   $ cd /etc          # absolute path: starts with /
   $ pwd
   $ cd ..            # .. = parent directory
   $ pwd
   $ cd               # cd with no argument = go home
   $ cd -             # go back to the previous directory
   $ cd ~             # ~ = home
   ```

5. Make a practice folder tree and navigate it with **relative** paths:

   ```bash
   $ mkdir -p ~/lab01/project/{data,scripts,results}
   $ cd ~/lab01/project/data
   $ cd ../scripts            # relative: up one, then into scripts
   $ cd ../../                # up two
   $ pwd
   /home/ada/lab01
   ```

   ✏️ **Question B2.** From `~/lab01/project/results`, write **two** different commands that take you to `~/lab01/project/data`, one absolute and one relative.

## Part C — Windows ↔ Linux (15 min)

1. Your `C:` drive is mounted at `/mnt/c`:

   ```bash
   $ ls /mnt/c/Users/
   $ ls "/mnt/c/Users/<YourWindowsName>/Desktop"
   ```

   Note the quotes: Windows folder names often contain spaces.

2. Open your Linux home folder in Windows Explorer:

   ```bash
   $ explorer.exe .
   ```

   The address bar shows `\\wsl.localhost\Ubuntu\home\<you>`.

3. Copy a file from Windows into Linux. Create `C:\Users\<You>\Desktop\hello.txt` in Notepad first:

   ```bash
   $ cp "/mnt/c/Users/<YourWindowsName>/Desktop/hello.txt" ~/lab01/
   $ cat ~/lab01/hello.txt
   ```

> ⚠️ **Rule of thumb.** Keep your projects in your Linux home (`~/...`), not under `/mnt/c/...`.
> Linux tools run **much** faster there, and file permissions and executable bits behave correctly.
> Use `/mnt/c` only to move files in or out.

✏️ **Question C1.** Run `time ls -R /mnt/c/Windows/System32 > /dev/null` and then `time ls -R /usr > /dev/null`. Which is faster per file, and why?

## Part D — Helping yourself (15 min)

```bash
$ man ls              # manual page: arrows/PgUp/PgDn to scroll, /word to search, q to quit
$ ls --help | less    # shorter built-in help
$ type cd             # cd is a shell builtin
$ which ls python3    # where is the program file?
$ whereis bash
$ file /bin/ls ~/.bashrc
$ history | tail -20
$ !!                  # rerun the last command
```

Keyboard shortcuts to try: **Tab** (autocomplete, press twice to list options), **↑/↓** (history), **Ctrl+R** (search history), **Ctrl+C** (cancel), **Ctrl+L** or `clear` (clear screen), **Ctrl+A / Ctrl+E** (start/end of line).

✏️ **Question D1.** Using `man ls`, find the option that sorts files by modification time, newest first, and the option that reverses the sort order.

## Part E — Environment variables and `$PATH` (15 min)

```bash
$ echo $HOME
$ echo $USER
$ env | head
$ echo $PATH
$ echo $PATH | tr ':' '\n'
```

`$PATH` is a list of folders that Bash searches, **in order**, when you type a command name.

```bash
$ greeting="Hello"            # a shell variable (no spaces around =)
$ echo "$greeting, $USER"
$ export COURSE=~/scripting-101 # an environment variable (inherited by programs you start)
$ echo $COURSE
```

✏️ **Question E1.** What happens if you type `greeting = "Hello"` with spaces? Read the error message carefully and explain it.

---

## Independent exercises

1. Create this structure using **one** `mkdir` command, then verify it with `ls -R` (or `tree` if installed):

   ```text
   ~/lab01/field_season/
   ├── 2023/{raw,clean}
   └── 2024/{raw,clean}
   ```

2. Create empty files `notes.txt` and `.secret_settings` in `~/lab01/field_season` with `touch`. Show that `ls` hides one of them and `ls -a` shows both.
3. Write the absolute path of your Windows Downloads folder as seen from WSL, then list its five most recently modified files.
4. Find out which version of Python 3 is installed (`python3 --version`) and where it is (`which python3`).

## Challenge

Without using `cd`, list the contents of `/usr/share` sorted by size, largest first, showing human-readable sizes. *(Hint: `man ls`.)*

## Quiz (self-check)

1. What is the difference between `~/data` and `/data`?
2. What does `cd ..` do when you are in `/`?
3. Name three ways to learn how a command works.
4. Why is `ls -la` called with a single dash, and `ls --all` with two?
5. What does `$PATH` control?

## Submit

A text file `lab01_answers.txt` with your answers to the ✏️ questions, exercises and quiz.

# Linux CLI Cheat Sheet

## Navigate
| Command | Does |
|---|---|
| `pwd` | print working directory |
| `ls -lah` | list (long, all incl. hidden, human sizes) · `-t` by time · `-S` by size · `-r` reverse |
| `cd DIR` · `cd ..` · `cd` · `cd -` | go to DIR · up · home · previous |
| `tree -L 2` | folder tree, 2 levels |
| `~` `.` `..` `/` | home · here · parent · root |

## Files and folders
| Command | Does |
|---|---|
| `mkdir -p a/b/c` | create nested folders |
| `touch f` | create empty file |
| `cp f g` · `cp -r d e` | copy file · folder |
| `mv a b` | move / rename |
| `rm f` · `rm -r d` · `rm -i f` | delete · folder · ask first (**no undo!**) |
| `rmdir d` | remove empty folder |
| `ln -s TARGET LINK` | symbolic link (pointer, no copy) |

## View and inspect
| Command | Does |
|---|---|
| `cat f` · `less -S f` | print · page (q quit, /search) |
| `head -n 5 f` · `tail -n 5 f` · `tail -f log` | first/last lines · follow a growing file |
| `wc -l f` | count lines |
| `file f` | file type (CRLF? compressed?) |
| `cat -A f` | show hidden characters (`^M` = Windows CR) |
| `du -sh d` · `df -h` | size of folder · free disk |

## Columns and text
| Command | Does |
|---|---|
| `cut -d, -f2,5 f.csv` | columns 2 and 5 (CSV); `cut -f` for tabs |
| `sort` · `-n` · `-g` · `-r` · `-k3,3` · `-t,` · `-u` | sort: numeric, general numeric, reverse, by column 3, separator, unique |
| `uniq -c` · `uniq -d` | count / show duplicates (**input must be sorted**) |
| `paste -d'\t' a b` | join files side by side |
| `tr ',' '\t'` · `tr -d '\r'` | translate / delete characters |
| `grep -i -v -c -n -w -E` | search: ignore case, invert, count, line no., word, regex |
| `echo "text"` · `printf "%s\t%d\n" a 1` | print |

## Find
`find . -name "*.csv"` · `-type f` / `-type d` · `-empty` · `-size +100M` · `-mtime -1` · `-print0 | xargs -0 CMD`
`locate NAME` (needs `sudo updatedb`) · `which CMD` · `whereis CMD` · `type CMD`

## Wildcards
`*` any string · `?` one char · `[0-9]` one char from set · `{a,b,c}` brace expansion · `{001..100}` sequence

## Redirection and pipes
| | |
|---|---|
| `>` / `>>` | stdout to file (overwrite / append) |
| `2>` | stderr to file |
| `> f 2>&1` / `&> f` | both to file |
| `<` | stdin from file |
| `\|` | pipe stdout into next command |
| `&&` / `\|\|` / `;` | run next if success / if failure / always |
| `> /dev/null` | discard |

⚠️ `sort f > f` empties `f`: redirect to a new file.

## Permissions
`-rwxr-xr--` = type · user · group · others. r=4 w=2 x=1.
`chmod u+x f` · `chmod 755 f` · `chmod 644 f` · `chmod a-w raw.csv` · `ls -l`

## Compression
| | |
|---|---|
| `gzip f` · `gunzip f.gz` · `zcat f.gz \| head` | compress · decompress · read without decompressing |
| `tar -czvf a.tar.gz dir/` | create archive |
| `tar -tzf a.tar.gz` | list |
| `tar -xzf a.tar.gz -C dest/` | extract |
| `zip -r a.zip dir/` · `unzip -l a.zip` · `unzip a.zip` | zip |

## Environment
`echo $HOME $USER $PATH` · `export VAR=value` · `env` · `~/.bashrc` (runs at shell start)

## Help and history
`man CMD` · `CMD --help` · `history` · `!!` (repeat) · `Ctrl+R` (search) · `clear` / `Ctrl+L`

## Keys
Tab complete · ↑↓ history · Ctrl+C cancel · Ctrl+Z suspend · Ctrl+D exit · Ctrl+A/E line start/end

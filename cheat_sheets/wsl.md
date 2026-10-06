# WSL Cheat Sheet

## Install / manage (Windows PowerShell)
| Command | Does |
|---|---|
| `wsl --install` | install WSL 2 + Ubuntu (admin; reboot) |
| `wsl --list --verbose` (`wsl -l -v`) | distributions and versions (should be 2) |
| `wsl --update` | update the WSL kernel |
| `wsl --shutdown` | stop all distributions (apply `.wslconfig`, fix hangs) |
| `wsl` / `wsl -d Ubuntu` | open Linux shell |
| `wsl --set-default-version 2` | use WSL 2 for new distributions |
| `wsl --export Ubuntu backup.tar` / `--import` | back up / restore a distribution |

## Files between Windows and Linux
| From Linux (WSL) | From Windows |
|---|---|
| `/mnt/c/Users/<Name>/Desktop` = `C:\Users\<Name>\Desktop` | `\\wsl.localhost\Ubuntu\home\<user>` in Explorer |
| `explorer.exe .` opens the current Linux folder in Explorer | |
| `code .` opens VS Code (WSL extension) | |
| `wslpath 'C:\Users\Ada'` → `/mnt/c/Users/Ada` | `wslpath -w ~/x` → Windows path |
| `clip.exe < file` copies to the Windows clipboard | |

⚠️ **Work in `~` (Linux filesystem).** `/mnt/c` is slow for many files and doesn't support Linux permissions properly. Keep SSH keys, conda and projects on the Linux side; use `/mnt/c` only to move files in and out.

## Resources: `C:\Users\<Name>\.wslconfig`
```ini
[wsl2]
memory=12GB        # max RAM for WSL (default: 50 % of Windows RAM)
processors=8       # max CPU cores
swap=4GB
```
Then `wsl --shutdown` and reopen.

## Ubuntu basics
```bash
sudo apt update && sudo apt upgrade        # update system software
sudo apt install -y zip unzip tree plocate dos2unix htop shellcheck build-essential
lsb_release -a ; uname -r                   # versions
nproc ; free -h ; df -h ~                   # CPUs, RAM, disk
```

## Line endings
Windows editors write CRLF (`\r\n`); Linux expects LF (`\n`).
Symptoms: `$'\r': command not found`, `bad interpreter: /usr/bin/env: 'bash\r'`.
Fix: `dos2unix file` · `sed -i 's/\r$//' file` · VS Code status bar: CRLF → LF · `git config --global core.autocrlf input`

## Windows Terminal tips
Settings → Ubuntu profile → **Starting directory** `\\wsl.localhost\Ubuntu\home\<user>` · font size · Ctrl+Shift+T new tab · Alt+Shift+D split pane · Ctrl+Shift+C/V copy/paste

## Common problems
| Problem | Fix |
|---|---|
| "WslRegisterDistribution failed" / virtualisation error | enable virtualisation in BIOS/UEFI; `wsl --install` again |
| WSL version 1 | `wsl --set-version Ubuntu 2` |
| no internet inside WSL (VPN) | `wsl --shutdown`; try `networkingMode=mirrored` under `[wsl2]` in `.wslconfig` (Windows 11) |
| Disk full | `df -h`; clean conda (`conda clean --all`), delete big intermediates |
| Clock wrong after sleep (Git/SSL errors) | `sudo hwclock -s` or `wsl --shutdown` |
| Forgot Linux password | PowerShell: `wsl -u root`, then `passwd <user>` |

# Setup Guide: WSL, Ubuntu, Miniforge, Git and the Course Repository

Allow **45–60 minutes**. Do this **before** the first session. If anything fails, note the exact error message and bring it to the setup clinic.

## 1. Check Windows

* Windows 10 version 2004 or later (build 19041+) or Windows 11. Check: `Win + R` → `winver`.
* At least 8 GB RAM recommended (16 GB comfortable), 20 GB free disk space.
* Hardware virtualisation enabled. Check: Task Manager → Performance → CPU → "Virtualization: Enabled". If disabled, enable *Intel VT-x* / *AMD-V (SVM)* in BIOS/UEFI.

## 2. Install WSL 2 and Ubuntu

1. Right-click **Start → Terminal (Admin)** (or *Windows PowerShell (Admin)*).
2. Run:
   ```powershell
   wsl --install
   ```
3. **Restart** the computer.
4. Ubuntu opens automatically (or start **Ubuntu** from the Start menu). Choose a Linux **username** (lowercase, no spaces) and **password**. The password is typed invisibly; that is normal.
5. Verify in PowerShell:
   ```powershell
   wsl -l -v
   ```
   ```text
     NAME      STATE           VERSION
   * Ubuntu    Running         2
   ```
   If VERSION is 1: `wsl --set-version Ubuntu 2`.

## 3. Recommended Windows tools

* **Windows Terminal** (Microsoft Store; preinstalled on Windows 11). Set the Ubuntu profile's *Starting directory* to `\\wsl.localhost\Ubuntu\home\<your-linux-user>`.
* **VS Code** with the **WSL** extension. In Ubuntu, `code .` opens the current folder.

## 4. Update Ubuntu and install tools

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl git zip unzip tree plocate dos2unix htop shellcheck
```

## 5. Install Miniforge (conda)

```bash
cd ~
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b -p ~/miniforge3
~/miniforge3/bin/conda init bash
exec bash
conda --version
```

## 6. Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
git config --global init.defaultBranch main
git config --global core.autocrlf input
```

## 7. Get the course materials and environment

```bash
cd ~
git clone https://github.com/<instructor>/scripting-101.git
cd scripting-101
conda env create -f environment.yml          # 3-10 minutes
conda activate scripting101
python --version && seqkit version && bash scripts/bash/checksums.sh verify datasets
```

The last command should print `All files OK`.

## 8. Optional: limit WSL resources

Create `C:\Users\<YourName>\.wslconfig`:

```ini
[wsl2]
memory=8GB
processors=4
```

Then run `wsl --shutdown` in PowerShell.

## Troubleshooting

| Problem | Fix |
|---|---|
| `0x80370102` / virtualisation error | enable virtualisation in BIOS/UEFI; also enable *Virtual Machine Platform* under "Turn Windows features on or off" |
| `wsl --install` shows only help text | WSL is already partly installed: `wsl --install -d Ubuntu` |
| Ubuntu window flashes and closes | `wsl --update`, then reboot |
| `Temporary failure resolving` (no internet in Ubuntu) | VPN/corporate DNS: try off-VPN; Windows 11: add `networkingMode=mirrored` under `[wsl2]` in `.wslconfig` |
| conda download is very slow or blocked | try another network; ask the instructor for an offline environment pack |
| Accidentally installed things under `/mnt/c` | remove them and reinstall under `~` |

## Mac or Linux users

You don't need WSL. On Linux, start at step 4. On macOS, open Terminal, install the Xcode command line tools (`xcode-select --install`), and follow steps 5–7 (the Miniforge installer name differs; the `$(uname)-$(uname -m)` part selects it automatically). Note that macOS ships BSD versions of `sed`, `find` and others, with small differences, and its default shell is zsh. Run `bash` to follow the course exactly.

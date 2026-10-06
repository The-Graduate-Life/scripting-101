# Getting started

Do this **before the first session**. It takes 45–60 minutes. If something fails, write down the exact error message and bring it along.

## 1. Install WSL and Ubuntu (Windows)

Open **Terminal (Admin)** from the Start menu and run:

```powershell
wsl --install
```

Restart the computer, open **Ubuntu** from the Start menu, and choose a Linux user name and password.
Full guide with troubleshooting: [WSL setup](resources/wsl_setup.md).

!!! tip "Mac or Linux?"
    You don't need WSL. Open a terminal and continue with step 2.

## 2. Install tools and Miniforge (conda)

```bash
sudo apt update && sudo apt install -y build-essential curl git zip unzip tree plocate dos2unix htop shellcheck
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b -p ~/miniforge3
~/miniforge3/bin/conda init bash && exec bash
```

## 3. Get the course materials

```bash
cd ~
git clone {{CLONE_URL}}
cd scripting-101
conda env create -f environment.yml
conda activate scripting101
bash scripts/bash/checksums.sh verify datasets      # should print: All files OK
```

!!! warning "Work in your Linux home folder"
    Keep everything under `~` (for example `~/scripting-101`), **not** under `/mnt/c/...`.
    Linux tools are much faster there, and file permissions work correctly.

No Git yet? Download the [datasets]({{ZIP_DATASETS}}), [example scripts]({{ZIP_SCRIPTS}}) and [environment file](downloads/environment.yml) from the [Downloads](downloads.md) page instead.

## 4. Create a GitHub account

Sign up at [github.com](https://github.com). You'll need it in Module 5.

## How to work in this course

- **Type, don't paste.** Typing builds memory; fixing your own typos teaches you to read errors.
- **Read the error message**, the last line first.
- **Build step by step.** Run each piece and look at the output before adding the next.
- **Stuck for 15 minutes?** Ask, and bring the exact command and the full error text.

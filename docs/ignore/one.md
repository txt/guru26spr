<p align="center">
  <a href="https://github.com/txt/guru26spr/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/docs/syllabus.md"><img 
      src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/12Jg_K_E4t8qo0O2uBE-s_t4IAR8f4lXjrdBiItLVs_8/edit?gid=0#gid=0"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8118&bp=s"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591: How to be a SE Guru <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/guru26spr/refs/heads/main/etc/img/banenr.png"> 


At 4:30pm on Wendesday please be in your seat with a  laptop open running a script
runs and reports the version numbers of the following tools. 

Also, have a sheet of paper to submit with your name on it and screen snap of that script in action.

Reality check:
If you cannot get the following numbers,
just go as high as you can. And if you can't get all of these, no worries. Just do what you can.


(Aside: never actually tried installing this many tools for this many people on this many platforms before. I think we have an 80% chance of getting 70% of the following. Let's see what happens!)


| Tool | Target Version (Jan 2026) | Strategy Used in Script |
| --- | --- | --- |
| **Python** | **3.14.x** | **Ubuntu:** PPA (Deadsnakes). **Fedora/Arch:** Native Repo. |
| **Gawk** | **5.3.2** | Native Repo (Updates are slow, but 5.3 is likely). |
| **Make** | **4.4.1** | Native Repo. |
| **Neovim** | **0.11.x** | **Ubuntu:** AppImage (guarantees latest). **Arch:** Native. |
| **Micro** | **2.0.15+** | Official install script (fetches latest binary). |
| **Pandoc** | **3.8.x** | **Ubuntu:** GitHub Release `.deb`. **Arch:** Native. |
| **Helix** | **25.07** | **Ubuntu:** PPA. **Arch/Fedora:** Native. |
| **Zellij** | **0.43.x** | Official install script (fetches latest binary). |
| **Tmux** | **3.6a** | Native Repo. |

To get a version number, do something like the following (but this will vary from tool to tool):

     bash --version

here's a script which might run on mac, linux and WSL2 (assuming windows subsystem for linux).
The script detects your specific distribution and attempts to install the **absolute latest** versions of the tools you requested, bypassing often outdated package repositories where necessary.

Save this as `install_tools.sh`, then run `chmod +x install_tools.sh` and `./install_tools.sh`.


```bash
#!/bin/bash

# Tools: python, gawk, make, nvim, micro, pandoc, helix, zellij, tmux
# + wl-clipboard for WSL2 clipboard integration

set -e

echo "🚀 Starting WSL2 Tool Installer..."

install_ubuntu() {
    echo "📦 Detected Debian/Ubuntu. Updating sources..."
    sudo apt update && sudo apt install -y curl wget git build-essential

    # 1. Base Tools (Repo is usually fine or PPA needed)
    echo "Installing base tools (Make, Gawk, Tmux)..."
    sudo apt install -y make gawk tmux wl-clipboard

    # 2. Python (Use Deadsnakes PPA for latest stable)
    echo "Installing latest Python..."
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.14 python3.14-venv || sudo apt install -y python3.13 python3.13-venv

    # 3. Neovim (AppImage for latest version)
    echo "Installing Neovim (Latest AppImage)..."
    curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
    chmod u+x nvim.appimage
    sudo mv nvim.appimage /usr/local/bin/nvim

    # 4. Micro (Official Script)
    echo "Installing Micro..."
    curl https://getmic.ro | bash
    sudo mv micro /usr/local/bin/

    # 5. Pandoc (Deb for latest, repo often old)
    echo "Installing Pandoc (Latest .deb)..."
    PANDOC_URL=$(curl -s https://api.github.com/repos/jgm/pandoc/releases/latest | grep "browser_download_url.*amd64.deb" | cut -d : -f 2,3 | tr -d \")
    wget -O pandoc.deb "$PANDOC_URL"
    sudo dpkg -i pandoc.deb
    rm pandoc.deb

    # 6. Helix (PPA or Binary - Binary is safer for 'latest')
    echo "Installing Helix..."
    sudo add-apt-repository -y ppa:maveonair/helix-editor
    sudo apt update && sudo apt install -y helix

    # 7. Zellij (Binary)
    echo "Installing Zellij..."
    bash <(curl -L https://zellij.dev/launch.sh)
}

install_fedora() {
    echo "🎩 Detected Fedora. Using dnf..."
    sudo dnf upgrade -y
    # Fedora repos are usually very fresh
    sudo dnf install -y python3 make gawk tmux neovim micro pandoc helix zellij wl-clipboard
}

install_arch() {
    echo "🏹 Detected Arch Linux. Using pacman..."
    sudo pacman -Syu --noconfirm base-devel python gawk make neovim micro pandoc helix zellij tmux wl-clipboard
}

# OS Detection
if [ -f /etc/debian_version ]; then
    install_ubuntu
elif [ -f /etc/fedora-release ]; then
    install_fedora
elif [ -f /etc/arch-release ]; then
    install_arch
else
    echo "❌ Unsupported Distribution. Please install manually."
    exit 1
fi

echo "✅ Installation Complete! Restart your terminal."

```


### **Specific WSL2 Nuances**

1. **Clipboard (`wl-clipboard`):**
The script installs `wl-clipboard`. In Neovim, Helix, and Micro, this allows you to copy/paste directly to your Windows clipboard using the standard Linux system clipboard registers.
* *Tip:* If pasting in Windows is funky, ensure `win32yank.exe` (installed by default in WSL) is in your path, but `wl-copy` is generally preferred now.


2. **Helix/Neovim Colors:**
Ensure your Windows Terminal (or Alacritty/WezTerm on Windows) supports **True Color**. WSL2 supports this out of the box, but you must enable it in your `TERM` settings:
`export TERM=xterm-256color` (or `wezterm`, `alacritty` depending on your emulator).

3. **Zellij/Tmux inside WSL:**
Since you are in WSL, you don't need to worry about the Windows "Command Prompt" limitations. You are running a real Linux kernel.
* **Pro Tip:** Zellij can feel slightly sluggish in WSL2 on *very* large window resizes due to the rendering across the VM boundary. If this happens, verify you are using the **Windows Terminal Preview** version, which has faster rendering pipelines.




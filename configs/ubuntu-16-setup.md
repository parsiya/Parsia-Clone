---
draft: false
toc: false
comments: false
categories:
- Configs
tags:
- Ubuntu
title: "Ubuntu Setup after Installation"
wip: false
snippet: "What to do after starting a fresh Ubuntu VM."

---

# Ubuntu Setup after Installation
Every once in a while I setup a new Ubuntu VM and I have to redo all these steps. This will help me speed things up.

<!-- MarkdownTOC -->

- [VM Specifications](#vm-specifications)
- [Install Virtualization Plugins](#install-virtualization-plugins)
  - [VirtualBox](#virtualbox)
  - [VMWare](#vmware)
- [Set Keyboard Shortcuts](#set-keyboard-shortcuts)
- [Install Useful Packages](#install-useful-packages)
- [Disable Screenlock and Screensaver](#disable-screenlock-and-screensaver)
- [Install Go 1.10](#install-go-110)
- [Edit .bashrc](#edit-bashrc)
- [Install VS Code](#install-vs-code)
- [Install Docker - Optional](#install-docker---optional)

<!-- /MarkdownTOC -->

<a id="vm-specifications"></a>
# VM Specifications

- RAM: 4GB.
- VGA memory: 128MB (max) in VirtualBox and 1GB in VMWare.
- Enable 3D acceleration.
- Disk space: 30 or 40GB.

<a id="install-virtualization-plugins"></a>
# Install Virtualization Plugins
These allow clipboard copy/paste and sometimes even drag/drop.

<a id="virtualbox"></a>
## VirtualBox

1. If the VM does not have a CD-ROM, shut it down, add one and launch.
2. Load the guest additions ISO: `Devices > Insert Guest Additions CD Image...`.
3. Navigate to the mounted drive.
4. Run `sudo ./VBoxLinuxAdditions.run`.
5. Enable:
    - `Devices > Shared Clipboard > Bidirectional`.
    - `Devices > Drag and Drop > Bidirectional`.
        - Dropped files will be in `/tmp/VirtualBox Dropped Files` and the directory is deleted on boot.
6. Restart.
7. Profit.

<a id="vmware"></a>
## VMWare

1. `sudo open-vm-tools open-vm-tools-desktop`.
2. Restart.
3. Shared clipboard will work, not sure about files.

<a id="set-keyboard-shortcuts"></a>
# Set Keyboard Shortcuts
Set at `System Settings > Keyboard > Shortcuts`.

- `Custom Shortcuts > New` - Name: `terminal` - Command: `gnome-terminal` - Key: `Super+R`.
- `Navigation > Hide all normal windows` - change to `Super+D`. Works after logout.

<a id="install-useful-packages"></a>
# Install Useful Packages
Some packages are not installed by default.

``` bash
sudo apt-get update
sudo apt-get install curl git libltdl-dev 
```

<a id="disable-screenlock-and-screensaver"></a>
# Disable Screenlock and Screensaver
No reason to have them in a VM.

`Settings > Brightness & Lock`:
- Set lock to off.
- `Turn screen off when inactive for: Never`.

<a id="install-go-110"></a>
# Install Go 1.10
Current `golang` package is not up to date.

1. `sudo apt-get update`.
2. `sudo apt-get install golang-1.10`.
    - This will install go in `/usr/lib/go-1.10/`.
3. I don't like the default `GOPATH` (`/home/$USER/go`). I prefer files to be on desktop.
    - `mkdir -p /home/$USER/Desktop/Go/{src,bin,pkg}`.

<a id="edit-bashrc"></a>
# Edit .bashrc
Inb4 that's not the correct way to do this.

Set `GOROOT` and new `GOPATH` to PATH:
- `export PATH="/usr/lib/go-1.10/bin:/home/$USER/Desktop/Go/bin:$PATH"`.
- `export GOPATH="/home/$USER/Desktop/Go"`.

Navigate to `Desktop` in every new terminal (this will cause errors if terminals are opened in other paths):

- `cd Desktop`.

Apply settings with:

- `source ~/.bashrc`.

<a id="install-vs-code"></a>
# Install VS Code
Electron app, so be sure to ~~download more RAM~~ assign lots of RAM to VM.

Copied from [official instructions][vs-code-official-installation]:

``` bash
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt-get update
sudo apt-get install code
```

<a id="install-docker---optional"></a>
# Install Docker - Optional
Instead of using the `docker.io` package through aptitude, use the official instructions at:

- https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce

``` bash
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88 # This might change in the future

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce docker-compose

# Test
sudo docker run hello-world
```

If `docker-compose` does not work after installation and you get this error message `Couldn't connect to Docker daemon at http+unix://var/run/docker.sock` or [something similar][docker-compose-issue], add yourself to the `docker` group, logout and login:

- `usermod -aG docker ${USER}`

<!-- Links -->
[vs-code-official-installation]: https://code.visualstudio.com/docs/setup/linux#_installation
[docker-compose-issue]: https://github.com/docker/compose/issues/1214#issuecomment-102246925

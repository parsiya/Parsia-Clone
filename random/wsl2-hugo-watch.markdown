---
draft: false
toc: false
comments: false
categories:
- Random
tags:
- hugo
- wsl2
title: "Hugo Server doesn't See File Notification Events in WSL2"
wip: false
snippet: "If you modify files in the Windows subsystem, Hugo won't see the modification event in WSL2."
---

# Problem
The local Hugo server running in WSL2 doesn't see file updates so it doesn't
rebuild the website. The files are under the Windows file system (e.g.,
`/mnt/c/...`).

# Solution
Move the file to the WSL2 subsystem (e.g., `~/...`).

# Details
Note: I am using this section to document my workflow and extra information for
later reference.

## VS Code Task
I've got a fun little setup for using Hugo in VS Code. I have set the default
build task to run the local server and open a browser window. With a single
`ctrl+shift+b` the server runs and shows the generated website. When I modify a
file, the website is rebuilt and it navigates to the modified section.

This is done with this VS Code task.

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "start-hugo-server",
            "type": "shell",
            "command": "hugo server -v --navigateToChanged", // if the default VS Code terminal on Windows is cmd, use `wsl.exe hugo serve -vw`
            "isBackground": true    // this is a watch process that keeps running
        },
        {
            // opens http://localhost:1313 in the system browser to preview the site.
            "label": "open-browser-1313",
            "type": "shell",
            "command": "/c start http://localhost:1313", // Windows only thing.
            "options": {
                "shell": {
                    "executable": "cmd.exe", // My VS Code's default shell is wsl so I have to change the shell to cmd.exe here.
                }
            }
        },
        {
            "label": "preview-blog",
            // runs both of these together
            "dependsOn": [
                "start-hugo-server",
                "open-browser-1313"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

There are two tasks:

1. `start-hugo-server`: Runs the Hugo server in WSL. It watches for changes by default
   (no need to supply `-w` anymore) and `--navigateToChanged` navigates the
   browser to the latest file modified so I automagically see the modified
   section without any clicks.
2. `open-browser-1313`: Opens the browser on Windows and goes to the URL that
   servers the local website.

I recently switched from an old Ubuntu 18 WSL 1 instance to a Debian 11 running
under WSL2. The local copy of my website was under the Windows file system and
**when I modified the files in VS Code, the server did not see the file updates**
so the website was not rebuilt.

## WSL 1 vs. WSL 2
WSL 1 and 2 have differences in terms of performance and
implementation. See [Comparing WSL 1 and WSL 2][comp]. 

[comp]: https://learn.microsoft.com/en-us/windows/wsl/compare-versions#comparing-features

The only thing I care about is "file system performance."

* WSL 1 has better performance across the board.
* WSL 2 has better performance for files in its own file system (e.g., `~/...`).

The reason is mainly behind the `Managed VM` feature of WSL 2. When I had Ubuntu
18 on WSL 1, I could go to
`%LocalAppData%/packages/CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc/LocalState`
and see the entire file system there. In other words, each Linux file was a
separate file.

For my Debian 11 running on WSL 2, I go to
`%LocalAppData%/Packages/TheDebianProject.DebianGNULinux_76v4gfsz19hv4/LocalState`
and I see `ext4.vhdx` (which is a Hyper-V virtual hard disk format). If you want
to see access the files system, you can paste this in the run menu:
`\\wsl$\Debian`.

Where `Debian` is the name of the distro. You can see all of them with `wsl.exe
-l -v`. This works both on Windows and inside WSL. Make sure you're pasting the
command as-is. `wsl -l -v` in WSL won't work, it must be `wsl.exe -l -v`.

## What was the Solution?
I copied my entire local git directory to Debian's home. It took a while but I
realized I do almost all of my development in WSL so why not take advantage of
it.

On a side note, you can convert a WSL 1 distro to WSL 2 and back. It takes a few
minutes mainly because files must be copied from one file system to the other.

```
wsl --set-version {DistroName} 2 # or 1
```
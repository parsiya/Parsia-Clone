---
title: "VS Code Tasks - Notes"
draft: false
toc: true
comments: false
categories:
- Configs
tags:
- VS Code
wip: false
snippet: "Quick notes on Visual Studio Code tasks."
---


VS Code tasks are a way to run external tools. I used VS Code tasks to preview
my blogs. All of my blogs are based on Hugo so I use the local watch server to
preview them.

# Single Task - Hugo Server
Initially I wrote a task to run the local Hugo watch server. Tasks are JSON
files and you can read about them here:

* [https://code.visualstudio.com/docs/editor/tasks][tasks-link]

[tasks-link]: https://code.visualstudio.com/docs/editor/tasks

My default shell in VS Code is [Windows Subsystem for Linux 2 (WSL2)][wsl-link]
so I have installed Hugo there but, it doesn't really matter. We want to run
`hugo serve -vw` (`serve` and `server` are the same).

[wsl-link]: https://docs.microsoft.com/en-us/windows/wsl/install-win10
[hugo-server]: https://gohugo.io/commands/hugo_server/

```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "start-hugo-server",
            "type": "shell",
            // if the default VS Code terminal on Windows is cmd, use `wsl.exe hugo serve -vw`
            "command": "hugo serve -vw",
            "group": {
                "kind": "build",
                "isDefault": true
            },
        }
    ]
}
```

The `group` object designates the default build task. I can run it with
`ctrl+shift+b`. This makes my life a bit easier.

# WSL vs. cmd - Opening the Preview Website
A second step is also opening the browser and going to the local website's URL.
The default address is `http://localhost:1313`. If the base URL has a directory
in its path, then you need to use it. E.g., my Persian (or Farsi depending on
who you ask) is a project site at https://parsiya.github.io/parsiya.fa/ so the
preview URL is `http://localhost:1313/parsiya.fa`.

So, it helps to automatically go to that URL instead of having to use a shortcut
or type it (*gasp*). You can have unlimited websites hosted on GitHub pages
(with or without custom domains):

* https://parsiya.net/blog/2021-02-17-automagically-deploying-websites-with-custom-domains-to-github-pages/

Adding a second task started simple but turned complex really fast. I am on
Windows but my default VS Code shell is WSL2.

Inside the cmd we can use `start http://localhost:1313` but, it does not work in
WSL. In both WSL and cmd we can use `explorer.exe http://localhost:1234` to open
the URL in the system's default browser. But using it as the command in the task
does not work because it's run as `wsl.exe -e explorer.exe
http://localhost:1234` and it silently fails.

So, we use the `options > shell > executable` object to designate the shell
executable. Also, note the `/c` command line switch passed to the cmd.

The command to run the task can be `start http://localhost:1313`

```json
// "tasks": [
{
    // opens http://localhost:1313 in the system browser to preview the site.
    "label": "open-browser-1313",
    "type": "shell",
    "command": "/c start http://localhost:1313",
    "options": {
        "shell": {
            "executable": "cmd.exe",
        }
    }
}
// ]
```

# Multiple Tasks
Now, we have two different tasks that do what we want. The next step is to run
them both at once. My initial thought was to use the `dependsOn` attribute. So I
modified the `open-browser-1313` task to depend on the preview website task.
This means if I run the `open-browser-1313` task, it will run the
`start-hugo-server` task first and then execute after it has finished.

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "start-hugo-server",
            "type": "shell",
            "command": "hugo serve -vw",
            "isBackground": true    // this is a watch process that keeps running
        },
        {
            "label": "open-browser-1313",
            "type": "shell",
            "command": "/c start http://localhost:1313",
            "options": {
                "shell": {
                    "executable": "cmd.exe",
                }
            },
            "dependsOn": [
                "start-hugo-server"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

But this does not work. Running the `open-browser-1313` task will run the
`start-hugo-server` task but it does not start itself until the previous task
has finished even though the Hugo server task is a background task.

The solution is to `create a new task that runs both of them`.

```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "start-hugo-server",
            "type": "shell",
            "command": "hugo serve -vw", // if the default VS Code terminal on Windows is cmd, use `wsl.exe hugo serve -vw`
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

Now, if I hit `ctrl+shift+b` the `preview-blog` runs the Hugo server and then
opens the preview site is the system's default browser.

**Note on port:** If you prefer a different port, you can run your server 
with `hugo serve -p 1234` and then open `http://localhost:1234`.
---
draft: false
toc: true
comments: false
categories:
- Development
title: "Kotlin Development"
wip: false
snippet: "Notes on Kotline development, especially Burp extensions."
---

## Kotlin Language Server not Recognizing Burp API
The [Kotlin extension by fwcd][kotlin-ext] has a language server, but doesn't 
recognize imported libraries, either. The extension is supposed to find
them inside a gradle or maven project, but it didn't work for me with gradle.

[kotlin-ext]: https://marketplace.visualstudio.com/items?itemName=fwcd.kotlin

Apparently, the fix is to build the server yourself and replace it with the one
from the extension according to the instructions by [BuZZ-dEE on GitHub][buzz].

[buzz]: https://github.com/fwcd/vscode-kotlin/issues/85#issuecomment-2095793958

Modified instructions from the link above:

```bash
# install openjdk 11, you probably need 21 for Burp, too.
sudo apt install msopenjdk-11
git clone https://github.com/fwcd/kotlin-language-server
cd kotlin-language-server
./gradlew :server:installDist
mv ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server server-backup
# assuming /kotlin-language-server is where you built the server
cp -r ~/kotlin-language-server/server/build/install/server ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/
```

Instead of a symlink per the original instructions, I just copied the server.
It didn't work anyways! I cannot see any error messages either. I can run the
language server manually.

In the extension settings, there is a path to language server. So I set it like this:

```json
"kotlin.languageServer.path":
    "~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server/bin/kotlin-language-server"
```

But I got this error

```
[Error - 11:56:46 AM] Kotlin Language Client client: couldn't create connection to server.
Launching server using command ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server/bin/kotlin-language-server failed. Error: spawn ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server/bin/kotlin-language-server ENOENT
```

Which is weird, because I can run the language server manually with that command and it says:

```json
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
Content-Length: 127

{"jsonrpc":"2.0","method":"window/logMessage","params":{"type":3,"message":"main      Kotlin Language Server: Version 1.3.14"}}Content-Length: 108

{"jsonrpc":"2.0","method":"window/logMessage","params":{"type":3,"message":"main      Connected to client"}}
```

Not sure which client it is.

Replacing `~` with the complete path does the job. I can see the server running,
but it still cannot find the imports inside a gradle project.

At this point I gave up and uninstalled the extension. Instead of used the
https://github.com/Kotlin/kotlin-lsp extension. You have to download and install
the vsix manually, but it works.

----------


---
draft: false
toc: false
comments: false
categories:
- Reverse engineering
tags:
- winappdbg
title: "WinAppDbg Notes"
wip: false
snippet: "Blogs are at [https://parsiya.net/categories/winappdbg/](https://parsiya.net/categories/winappdbg/)."

---

# WinAppDbg

Main guide is here: http://winappdbg.readthedocs.io/en/latest/ProgrammingGuide.html

## 32-bit and 64-bit Python
Generally you want to debug 32-bit applications in 32-bit Python. You can have both of them together on one machine. When installing the 2nd Python, uncheck `register extensions` in the installer. On a VM it does not really matter because you can install/uninstall Python 32 and 64 bit versions at will.

## Installation
Pip installed version 1.5.

To get 1.6, we use the github repo at https://github.com/MarioVilas/winappdbg. Clone and run `install.bat`.

According to the installation documentation we may benefit from additional software.

- Capstone: `python -m pip install capstone-windows`
- distorm3: Download binaries from release page https://github.com/gdabah/distorm/releases

https://breakingcode.wordpress.com/2012/04/08/quickpost-installer-for-beaenginepython/

Has installers for the rest.

---------

## Debugging

This is what I want:

* http://winappdbg.readthedocs.io/en/latest/Debugging.html#breakpoints-watches-and-hooks


``` python
from winappdbg.win32 import *


# Create a snapshot of the process, only take the heap list.
hSnapshot = CreateToolhelp32Snapshot( TH32CS_SNAPHEAPLIST, pid )
```

- HexDump:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L451
- take_memory_snapshot:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L3261
- restore_memory_snapshot:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L3301
- bSkipMappedFiles:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L3317
- break_at:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/breakpoint.py#L3905
    - http://winappdbg.readthedocs.io/en/latest/Debugging.html?highlight=break_at#example-11-setting-a-breakpoint
- get_context:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/thread.py#L469
- set_context:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/thread.py#L570
- All memory read stuff are at:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L125
- Use built-in Table:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L1094
    - `table = Table("|")` we can add separator here.
- Logger class:
    - https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L1766

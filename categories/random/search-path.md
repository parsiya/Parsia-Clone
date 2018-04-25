---
draft: false
toc: false
comments: false
categories:
- Random
tags:
- Windows
- SearchPath
title: "Windows SearchPath"
wip: false
snippet: "Notes about Windows SearchPath."
---

A while ago I was playing with the Windows API [SearchPath][searchpath-link]. It will search for a specific file in `PATH`.

``` cpp
DWORD WINAPI SearchPath(
    _In_opt_  LPCTSTR lpPath,
    _In_      LPCTSTR lpFileName,
    _In_opt_  LPCTSTR lpExtension,
    _In_      DWORD   nBufferLength,
    _Out_     LPTSTR  lpBuffer,
    _Out_opt_ LPTSTR  *lpFilePart
);
```

Note this quirk from the "Remarks" section. When `lpPath` is NULL (which usually is). It looks up the following registry key. If the value is `1` it will first search in PATH then in current working directory and vice versa if `0`. Default is `0`.

- HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\SafeProcessSearchMode

[searchpath-link]: https://msdn.microsoft.com/en-us/library/windows/desktop/aa365527(v=vs.85).aspx

# Call Windows APIs with C++ using MinGW

1. Install MinGW setup:
    - [https://sourceforge.net/projects/mingw/files/Installer/][mingw-link]
2. Install `mingw32-gcc-g++`.
3. Add `C:\MinGW\bin` to PATH.
4. Do `g++ -g test.cpp -o text.exe -w -mwindows` (mix and match switches).

## Simple Windows API Call
Just add `#include <windows.h>` and call stuff.

For example the following program displays a message box, sleeps for 2 seconds and then displays another message box.

``` cpp
// g++ -g test.cpp -o test.exe -w

#include <stdio.h>
#include <windows.h>

// MessageBox: https://msdn.microsoft.com/en-us/library/windows/desktop/ms645505(v=vs.85).aspx
// Sleep: https://msdn.microsoft.com/en-us/library/windows/desktop/ms686298(v=vs.85).aspx

int main(void)
{
    MessageBox(NULL, "test", "test", 0x20);
    Sleep(2000);
    MessageBox(NULL, "test2", "test2", 0x06);
    return 0;
}
```

Now run `test.exe`.


<!-- Links -->

[mingw-link]: https://sourceforge.net/projects/mingw/files/Installer/

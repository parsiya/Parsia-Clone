# Call Windows APIs with C++ using MinGW
This can be accomplished without Cygwin/MSYS.

## Example Program
Let's assume we want to build the following program `test.c`. It displays a message box, sleeps for two seconds and displays another message box.

Using `#include <windows.h>` enables us to call Windows APIs.

``` cpp
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

## Using win-builds.org

1. Download the installer from [http://win-builds.org/][win-builds].
2. Run the installer. Select `Native Windows` and `i686` arch.
3. Choose a path for 32-bit installation. For example: `c:\mingw\x86`.
4. Click on `Process` to start downloading.
5. If there's an error during a download, the tool will just stop. If the tools is not doing anything for a while, check the errors in command prompt. If this happens:
    - Close the installer.
    - Navigate to `c:\mingw\x86\` and run `yypkg-1.5.0.exe` (version number might be different).
    - Click on `Process` again to continue downloading.
    - Rinse and repeat until everything is downloaded
6. Go back to step 2, re-run the installer. Select `Native Windows` and `x86_64`.
7. Choose a path for 64-bit installation (must be on a Windows 64-bit machine). For example `c:\mingw\x64`.
8. Follow steps 4 and 5 until everything is installed.
9. Now we can build the program for both architectures (switches are optional).
    - 32-bit:
        - `cd c:\mingw\x86\bin`
        - `c:\mingw\x86\bin\> gcc.exe -g c:\path\to\test.c -o c:\path\to\test-32.exe -w -mwindows`
    - 64-bit: 
        - `cd c:\mingw\x64\bin`
        - `c:\mingw\x64\bin\> gcc.exe -g c:\path\to\test.c -o c:\path\to\test-32.exe -w -mwindows`
10. If you see yourself building only one architecture, add the corresponding `bin` directory to PATH.

## Using MinGW (32-bit)

1. Install MinGW setup:
    - [https://sourceforge.net/projects/mingw/files/Installer/][mingw-link]
2. Install `mingw32-gcc-g++` using the package manager.
3. Add `C:\MinGW\bin` to PATH.
4. Do `gcc -g test.cpp -o text.exe -w -mwindows` (mix and match switches).

<!-- Links -->

[mingw-link]: https://sourceforge.net/projects/mingw/files/Installer/
[win-builds]: http://win-builds.org/

// gcc -g test.cpp -o test.exe -mwindows -w

// See Also: https://github.com/parsiya/Parsia-Clone/blob/master/clone/random/mingw-windows.md

#include <windows.h>

int main(void)
{
    MessageBox(NULL, "test", "test", 0x20);
    Sleep(2000);
    MessageBox(NULL, "test2", "test2", 0x06);
    return 0;
}
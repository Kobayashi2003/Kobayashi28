// play music
#include <windows.h>
#include <tchar.h>
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

int main() {
    mciSendString(TEXT("play bg.mp3"), NULL, 0, NULL);
    system("pause");
    return 0;
}
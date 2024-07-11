/*
 * @Description: 
 * @Autor: Kadia
 * @Date: 2020-05-18 22:03:18
 * @LastEditors: Kadia
 * @connect: vx:ccz1354 qq:544692713
 * @LastEditTime: 2020-05-19 12:22:14
 */ 
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <time.h>
#include <windows.h>
char date[35][65];
int fxx[5]={0,1,-1,0,0};
int fxy[5]={0,0,0,-1,1};
HANDLE hOutput, hOutBuf;
COORD coord = { 0,0 };
DWORD bytes = 0;
void initconsoleScreenBuffer();
int show(char input);
int main()
{
    char input;
    initconsoleScreenBuffer();
    while(1)
    {
        if(!show(input))
            break;
        input=getch();
        if(input=='0')
            break;
    }
    return 0;
}
void initconsoleScreenBuffer()
{
    hOutBuf = CreateConsoleScreenBuffer(
        GENERIC_WRITE,
        FILE_SHARE_WRITE,
        NULL,
        CONSOLE_TEXTMODE_BUFFER,
        NULL
    );
    hOutput = CreateConsoleScreenBuffer(
        GENERIC_WRITE,
        FILE_SHARE_WRITE,
        NULL,
        CONSOLE_TEXTMODE_BUFFER,
        NULL
    );
    CONSOLE_CURSOR_INFO cci;
    cci.bVisible = 0;
    cci.dwSize = 1;
    SetConsoleCursorInfo(hOutput, &cci);
    SetConsoleCursorInfo(hOutBuf, &cci);
    for(int i=0;i<30;i++)
    {
        for(int j=0;j<60;j++)
        {
            date[i][j]='-';
            if(i==15&&j==15)
                date[i][j]='W';
        }
    }
}
int show(char input)
{
    int toward;
    switch(input)
    {
        case 's' : toward=1;break;
        case 'w' : toward=2;break;
        case 'a' : toward=3;break;
        case 'd' : toward=4;break;
        default  : toward=0;break;
    }
    for(int i=0;i<30;i++)
    {
        for(int j=0;j<60;j++)
        {
            if(date[i][j]=='W'&&i+fxx[toward]>=0&&i+fxx[toward]<30&&j+fxy[toward]>=0&&j+fxy[toward]<60)
            {
                date[i][j]='-';
                date[i+fxx[toward]][j+fxy[toward]]='W';
                goto loop1;
            }
        }
    }
loop1:
    for(int i=0;i<30;i++)
    {
        coord.Y=i;
        WriteConsoleOutputCharacterA(hOutBuf,date[i],60,coord,&bytes);
    }
    SetConsoleActiveScreenBuffer(hOutBuf);
    input=getch();
    if(input=='0')
        return 0;
    switch(input)
    {
        case 's' : toward=1;break;
        case 'w' : toward=2;break;
        case 'a' : toward=3;break;
        case 'd' : toward=4;break;
        default  : toward=0;break;
    }
    for(int i=0;i<30;i++)
    {
        for(int j=0;j<60;j++)
        {
            if(date[i][j]=='W'&&i+fxx[toward]>=0&&i+fxx[toward]<30&&j+fxy[toward]>=0&&j+fxy[toward]<60)
            {
                date[i][j]='-';
                date[i+fxx[toward]][j+fxy[toward]]='W';
                goto loop2;
            }
        }
    }
loop2:
    for(int i=0;i<30;i++)
    {
        coord.Y=i;
        WriteConsoleOutputCharacterA(hOutput,date[i],60,coord,&bytes);
    }
    SetConsoleActiveScreenBuffer(hOutput);
    return 1;
}

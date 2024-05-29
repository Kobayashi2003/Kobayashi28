#ifndef STDIO_H
#define STDIO_H

#include "os_type.h"

class STDIO
{
private:
    uint8 *screen;

public:
    STDIO();
    // initialize function
    void initialize();

    // print character c with color to current cursor position 
    void print(uint8 c, uint8 color = 0x07);
    // print character c with color to position (x, y)
    void print(uint x, uint y, uint8 c, uint8 color = 0x07);

    // print string with color to current cursor position, return the number of characters
    int print(const char *const str, uint8 color = 0x07);
    // print string with color to position (x, y), return the number of characters
    int print(uint x, uint y, const char *const str, uint8 color = 0x07);

    // move cursor to a one dimensional position
    void moveCursor(uint position);
    // move cursor to a two dimensional position
    void moveCursor(uint x, uint y);
    // get cursor position
    uint getCursor();

private:
    // roll up the screen 
    void rollUp();

    void print_backslash_n();
    void print_backslash_t();
    void print_backslash_b();
};

int printf(const char *const fmt, ...);

#endif
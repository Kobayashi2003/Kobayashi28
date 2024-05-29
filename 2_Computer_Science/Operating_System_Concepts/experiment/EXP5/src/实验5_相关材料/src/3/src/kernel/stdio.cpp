#include "stdio.h"
#include "os_type.h"
#include "asm_utils.h"
#include "os_modules.h"
#include "stdarg.h"
#include "stdlib.h"


void STDIO::initialize() {
    screen = (uint8 *)(0xb8000);
}

void STDIO::print(uint x, uint y, uint8 c, uint8 color) {

    if (x >= 25 || y >= 80) {
        return;
    }

    uint pos = x * 80 + y;
    screen[2 * pos] = c;
    screen[2 * pos + 1] = color;
}

void STDIO::print(uint8 c, uint8 color=0x07) {
    uint cursor = getCursor();
    screen[2 * cursor] = c;
    screen[2 * cursor + 1] = color;
    cursor++;
    if (cursor == 25 * 80) {
        rollUp();
        cursor = 24 * 80;
    }
    moveCursor(cursor);
}

void STDIO::print(uint8 c) {
    print(c, 0x07);
}

int STDIO::print(const char* str) {
    int i = 0;
    while (str[i]) {
        if (str[i] == '\n') {
            uint row = getCursor() / 80;
            if (row == 24) {
                rollUp();
            } else {
                ++row;
            }
            moveCursor(row * 80);
        } 
        else if (str[i] == '\t') {
            // Assuming tab size of 4 spaces for simplicity
            uint8 space_indent = 4 - getCursor() % 4; 
            for (int i = 0; i < space_indent; ++i) {
                print(' ', 0x07);
            }
        }
        else {
            print(str[i]);
        }
    }

    return i;
}

void STDIO::moveCursor(uint position) {
    if (position >= 80 * 25) {
        return;
    }

    uint8 high = (position >> 8) & 0xFF;
    uint8 low = position & 0xFF;

    asm_out_port(0x3D4, 0x0E);
    asm_out_port(0x3D5, high);
    asm_out_port(0x3D4, 0x0F);
    asm_out_port(0x3D5, low);
}

void STDIO::moveCursor(uint x, uint y) {
    if (x >= 25 || y >= 80) {
        return;
    }
    moveCursor(x * 80 + y);
}

uint STDIO::getCursor() {
    uint pos = 0;
    uint8 temp;

    // Get the high byte of the cursor's position
    asm_out_port(0x3D4, 0x0E);
    asm_in_port(0x3D5, &temp);
    pos = ((uint)temp) << 8;
    // Get the low byte of the cursor's position
    asm_out_port(0x3D4, 0x0F);
    asm_in_port(0x3D5, &temp);
    pos |= (uint)temp;
    
    return pos;
}

void STDIO::rollUp() {
    uint length = 25 * 80;
    for (uint i = 80; i < length; ++i) {
        screen[2 * (i - 80)] = screen[2 * i];
        screen[2 * (i - 80) + 1] = screen[2 * i + 1];
    }
    for (uint i = 24 * 80; i < length; ++i) {
        screen[2 * i] = ' ';
        screen[2 * i + 1] = 0x07;
    }
}



int STDIO::printf(const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    int printed = 0;
    for (int i = 0; fmt[i]; ++i) {
        if (fmt[i] == '%') {
            i++;
            switch (fmt[i]) {
                case 'c':
                    print(va_arg(args, int)); // char promoted to int
                    break;
                case 's':
                    print(va_arg(args, const char*));
                    break;
                case 'd':
                    // Convert integer to string and print
                    break;
                case 'x':
                    // Convert integer to hexadecimal string and print
                    break;
                default:
                    print(fmt[i]);
                    break;
            }
        } else {
            print(fmt[i]);
        }
    }
    va_end(args);
    return printed;
}

// Implementations for asm_out_port and asm_in_port are platform-specific and omitted for brevity.

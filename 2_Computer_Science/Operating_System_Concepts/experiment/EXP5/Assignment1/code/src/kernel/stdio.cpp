#include "stdio.h"
#include "os_type.h"
#include "asm_utils.h"
#include "os_modules.h"
#include "stdarg.h"
#include "stdlib.h"

STDIO::STDIO() {
    initialize();
}

void STDIO::initialize() {
    screen = (uint8 *)(0xb8000);
}

void STDIO::print(uint8 character, uint8 color) {
    uint cursor_pos = getCursor();
    uint cur_x = cursor_pos / 80;
    uint cur_y = cursor_pos % 80;
    print(cur_x, cur_y, character, color);
    cursor_pos++;
    if (cursor_pos == 25 * 80) {
        rollUp();
        cursor_pos = 24 * 80;
    }
    moveCursor(cursor_pos);
}

void STDIO::print(uint x, uint y, uint8 character, uint8 color) {

    if (x >= 25 || y >= 80) {
        return ;
    }

    switch (character) {
    case '\n':
        print_backslash_n();
        return ;
    case '\t':
        print_backslash_t();
        return ;
    case '\b':
        print_backslash_b();
        return ;
    }
  
    uint pos = x * 80 + y;
    screen[2 * pos] = character;
    screen[2 * pos + 1] = color;
}

int STDIO::print(const char* str, uint8 color) {
    int i = 0;
    while (str[i]) {
        print(str[i], color);
        i++;
    }
    return i;
}

int STDIO::print(uint x, uint y, const char *const str, uint8 color) {
    uint cur_pos = getCursor();
    moveCursor(x, y);
    int i = 0;
    while (str[i]) {
        print(str[i], color);
        i++;
    }
    moveCursor(cur_pos);
    return i;
}

void STDIO::moveCursor(uint position) {

    if (position >= 80 * 25) {
        return ;
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
        return ;
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

void STDIO::print_backslash_n() {
    uint row = getCursor() / 80;
    if (row == 24) {
        rollUp();
    } else {
        ++row;
    }
    moveCursor(row * 80);
}

void STDIO::print_backslash_t() {
    // Assuming tab size of 4 spaces for simplicity
    int space_indent = 4 - getCursor() % 4;
    for (int i = 0; i < space_indent; ++i) {
        print(' ');
    }
}

void STDIO::print_backslash_b() {
    uint cursor_pos = getCursor();
    if (cursor_pos == 0) {
        return ;
    }
    moveCursor(--cursor_pos);
}

int printf_add_to_buffer(char *buffer, char character, int &idx, const int BUF_LEN)
{
    int counter = 0;

    buffer[idx] = character;
    ++idx;

    if (idx == BUF_LEN)
    {
        buffer[idx] = '\0';
        counter = stdio.print(buffer);
        idx = 0;
    }

    return counter;
}

int printf(const char *const fmt, ...)
{
    const int BUF_LEN = 32;

    char buffer[BUF_LEN + 1];
    char number[33];

    int idx, counter;
    va_list ap;

    va_start(ap, fmt);
    idx = 0;
    counter = 0;

    for (int i = 0; fmt[i]; ++i)
    {
        if (fmt[i] != '%')
        {
            counter += printf_add_to_buffer(buffer, fmt[i], idx, BUF_LEN);
        }
        else
        {
            i++;
            if (fmt[i] == '\0')
            {
                break;
            }

            switch (fmt[i])
            {
            case '%':
                counter += printf_add_to_buffer(buffer, fmt[i], idx, BUF_LEN);
                break;

            case 'c':
                counter += printf_add_to_buffer(buffer, va_arg(ap, char), idx, BUF_LEN);
                break;

            case 's':
                buffer[idx] = '\0';
                idx = 0;
                counter += stdio.print(buffer);
                counter += stdio.print(va_arg(ap, const char *));
                break;

            case 'd':
            case 'x':
                int temp = va_arg(ap, int);

                if (temp < 0 && fmt[i] == 'd')
                {
                    counter += printf_add_to_buffer(buffer, '-', idx, BUF_LEN);
                    temp = -temp;
                }

                itos(number, temp, (fmt[i] == 'd' ? 10 : 16));

                for (int j = 0; number[j]; ++j)
                {
                    counter += printf_add_to_buffer(buffer, number[j], idx, BUF_LEN);
                }
                break;
            }
        }
    }

    buffer[idx] = '\0';
    counter += stdio.print(buffer);

    return counter;
}


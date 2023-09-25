import win32console
import shutil
import time
import msvcrt

def main():
    width, height = shutil.get_terminal_size()
    buf = win32console.CreateConsoleScreenBuffer()
    output = 'X' * width * height
    buf.WriteConsoleOutputCharacter(output, win32console.PyCOORDType(0, 0))
    buf.SetConsoleActiveScreenBuffer()
    msvcrt.getch()
    for i in range(0, width * height):
        # output = '#' * i
        # buf.WriteConsoleOutputCharacter(output, win32console.PyCOORDType(0, 0))
        # buf.SetConsoleActiveScreenBuffer()
        buf.WriteConsole('#')
        # time.sleep(0.01)
    msvcrt.getch()
    buf.ScrollConsoleScreenBuffer(win32console.PySMALL_RECTType(0, 0, width-1, 2), None, win32console.PyCOORDType(0, 3), ' ', 0x0f)
    msvcrt.getch()
    buf.SetConsoleCursorPosition(win32console.PyCOORDType(0, 0))
    for i in range(0, 3):
        buf.WriteConsole(f'{i}' * width)
        time.sleep(0.5)
    buf.SetConsoleCursorPosition(win32console.PyCOORDType(0, 0))
    msvcrt.getch()


if __name__ == '__main__':
    main()

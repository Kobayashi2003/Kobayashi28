import win32console
import time

def fun1():
    buf = win32console.CreateConsoleScreenBuffer()
    # int = WriteConsole(Buffer)
    # Writes characters at current cursor position

    # Parameters
    # Buffer: PyUNICODE
    #   String or Unicode to be written to console

    # Return Value
    # Returns the number of characters written
    num = buf.WriteConsole('test')
    buf.SetConsoleActiveScreenBuffer()

    # FlushConsoleInputBuffer()
    # Flush input buffer

    time.sleep(1)
    print(num)

def fun2():
    buf = win32console.CreateConsoleScreenBuffer()
    # (size, bVisible) = GetConsoleCursorInfo()

    # Return Value
    # Returns the size of the console's cursor expressed as a 
    # percentage of character size, and a boolen indicating
    # if cursor is visible.
    curseinfo = buf.GetConsoleCursorInfo()
    print(curseinfo) 

def fun3():
    buf = win32console.CreateConsoleScreenBuffer()
    buf.WriteConsole('test')
    buf.SetConsoleActiveScreenBuffer()

    # SetConsoleCursorInfo(Size, Visible)

    # Parameters
    # Size: int
    #   Percentage of character size that cursor will occupy.
    # Visible: boolen
    #   Determines if cursor is visible.

    ori = buf.GetConsoleCursorInfo()
    
    buf.SetConsoleCursorInfo(100, True)
    time.sleep(1)
    buf.SetConsoleCursorInfo(1, False)
    time.sleep(1)
    buf.SetConsoleCursorInfo(ori[0], ori[1])
    time.sleep(1)


def fun4():
    buf = win32console.CreateConsoleScreenBuffer()
    # int = GetConsoleMode()
    # Returns a combination of ENABLE_*_INPUT or ENABLE_*_OUTPUT constants
    mode = buf.GetConsoleMode()
    print(mode)

    # SetConsoleMode(mode)

def fun5():



    pass

    # PyUNICODE = ReadConsole(NumberOfCharsToRead)
    # Reads characters from the console input buffer

    # Parameters
    # NumberOfCharsToRead: int
    #   Characters to read

def fun6():
    # SetConsoleTextAtrribufe(Attributes)
    # Sets character attributes for subsequent write operations
    # Parameters
    # Attributes: int
    #   Attributes to set, combination of FOREGROUND_* and BACKGROUND_* and COMMON_LVB_* constants

    buf = win32console.CreateConsoleScreenBuffer()
    buf.WriteConsole('test')
    buf.SetConsoleActiveScreenBuffer()
    time.sleep(1)

    buf.SetConsoleTextAttribute(0x0f)
    buf.WriteConsole('test')
    time.sleep(1)   


def fun7():
    # SetConsoleCursorPosition(CursorPosition)
    # Sets the console screen buffer's cursor position

    # Parameters
    # CursorPosition: PyCOORD
    #   A PyCOORD containing the new cursor position

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()


    p1 = win32console.PyCOORDType(0, 0)
    p2 = win32console.PyCOORDType(10, 10)

    buf.WriteConsole('test')
    time.sleep(1)
    buf.SetConsoleCursorPosition(p1)
    buf.WriteConsole('hello')
    time.sleep(1)
    buf.SetConsoleCursorPosition(p2)
    buf.WriteConsole('world')
    time.sleep(1)


def fun8():
    # SetConsoleScreenBufferSize(Size)
    # Sets the size of the console screen buffer

    # Parameters
    # Size: PyCOORD
    #   COORD object containing the new dimensions

    pass

def fun9():

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    # dict = GetConsoleScreenBufferInfo()
    print(buf.GetConsoleScreenBufferInfo())
    time.sleep(1)

    # SetConsoleWindowInfo(Absolute, ConsoleWindow)
    # Changes size and position of a console's window

    # Parameters
    # Absolute: boolen
    #   If False, coordinates are relative to current position
    # ConsoleWindow: PySMALL_RECT
    #   A SMALL_RECT containing the new window coordinates

    coor = win32console.PySMALL_RECTType(0, 0, 100, 100)
    buf.SetConsoleWindowInfo(True, coor)

    print(buf.GetConsoleScreenBufferInfo())
    time.sleep(1)


def fun10():
    # PyCOORD = GetLargestConsoleWindowSize()
    # Returns the largest possible size for the console window
    buf = win32console.CreateConsoleScreenBuffer()
    print(buf.GetLargestConsoleWindowSize())


def fun11():
    # int = FillConsoleOutputAttribute(Attribute, Length, WriteCoord)
    # Set text attributes for a consecutive series of characters

    # Parameters
    # Attribute: int
    #   Text attributes to be set, combination of FOREGROUND_* and BACKGROUND_* and COMMON_LVB_* constants
    # Length: int
    #   The number of characters to set
    # WriteCoord: PyCOORD
    #   The screen position to begin at
    # Return Value
    #   Returns the number of characters cells whose attributes were set

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    buf.WriteConsole('hello world')
    time.sleep(1)
    buf.FillConsoleOutputAttribute(0x0f, 4, win32console.PyCOORDType(0, 0))
    time.sleep(1)


def fun12():
    # int = FillConsoleOutputCharacter(Character, Length, WriteCoord)
    #   Sets consecutive character positions to a specified character
    # Parameters
    # Character: PyUNICODE
    #   A single character to be used to fill the specified range
    # Length: int
    #   The number of characters positions to fill
    # WriteCoord: PyCOORD
    #   The screen position to begin at
    # Return Value
    #   Returns the number of characters actually written

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    buf.FillConsoleOutputCharacter('a', 100, win32console.PyCOORDType(10, 10))
    time.sleep(1)


def fun13():
    # PyUnicode = ReadConsoleOutputCharacter(Length, ReadCoord)
    #   Reads consecutive characters from a starting position
    # Parameters
    # Length: int
    #   The number of characters positions to read
    # ReadCoord: PyCOORD
    #   The screen position start reading from

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    buf.WriteConsole('hello world')
    time.sleep(1)
    print(buf.ReadConsoleOutputCharacter(5, win32console.PyCOORDType(0, 0)))


def fun14():
    # (int,...) = ReadConsoleOutputAttribute(Length, ReadCoord)
    pass


def fun15():
    # int = WriteConsoleOutputCharacter(Characters, WriteCoord)
    #   Writes a string of characters at a specified position
    # Parameters
    # Characters: PyUNICODE
    #   Characters to be written
    # WriteCoord: PyCOORD
    #   The screen position at which to start writing
    # Return Value
    #   Returns the number of characters actually  written 

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    buf.WriteConsoleOutputCharacter('hello world', win32console.PyCOORDType(10, 10))
    time.sleep(1)


    # int = WriteConsoleOutputAttribute(Attributes, WriteCoord)

    
def fun16():
    # ScrollConsoleScreenBuffer(ScrollRectangle, ClipRectangle, DestinationOrigin, FillCharacter, FillAttribute)
    #   Scrolls a region of the display
    # Parameters
    # ScrollRectangle: PySMALL_RECT
    #   The region to be scrolled
    # ClipRectangle: PySMALL_RECT
    #   Rectangle that limits display area affected, can be None
    # DestinationOrigin: PyCOORD
    #   The position to which ScrollRectangle wil be moved
    # FillCharacter: PyUNICODE
    #   Character to fill in the area left blank by scrolling operation
    # FillAttribute: int
    #   Text attributes to apply to FillCharacter

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    wininfo = buf.GetConsoleScreenBufferInfo()
    size = wininfo['Size']

    buf.FillConsoleOutputCharacter('a', size.X * (size.Y // 4), win32console.PyCOORDType(0, 0))
    buf.FillConsoleOutputCharacter('b', size.X * (size.Y // 4), win32console.PyCOORDType(0, size.Y // 4))
    buf.FillConsoleOutputCharacter('c', size.X * (size.Y // 4), win32console.PyCOORDType(0, size.Y // 4 * 2))
    buf.FillConsoleOutputCharacter('d', size.X * (size.Y // 4), win32console.PyCOORDType(0, size.Y // 4 * 3))
    input()

    buf.ScrollConsoleScreenBuffer(win32console.PySMALL_RECTType(0, 0, size.X // 4 - 1, size.Y // 4 - 1 ), None, win32console.PyCOORDType(0, size.Y // 4), ' ', 0x0f)
    input()



def fun17():
    # (int, PyCOORD) = GetCurrentConsoleFont(MaximumWindow)
    #   Returns currently displayed font

    # Parameters
    # MaximumWindow: boolen
    #   If True, retrieves font for maximum window size

    # Comments
    #     Only exists on XP or later.
    #     MSDN docs claim the returned COORD is the font size, but it's actually the window size.
    #     Use PyConsoleScreenBuffer::GetConsoleFontSize for the font size.

    # Return Value
    #  Returns the index of current font and window size

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    index, size = buf.GetCurrentConsoleFont(True)
    print(index, size)


def fun18():
    # PyCOORD = GetConsoleFontSize(Font)
    #   Returns size of specified font for the console

    # Parameters
    # Font: int
    #   Index of font as returned by GetCurrnetConsoleFont

    # Comments
    #   Only exists on XP or later.

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()
    index, _ = buf.GetCurrentConsoleFont(True)
    print(buf.GetConsoleFontSize(index))


def fun19():
    # SetConsoleFont(Font)
    #   Changes the font used by the screen buffer

    # Parameters
    # Font: int
    #   The number of the font to be set

    pass


def fun20():
    # SetConsoleDisplayMode(Flags, NewScreenBufferDimensions)
    #   Sets the display mode of the console buffer

    # Parameters
    # Flags: int
    #   CONSOLE_FULLSCREEN_MODE or CONSOLE_WINDOW_MODE

    # NewScreenBufferDimensions: PyCOORD
    #   New size of the screen buffer in characters

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    buf.SetConsoleDisplayMode(1, win32console.PyCOORDType(100, 100))
    input()



def fun21():

    buf = win32console.CreateConsoleScreenBuffer()
    buf.SetConsoleActiveScreenBuffer()

    # int = WriteConsoleInput(Buffer)
    #   Places input records in the console's input queue

    # Parameters
    # Buffer: (PyINPUT_RECORD, ...)
    #   A sequence of PyINPUT_RECORD objects

    # Return Value
    #   Returns the number of records written 


    # (PyINPUT_RECORD, ...) = ReadConsoleInput(Length)
    #   Reads input records and removes them from the input queue

    # Parameters
    # Length: int
    #   The number of input records to read

    # Comments
    # This functions blocks until at least one record is read.
    # The number of records returned may be less than the nbr requested

    # Return Value
    # Returns a sequence of PyINPUT_RECORD objects

    pass


if __name__ == '__main__':
    fun18()

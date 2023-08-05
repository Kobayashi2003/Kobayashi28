import msvcrt

def readch(echo=True):
    "Get a single character on Windows."
    while msvcrt.kbhit():  # clear out keyboard buffer
        msvcrt.getwch()
    ch = msvcrt.getwch()
    if ch in u'\\x00\\xe0':  # arrow or function key prefix?
        ch = msvcrt.getwch()  # second call returns the actual key code
    if echo:
        msvcrt.putwch(ch)
    return ch

def pause(prompt='Press any key to continue . . .'):
    if prompt:
        print(prompt),
    readch(echo=False)

if __name__ == '__main__':
    while True:
        c = readch()
        if c == 'q':
            break
        print(f"you pressed {c}")
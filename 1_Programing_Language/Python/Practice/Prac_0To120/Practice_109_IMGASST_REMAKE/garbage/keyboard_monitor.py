class _Getch:
    """Gets a single character from standard input.  Does not echo to the
    screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
    

getch = _Getch()


if __name__ == '__main__': # a little test

    while True:
        ch = getch()
        # ch = ch.decode('utf-8')
        print(ch)
        if ch == 'q'.encode('utf-8'):
            break

    # import asyncio
    # import msvcrt
    # from time import sleep

    # signal = True
    # last_press = None

    # async def print_last_press():
    #     global signal, last_press
    #     while signal:
    #         if last_press is not None:
    #             print(f"you pressed {last_press}")
    #             last_press = None
    #         await asyncio.sleep(0.01)

    # async def get_input():
    #     global signal, last_press
    #     while signal:
    #         if msvcrt.kbhit():
    #             ch = getch()
    #             ch = ch.decode('utf-8')
    #             if ch == 'q':
    #                 signal = False
    #                 break
    #             last_press = ch
    #         await asyncio.sleep(0.01)

    # async def main():
    #     await asyncio.gather(
    #         print_last_press(),
    #         get_input()
    #     )
    #     print("done")


    # asyncio.run(main())


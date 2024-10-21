import threading
import itertools
import time
import sys


class Signal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = char + " " + msg
        write(status)
        flush()
        write("\x08" * len(status))
        time.sleep(0.1)
        if not signal.go:
            break


def slow_function():
    time.sleep(3) # pretend waiting a long time for I/O
    return 42


def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("thinking!", signal))
    print("spinner object:", spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result


def main():
    result = supervisor()
    print("Answer:", result)


if __name__ == "__main__":
    main()
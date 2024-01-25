import time
import functools
import contextlib
from collections import namedtuple
from multiprocessing import cpu_count
from enum import Enum


# --- Settings --- #

# log settings
LOG_PATH          = './log.txt'
LOG_FORMAT        = '[{time}] -- {func} -- : {msg}\n'
LOG_TIME_FORMAT   = '%Y-%m-%d %H:%M:%S'

# cache settings
CACHEFOLDER_PATH  = './.cache'
MAX_CACHE_SIZE    = 1e12

# font settings
DEFAULT_FONT_PATH = './font/Hack Regular Nerd Font Complete Mono Windows Compatible.ttf'
DEFAULT_FONT_SIZE = 2

# generator settings
MAX_WIDTH         = 1e5
MAX_HEIGHT        = 1e5
MAX_WORKERS       = cpu_count() - 1
MAX_LOAD_NUM      = 5
MAX_WAITING_TIME  = 10
ERROR_RATE        = 0.1
DEFAULT_GENERATE_TYPE     = 'multiprocessing' # classic stringio numpy
DEFAULT_GENERATE_POSITION = 'center'  # center ...

# path settings
MAX_DEPTH         = 10

# supported image format
SUPPORTED_IMAGE_FORMAT          = ( 'jpg', 'jpeg', 'png', 'bmp', 'ico', 'jfif' )
SUPPORTED_IMAGE_FORMAT_SEQUENCE = ( 'gif', 'tif')
SUPPORTED_IMAGE_FORMAT_ALL      = SUPPORTED_IMAGE_FORMAT + SUPPORTED_IMAGE_FORMAT_SEQUENCE

Result = namedtuple('Result', 'status data')
Status = Enum('Status', 'done processing pending error unfound')

DEFAULT_FMT_TIME  = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

SIMPLE_MODE_CODE   = 9070
ADVANCED_MODE_CODE = 9071
TEST_MODE_CODE     = 9072

# --- Decorators --- #

def clock(fmt=DEFAULT_FMT_TIME):
    # clock decorator: print the elapsed time of the function
    def decorator(func):
        @functools.wraps(func)
        def clocked(*_args, **_kwargs):
            t0 = time.perf_counter()
            _result = func(*_args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args_lst = []
            if _args:
                args_lst.append(', '.join(repr(arg) for arg in _args))
            if _kwargs:
                pairs = ['{}={}'.format(k, w) for k, w in _kwargs.items()]
                args_lst.append(', '.join(pairs))
            args = ', '.join(args_lst)
            if len(args) > 30:
                args = args[:13] + '...' + args[-13:]
            result = repr(_result)
            if len(result) > 30:
                result = result[:13] + '...' + result[-13:]
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorator


def parallel_run(func):
    # parallel run decorator: run the function in a new thread
    import threading
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
        return thread
    return wrapper


def suppress_keyboard_interrupt(func):
    # suppress keyboard interrupt decorator: suppress the keyboard interrupt
    import signal
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            pass
    return wrapper


# --- Functions --- #

def get_terminal_size(subprocess=False):
    import os
    if os.name == "posix": # linux
        if subprocess:
            # other possible commands: tput cols
            rows, cols = [ int(x) for x in
                        os.popen("stty size").readline().strip().split()]
        else:
        # http://bytes.com/topic/python/answers/607757-getting-terminal-display-size
        # You may also want to handle the WINCH signal so that you know
        # when the window size has been changed.
            import termios, fcntl, struct, sys
            s = struct.pack("HHHH", 0, 0, 0, 0)
            x = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s)
            rows, cols, x_pixels, y_pixels = struct.unpack("HHHH", x)
        return cols, rows
    else: # windows
        # from http://rosettacode.org/wiki/Terminal_control/Dimensions#Python
        from ctypes import windll, create_string_buffer
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        #return default size if actual size can't be determined
        if not res:
            return 80, 25
        import struct
        (bufx, bufy, curx, cury, wattr, left, top, right, bottom,
                            maxx, maxy)= struct.unpack("hhhhHhhhhhh", csbi.raw)
        width = right - left + 1
        height = bottom - top + 1
        return width, height


def calculate_aspect_ratio(terminal_size, aspect_ratio_table):
    width, height = terminal_size

    if len(aspect_ratio_table) == 0:
        return 1.0

    aspect_ratio_table = { float(key): value for key, value in aspect_ratio_table.items() }
    sorted_keys = sorted(aspect_ratio_table.keys())

    if width / height in aspect_ratio_table:
        return aspect_ratio_table[width / height]

    if width / height < sorted_keys[0]:
        return aspect_ratio_table[sorted_keys[0]]

    if width / height > sorted_keys[-1]:
        return aspect_ratio_table[sorted_keys[-1]]

    for i in range(len(sorted_keys) - 1):
        if sorted_keys[i] <= width / height < sorted_keys[i+1]:
            return aspect_ratio_table[sorted_keys[i]] + (aspect_ratio_table[sorted_keys[i+1]] - aspect_ratio_table[sorted_keys[i]]) * (width / height - sorted_keys[i]) / (sorted_keys[i+1] - sorted_keys[i])

    return 1.0


def get_proc_args():
    try:
        import argparse
    except:
        raise ImportError('proc_args: import error')

    parser = argparse.ArgumentParser(description='Image Assistant')
    parser.add_argument('path', type=str, nargs='?', default=None, help='the path of the image')
    # parser.add_argument('-p', '--path', type=str, default=None, help='the path of the image')
    parser.add_argument('-f', '--fit',  type=int, default=3, help='the fit mode of the image')
    parser.add_argument('-m', '--mode', type=str, default='RGB', help='the mode of the image')
    parser.add_argument('-s', '--size', type=int, nargs=2, default=None, help='the size of the image')
    parser.add_argument('-a', '--aspect_ratio', type=float, default=None, help='the aspect ratio of the image')
    run_mode_group = parser.add_mutually_exclusive_group()
    run_mode_group.add_argument('--simple',   action='store_true', help='run in simple mode')
    run_mode_group.add_argument('--advanced', action='store_true', help='run in advanced mode')
    run_mode_group.add_argument('--test',     action='store_true', help='run in test mode')
    parser.set_defaults(simple=False, advanced=False, test=False)

    return parser.parse_args()


@contextlib.contextmanager
def redirect_stdout(stream):
    import sys
    sys.stdout = stream
    yield
    sys.stdout = sys.__stdout__


if __name__ == '__main__':
    # a little test
    @parallel_run
    @clock()
    def test1():
        time.sleep(1)
        print('1')
        time.sleep(2)
        print('3')

    @parallel_run
    @clock()
    def test2():
        time.sleep(2)
        print('2')

    test1()
    test2()
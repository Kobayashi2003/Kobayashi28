import time
import functools
from collections import namedtuple
from multiprocessing import cpu_count
from enum import Enum

DEFAULT_FONT_PATH = './Hack Regular Nerd Font Complete Mono Windows Compatible.ttf'
DEFAULT_FONT_SIZE = 2

MAX_WIDTH = 1e5
MAX_HEIGHT = 1e5

MAX_WORKERS = cpu_count() - 1

ERROR_RATE = 0.1

MAX_DEPTH = 1e5

DEFAULT_FMT_TIME = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

SUPPORTED_IMAGE_FORMAT = (
    'jpg', 'jpeg', 'png', 'bmp', 'ico', 'jfif'
)
SUPPORTED_IMAGE_FORMAT_SEQUENCE = (
    'gif', 'tif'
)
SUPPORTED_IMAGE_FORMAT_ALL = SUPPORTED_IMAGE_FORMAT + SUPPORTED_IMAGE_FORMAT_SEQUENCE

Result = namedtuple('Result', 'status data')
Status = Enum('Status', 'done processing pending error unfound')

def clock(fmt=DEFAULT_FMT_TIME):
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
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorator



def parallel_run(func):
    import threading
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
            



if __name__ == '__main__':

    @clock()
    def test(sec, msg=''):
        time.sleep(sec)
        print(msg)
        return msg
    test(1, msg='hello')

import time
import functools


DEFAULT_FMT_TIME = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


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